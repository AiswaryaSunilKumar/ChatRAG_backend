import os
from typing import List
import re
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from sqlalchemy import create_engine, text

import os
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from sqlalchemy import create_engine, text

from services.llm.config_llm import LLMFactory
from services.llm.settings import settings
from langchain_community.document_loaders import UnstructuredPDFLoader


def load_pdf(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    return docs

# def load_pdf(pdf_path: str):
#     loader = UnstructuredPDFLoader(
#         pdf_path, 
#         mode="elements",
#         strategy="hi_res" 
#     )
    
#     docs = loader.load()
#     return docs


def chunk_documents(docs):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000,
        chunk_overlap=1000,
        separators=["\n\n", "."],
    )
    chunks = splitter.split_documents(docs)
    return chunks


def get_embedding(text: str, embeddings) -> List[float]:
    response = embeddings.embed_query(text)
    return response

def sanitize_table_name(name: str) -> str:
    name = name.lower()
    name = re.sub(r'[^a-z0-9_]', '_', name)
    if not re.match(r'^[a-z_]', name):       
        name = f"t_{name}"
    return name

def create_table_if_not_exists(engine,pdf_path):

    pdf_path = pdf_path.replace(".pdf", "")
    table_name = sanitize_table_name(pdf_path)
    create_table_sql = f"""
    CREATE EXTENSION IF NOT EXISTS vector;

    DROP TABLE IF EXISTS {table_name};

    CREATE TABLE {table_name} (
        id BIGSERIAL PRIMARY KEY,
        source_file TEXT,
        page_number INT,
        chunk_index INT,
        chunk_text TEXT,
        embedding vector(3072) 
    );
    """

    with engine.begin() as conn:
        conn.execute(text(create_table_sql))


def insert_chunks_with_embeddings(engine, chunks, source_file: str, embeddings):
    pdf_path = source_file.replace(".pdf", "") 
    table_name = sanitize_table_name(pdf_path)
    insert_sql = f"""
        INSERT INTO {table_name} (source_file, page_number, chunk_index, chunk_text, embedding)
        VALUES (:source_file, :page_number, :chunk_index, :chunk_text, :embedding)
    """

    with engine.begin() as conn:
        for i, chunk in enumerate(chunks):
            page_number = chunk.metadata.get("page", None)
            chunk_text = chunk.page_content

            embedding = get_embedding(chunk_text, embeddings)
            conn.execute(
                text(insert_sql),
                {
                    "source_file": source_file,
                    "page_number": page_number,
                    "chunk_index": i,
                    "chunk_text": chunk_text,
                    "embedding": embedding,  
                },
            )

def create_vector_store(PDF_PATH,docs):
    # docs = load_pdf(PDF_PATH)
    chunks = chunk_documents(docs)

    engine = create_engine(settings.SUPABASE_CONNECTION_STRING)

    create_table_if_not_exists(engine, PDF_PATH)

    insert_chunks_with_embeddings(engine, chunks, source_file=PDF_PATH, embeddings=LLMFactory.gemini_embeddings())

    return PDF_PATH

