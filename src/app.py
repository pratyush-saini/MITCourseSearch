from fastapi import FastAPI
from thirdai import neural_db as ndb

db = ndb.NeuralDB.from_checkpoint("model.ndb")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/query")
async def read_item(query_str):
    results = db.search(query_str)
    json_response = {
        "results": [r.metadata for r in results]
    }
    return {"results": json_response}
