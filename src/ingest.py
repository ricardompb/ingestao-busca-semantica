from envloader import load_env
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_postgres import PGVector

def has_documents(store):
    try:
        results = store.similarity_search("teste", k=1)
        if results is None:
            return False
        return bool(results)
    except Exception:
        return False

def ingest_pdf():  

    env = load_env()
    store = PGVector(embeddings=env["EMBEDDINGS"],
                    collection_name=env["PG_VECTOR_COLLECTION_NAME"],
                    connection=env["DATABASE_URL"], 
                    use_jsonb=True)

    # Verifica se já há documentos na coleção
    if has_documents(store):
        print("Documentos já inseridos no banco. Pulando ingestão.")
        return

    # dividir o pdf
    print("Fazendo a ingestão dos documentos no banco.")
    docs = PyPDFLoader(str(env["PDF_PATH"])).load()
    splits = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150, add_start_index=False).split_documents(docs)
    if not splits:
        raise SystemExit(0)

    # gerar ids, enriquecer os documentos
    enriched = [
        Document(page_content=d.page_content, 
                metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
                ) for d in splits
    ]

    ids = [ f"doc-{i}" for i in range(len(enriched)) ]

    # inserir no banco usando pgvector
    store.add_documents(documents=enriched, ids=ids)
    


if __name__ == "__main__":
    ingest_pdf()