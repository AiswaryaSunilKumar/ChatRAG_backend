from .creation import sanitize_table_name
from sqlalchemy import create_engine, text
from ..llm.config_llm import LLMFactory
from ..llm.settings import settings

def get_similar_chunks(engine,query,table_name, top_k=10):
    embeddings = LLMFactory.gemini_embeddings()
    query_embedding = embeddings.embed_query(query)
    sql = text(f"""  
    SELECT chunk_text
    FROM {table_name}
    ORDER BY embedding <=> CAST(:query_embedding AS vector)
    LIMIT :top_k;
    """)

    with engine.begin() as conn:
        result = conn.execute(sql, {"query_embedding": query_embedding, "top_k": top_k})
        return [row[0] for row in result]


def search_vector_store(query,pdf_path, top_k=5):
    pdf_path = pdf_path.replace(".pdf", "")
    table_name = sanitize_table_name(pdf_path)
    engine = create_engine(settings.SUPABASE_CONNECTION_STRING)
    search_result = get_similar_chunks(engine, query, table_name, top_k)
    ret_info = ""
    for i in search_result:
        ret_info += "------------------------------------------------ \n\n" + i + "\n\n"
    print(ret_info)
    return ret_info
