from pydantic import BaseModel
from typing import List, Dict, Any

class VectorRequest(BaseModel):
    table_path :str

class VectorResponse(BaseModel):
    table_path :str