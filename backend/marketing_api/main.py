from fastapi import FastAPI

app = FastAPI(version="0.1")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}