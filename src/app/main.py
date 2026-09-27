import os

import sentry_sdk
from fastapi import FastAPI

sentry_dsn = os.environ.get("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(dsn=sentry_dsn, traces_sample_rate=0.0, send_default_pii=False)

app = FastAPI(title="Campanha Debate RAG")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/")
def root() -> dict:
    return {"service": "campanha-debate-rag", "status": "ok"}
