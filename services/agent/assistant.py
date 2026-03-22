from ..llm.config_llm import LLMFactory
from ..vector_store.search import search_vector_store

def research_assistant(query, pdf_path):
    llm = LLMFactory.gemini()

    ret_info = search_vector_store(query, pdf_path, top_k=5)

    prompt = """ 
    You are a keen assistant and an expert in reading Research papers. 
    You are given a user query and 10 excerpts from the Research paper which is linked to the user query. Use it to answer the user query.

    If any information is missing in the excerpts, DO NOT MENTION THAT TO THE USER.
    ALSO, THEN AND ONLY THEN TRY TO ANSWER THE QUERY FROM YOUR INTERNAL KNOWLEDGE BASE

    User Query : {query}

    Excerpts : {ret_info}

    """

    prompt = prompt.format(query=query, ret_info=ret_info)

    response = llm.invoke(prompt)

    return response.content


