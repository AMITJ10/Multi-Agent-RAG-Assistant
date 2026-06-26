import streamlit as st
import requests


API_URL = "https://multi-agent-rag-assistant.onrender.com"

MAX_FILES = 5
MAX_FILE_SIZE_MB = 10

st.set_page_config(
    page_title="Multi-Agent RAG Assistant",
    page_icon="🤖",
    layout="wide",
)

st.markdown(
    """
    <style>
    [data-testid="stFileUploaderDropzoneInstructions"] small {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
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
        "Upload up to 5 PDF files, max 10 MB each",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        too_many_files = len(uploaded_files) > MAX_FILES
        oversized_files = [
            file.name
            for file in uploaded_files
            if file.size > MAX_FILE_SIZE_MB * 1024 * 1024
        ]

        if too_many_files:
            st.error("You can upload at most 5 PDFs.")

        elif oversized_files:
            st.error("Each PDF must be 10 MB or smaller.")

        else:
            file_signature = [
                f"{file.name}-{file.size}"
                for file in uploaded_files
            ]

            if "last_uploaded_files" not in st.session_state:
                st.session_state.last_uploaded_files = []

            if file_signature != st.session_state.last_uploaded_files:
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
                    with st.spinner("Uploading and indexing documents..."):
                        response = requests.post(
                            f"{API_URL}/upload",
                            files=files,
                            timeout=180,
                        )

                    if response.status_code == 200:
                        st.session_state.last_uploaded_files = file_signature
                        st.success("Documents uploaded and indexed successfully.")
                    else:
                        try:
                            error_detail = response.json().get("detail", "Upload failed.")
                        except Exception:
                            error_detail = "Upload failed."
                        st.error(error_detail)

                except requests.exceptions.ReadTimeout:
                    st.error(
                        "Upload timed out. The free backend server is slow. "
                        "Try a smaller PDF or wait and try again."
                    )

                except requests.exceptions.ConnectionError:
                    st.error("Backend is not reachable. Please check Render backend.")

                except Exception as e:
                    st.error(f"Unexpected upload error: {str(e)}")

            else:
                st.info("Documents already indexed.")

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
                    timeout=120,
                )

            if response.status_code == 200:
                data = response.json()

                st.subheader("Final Answer")
                st.success(data.get("answer", "No answer returned."))

                next_questions = data.get("next_questions", [])

                if next_questions:
                    st.subheader("Recommended Next Questions")
                    for q in next_questions:
                        st.write(f"👉 {q}")
            else:
                st.error("Something went wrong while getting the answer.")

        except requests.exceptions.ReadTimeout:
            st.error("The backend is taking too long. Please try again.")

        except requests.exceptions.ConnectionError:
            st.error("Backend is not reachable. Please check Render backend.")

        except Exception as e:
            st.error(f"Unexpected chat error: {str(e)}")