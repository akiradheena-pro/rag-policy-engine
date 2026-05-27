import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Initialize once at module load, not on every query
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

def ask_question(query: str):
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)
    
    if not docs:
        return {
            "answer": "I cannot find any relevant information in the provided policies to answer your question.",
            "sources": [],
            "snippets": []
        }
    
    context = "\n\n".join([d.page_content for d in docs])
    sources = list(set([d.metadata.get('source', 'Unknown') for d in docs]))
    snippets = [d.page_content[:150] + "..." for d in docs]
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise EnvironmentError("❌ GROQ_API_KEY not found.")
    
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        groq_api_key=groq_api_key,
        temperature=0
    )
    
    prompt_template = """
You are an HR Policy Assistant. Answer ONLY based on the provided context.
If the answer is not in the context, say: "I cannot answer this question based on the provided policies."
Always cite the source document name(s) in your answer.
Keep answers concise and professional.
Context:
{context}
Question:
{question}
Answer:
"""
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | llm
    
    try:
        response = chain.invoke({"context": context, "question": query})
        answer_text = response.content.strip()
    except Exception as e:
        answer_text = f"Error generating answer: {str(e)}"
    
    return {
        "answer": answer_text,
        "sources": sources,
        "snippets": snippets
    }
