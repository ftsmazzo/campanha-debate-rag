from fastapi import FastAPI

app = FastAPI(title="Campanha Debate RAG")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/")
def root() -> dict:
    return {"service": "campanha-debate-rag", "status": "ok"}
