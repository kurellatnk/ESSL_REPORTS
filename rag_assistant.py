import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 1. Load environment secrets
load_dotenv()

print("=== Initializing RAG Pipeline ===")

# 2. Load your private text file
loader = TextLoader("secret_project.txt")
docs = loader.load()

# 3. Chop the text into manageable chunks
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
chunks = text_splitter.split_documents(docs)

# 4. Convert chunks into vector embeddings and store them in a local database
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
vector_store = Chroma.from_documents(chunks, embeddings)

# 5. Create a retriever to search the local database
retriever = vector_store.as_retriever(search_kwargs={"k": 1})

# 6. Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0)

# 7. Define how the AI should use the retrieved document context
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know.\n\n"
    "{context}"
)
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# 8. Combine everything into a RAG Chain
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# 9. Ask a question that requires reading your private file!
query = "Who is the Lead Architect and what hardware is being used?"
print(f"\nUser Query: {query}\n")

response = rag_chain.invoke({"input": query})

print(f"AI Response:\n{response['answer']}")