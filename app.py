import hashlib
import io

import streamlit as st
from pypdf import PdfReader

from rag.config import UPLOAD_DIR, TOP_K
from rag.loader import load_pdf
from rag.chunker import chunk_pages
from rag.store import collection_exists, index_chunks, search
from rag.generate import answer_question

st.set_page_config(page_title="Ask your PDF", page_icon="📄")
st.title("📄 Ask your PDF")
st.caption("Upload a document, then ask questions in plain English.")


def relevance_label(score):
    """Turn a raw similarity score into words a user understands."""
    if score >= 0.5:
        return "🟢 Very relevant"
    if score >= 0.35:
        return "🟡 Relevant"
    return "🟠 Possibly relevant"


def show_sources(chunks):
    """Show where the answer came from, without technical terms."""
    if not chunks:
        return
    pages = sorted({c["page"] for c in chunks})
    page_text = ", ".join(str(p) for p in pages)
    with st.expander(f"📚 See where this came from (page {page_text})"):
        for c in chunks:
            st.markdown(f"**Page {c['page']}** · {relevance_label(c['score'])}")
            preview = c["text"][:300] + ("..." if len(c["text"]) > 300 else "")
            st.caption(preview)
            st.divider()


# ---------- Sidebar ----------
with st.sidebar:
    st.header("Your document")
    uploaded = st.file_uploader("Upload a PDF", type="pdf")

if not uploaded:
    st.info("👈 Start by uploading a PDF from the left panel.")
    st.stop()

# ---------- Prepare the PDF (only once per file) ----------
data = uploaded.getvalue()
file_id = hashlib.md5(data).hexdigest()[:12]
collection = f"pdf_{file_id}"

if st.session_state.get("file_id") != file_id:
    st.session_state.file_id = file_id
    st.session_state.messages = []

    if not collection_exists(collection):
        with st.spinner("Reading your document... this may take a minute."):
            UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
            path = UPLOAD_DIR / f"{file_id}.pdf"
            path.write_bytes(data)

            pages = load_pdf(path)
            chunks = chunk_pages(pages)

            if not chunks:
                st.error(
                    "😕 I couldn't find any text in this PDF. "
                    "It may be a scanned document (images only). Try a different file."
                )
                st.stop()

            index_chunks(collection, chunks, uploaded.name)

total_pages = len(PdfReader(io.BytesIO(data)).pages)
st.sidebar.success("✅ Ready! Ask your questions.")
st.sidebar.write(f"**File:** {uploaded.name}")
st.sidebar.write(f"**Pages:** {total_pages}")

# ---------- Welcome message ----------
if not st.session_state.messages:
    st.markdown(
        "**Try asking things like:**\n"
        "- What is this document about?\n"
        "- Summarize the main points\n"
        "- What does it say about *(any topic)*?"
    )

# ---------- Chat history ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            show_sources(msg["sources"])

# ---------- New question ----------
question = st.chat_input("Type your question here...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Looking through your document..."):
                chunks = search(collection, question, top_k=TOP_K)
                answer = answer_question(question, chunks)
        except Exception:
            chunks = []
            answer = "⚠️ Something went wrong while answering. Please try again."

        if not chunks:
            answer = (
                "🤔 I couldn't find this in your document. "
                "Try rephrasing your question, or ask about something the document covers."
            )

        st.markdown(answer)
        show_sources(chunks)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": chunks}
    )