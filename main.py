from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import pandasai as pai
from pandasai_litellm.litellm import LiteLLM
import os, io

app = FastAPI(title="PandasAI on Render")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def configure_pandasai():
    if OPENAI_API_KEY:
        llm = LiteLLM(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
        pai.config.set({"llm": llm})
    else:
        pai.config.set({})

configure_pandasai()

@app.post("/chat-csv")
async def chat_csv(prompt: str = Form(...), file: UploadFile = File(...)):
    if file.content_type not in ("text/csv","application/vnd.ms-excel","application/octet-stream"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")
    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not parse CSV: {e}")
    configure_pandasai()
    if not pai.config.get("llm"):
        raise HTTPException(status_code=500, detail="LLM not configured. Set OPENAI_API_KEY.")
    try:
        response = df.chat(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PandasAI error: {e}")
    return JSONResponse({"response": str(response)})

@app.get("/health")
def health():
    return {"status":"ok"}
