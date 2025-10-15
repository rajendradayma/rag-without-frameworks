from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from backend.rag import InMemoryRAG
from backend.pdf_loader import load_pdf_and_chunk
from backend.llm_client import GroqClient

app = FastAPI()
rag = InMemoryRAG()
llm = GroqClient()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.post("/upload_pdf/")
async def upload_pdf(pdf: UploadFile = File(...)):
    content = await pdf.read()
    from io import BytesIO
    chunks = load_pdf_and_chunk(BytesIO(content))
    rag.add_chunks(chunks)
    return {"status": "success", "chunks_added": len(chunks)}

@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    top_chunks = rag.retrieve(question, top_k=3)
    if not top_chunks:
        context = "No relevant data was found in the uploaded documents."
    else:
        context = "\n\n".join(top_chunks)
    full_prompt = (
        f"Answer the following question based ONLY on the given context from PDF materials.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n"
    )
    try:
        answer = await llm.generate(full_prompt)
    except Exception as e:
        answer = f"Error with LLM: {str(e)}"
    return {"answer": answer, "retrieved_context": top_chunks}

