from langchain.document_loaders import DirectoryLoader, BSHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

def ingest_docs(path:str) -> None:
    loader = DirectoryLoader(path=path,glob= '**/*.html', recursive=True, loader_cls=BSHTMLLoader)
    documents = loader.load()
    print(len(documents))
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100, separators=["\n\n", "\n", " ", ""]
    )
    docs = text_splitter.split_documents(documents=documents)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embedding=embeddings)
    vectorstore.save_local("vector_stores/faiss_index")
    print(len(docs))
