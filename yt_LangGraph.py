from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
import os




CHUNK_DIR = "qa_transcripts"
embedding = OpenAIEmbeddings()

docs = []
for file in os.listdir(CHUNK_DIR):
    if file.endswith("_qa_chunks.txt"):
        with open(os.path.join(CHUNK_DIR, file), 'r', encoding='utf-8') as f:
            raw = f.read().split('\n\n')
            for chunk in raw:
                if chunk.strip():
                    lines = chunk.strip().split('\n')
                    metadata = {'source': file, 'timestamp': lines[0]}
                    content = " ".join(lines[1:])
                    docs.append(Document(page_content=content, metadata=metadata))

# Build Chroma vector store
vectorstore = Chroma.from_documents(docs, embedding, persist_directory="./chroma_store")