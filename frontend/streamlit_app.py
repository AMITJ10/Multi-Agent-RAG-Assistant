import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Multi-Agent RAG Assistant",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Multi-Agent RAG Assistant")

st.write(
    "How can I help you today? Upload documents and ask anything. "
    "I’ll search your uploaded files first. If the answer is not found, "
    "I’ll use free internet sources."
)

with st.sidebar:
    st.header("Upload Documents")

    uploaded_files = st.file_uploader(
        "Upload up to 10 PDF files",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        if len(uploaded_files) > 10:
            st.error("You can upload at most 10 PDFs.")
        else:
            file_names = [file.name for file in uploaded_files]

            if "last_uploaded_files" not in st.session_state:
                st.session_state.last_uploaded_files = []

            if file_names != st.session_state.last_uploaded_files:
                files = []

                for uploaded_file in uploaded_files:
                    files.append(
                        (
                            "files",
                            (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                "application/pdf",
                            ),
                        )
                    )

                try:
                    with st.spinner("Indexing uploaded documents..."):
                        response = requests.post(
                            f"{API_URL}/upload",
                            files=files,
                            timeout=180,
                        )

                    if response.status_code == 200:
                        st.session_state.last_uploaded_files = file_names
                        st.success("Documents uploaded and indexed successfully.")
                    else:
                        st.error("Upload/indexing failed.")

                except requests.exceptions.ConnectionError:
                    st.error(
                        "Backend is not running. Start FastAPI on http://127.0.0.1:8000"
                    )
            # else:
            #     st.info("Documents already indexed.")

            if st.button("Re-index Documents"):
                st.session_state.last_uploaded_files = []
                st.rerun()

st.header("Ask a Question")

question = st.text_input("Enter your question")

if st.button("Ask AI"):
    if not question:
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Searching documents and internet if needed..."):
                response = requests.post(
                    f"{API_URL}/chat",
                    json={"question": question},
                    timeout=180,
                )

            if response.status_code == 200:
                data = response.json()

                st.subheader("Final Answer")
                st.success(data["answer"])

                next_questions = data.get("next_questions", [])

                if next_questions:
                    st.subheader("Recommended Next Questions")

                    for q in next_questions:
                        st.write(f"👉 {q}")
            else:
                st.error("Something went wrong.")

        except requests.exceptions.ConnectionError:
            st.error(
                "Backend is not running. Start FastAPI on http://127.0.0.1:8000"
            )