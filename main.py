#!/usr/bin/env python3

import requests
import json
from os import getenv
from fastapi import FastAPI, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse, RedirectResponse
from src.wiki import WikiSummarySearch

# TODO: 
# Populate a dynamodb table with the latest queries with timestamps. Eventually sort functionality by top 10, etc.
# /random: pick random topic and tell me about it

app = FastAPI(
    title="Wikipedia Search Service",
    description="API that searches wikipedia based on search term",
    version="1.0.0",
)

class Search(BaseModel):
    term: str

wiki = WikiSummarySearch()

@app.get("/health")
def health():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"Status": "Healthy"})

@app.get("/")
def root():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"Response": "Please navigate to /docs for more information"})

def post_summary_results(term, results):
    return requests.post(
        url=f"http://{getenv('SUMMARY_API_URL')}/summary",
        data=json.dumps({'term': term, 'results': results}),
        headers={'Content-Type': 'application/json'}
    )

@app.post("/summary")
def return_summary_result(search_term: Search):
    """
    Returns response with summary, recommendation for too generic of searches, and error if nothing.
    """
    try:
        result = wiki.get_summary(search_term.term)
        if result['Status'] in ['Error', 'NotFound']:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result)
        else:
            #post_summary_results(search_term.term, result['Response'])
            return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"Response": e})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info")
