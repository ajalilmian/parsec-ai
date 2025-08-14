import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage

load_dotenv()

CHROMA_PATH = "chroma_db"


def process_document(file_path: str):
    """
    Loads a PDF, splits it into chunks, and stores embeddings in ChromaDB.
    """
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)

    collection_name = datetime.now().strftime("%Y%m%d%H%M%S")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings(),
        persist_directory=CHROMA_PATH,
        collection_name=collection_name
    )
    vectorstore.persist()
    return collection_name


def query_document(question: str, collection_name: str):
    """
    Queries the document using a RAG pipeline.
    """
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=OpenAIEmbeddings(),
        collection_name=collection_name
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity", search_kwargs={"k": 5})

    system_prompt = (
        "You are an expert marketing analyst. Use the provided context to answer the user's question."
        "If you don't know the answer, just say that you don't know. Don't try to make up an answer."
        "\n\n"
        "{context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    Youtube_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, Youtube_chain)

    response = rag_chain.invoke({"input": question})

    return response["answer"]
