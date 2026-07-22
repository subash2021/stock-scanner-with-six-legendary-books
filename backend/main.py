from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import json
import os
from datetime import datetime
from scanners.unified_scanner import UnifiedScanner

app = FastAPI(title="10X Stock Scanner", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scanner = UnifiedScanner()

CACHE_FILE = "scan_cache.json"


def load_cache() -> Dict:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {"results": [], "last_scan": None}


def save_cache(results: List[Dict]):
    cache = {"results": results, "last_scan": datetime.now().isoformat()}
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)


@app.get("/")
def root():
    return {"message": "10X Stock Scanner API", "version": "3.0.0"}


@app.get("/api/scan")
def run_scan(background_tasks: BackgroundTasks):
    results = scanner.scan()
    background_tasks.add_task(save_cache, results)
    return {
        "status": "success",
        "count": len(results),
        "last_scan": datetime.now().isoformat(),
        "results": results
    }


@app.get("/api/stock/{ticker}")
def get_stock_analysis(ticker: str):
    result = scanner.analyze_stock(ticker.upper())
    if not result:
        raise HTTPException(status_code=404, detail=f"Could not analyze {ticker}")
    return result


@app.get("/api/results")
def get_results():
    cache = load_cache()
    return {
        "last_scan": cache.get("last_scan"),
        "count": len(cache.get("results", [])),
        "results": cache.get("results", [])
    }


@app.get("/api/top")
def get_top(limit: int = 20):
    cache = load_cache()
    results = cache.get("results", [])
    return {
        "count": min(limit, len(results)),
        "results": results[:limit]
    }


@app.get("/api/scan/status")
def get_scan_status():
    cache = load_cache()
    return {
        "last_scan": cache["last_scan"],
        "cached_results": len(cache["results"])
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
