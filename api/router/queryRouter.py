from fastapi import APIRouter, Query
from services.agent.assistant import research_assistant
from api.model.queryModel import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/query", response_model = QueryResponse)
async def query(request : QueryRequest):
    return {"answer" : research_assistant(request.query, request.table_path)}
    
