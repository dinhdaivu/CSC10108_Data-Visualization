# Power BI Dashboard Guide

## 1. Dataset overview

Source dataset:
- Kaggle: https://www.kaggle.com/datasets/mann14/global-ai-and-data-science-job-market-20202026/code

Files explored in this project:
- `ai_jobs.csv`
- `skills_demand.csv`
- `country_ai_trends.csv`
- `data_dictionary.csv`
- `job_title_mapping.csv`
- `powerbi_data/*.csv`

Local dataset profile from the files in this workspace:
- `ai_jobs.csv`: 50,000 rows
- `skills_demand.csv`: 224,605 rows
- Countries: Australia, Canada, Germany, India, UK, USA
- Years: 2020 to 2026
- Job titles: 6
- Experience levels: Entry, Mid, Senior
- Industries: Tech, Finance, Healthcare, Education, Retail
- Company sizes: Small, Medium, Large
- Work arrangements: Remote, Hybrid, Onsite

## 2. Important reading before you build

This dataset is very clean and Power BI friendly, but it also looks strongly synthetic.

Why that matters:
- Category counts are unusually balanced across countries, roles, industries, company sizes, and experience levels.
- Salary bands are very regular, with clean separation between Entry, Mid, and Senior levels.
- Many derived comparisons are useful for storytelling, but they should be framed as simulated market patterns, not as real-world labor-market proof.

Use the dashboard for:
- portfolio storytelling
- trend exploration
- comparison pages
- KPI practice
- DAX and visual design practice

Do not overclaim:
- "best time to job hunt" at monthly or seasonal level
- "city premium" from `Q11` because the file is grouped by work arrangement, not city
- "degree path pays off faster" from `Q13` because the dataset has no education field
- "undersupplied skills" from `Q18` because the file shows advanced demand intensity, not labor supply

## 3. Best dashboard framing

The safest framing is:

**Global AI & Data Science Job Market Dashboard (2020-2026)**

Subtitle suggestion:

**Role demand, salary patterns, skills, geography, and hiring structure from a synthetic multi-country job market dataset**

## 4. Recommended report structure

Recommended page flow:
1. Executive overview
2. Entry-level career path
3. Senior salary and industry
4. Work arrangement and pay
5. Skills and cloud premium
6. Hiring trend over time
7. Geography and opportunity
8. Company strategy and hiring mix

Suggested global slicers:
- `country`
- `posted_year`
- `experience_level`
- `job_title`
- `industry`

Important modeling note:
- The files in `powerbi_data` are separate aggregated outputs for specific questions.
- They are excellent for page-specific visuals.
- They are not a perfect shared star schema by themselves.
- If you want consistent slicers across the whole report, also import `ai_jobs.csv` and `skills_demand.csv` as the base model.

## 5. Review of every file in `powerbi_data`

### Q1 - `Q1_entry_level_jobs_by_role.csv`

Current question:
- Which role to target first?

What it actually answers:
- How entry-level job volume and salary compare across `Data Analyst`, `Data Scientist`, and `Machine Learning Engineer`, by country and year.

What is good:
- Strong page starter for early-career users.
- Balanced structure: 3 roles x 6 countries x 7 years.
- Easy to use for trend lines, bars, and scatter plots.

Watch out for:
- It excludes `AI Researcher`, `Applied Scientist`, and `MLOps Engineer`.
- "Best role" depends on whether you prioritize volume or salary.

Better dashboard title:
- **Which entry-level role offers the best mix of demand and pay?**

Best visuals:
- clustered bar: `job_count` by `job_title`
- line chart: `job_count` by `posted_year`
- scatter chart: `job_count` vs `avg_salary_usd`
- matrix: `country` x `job_title`

### Q6 - `Q6_senior_salary_ceiling_by_industry.csv`

Current question:
- Which industry should I move into?

What it actually answers:
- Which industry-country combinations have the highest average senior salary ceilings.

What is good:
- Clear salary comparison page.
- Includes `avg_max_salary_usd`, `avg_salary_usd`, `avg_min_salary_usd`, and `job_count`.

Watch out for:
- It is senior-only, so it should not be mixed with entry-level interpretation.
- Differences are present, but they are narrow because the dataset is synthetic.

Better dashboard title:
- **Which industries offer the highest senior salary ceilings?**

Best visuals:
- sorted bar chart by `avg_max_salary_usd`
- dumbbell chart using `avg_min_salary_usd` and `avg_max_salary_usd`
- heatmap: `industry` by `country`

### Q11 - `Q11_salary_city_vs_remote.csv`

Current question:
- Does my city matter?

What it actually answers:
- How salary differs by work arrangement: `Remote`, `Hybrid`, and `Onsite (City)`, by role and experience level.

What is good:
- Useful for a flexible-work page.
- Good comparison across role and seniority.

Watch out for:
- This is not a city analysis.
- The dataset contains a `city` field, but this file does not group by city.
- Rename this concept in the dashboard to avoid misleading viewers.

Better dashboard title:
- **How does pay vary by work arrangement?**

Best visuals:
- clustered bar: `avg_salary_usd` by `location_group`
- small multiples by `experience_level`
- matrix by `job_title` and `location_group`

### Q13 - `Q13_analytics_vs_engineering_entry.csv`

Current question:
- Which degree path pays off faster?

What it actually answers:
- How entry-level salaries compare between role families labeled `Analytics` and `Engineering`, by job title and country.

What is good:
- Useful for grouping related roles.
- Good for a beginner-career page.

Watch out for:
- The dataset has no degree or education columns.
- The title should be about role category, not degree path.
- `AI Researcher` is grouped under `Analytics`, which is okay for this project but should be explained.

Better dashboard title:
- **How do entry-level salaries compare between analytics and engineering roles?**

Best visuals:
- bar chart by `role_category`
- decomposition tree from `role_category` to `job_title` to `country`
- matrix with conditional formatting on `avg_salary_usd`

### Q14 - `Q14_cloud_skill_salary_premium.csv`

Current question:
- Is cloud expertise worth it?

What it actually answers:
- Whether jobs linked to at least one advanced cloud skill have higher average salaries, by experience level and job title.

What is good:
- Strong story page.
- Combines job data with skill data.
- Good candidate for a premium comparison visual.

Watch out for:
- This is correlation, not causation.
- "Has Advanced Cloud Skill" means the job links to at least one advanced cloud skill in `skills_demand.csv`.
- A premium measure would be easier to read if calculated in Power BI.

Better dashboard title:
- **Do advanced cloud skills correlate with higher pay?**

Best visuals:
- clustered column chart by `has_advanced_cloud`
- matrix by `job_title` and `experience_level`
- KPI card for cloud premium difference

Useful DAX:
```DAX
Cloud Premium USD =
VAR CloudPay =
    CALCULATE(
        AVERAGE('Q14_cloud_skill_salary_premium'[avg_salary_usd]),
        'Q14_cloud_skill_salary_premium'[has_advanced_cloud] = "Has Advanced Cloud Skill"
    )
VAR NonCloudPay =
    CALCULATE(
        AVERAGE('Q14_cloud_skill_salary_premium'[avg_salary_usd]),
        'Q14_cloud_skill_salary_premium'[has_advanced_cloud] = "No Advanced Cloud Skill"
    )
RETURN
    CloudPay - NonCloudPay
```

### Q16 - `Q16_hiring_trend_by_year.csv`

Current question:
- When is the best time to job hunt?

What it actually answers:
- How annual hiring volume changes by year, country, and experience level.

What is good:
- Good time-series page.
- Includes total yearly volume plus YoY growth.

Watch out for:
- The dataset only has year, not month or quarter.
- This file supports year-over-year trend analysis, not seasonal timing advice.

Better dashboard title:
- **How has hiring volume changed over time?**

Best visuals:
- line chart of `year_total` by `posted_year`
- ribbon chart by `country`
- line and clustered column chart with `year_total` and `yoy_growth_pct`

### Q18 - `Q18_undersupplied_skills.csv`

Current question:
- Which skills are most undersupplied?

What it actually answers:
- Which skills have the largest count and share of advanced-level demand in job postings.

What is good:
- Useful skill prioritization page.
- Small table, easy to visualize.

Watch out for:
- It does not measure market supply.
- It should be framed as advanced-demand concentration, not undersupply.
- The percentages are very close together, so ranking by count may be clearer than ranking by percentage.

Better dashboard title:
- **Which skills show the strongest advanced-level demand?**

Best visuals:
- horizontal bar chart by `advanced_demand_count`
- lollipop chart with `advanced_demand_pct`
- table with skill category color coding

### Q19 - `Q19_mid_vs_2_juniors.csv`

Current question:
- Hire mid-level or two juniors?

What it actually answers:
- Whether one mid-level salary is cheaper than paying two entry-level salaries, by role and country.

What is good:
- Clear business tradeoff page.
- Simple comparison logic.

Watch out for:
- It only compares salary cost.
- It ignores productivity, onboarding, span of control, and hiring risk.
- `mid_to_entry_ratio` is useful, but the interpretation should stay narrow.

Better dashboard title:
- **Is one mid-level hire cheaper than two entry-level hires?**

Best visuals:
- clustered bar comparing `mid_avg_salary_usd` and `cost_2_juniors_usd`
- card for count of cases where `Mid is cheaper`
- matrix by `job_title` and `country`

### Q21 - `Q21_opportunity_by_country.csv`

Current question:
- Which countries have the most AI opportunities?

What it actually answers:
- Which country-year combinations combine higher job volume and salary into a custom composite opportunity score.

What is good:
- Good executive page material.
- Combines scale and compensation.
- Includes remote share.

Watch out for:
- The score is custom, not a source field.
- The 60% salary / 40% jobs weighting is a modeling decision.
- The original export had a rounding issue that collapsed the score to `0` or `1`; this has been fixed.

Better dashboard title:
- **Which country-year combinations score highest on job volume and pay?**

Best visuals:
- bubble chart: `total_jobs` vs `avg_salary_usd`, bubble size `remote_pct`
- heatmap: `country` by `posted_year`
- ranked table by `opportunity_score`

### Q25 - `Q25_growth_by_company_size.csv`

Current question:
- Large vs small company: who drives AI growth?

What it actually answers:
- How job volume and year-over-year growth differ by company size, year, and country.

What is good:
- Strong organizational strategy page.
- Good for stacked trends and company size segmentation.

Watch out for:
- First year YoY is blank by design.
- Growth is sensitive to the balanced synthetic structure of the dataset.

Better dashboard title:
- **How does hiring growth differ by company size?**

Best visuals:
- line chart by `company_size`
- stacked column by `posted_year`
- matrix with `yoy_growth_pct`

### ZZ - `ZZ_reference_values.csv`

Purpose:
- Reference list for values and categories.

What is good:
- Helpful for tooltip descriptions and display logic.

Watch out for:
- It is not a full semantic dimension table.
- It should not be the backbone of your model.

Use it for:
- helper tooltips
- legend ordering support
- QA checks on category names

## 6. Recommended improvements for the dashboard

Use these improved page titles:
- Q1: Which entry-level role offers the best mix of demand and pay?
- Q6: Which industries offer the highest senior salary ceilings?
- Q11: How does pay vary by work arrangement?
- Q13: How do entry-level salaries compare between analytics and engineering roles?
- Q14: Do advanced cloud skills correlate with higher pay?
- Q16: How has hiring volume changed over time?
- Q18: Which skills show the strongest advanced-level demand?
- Q19: Is one mid-level hire cheaper than two entry-level hires?
- Q21: Which country-year combinations score highest on job volume and pay?
- Q25: How does hiring growth differ by company size?

Recommended visual tone:
- Keep the dashboard analytical, not sensational.
- Use "compare", "correlate", "trend", and "share" language.
- Avoid "prove", "best", and "cause" unless the page clearly supports it.

## 7. Power BI modeling guidance

Recommended approach:
- Use `ai_jobs.csv` as the core fact table.
- Use `skills_demand.csv` as a secondary fact table linked by `job_id`.
- Use `job_title_mapping.csv` as a small dimension.
- Treat `powerbi_data/*.csv` as page-level analytic marts or export tables.

If you only use `powerbi_data`:
- Keep each page mostly independent.
- Avoid forcing relationships between unrelated aggregated tables.
- Use separate slicers per page when necessary.

If you use the full raw model:
- Build dimensions for Country, Year, Job Title, Experience Level, Industry, Company Size, and Work Arrangement.
- Then use the `powerbi_data` tables only when they save time or support specific visuals.

## 8. Suggested KPI cards

Good KPI candidates:
- Total jobs
- Average salary
- Average senior salary ceiling
- Remote share
- Top opportunity country-year
- Top advanced-demand skill
- Number of cases where mid-level is cheaper than two juniors

## 9. Final recommendation

The current `powerbi_data` folder is usable and mostly well prepared for a strong Power BI dashboard. The biggest improvement is not adding more visuals, but tightening the story:

- rename the question titles so they match the data exactly
- present the dataset as synthetic market analysis
- use the raw files for shared slicers when you want a more connected report
- use the aggregated files for focused question pages

If you build the report this way, it will feel much more credible, cleaner, and easier to explain during presentation.
