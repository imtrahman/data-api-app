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
    from boto3 import client
    from datetime import datetime
    timestamp = datetime.now().strftime("%H%M%S%d%m%Y")
    try:
        ddb = client('dynamodb')
        ddb.put_item(
            TableName=getenv('TableName'),
            Item={
                "TimeStamp": {
                    "N": timestamp
                },
                "SearchTerm": {
                    "S": term
                },
                "SearchResults": {
                    "S": results
                }
            }
        )
        return "Successfully put item in database"
    except Exception as e:
        print(e)
        return "Error: Unable to put item in database"

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
            response = post_summary_results(search_term.term, result['Response'])
            print(response)
            return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"Response": e})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info")
