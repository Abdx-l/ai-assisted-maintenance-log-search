import os,random
from datetime import date,timedelta
import psycopg
from app import encoder
rng=random.Random(42)
with psycopg.connect(os.environ["DATABASE_URL"]) as db:
 if db.execute("SELECT count(*) FROM maintenance").fetchone()[0]:raise SystemExit("Database already seeded")
 for i in range(5000):
  issue=rng.choice(["bearing vibration","oil pressure low","coolant leak","filter replacement","normal inspection"])
  text=f"{issue} on pump {i%200}; technician inspected unit"
  vector="["+ ",".join(map(str,encoder().encode(text,normalize_embeddings=True).tolist()))+"]"
  db.execute("INSERT INTO maintenance(equipment,occurred,severity,body,embedding) VALUES(%s,%s,%s,%s,%s::vector)",(f"P{i%200}",date(2025,1,1)+timedelta(days=i%365),rng.choice(["low","medium","high"]),text,vector))
