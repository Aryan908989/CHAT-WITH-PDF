import os
from dotenv import load_dotenv
from groq import Groq

from rag.config import LLM_MODEL

load_dotenv()
_api_key = os.getenv("GROQ_API_KEY")
if not _api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=_api_key)

SYSTEM_PROMPT = """You answer questions using ONLY the context provided.
If the answer is not in the context, reply exactly: I don't know based on this document.
Be concise. Mention page numbers like (page 3) when you use a fact."""


def answer_question(question, chunks):
    if not chunks:
        return "I don't know based on this document."

    context = "\n\n".join(f"[Page {c['page']}]\n{c['text']}" for c in chunks)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=3000,
    )
    return response.choices[0].message.content