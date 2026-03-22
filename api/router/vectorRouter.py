from fastapi import APIRouter, Query
from services.vector_store.creation import create_vector_store
from api.model.vectorModel import VectorRequest, VectorResponse

router = APIRouter()


@router.post("/vector", response_model = VectorResponse)
async def query(request : VectorRequest):
    return {"table_path" : create_vector_store(request.table_path, request.docs)}
    
