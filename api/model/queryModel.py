from pydantic import BaseModel
from typing import List, Dict, Any

class QueryRequest(BaseModel):
    query: str
    table_path :str

class QueryResponse(BaseModel):
    answer: str