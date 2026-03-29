"""
=============================================================================
  POWER BI DATA PREPARATION
  Global AI & Data Science Job Market (2020-2026)
  Dataset: Kaggle - mann14/global-ai-and-data-science-job-market-20202026
=============================================================================
  Generates 11 aggregated CSV files ready for Power BI import,
  one per analysis question.
=============================================================================
"""

import pandas as pd
import os

# ─────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "powerbi_data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save(df, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"   OK  {filename}")

# ─────────────────────────────────────────────
# LOAD RAW DATA
# ─────────────────────────────────────────────
print("Loading source data...")
jobs   = pd.read_csv(os.path.join(BASE_DIR, "ai_jobs.csv"))
skills = pd.read_csv(os.path.join(BASE_DIR, "skills_demand.csv"))
print(f"   ai_jobs.csv        -> {len(jobs):,} rows")
print(f"   skills_demand.csv  -> {len(skills):,} rows")

# ─────────────────────────────────────────────
# DERIVED COLUMNS
# ─────────────────────────────────────────────
jobs["avg_salary_usd"] = (jobs["salary_min_usd"] + jobs["salary_max_usd"]) / 2

# 11-char key for joining with skills_demand (job_id is truncated there)
jobs["job_id_short"]   = jobs["job_id"].str[:11]
skills["job_id_short"] = skills["job_id"].str[:11]

# Role category grouping
analytics_titles   = ["Data Analyst", "Data Scientist", "AI Researcher", "Applied Scientist"]
engineering_titles = ["Machine Learning Engineer", "MLOps Engineer"]

def get_role_category(title):
    if title in analytics_titles:
        return "Analytics"
    elif title in engineering_titles:
        return "Engineering"
    return "Other"

jobs["role_category"] = jobs["job_title"].apply(get_role_category)

# Work location grouping (before any column renaming)
def get_location_group(row):
    if row["remote_type"] == "Remote":
        return "Remote"
    elif row["remote_type"] == "Onsite":
        return "Onsite (City)"
    elif row["remote_type"] == "Hybrid":
        return "Hybrid"
    return "Other"

jobs["location_group"] = jobs.apply(get_location_group, axis=1)

print("\nProcessing and exporting...\n")

# ═════════════════════════════════════════════
# Q1 — WHICH ROLE TO TARGET FIRST?
# Entry-level openings: Data Analyst / Data Scientist / ML Engineer
# by country and year
# ═════════════════════════════════════════════
target_roles = ["Data Analyst", "Data Scientist", "Machine Learning Engineer"]

df_q1 = (
    jobs[
        (jobs["experience_level"] == "Entry") &
        (jobs["job_title"].isin(target_roles))
    ]
    .groupby(["job_title", "country", "posted_year"])
    .agg(
        job_count         = ("job_id", "count"),
        avg_salary_usd    = ("avg_salary_usd", "mean"),
        min_salary_usd    = ("salary_min_usd", "mean"),
        max_salary_usd    = ("salary_max_usd", "mean"),
    )
    .reset_index()
    .round(0)
)
save(df_q1, "Q1_entry_level_jobs_by_role.csv")

# ═════════════════════════════════════════════
# Q6 — WHICH INDUSTRY SHOULD I MOVE INTO?
# Average max salary for Senior roles by industry and country
# ═════════════════════════════════════════════
df_q6 = (
    jobs[jobs["experience_level"] == "Senior"]
    .groupby(["industry", "country"])
    .agg(
        avg_max_salary_usd  = ("salary_max_usd", "mean"),
        avg_salary_usd      = ("avg_salary_usd", "mean"),
        avg_min_salary_usd  = ("salary_min_usd", "mean"),
        job_count           = ("job_id", "count"),
    )
    .reset_index()
    .sort_values("avg_max_salary_usd", ascending=False)
    .round(0)
)
save(df_q6, "Q6_senior_salary_ceiling_by_industry.csv")

# ═════════════════════════════════════════════
# Q11 — DOES MY CITY MATTER?
# Salary comparison: Remote vs Hybrid vs Onsite (City)
# by role and experience level
# ═════════════════════════════════════════════
df_q11 = (
    jobs[jobs["location_group"] != "Other"]
    .groupby(["location_group", "job_title", "experience_level"])
    .agg(
        avg_salary_usd  = ("avg_salary_usd", "mean"),
        min_salary_usd  = ("salary_min_usd", "mean"),
        max_salary_usd  = ("salary_max_usd", "mean"),
        job_count       = ("job_id", "count"),
    )
    .reset_index()
    .sort_values("avg_salary_usd", ascending=False)
    .round(0)
)
save(df_q11, "Q11_salary_city_vs_remote.csv")

# ═════════════════════════════════════════════
# Q13 — WHICH DEGREE PATH PAYS OFF FASTER?
# Entry-level salary: Analytics roles vs Engineering roles
# ═════════════════════════════════════════════
df_q13 = (
    jobs[jobs["experience_level"] == "Entry"]
    .groupby(["role_category", "job_title", "country"])
    .agg(
        avg_salary_usd  = ("avg_salary_usd", "mean"),
        min_salary_usd  = ("salary_min_usd", "mean"),
        max_salary_usd  = ("salary_max_usd", "mean"),
        job_count       = ("job_id", "count"),
    )
    .reset_index()
    .round(0)
)
save(df_q13, "Q13_analytics_vs_engineering_entry.csv")

# ═════════════════════════════════════════════
# Q14 — IS CLOUD EXPERTISE WORTH IT?
# Avg salary: jobs requiring Advanced Cloud skills vs not
# (Uses original English column names in skills df for filtering)
# ═════════════════════════════════════════════
cloud_adv_ids = set(
    skills[
        (skills["skill_category"] == "Cloud") &
        (skills["skill_level"]    == "Advanced")
    ]["job_id_short"]
)
jobs["has_advanced_cloud"] = jobs["job_id_short"].apply(
    lambda x: "Has Advanced Cloud Skill" if x in cloud_adv_ids else "No Advanced Cloud Skill"
)
df_q14 = (
    jobs
    .groupby(["has_advanced_cloud", "experience_level", "job_title"])
    .agg(
        avg_salary_usd  = ("avg_salary_usd", "mean"),
        max_salary_usd  = ("salary_max_usd", "mean"),
        job_count       = ("job_id", "count"),
    )
    .reset_index()
    .round(0)
)
save(df_q14, "Q14_cloud_skill_salary_premium.csv")

# ═════════════════════════════════════════════
# Q18 — WHICH SKILLS ARE MOST UNDERSUPPLIED?
# Skills required at Advanced level — most in-demand but hardest to hire
# ═════════════════════════════════════════════
df_adv = skills[skills["skill_level"] == "Advanced"]

df_q18 = (
    df_adv
    .groupby(["skill", "skill_category"])
    .agg(advanced_demand_count=("job_id_short", "nunique"))
    .reset_index()
)
df_total = (
    skills
    .groupby("skill")["job_id_short"]
    .nunique()
    .reset_index()
    .rename(columns={"job_id_short": "total_demand_count"})
)
df_q18 = df_q18.merge(df_total, on="skill", how="left")
df_q18["advanced_demand_pct"] = (
    df_q18["advanced_demand_count"] / df_q18["total_demand_count"] * 100
).round(1)
df_q18 = df_q18.sort_values("advanced_demand_count", ascending=False)
save(df_q18, "Q18_undersupplied_skills.csv")

# ═════════════════════════════════════════════
# Q19 — HIRE MID-LEVEL OR TWO JUNIORS?
# Cost comparison: 1 Mid vs 2 × Entry by role and country
# ═════════════════════════════════════════════
sal = (
    jobs[jobs["experience_level"].isin(["Entry", "Mid"])]
    .groupby(["job_title", "experience_level", "country"])
    .agg(avg_salary=("avg_salary_usd", "mean"))
    .reset_index()
)
entry = sal[sal["experience_level"] == "Entry"][["job_title","country","avg_salary"]].rename(
    columns={"avg_salary": "entry_avg_salary_usd"}
)
mid   = sal[sal["experience_level"] == "Mid"][["job_title","country","avg_salary"]].rename(
    columns={"avg_salary": "mid_avg_salary_usd"}
)
df_q19 = entry.merge(mid, on=["job_title","country"], how="inner")
df_q19["cost_2_juniors_usd"]  = df_q19["entry_avg_salary_usd"] * 2
df_q19["mid_to_entry_ratio"]  = (df_q19["mid_avg_salary_usd"] / df_q19["entry_avg_salary_usd"]).round(2)
df_q19["cost_verdict"] = df_q19.apply(
    lambda r: "Mid is cheaper" if r["mid_avg_salary_usd"] < r["cost_2_juniors_usd"] else "2 Juniors cheaper",
    axis=1
)
df_q19 = df_q19.round(0)
save(df_q19, "Q19_mid_vs_2_juniors.csv")

# ═════════════════════════════════════════════
# Q21 — WHICH COUNTRIES HAVE THE MOST AI OPPORTUNITIES?
# Total jobs + avg salary + remote % + composite opportunity score
# ═════════════════════════════════════════════
df_q21 = (
    jobs
    .groupby(["country", "posted_year"])
    .agg(
        total_jobs      = ("job_id", "count"),
        avg_salary_usd  = ("avg_salary_usd", "mean"),
        avg_max_salary  = ("salary_max_usd", "mean"),
    )
    .reset_index()
)
remote_count = (
    jobs[jobs["remote_type"] == "Remote"]
    .groupby(["country","posted_year"])["job_id"]
    .count()
    .reset_index()
    .rename(columns={"job_id": "remote_jobs"})
)
df_q21 = df_q21.merge(remote_count, on=["country","posted_year"], how="left")
df_q21["remote_jobs"]    = df_q21["remote_jobs"].fillna(0)
df_q21["remote_pct"]     = (df_q21["remote_jobs"] / df_q21["total_jobs"] * 100).round(1)
df_q21 = df_q21.drop(columns=["remote_jobs"])

# Composite opportunity score (60% salary weight + 40% volume weight)
lmax, lmin = df_q21["avg_salary_usd"].max(), df_q21["avg_salary_usd"].min()
vmax, vmin = df_q21["total_jobs"].max(), df_q21["total_jobs"].min()
df_q21["opportunity_score"] = (
    0.6 * (df_q21["avg_salary_usd"] - lmin) / (lmax - lmin) +
    0.4 * (df_q21["total_jobs"]     - vmin) / (vmax - vmin)
).round(3)

df_q21["total_jobs"] = df_q21["total_jobs"].round(0)
df_q21["avg_salary_usd"] = df_q21["avg_salary_usd"].round(0)
df_q21["avg_max_salary"] = df_q21["avg_max_salary"].round(0)
df_q21["remote_pct"] = df_q21["remote_pct"].round(1)
save(df_q21, "Q21_opportunity_by_country.csv")

# ═════════════════════════════════════════════
# Q16 — WHEN IS THE BEST TIME TO JOB HUNT?
# Job posting volume by year, country, experience level + YoY growth
# NOTE: Dataset has year only (no month-level data)
# ═════════════════════════════════════════════
df_q16 = (
    jobs
    .groupby(["posted_year", "country", "experience_level"])
    .agg(
        total_jobs      = ("job_id", "count"),
        avg_salary_usd  = ("avg_salary_usd", "mean"),
    )
    .reset_index()
)
# YoY growth per country
yoy = (
    jobs.groupby(["posted_year","country"])
    .agg(year_total=("job_id","count"))
    .reset_index()
)
yoy["yoy_growth_pct"] = (
    yoy.groupby("country")["year_total"].pct_change() * 100
).round(1)
df_q16 = df_q16.merge(yoy, on=["posted_year","country"], how="left")
save(df_q16.round(0), "Q16_hiring_trend_by_year.csv")

# ═════════════════════════════════════════════
# Q25 — LARGE VS SMALL COMPANY: WHO DRIVES AI GROWTH?
# Job posting growth by company size, year, and country
# ═════════════════════════════════════════════
df_q25 = (
    jobs
    .groupby(["company_size", "posted_year", "country"])
    .agg(
        total_jobs      = ("job_id", "count"),
        avg_salary_usd  = ("avg_salary_usd", "mean"),
    )
    .reset_index()
)
df_q25["yoy_growth_pct"] = (
    df_q25.groupby(["company_size","country"])["total_jobs"]
    .pct_change() * 100
).round(1)
save(df_q25.round(0), "Q25_growth_by_company_size.csv")

# ─────────────────────────────────────────────
# REFERENCE: English-to-English value dictionary
# (useful for Power BI tooltips and slicers)
# ─────────────────────────────────────────────
ref = pd.DataFrame({
    "value": [
        "Entry","Mid","Senior",
        "Data Analyst","Data Scientist","Machine Learning Engineer",
        "AI Researcher","Applied Scientist","MLOps Engineer",
        "Startup","MNC","Research Lab",
        "Small","Medium","Large",
        "Remote","Hybrid","Onsite",
        "Tech","Finance","Healthcare","Education","Retail",
        "USA","India","UK","Germany","Canada","Australia",
        "Programming","ML","Cloud",
        "Basic","Intermediate","Advanced",
        "Analytics","Engineering",
    ],
    "category": [
        "Experience","Experience","Experience",
        "Job Title","Job Title","Job Title",
        "Job Title","Job Title","Job Title",
        "Company Type","Company Type","Company Type",
        "Company Size","Company Size","Company Size",
        "Work Type","Work Type","Work Type",
        "Industry","Industry","Industry","Industry","Industry",
        "Country","Country","Country","Country","Country","Country",
        "Skill Category","Skill Category","Skill Category",
        "Skill Level","Skill Level","Skill Level",
        "Role Category","Role Category",
    ]
})
save(ref, "ZZ_reference_values.csv")

# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────
print("\n" + "="*62)
print("DONE! All files saved to:")
print(f"  {OUTPUT_DIR}")
print("="*62)
files = sorted(os.listdir(OUTPUT_DIR))
total_kb = 0
for f in files:
    p  = os.path.join(OUTPUT_DIR, f)
    kb = os.path.getsize(p) / 1024
    total_kb += kb
    print(f"  {f:<52}  {kb:>6.1f} KB")
print(f"\n  Total: {total_kb:.1f} KB across {len(files)} files")
