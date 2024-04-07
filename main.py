import os

from dotenv import load_dotenv

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.indexes import VectorstoreIndexCreator
from langchain_experimental.agents import create_csv_agent
from langchain_community.document_loaders import pdf
from langchain_community.document_loaders.merge import MergedDataLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

import streamlit as st

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)

header = st.container()
header.title("Neuramonks Assignment")
header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

st.markdown(
    """
<style>
    div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
        position: sticky;
        top: 2.875rem;
        background-color: #0e1016;
        z-index: 999;
    }
    .fixed-header {
        border-bottom: 1px solid black;
    }
</style>
    """,
    unsafe_allow_html=True
)


@st.cache_resource
def prepare_docs(upload_files):
    index = csv_agent = None
    pdf_docs = []
    csv_docs = []

    for upload_file in upload_files:
        if 'csv' == upload_file.name.split(".")[-1]:
            csv_docs.append(os.path.join("uploads", upload_file.name))
        if 'pdf' == upload_file.name.split(".")[-1]:
            pdf_docs.append(os.path.join("uploads", upload_file.name))

    if pdf_docs:
        loaders = []
        for doc in pdf_docs:
            loaders.append(pdf.PyMuPDFLoader(doc))
        loader_merged = MergedDataLoader(loaders=loaders)
        index = VectorstoreIndexCreator(
            embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=google_api_key),
            text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        ).from_documents(loader_merged.load())

    if csv_docs:
        csv_agent = create_csv_agent(llm, csv_docs, pandas_kwargs={'delimiter': ';'})

    return index, csv_agent


def format_response(pdf_response, csv_response, index, csv_agent):

    response = ""
    if index is not None:
        response += "Response from pdf \n\n" + pdf_response['result']

    if csv_agent is not None:
        response += "\n\nResponse from CSV\n\n" + csv_response['output']

    return response


st.sidebar.header("Upload Files")
uploaded_files = st.sidebar.file_uploader("Upload your files", type=['pdf', "csv"], accept_multiple_files=True)

if 'flag' not in st.session_state:
    st.session_state.flag = 0
if uploaded_files:

    st.sidebar.success("Files uploaded successfully.")
    for uploaded_file in uploaded_files:
        st.sidebar.markdown(f"Selected file: {uploaded_file.name}")
        os.makedirs("uploads", exist_ok=True)
        if not os.path.exists(f"uploads/{uploaded_file.name}"):
            with open(f"uploads/{uploaded_file.name}", "wb") as file:
                file.write(uploaded_file.getvalue())
    if st.sidebar.button("Prepare Docs for QnA"):
        with st.spinner("Preparing Your Files for QnA"):
            prepare_docs(uploaded_files)
            st.session_state.flag = 1
    if st.session_state.flag:
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        for message in st.session_state.messages:
            st.chat_message(message['role']).markdown(message['content'])
        question = st.chat_input('Ask any question...')

        if question:
            st.chat_message('user').markdown(question)
            st.session_state.messages.append({'role': 'user', 'content': question})

            index, csv_agent = prepare_docs(uploaded_files)

            with st.spinner("Processing Your Question..."):
                pdf_response = {"result": ""}
                csv_response = {"output": ""}
                if index is not None:
                    retriever = index.vectorstore.as_retriever()
                    prompt = PromptTemplate(
                        template="""You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
                        Question: {question}
                        Context: {context}
                        Answer:""",
                        input_variables=["context", "question"])

                    rag_chain = RetrievalQA.from_chain_type(
                        llm=llm,
                        chain_type="stuff",
                        retriever=retriever,
                        return_source_documents=True,
                        chain_type_kwargs={"prompt": prompt}, )
                    pdf_response = rag_chain.invoke(question)

                if csv_agent is not None:
                    csv_response = csv_agent.invoke(question, handle_parsing_errors=True)

                response = format_response(pdf_response, csv_response, index, csv_agent)
                st.chat_message('assistant').markdown(response)
                st.session_state.messages.append({'role': 'assistant', 'content': response})

else:
    st.session_state.clear()
