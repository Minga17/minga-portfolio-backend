from database import get_db

db = get_db()

# Project 09 - Job Market Analysis - in progress
db.execute("UPDATE projects SET status = 'active', date = 'Jul 2026' WHERE number = 9")

# Project 10 - World Happiness Report - in progress
db.execute("UPDATE projects SET status = 'active', date = 'Jul 2026' WHERE number = 10")

# Project 12 - Africa Development Dashboard - in progress
db.execute("""
    UPDATE projects SET 
        status = 'active',
        date = 'Jul 2026',
        date_sub = 'SQL · Excel · Tableau · Power BI',
        title = 'Africa Rising: Economic and Social Development Dashboard',
        category = 'Data Analysis · Dashboard · SQL · Tableau · Power BI',
        problem = 'Using 30 years of World Bank data covering 53 African countries, this project tracks how Zimbabwe, DRC and the wider continent have changed across GDP, life expectancy, electricity access, internet usage and school enrollment. The question: what do the numbers actually say about development in Africa?',
        what_i_did = 'Downloaded 8.2 million rows of World Bank data from Kaggle, cleaned and filtered to 53 African countries and 6 key indicators using Python. Wrote 6 SQL queries in DB Browser for SQLite to answer real business questions. Building interactive charts in Tableau and a final executive dashboard in Power BI.'
    WHERE number = 12
""")

db.commit()

rows = db.execute("SELECT number, title, status FROM projects WHERE number IN (9, 10, 12)").fetchall()
for r in rows:
    print(f"Project {r[0]}: {r[1]} — {r[2]}")

db.close()
