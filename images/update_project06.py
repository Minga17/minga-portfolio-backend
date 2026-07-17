from database import get_db
import json

db = get_db()

insights = json.dumps([
    "Total revenue of £10,666,684.54 across 530,104 transactions.",
    "4,338 unique customers across 38 countries worldwide.",
    "19,960 total orders covering 4,026 unique products.",
    "Best selling product: PAPER CRAFT, LITTLE BIRDIE with 80,995 units sold.",
    "Peak month was November 2011 with £1,509,496.33 in revenue — driven by Black Friday.",
    "Peak trading hours are 10am–12pm — when most orders are placed.",
    "United Kingdom dominates revenue as expected — this is a UK-based retailer.",
])

tags = json.dumps([
    "Python", "SQL", "SQLite", "Pandas", "Matplotlib",
    "Data Pipeline", "EDA", "530,104 Rows"
])

db.execute("""
    UPDATE projects SET
        status      = 'done',
        insights    = ?,
        tags        = ?,
        github_url  = 'https://github.com/Minga17/sql-python-pipeline',
        kaggle_url  = 'https://www.kaggle.com/code/mingangolo/notebook095e3b4cf3',
        chart_image = 'images/chart3_monthly_revenue.png',
        what_i_did  = 'Loaded 541,909 rows of e-commerce data, cleaned it with Pandas, then loaded it into a real SQLite database. Wrote 6 SQL queries using COUNT, SUM, GROUP BY, ORDER BY, DISTINCT and strftime to answer real business questions. Pulled results back into Python with pd.read_sql() and built 4 Matplotlib charts. This mirrors how data actually flows in real companies — SQL does the heavy lifting, Python handles the presentation.'
    WHERE number = 6
""", [insights, tags])

db.commit()

row = db.execute("SELECT status, github_url, kaggle_url FROM projects WHERE number = 6").fetchone()
print("Status:", row[0])
print("GitHub:", row[1])
print("Kaggle:", row[2])
db.close()
print("Done!")
