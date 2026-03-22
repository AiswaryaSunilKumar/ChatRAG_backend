from fastapi import APIRouter, Query
from services.vector_store.creation import create_vector_store
from api.model.vectorModel import VectorRequest, VectorResponse
from langchain_core.documents import Document

router = APIRouter()


@router.post("/vector", response_model = VectorResponse)
async def query(request : VectorRequest):
    docs = [
        Document(
            page_content=d["page_content"],
            metadata=d.get("metadata", {})
        )
        for d in request.docs
    ]
    return {"table_path" : create_vector_store(request.table_path, docs)}
    
