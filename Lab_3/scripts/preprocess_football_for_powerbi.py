from __future__ import annotations

from pathlib import Path
import json
import sqlite3

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT_DIR / "football" / "raw"
PROCESSED_DIR = ROOT_DIR / "football" / "processed"
DB_PATH = RAW_DIR / "database.sqlite"


def read_table(conn: sqlite3.Connection, table_name: str) -> pd.DataFrame:
    return pd.read_sql_query(f"SELECT * FROM [{table_name}]", conn)


def normalize_date(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce").dt.normalize()


def to_date_key(series: pd.Series) -> pd.Series:
    normalized = normalize_date(series)
    return normalized.dt.strftime("%Y%m%d").where(normalized.notna())


def build_dim_country(country: pd.DataFrame) -> pd.DataFrame:
    dim_country = country.copy()
    dim_country = dim_country.rename(columns={"id": "country_key", "name": "country_name"})
    return dim_country[["country_key", "country_name"]].drop_duplicates()


def build_dim_league(league: pd.DataFrame, dim_country: pd.DataFrame) -> pd.DataFrame:
    dim_league = league.copy()
    dim_league = dim_league.rename(
        columns={
            "id": "league_key",
            "country_id": "country_key",
            "name": "league_name",
        }
    )
    dim_league = dim_league.merge(dim_country, on="country_key", how="left")
    return dim_league[["league_key", "country_key", "league_name", "country_name"]].drop_duplicates()


def build_dim_team(team: pd.DataFrame) -> pd.DataFrame:
    dim_team = team.copy()
    dim_team = dim_team.rename(
        columns={
            "id": "team_row_id",
            "team_api_id": "team_key",
            "team_fifa_api_id": "team_fifa_id",
        }
    )
    return dim_team[
        [
            "team_key",
            "team_row_id",
            "team_fifa_id",
            "team_long_name",
            "team_short_name",
        ]
    ].drop_duplicates()


def build_dim_player(player: pd.DataFrame) -> pd.DataFrame:
    dim_player = player.copy()
    dim_player = dim_player.rename(
        columns={
            "id": "player_row_id",
            "player_api_id": "player_key",
            "player_fifa_api_id": "player_fifa_id",
            "birthday": "player_birthday",
        }
    )
    dim_player["player_birthday"] = pd.to_datetime(dim_player["player_birthday"], errors="coerce")
    return dim_player[
        [
            "player_key",
            "player_row_id",
            "player_name",
            "player_fifa_id",
            "player_birthday",
            "height",
            "weight",
        ]
    ].drop_duplicates()


def build_dim_date(match_df: pd.DataFrame, team_attr: pd.DataFrame, player_attr: pd.DataFrame) -> pd.DataFrame:
    match_dates = normalize_date(match_df["date"])
    team_attr_dates = normalize_date(team_attr["date"])
    player_attr_dates = normalize_date(player_attr["date"])

    all_dates = pd.concat([match_dates, team_attr_dates, player_attr_dates], ignore_index=True).dropna()
    full_range = pd.date_range(all_dates.min(), all_dates.max(), freq="D")

    dim_date = pd.DataFrame({"date": full_range})
    dim_date["date_key"] = dim_date["date"].dt.strftime("%Y%m%d").astype(int)
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["quarter"] = "Q" + dim_date["date"].dt.quarter.astype(str)
    dim_date["month_number"] = dim_date["date"].dt.month
    dim_date["month_name"] = dim_date["date"].dt.strftime("%B")
    dim_date["year_month"] = dim_date["date"].dt.strftime("%Y-%m")
    dim_date["day_of_month"] = dim_date["date"].dt.day
    dim_date["day_of_week_number"] = dim_date["date"].dt.dayofweek
    dim_date["day_of_week_name"] = dim_date["date"].dt.strftime("%A")
    dim_date["is_weekend"] = dim_date["day_of_week_number"].isin([5, 6]).astype(int)
    return dim_date


def build_team_attributes_latest(team_attr: pd.DataFrame) -> pd.DataFrame:
    latest = team_attr.copy()
    latest["date"] = pd.to_datetime(latest["date"], errors="coerce")
    latest = latest.sort_values(["team_api_id", "date"]).groupby("team_api_id", as_index=False).tail(1)
    latest = latest.rename(columns={"team_api_id": "team_key", "date": "attribute_date"})
    latest["attribute_date_key"] = to_date_key(latest["attribute_date"])
    return latest


def build_player_attributes_latest(player_attr: pd.DataFrame) -> pd.DataFrame:
    latest = player_attr.copy()
    latest["date"] = pd.to_datetime(latest["date"], errors="coerce")
    latest = latest.sort_values(["player_api_id", "date"]).groupby("player_api_id", as_index=False).tail(1)
    latest = latest.rename(columns={"player_api_id": "player_key", "date": "attribute_date"})
    latest["attribute_date_key"] = to_date_key(latest["attribute_date"])
    return latest


def build_fact_match_summary(
    match_df: pd.DataFrame,
    dim_country: pd.DataFrame,
    dim_league: pd.DataFrame,
    dim_team: pd.DataFrame,
) -> pd.DataFrame:
    fact = match_df.copy()
    fact["match_date"] = normalize_date(fact["date"])
    fact["match_date_key"] = to_date_key(fact["date"])
    fact = fact.rename(
        columns={
            "id": "match_key",
            "country_id": "country_key",
            "league_id": "league_key",
            "home_team_api_id": "home_team_key",
            "away_team_api_id": "away_team_key",
        }
    )

    fact = fact.merge(dim_country, on="country_key", how="left")
    fact = fact.merge(dim_league[["league_key", "league_name"]], on="league_key", how="left")
    fact = fact.merge(
        dim_team[["team_key", "team_long_name", "team_short_name"]].rename(
            columns={
                "team_key": "home_team_key",
                "team_long_name": "home_team_name",
                "team_short_name": "home_team_short_name",
            }
        ),
        on="home_team_key",
        how="left",
    )
    fact = fact.merge(
        dim_team[["team_key", "team_long_name", "team_short_name"]].rename(
            columns={
                "team_key": "away_team_key",
                "team_long_name": "away_team_name",
                "team_short_name": "away_team_short_name",
            }
        ),
        on="away_team_key",
        how="left",
    )

    fact["total_goals"] = fact["home_team_goal"] + fact["away_team_goal"]
    fact["goal_difference"] = fact["home_team_goal"] - fact["away_team_goal"]
    fact["is_draw"] = (fact["home_team_goal"] == fact["away_team_goal"]).astype(int)
    fact["home_win"] = (fact["home_team_goal"] > fact["away_team_goal"]).astype(int)
    fact["away_win"] = (fact["home_team_goal"] < fact["away_team_goal"]).astype(int)
    fact["match_result"] = fact["goal_difference"].map(lambda x: "Home Win" if x > 0 else ("Away Win" if x < 0 else "Draw"))
    fact["winner_team_key"] = fact.apply(
        lambda row: row["home_team_key"] if row["home_team_goal"] > row["away_team_goal"] else (
            row["away_team_key"] if row["away_team_goal"] > row["home_team_goal"] else pd.NA
        ),
        axis=1,
    )

    return fact[
        [
            "match_key",
            "country_key",
            "country_name",
            "league_key",
            "league_name",
            "season",
            "stage",
            "date",
            "match_date",
            "match_date_key",
            "home_team_key",
            "home_team_name",
            "home_team_short_name",
            "away_team_key",
            "away_team_name",
            "away_team_short_name",
            "home_team_goal",
            "away_team_goal",
            "total_goals",
            "goal_difference",
            "is_draw",
            "home_win",
            "away_win",
            "match_result",
            "winner_team_key",
        ]
    ]


def build_fact_team_match(
    fact_match_summary: pd.DataFrame,
    dim_team: pd.DataFrame,
) -> pd.DataFrame:
    home = fact_match_summary[
        [
            "match_key",
            "country_key",
            "country_name",
            "league_key",
            "league_name",
            "season",
            "stage",
            "match_date",
            "match_date_key",
            "home_team_key",
            "away_team_key",
            "home_team_goal",
            "away_team_goal",
        ]
    ].copy()
    home["team_key"] = home["home_team_key"]
    home["opponent_team_key"] = home["away_team_key"]
    home["is_home"] = 1
    home["goals_for"] = home["home_team_goal"]
    home["goals_against"] = home["away_team_goal"]

    away = fact_match_summary[
        [
            "match_key",
            "country_key",
            "country_name",
            "league_key",
            "league_name",
            "season",
            "stage",
            "match_date",
            "match_date_key",
            "home_team_key",
            "away_team_key",
            "home_team_goal",
            "away_team_goal",
        ]
    ].copy()
    away["team_key"] = away["away_team_key"]
    away["opponent_team_key"] = away["home_team_key"]
    away["is_home"] = 0
    away["goals_for"] = away["away_team_goal"]
    away["goals_against"] = away["home_team_goal"]

    fact = pd.concat([home, away], ignore_index=True)
    fact["goal_difference"] = fact["goals_for"] - fact["goals_against"]
    fact["match_points"] = fact["goal_difference"].map(lambda x: 3 if x > 0 else (1 if x == 0 else 0))
    fact["match_result"] = fact["goal_difference"].map(lambda x: "Win" if x > 0 else ("Draw" if x == 0 else "Loss"))
    fact["team_match_key"] = fact["match_key"].astype(str) + "_" + fact["is_home"].astype(str)

    fact = fact.merge(
        dim_team[["team_key", "team_long_name", "team_short_name"]].rename(
            columns={"team_long_name": "team_name", "team_short_name": "team_short_name"}
        ),
        on="team_key",
        how="left",
    )
    fact = fact.merge(
        dim_team[["team_key", "team_long_name", "team_short_name"]].rename(
            columns={
                "team_key": "opponent_team_key",
                "team_long_name": "opponent_team_name",
                "team_short_name": "opponent_team_short_name",
            }
        ),
        on="opponent_team_key",
        how="left",
    )

    return fact[
        [
            "team_match_key",
            "match_key",
            "match_date",
            "match_date_key",
            "season",
            "stage",
            "country_key",
            "country_name",
            "league_key",
            "league_name",
            "team_key",
            "team_name",
            "team_short_name",
            "opponent_team_key",
            "opponent_team_name",
            "opponent_team_short_name",
            "is_home",
            "goals_for",
            "goals_against",
            "goal_difference",
            "match_points",
            "match_result",
        ]
    ]


def build_schema_outputs(
    dim_country: pd.DataFrame,
    dim_league: pd.DataFrame,
    dim_team: pd.DataFrame,
    dim_player: pd.DataFrame,
    dim_date: pd.DataFrame,
    team_attributes_latest: pd.DataFrame,
    player_attributes_latest: pd.DataFrame,
    fact_match_summary: pd.DataFrame,
    fact_team_match: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    schema_entities = pd.DataFrame(
        [
            {"table_name": "dim_country", "row_count": len(dim_country), "grain": "one row per country"},
            {"table_name": "dim_league", "row_count": len(dim_league), "grain": "one row per league"},
            {"table_name": "dim_team", "row_count": len(dim_team), "grain": "one row per team"},
            {"table_name": "dim_player", "row_count": len(dim_player), "grain": "one row per player"},
            {"table_name": "dim_date", "row_count": len(dim_date), "grain": "one row per date"},
            {"table_name": "team_attributes_latest", "row_count": len(team_attributes_latest), "grain": "latest row per team"},
            {"table_name": "player_attributes_latest", "row_count": len(player_attributes_latest), "grain": "latest row per player"},
            {"table_name": "fact_match_summary", "row_count": len(fact_match_summary), "grain": "one row per match"},
            {"table_name": "fact_team_match", "row_count": len(fact_team_match), "grain": "one row per team per match"},
        ]
    )

    schema_relationships = pd.DataFrame(
        [
            {"from_table": "dim_country", "from_column": "country_key", "to_table": "dim_league", "to_column": "country_key", "cardinality": "one-to-many"},
            {"from_table": "dim_country", "from_column": "country_key", "to_table": "fact_match_summary", "to_column": "country_key", "cardinality": "one-to-many"},
            {"from_table": "dim_country", "from_column": "country_key", "to_table": "fact_team_match", "to_column": "country_key", "cardinality": "one-to-many"},
            {"from_table": "dim_league", "from_column": "league_key", "to_table": "fact_match_summary", "to_column": "league_key", "cardinality": "one-to-many"},
            {"from_table": "dim_league", "from_column": "league_key", "to_table": "fact_team_match", "to_column": "league_key", "cardinality": "one-to-many"},
            {"from_table": "dim_team", "from_column": "team_key", "to_table": "team_attributes_latest", "to_column": "team_key", "cardinality": "one-to-one or one-to-many"},
            {"from_table": "dim_team", "from_column": "team_key", "to_table": "fact_team_match", "to_column": "team_key", "cardinality": "one-to-many"},
            {"from_table": "dim_player", "from_column": "player_key", "to_table": "player_attributes_latest", "to_column": "player_key", "cardinality": "one-to-one or one-to-many"},
            {"from_table": "dim_date", "from_column": "date_key", "to_table": "fact_match_summary", "to_column": "match_date_key", "cardinality": "one-to-many"},
            {"from_table": "dim_date", "from_column": "date_key", "to_table": "fact_team_match", "to_column": "match_date_key", "cardinality": "one-to-many"},
            {"from_table": "dim_date", "from_column": "date_key", "to_table": "team_attributes_latest", "to_column": "attribute_date_key", "cardinality": "one-to-many"},
            {"from_table": "dim_date", "from_column": "date_key", "to_table": "player_attributes_latest", "to_column": "attribute_date_key", "cardinality": "one-to-many"},
        ]
    )

    summary = {
        "source": {
            "dataset_name": "European Soccer Database",
            "source_url": "https://www.kaggle.com/datasets/hugomathien/soccer",
        },
        "generated_tables": {
            "dim_country": len(dim_country),
            "dim_league": len(dim_league),
            "dim_team": len(dim_team),
            "dim_player": len(dim_player),
            "dim_date": len(dim_date),
            "team_attributes_latest": len(team_attributes_latest),
            "player_attributes_latest": len(player_attributes_latest),
            "fact_match_summary": len(fact_match_summary),
            "fact_team_match": len(fact_team_match),
        },
        "date_range": {
            "match_date_min": str(fact_match_summary["match_date"].min()) if fact_match_summary["match_date"].notna().any() else None,
            "match_date_max": str(fact_match_summary["match_date"].max()) if fact_match_summary["match_date"].notna().any() else None,
        },
        "metrics": {
            "country_count": int(dim_country["country_key"].nunique()),
            "league_count": int(dim_league["league_key"].nunique()),
            "team_count": int(dim_team["team_key"].nunique()),
            "player_count": int(dim_player["player_key"].nunique()),
            "match_count": int(fact_match_summary["match_key"].nunique()),
            "team_match_rows": int(len(fact_team_match)),
            "average_goals_per_match": float(fact_match_summary["total_goals"].mean()),
            "home_win_rate": float(fact_match_summary["home_win"].mean()),
            "draw_rate": float(fact_match_summary["is_draw"].mean()),
        },
    }

    return schema_entities, schema_relationships, summary


def write_csv(df: pd.DataFrame, filename: str) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DIR / filename, index=False, encoding="utf-8-sig")


def main() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        country = read_table(conn, "Country")
        league = read_table(conn, "League")
        team = read_table(conn, "Team")
        player = read_table(conn, "Player")
        team_attr = read_table(conn, "Team_Attributes")
        player_attr = read_table(conn, "Player_Attributes")
        match_df = read_table(conn, "Match")

    dim_country = build_dim_country(country)
    dim_league = build_dim_league(league, dim_country)
    dim_team = build_dim_team(team)
    dim_player = build_dim_player(player)
    dim_date = build_dim_date(match_df, team_attr, player_attr)
    team_attributes_latest = build_team_attributes_latest(team_attr)
    player_attributes_latest = build_player_attributes_latest(player_attr)
    fact_match_summary = build_fact_match_summary(match_df, dim_country, dim_league, dim_team)
    fact_team_match = build_fact_team_match(fact_match_summary, dim_team)

    schema_entities, schema_relationships, summary = build_schema_outputs(
        dim_country=dim_country,
        dim_league=dim_league,
        dim_team=dim_team,
        dim_player=dim_player,
        dim_date=dim_date,
        team_attributes_latest=team_attributes_latest,
        player_attributes_latest=player_attributes_latest,
        fact_match_summary=fact_match_summary,
        fact_team_match=fact_team_match,
    )

    write_csv(dim_country, "dim_country.csv")
    write_csv(dim_league, "dim_league.csv")
    write_csv(dim_team, "dim_team.csv")
    write_csv(dim_player, "dim_player.csv")
    write_csv(dim_date, "dim_date.csv")
    write_csv(team_attributes_latest, "team_attributes_latest.csv")
    write_csv(player_attributes_latest, "player_attributes_latest.csv")
    write_csv(fact_match_summary, "fact_match_summary.csv")
    write_csv(fact_team_match, "fact_team_match.csv")
    write_csv(schema_entities, "schema_entities.csv")
    write_csv(schema_relationships, "schema_relationships.csv")

    with (PROCESSED_DIR / "dataset_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    pd.DataFrame([summary["metrics"]]).to_csv(
        PROCESSED_DIR / "model_summary.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("Generated processed football files in:", PROCESSED_DIR)


if __name__ == "__main__":
    main()
