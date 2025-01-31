# # Import necessary libraries
# from phi.knowledge import KnowledgeBase
# from phi.vectordb.lancedb import LanceDb
# from phi.agent import Agent
# from phi.model.groq import Groq
# from sentence_transformers import SentenceTransformer

# # Step 1: Define the Hugging Face Embedder
# class HuggingFaceEmbedder:
#     def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
#         self.model = SentenceTransformer(model_name)

#     def embed(self, texts):
#         if isinstance(texts, str):
#             texts = [texts]
#         return self.model.encode(texts, convert_to_tensor=True).tolist()


# # Step 2: Initialize the Vector Database and Knowledge Base
# def initialize_knowledge_base(embedder, table_name="knowledge_base", uri="tmp/lancedb"):
#     vector_db = LanceDb(
#         table_name=table_name,
#         uri=uri,
#         embedder=embedder,  # Attach HuggingFace embedder directly
#     )

#     # Create knowledge base
#     knowledge_base = KnowledgeBase(vector_db=vector_db)
#     return knowledge_base


# # Step 3: Populate the Knowledge Base
# def add_documents_to_kb(knowledge_base, documents):
#     knowledge_base.add_documents([doc["text"] for doc in documents])


# # Step 4: Create and Test the RAG Agent
# def create_agent(knowledge_base, model_id="gemma2-9b-it"):
#     # Initialize the generative model
#     generative_model = Groq(id=model_id)

#     # Create the RAG agent
#     agent = Agent(
#         model=generative_model,
#         knowledge=knowledge_base,
#         show_tool_calls=True,
#         markdown=True,
#     )
#     return agent


# if __name__ == "__main__":
#     # Initialize Hugging Face Embedder
#     embedder = HuggingFaceEmbedder()

#     # Initialize Knowledge Base
#     knowledge_base = initialize_knowledge_base(embedder)

#     # Sample Data for the Knowledge Base
#     documents = [
#         {"id": "1", "text": "Python is a versatile programming language."},
#         {"id": "2", "text": "Machine learning is a subset of artificial intelligence."},
#         {"id": "3", "text": "Retrieval-Augmented Generation improves answer relevance."},
#     ]

#     # Add Documents to Knowledge Base
#     add_documents_to_kb(knowledge_base, documents)

#     # Create the RAG Agent
#     rag_agent = create_agent(knowledge_base)

#     # Test the Agent
#     query = "What is RAG?"
#     response = rag_agent.chat(query)
#     print("Query:", query)
#     print("Response:", response)


# from phi.knowledge.text import TextKnowledgeBase
# from phi.vectordb.lancedb import LanceDb
# from phi.agent import Agent
# from phi.model.groq import Groq
# from sentence_transformers import SentenceTransformer

# # Custom Embedder using Hugging Face SentenceTransformer
# class HuggingFaceEmbedder:
#     def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
#         self.model = SentenceTransformer(model_name)
#         # Set the dimensions of the embeddings (number of features per embedding)
#         self.dimensions = self.model.encode(["Test sentence."]).shape[0]  # Extract from a dummy sentence

#     def get_embedding(self, text):
#         """
#         This method returns the embedding for a single text input.
#         """
#         return self.model.encode(text, convert_to_tensor=False).tolist()

#     def embed(self, texts):
#         """
#         Embeds multiple texts. This function is useful for batch processing.
#         """
#         if isinstance(texts, str):
#             texts = [texts]
#         return self.model.encode(texts, convert_to_tensor=False).tolist()


# # Initialize LanceDB as Vector Database
# def initialize_vector_db(embedder, table_name="knowledge_base", uri="tmp/lancedb"):
#     return LanceDb(
#         table_name=table_name,
#         uri=uri,
#         embedder=embedder,
#     )


# # Sample Data
# documents = [
#     {"id": "1", "text": "Python is a versatile programming language."},
#     {"id": "2", "text": "Machine learning is a subset of artificial intelligence."},
#     {"id": "3", "text": "Retrieval-Augmented Generation improves answer relevance."},
# ]


# # Main function to set up the knowledge base and agent
# def main():
#     # Initialize the embedder
#     embedder = HuggingFaceEmbedder()

#     # Initialize the vector database
#     vector_db = initialize_vector_db(embedder)

#     # Create the knowledge base with LanceDB, specify path where data will be stored
#     knowledge_base = TextKnowledgeBase(
#         vector_db=vector_db,
#         path="path/to/store/knowledge_base_data"  # Specify the path to store/load knowledge data
#     )

#     # Assuming that the TextKnowledgeBase can handle document insertions with a batch function.
#     # Adding documents after embedding them.
#     embeddings = embedder.embed([doc["text"] for doc in documents])
    
#     # Assuming add_documents method is available or an alternative way to add documents.
#     # You can use the following pattern if the knowledge base exposes such a method:
#     knowledge_base.add_documents(documents, embeddings)

#     # Initialize the Groq model and agent
#     model = Groq(id="gemma2-9b-it")
#     agent = Agent(
#         model=model,
#         knowledge=knowledge_base,
#         show_tool_calls=True,
#         markdown=True,
#     )

#     # Example query
#     query = "What is RAG?"
#     response = agent.chat(query)
#     print("Query:", query)
#     print("Response:", response)


# if __name__ == "__main__":
#     main()


# from phi.agent import Agent
# from phi.model.openai import OpenAIChat
# from phi.embedder.openai import OpenAIEmbedder
# # from phi.embedder.huggingface import HuggingFaceEmbedder
# from phi.knowledge.pdf import PDFUrlKnowledgeBase
# from phi.vectordb.lancedb import LanceDb, SearchType

# from phi.embedder.huggingface import HuggingfaceCustomEmbedder

# embeddings = HuggingfaceCustomEmbedder().get_embedding("The quick brown fox jumps over the lazy dog.")

# # Create a knowledge base from a PDF
# knowledge_base = PDFUrlKnowledgeBase(
#     urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
#     # Use LanceDB as the vector database
#     vector_db=LanceDb(
#         table_name="recipes",
#         uri="tmp/lancedb",
#         search_type=SearchType.vector,
#         embedder=HuggingfaceCustomEmbedder(),
#     ),
# )
# # Comment out after first run as the knowledge base is loaded
# knowledge_base.load()

# agent = Agent(
#     model=OpenAIChat(id="gpt-4o"),
#     # Add the knowledge base to the agent
#     knowledge=knowledge_base,
#     show_tool_calls=True,
#     markdown=True,
# )
# agent.print_response("How do I make chicken and galangal in coconut milk soup", stream=True)



from phi.agent import Agent
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader,JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from phi.knowledge.langchain import LangChainKnowledgeBase
from phi.agent import Agent
from phi.model.groq import Groq


# Load PDF file
# loader = PyPDFLoader(file_path="C:/Users/Lenovo/Downloads/Md_Shariar_Hossain_ML_CV.pdf")
loader=JSONLoader(file_path="HR_module/FAQs.json",jq_schema=".",text_content=False)
docs = loader.load()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(docs)

# Create Chroma vector store
db = Chroma(embedding_function=HuggingFaceEmbeddings(), persist_directory="./chroma_db")
db.add_documents(docs)

# Set up the retriever
retriever = db.as_retriever()

# Create a knowledge base
knowledge_base = LangChainKnowledgeBase(retriever=retriever)

from langchain.tools import Tool

from rag_db import get_candidate_info
# def query_db(email, question):
#     """Call the completed DB query agent to get an answer."""
#     query_prompt = f"My email is {email}. Answer this from the database: {question}."
#     return db_query_agent.run(query_prompt)  # Assuming db_query_agent is pre-built

query_db_tool = Tool(
    name="Database Query",
    func=lambda question: get_candidate_info(candidate_email, question),
    description="Use this tool when the answer should come from the database."
)


from langchain.memory import ConversationBufferMemory

# Memory per email session
memory = {}

def get_memory(email):
    """Retrieve or initialize memory for a given email address."""
    if email not in memory:
        memory[email] = ConversationBufferMemory(k=5)  # Store last 5 Q-A
    return memory[email]

from langchain.schema import AgentMemory
candidate_email="saminc97@gmail.com"
# Assuming get_memory returns ConversationBufferMemory
candidate_memory = get_memory(candidate_email)

# Wrap it inside AgentMemory
agent_memory = AgentMemory(memory=candidate_memory)

# Create the Knowledge Base Agent
# knowledge_agent = Agent(
#     name="Recruitment Agent",
#     role="Answers the common questions about the recruitment information, progress and progress of a candidate from the given knowledge.",
#     instructions=[
#          "Use the knowledge base to answer the common questions about the recruitment information, progress and progress of a candidate.",
#          "You will be given the candidate's email, identify the candidate by email and answer the question from his information.",
#          "Do not answer anything without the knowledge base you are given.",
#          "Follow the conversation context",
#      ],
#     model=Groq(id='gemma2-9b-it'),
#     knowledge=knowledge_base,
#     add_context=True,
#     search_knowledge=True,
#     debug=True,
#     markdown=True,
# )


knowledge_agent = Agent(
    name="Company Inquery Agent",
    role="Answers FAQs from knowledge base, recruitment questions and candidate progress queries from query db tool.",
    instructions=[
         "Use the knowledge base for Frequently Asked Questions(FAQs).",
         "For specific candidate details, use the database query tool.",
         "Maintain conversation history and provide responses based on past 5 interactions.",
         "Identify users by their email and keep session-based memory."
     ],
    model=Groq(id='gemma2-9b-it'),
    knowledge=knowledge_base,
    add_context=True,
    search_knowledge=True,
    debug=True,
    markdown=True,
    tools=[query_db_tool],  # Add the database query tool
    memory=get_memory(candidate_email)  # Add per-user memory
)


question="What is my Skills matching score?"
prompt = (
    f"My email is {candidate_email}. "
    f"Answer my question from the provided knowledge base: {question}."
)
result = knowledge_agent.run(prompt)
# result = knowledge_agent.run(f"Question: {question} ,my email is:{candidate_email}, Answer my question from the provided knowledge base.")
print(result.content)