from __future__ import annotations

from pathlib import Path
import json

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT_DIR / "football" / "processed"
DEMO_DIR = ROOT_DIR / "football" / "demo_processed"

TARGET_LEAGUES = {
    "England Premier League",
    "Spain LIGA BBVA",
}

TARGET_SEASONS = {
    "2014/2015",
    "2015/2016",
}


def read_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(SOURCE_DIR / name)


def write_csv(df: pd.DataFrame, name: str) -> None:
    DEMO_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(DEMO_DIR / name, index=False, encoding="utf-8-sig")


def main() -> None:
    dim_country = read_csv("dim_country.csv")
    dim_league = read_csv("dim_league.csv")
    dim_team = read_csv("dim_team.csv")
    dim_date = read_csv("dim_date.csv")
    team_attributes = read_csv("team_attributes_latest.csv")
    fact_match_summary = read_csv("fact_match_summary.csv")
    fact_team_match = read_csv("fact_team_match.csv")

    match_demo = fact_match_summary[
        fact_match_summary["league_name"].isin(TARGET_LEAGUES)
        & fact_match_summary["season"].isin(TARGET_SEASONS)
    ].copy()

    team_match_demo = fact_team_match[
        fact_team_match["match_key"].isin(match_demo["match_key"])
    ].copy()

    league_demo = dim_league[dim_league["league_name"].isin(TARGET_LEAGUES)].copy()
    country_demo = dim_country[dim_country["country_key"].isin(league_demo["country_key"])].copy()

    team_keys = pd.concat(
        [
            match_demo["home_team_key"],
            match_demo["away_team_key"],
            team_match_demo["team_key"],
            team_match_demo["opponent_team_key"],
        ],
        ignore_index=True,
    ).dropna().astype(int).unique()

    team_demo = dim_team[dim_team["team_key"].isin(team_keys)].copy()
    team_attributes_demo = team_attributes[team_attributes["team_key"].isin(team_keys)].copy()

    date_keys = pd.concat(
        [
            pd.to_numeric(match_demo["match_date_key"], errors="coerce"),
            pd.to_numeric(team_match_demo["match_date_key"], errors="coerce"),
            pd.to_numeric(team_attributes_demo["attribute_date_key"], errors="coerce"),
        ],
        ignore_index=True,
    ).dropna().astype(int)

    date_demo = dim_date[dim_date["date_key"].isin(date_keys.unique())].copy()

    schema_entities = pd.DataFrame(
        [
            {"table_name": "dim_country_demo", "row_count": len(country_demo), "grain": "one row per country"},
            {"table_name": "dim_league_demo", "row_count": len(league_demo), "grain": "one row per league"},
            {"table_name": "dim_team_demo", "row_count": len(team_demo), "grain": "one row per team"},
            {"table_name": "dim_date_demo", "row_count": len(date_demo), "grain": "one row per date actually used"},
            {"table_name": "team_attributes_demo", "row_count": len(team_attributes_demo), "grain": "latest row per selected team"},
            {"table_name": "fact_match_demo", "row_count": len(match_demo), "grain": "one row per match"},
            {"table_name": "fact_team_match_demo", "row_count": len(team_match_demo), "grain": "one row per team per match"},
        ]
    )

    schema_relationships = pd.DataFrame(
        [
            {"from_table": "dim_country_demo", "from_column": "country_key", "to_table": "dim_league_demo", "to_column": "country_key", "cardinality": "one-to-many"},
            {"from_table": "dim_league_demo", "from_column": "league_key", "to_table": "fact_match_demo", "to_column": "league_key", "cardinality": "one-to-many"},
            {"from_table": "dim_league_demo", "from_column": "league_key", "to_table": "fact_team_match_demo", "to_column": "league_key", "cardinality": "one-to-many"},
            {"from_table": "dim_team_demo", "from_column": "team_key", "to_table": "team_attributes_demo", "to_column": "team_key", "cardinality": "one-to-many"},
            {"from_table": "dim_team_demo", "from_column": "team_key", "to_table": "fact_team_match_demo", "to_column": "team_key", "cardinality": "one-to-many"},
            {"from_table": "dim_date_demo", "from_column": "date_key", "to_table": "fact_match_demo", "to_column": "match_date_key", "cardinality": "one-to-many"},
            {"from_table": "dim_date_demo", "from_column": "date_key", "to_table": "fact_team_match_demo", "to_column": "match_date_key", "cardinality": "one-to-many"},
        ]
    )

    summary = {
        "purpose": "Sample relational dataset for introducing Power BI features in Lab 03.",
        "why_this_matches_requirements": [
            "It is a sample dataset unrelated to the main Olist analysis dataset.",
            "It remains relational with multiple linked tables.",
            "It is intentionally simplified for demonstrating Power BI features.",
        ],
        "selected_leagues": sorted(TARGET_LEAGUES),
        "selected_seasons": sorted(TARGET_SEASONS),
        "generated_tables": {
            "dim_country_demo": len(country_demo),
            "dim_league_demo": len(league_demo),
            "dim_team_demo": len(team_demo),
            "dim_date_demo": len(date_demo),
            "team_attributes_demo": len(team_attributes_demo),
            "fact_match_demo": len(match_demo),
            "fact_team_match_demo": len(team_match_demo),
        },
        "metrics": {
            "match_count": int(match_demo["match_key"].nunique()),
            "team_count": int(team_demo["team_key"].nunique()),
            "league_count": int(league_demo["league_key"].nunique()),
            "country_count": int(country_demo["country_key"].nunique()),
            "average_goals_per_match": float(pd.to_numeric(match_demo["total_goals"], errors="coerce").mean()),
        },
    }

    write_csv(country_demo, "dim_country_demo.csv")
    write_csv(league_demo, "dim_league_demo.csv")
    write_csv(team_demo, "dim_team_demo.csv")
    write_csv(date_demo, "dim_date_demo.csv")
    write_csv(team_attributes_demo, "team_attributes_demo.csv")
    write_csv(match_demo, "fact_match_demo.csv")
    write_csv(team_match_demo, "fact_team_match_demo.csv")
    write_csv(schema_entities, "schema_entities_demo.csv")
    write_csv(schema_relationships, "schema_relationships_demo.csv")

    with (DEMO_DIR / "demo_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    pd.DataFrame([summary["metrics"]]).to_csv(
        DEMO_DIR / "demo_metrics.csv",
        index=False,
        encoding="utf-8-sig",
    )

    print("Generated football demo subset in:", DEMO_DIR)


if __name__ == "__main__":
    main()
