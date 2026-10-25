import os
from datetime import date
from functools import lru_cache
import psycopg
from fastapi import FastAPI,Query
from sentence_transformers import SentenceTransformer
app=FastAPI()
@lru_cache
def encoder():return SentenceTransformer("all-MiniLM-L6-v2")
@app.get("/search")
def search(q:str=Query(min_length=1,max_length=500),equipment:str|None=None,severity:str|None=None,start:date|None=None,end:date|None=None):
 vector="["+ ",".join(map(str,encoder().encode(q,normalize_embeddings=True).tolist()))+"]"
 with psycopg.connect(os.environ["DATABASE_URL"]) as db:
  rows=db.execute("""SELECT id,equipment,occurred,severity,body,
   .7*(1-(embedding<=>%s::vector))+.3*ts_rank_cd(search,websearch_to_tsquery('english',%s)) AS score
   FROM maintenance WHERE (%s::text IS NULL OR equipment=%s) AND (%s::text IS NULL OR severity=%s)
   AND (%s::date IS NULL OR occurred>=%s) AND (%s::date IS NULL OR occurred<=%s)
   ORDER BY score DESC,id LIMIT 20""",(vector,q,equipment,equipment,severity,severity,start,start,end,end)).fetchall()
 return [dict(zip(["id","equipment","date","severity","text","score"],r)) for r in rows]
