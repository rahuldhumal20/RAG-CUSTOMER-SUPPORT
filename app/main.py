
from fastapi import FastAPI
from pydantic import BaseModel

from app.embedder import build_vector_store
from app.graph import app_graph

app = FastAPI()

print("Building Vector DB...")

build_vector_store()


class QueryRequest(BaseModel):
    query:str


@app.get("/")
def home():

    return {
      "message":"RAG Customer Support API Running"
    }


@app.post("/ask")
def ask_question(data:QueryRequest):

    result = app_graph.invoke(
       {
         "query":data.query,
         "context":"",
         "route":"",
         "response":""
       }
    )

    return {
       "query":data.query,
       "answer":result["response"]
    }