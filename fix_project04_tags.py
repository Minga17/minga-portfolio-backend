from database import get_db
import json

db = get_db()

# Add rows tag to Project 04 which was missing it
tags = json.dumps(["Python", "Pandas", "Matplotlib", "Data Cleaning", "EDA", "9,994 Rows"])
db.execute("UPDATE projects SET tags = ? WHERE number = 4", [tags])
db.commit()

row = db.execute("SELECT tags FROM projects WHERE number = 4").fetchone()
print("Project 04 tags:", row[0])
db.close()
