import time
import streamlit as st
import requests


API_URL = "https://multi-agent-rag-assistant.onrender.com"

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
                    with st.spinner("Uploading documents..."):
                        response = requests.post(
                            f"{API_URL}/upload",
                            files=files,
                            timeout=60,
                        )

                    if response.status_code == 200:
                        st.session_state.last_uploaded_files = file_names
                        st.success("Documents uploaded. Indexing started in background.")

                        status_box = st.empty()

                        for _ in range(40):
                            status_response = requests.get(
                                f"{API_URL}/index-status",
                                timeout=20,
                            )

                            if status_response.status_code != 200:
                                status_box.warning("Checking indexing status...")
                                time.sleep(5)
                                continue

                            status_data = status_response.json()
                            status = status_data.get("status")
                            message = status_data.get("message", "")

                            if status == "completed":
                                status_box.success("Documents indexed successfully.")
                                break

                            if status == "failed":
                                status_box.error(f"Indexing failed: {message}")
                                break

                            status_box.info("Indexing documents... please wait.")
                            time.sleep(5)

                    else:
                        st.error("Upload failed. Try a smaller PDF.")

                except requests.exceptions.ReadTimeout:
                    st.error("Upload timed out. Please try a smaller PDF.")

                except requests.exceptions.ConnectionError:
                    st.error("Backend is not reachable. Please check Render backend.")

                except Exception as e:
                    st.error(f"Unexpected upload error: {str(e)}")

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