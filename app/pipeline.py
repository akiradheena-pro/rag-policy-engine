import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables from .env file (if present)
load_dotenv()

def ask_question(query: str):
    """
    Answers a user question using RAG over company policies.
    
    Args:
        query (str): User's question about company policy.
        
    Returns:
        dict: {
            "answer": str,          # Generated answer
            "sources": list[str],   # List of source document names
            "snippets": list[str]   # Optional: retrieved context snippets
        }
    """
    # 1. Initialize embeddings and vector store
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    
    # 2. Retrieve top-k relevant chunks
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)
    
    if not docs:
        return {
            "answer": "I cannot find any relevant information in the provided policies to answer your question.",
            "sources": [],
            "snippets": []
        }
    
    # 3. Build context and extract sources
    context = "\n\n".join([d.page_content for d in docs])
    sources = list(set([d.metadata.get('source', 'Unknown') for d in docs]))
    snippets = [d.page_content[:150] + "..." for d in docs]  # Optional: for UI display
    
    # 4. Get Groq API key from environment
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise EnvironmentError(
            "❌ GROQ_API_KEY not found. Please set it in .env file or system environment variables."
        )
    
    # 5. Initialize LLM (Groq)
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        groq_api_key=groq_api_key,
        temperature=0  # deterministic responses
    )
    
    # 6. Prompt with strict guardrails
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
    
    # 7. Generate response
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


# --- Local Test Block (for development only) ---
if __name__ == "__main__":
    print("🧪 Testing RAG Pipeline...\n")
    
    test_questions = [
        "How many days of PTO do employees receive annually?",
        "Can I expense alcohol?",
        "How many remote work days are allowed per week?",
        "Do unused PTO days roll over to next year?",
        "Are receipts required for meals under $25?"
    ]
    
    for q in test_questions:
        print(f"❓ Question: {q}")
        try:
            result = ask_question(q)
            print(f"✅ Answer: {result['answer']}")
            print(f"📚 Sources: {result['sources']}")
        except Exception as e:
            print(f"❌ Error: {e}")
        print("-" * 60)