from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pytube import YouTube
from thirdai import neural_db as ndb

app = FastAPI()
db = ndb.NeuralDB.from_checkpoint("model.ndb")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/query/")
async def search_youtube(query_text: str):
    # video_details = get_video_details(query_text)
    results = db.search(query_text, top_k=10)
    json_response = [r.metadata for r in results]
    return {"results": json_response}

if __name__ == "__main__":
    import uvicorn
# uvicorn main:app --reload --port 8000
