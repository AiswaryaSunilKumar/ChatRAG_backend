from pydantic import BaseModel
from typing import List, Dict, Any
from langchain_core.documents import Document

class VectorRequest(BaseModel):
    table_path :str
    docs : List[Document]

class VectorResponse(BaseModel):
    table_path :str