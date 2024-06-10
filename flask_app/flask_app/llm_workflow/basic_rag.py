from json import load
from os import environ
from weaviate import connect_to_local
from weaviate.classes.query import Filter
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents import Document

# Client Libraries of Langchain
from langchain_openai import OpenAIEmbeddings
from langchain_weaviate import WeaviateVectorStore
from langchain_community.retrievers.weaviate_hybrid_search import WeaviateHybridSearchRetriever

# Object Oriented Approach
class BasicRAG:
    """
    This is a retrieval augmented generation (RAG) system between Langchain, OpenAI, and Weaviate.

    - Embedding Model : Any embedding model that comes with OpenAI
        - Default: Ada 002 Embedding

    - Vector Search : Weaviate 
    """
    # Constructor
    def __init__(self, file_text: str, file_name: str, port: int = 8450, grpc_port: int = 50052):
        # Create your attributes
        self.port = port
        self.grpc_port = grpc_port

        # Weaviate client
        self.vclient = connect_to_local(port=self.port, grpc_port=self.grpc_port)

        # Introduce file_path as an attribute
        self.text = file_text

        self.file_name = file_name

        # Doc Processor
        self.doc_processor(chunk_size=2000)

    # Text to Document Conversion
    def text_to_doc(self, chunk_text: str) -> Document:
        # Document constructor
        doc = Document(page_content=chunk_text)

        doc.metadata = {
            "file_name" : self.file_name
        }

        return doc

    # Processor
    def doc_processor(self, chunk_size: int = 200, chunk_overlap: int = 50):
        
        # Create a text splitter
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        # Get the documents
        self.doc_chunks = text_splitter.split_text(text=self.text)

        # Transform the list of chunk text into a list of Documents
        self.doc_chunks = [self.text_to_doc(chunk_text=chunk) for chunk in self.doc_chunks]

        return self.doc_chunks
    
    # Helper Function for handling the environment variable
    def env_var_setup(self, json_path: str) -> None:
        # Context Manager
        with open(json_path, "r") as buffer:
            # Deserialization
            obj = load(buffer)
        
        # Close the buffer
        buffer.close()
        
        # Environment Update Method
        environ.update(obj)

        # Clear the object dictionary
        obj.clear()

    # Setup OpenAI Embedding Model
    def openai_embedding(self, model_name: str = "text-embedding-ada-002", toggle_json: bool = False, json_path: str = None) -> OpenAIEmbeddings:
        
        if toggle_json:
            # Update the environment variable
            self.env_var_setup(json_path=json_path)

            # Get the OpenAIEmbeddings
            self.embedding = OpenAIEmbeddings(model=model_name, api_key=environ['OPENAI_API_KEY'])
        else:
            # Re-assign the Embedding MOdel if someone wants to experiment rather than just relying Ada-02
            self.embedding = OpenAIEmbeddings(model=model_name)

        return self.embedding

    # Setup the interaction between your documents, Embedding Model, and weaviate
    def vector_etl(self):
        """
        Assumptions:
            - The .doc_processor() method must be run prior to using this method.
            - The .openai_embedding() method must be run prior to using this method.
        """

        # Attribute for the vector database
        self.db = WeaviateVectorStore.from_documents(self.doc_chunks, self.embedding, client=self.vclient)

        return self.db
    
    # Search Methods
    def get_top_chunk(self, query: str) -> str:
        """
        Inputs:
            - query (string): User query that is used to perform the similarity search against Weaviate.
        
            
        Output:
            - result (string): String content corresponding with the chunk that has been identified as the top result.
        """

        # Relevant results
        result = self.db.similarity_search(query=query, k=1, filters=Filter.by_property(name='file_name').equal(val=self.file_name))

        return result[0].page_content
    
    def get_n_chunks(self, query: str, n: int = 5) -> list[str]:
        """
        Inputs:
            - query (string): User's query to get results from Weaviate.
            - n (integer) 
                - Default value: 5
                - Number of chunks to receive results from based on a ranking metric (e.g. cosine similarity, MRMR, ...)
        
        Output:
            - results (list of strings): Document results from the vector database
        """

        # Relevant results
        results = self.db.similarity_search(query=query, k=n, filters=Filter.by_property(name='file_name').equal(val=self.file_name))

        return [result.page_content for result in results]

    # Get vector database as a retriever
    def db_as_retriever(self):
        # Create a retriever
        self.retriever = WeaviateHybridSearchRetriever(
            client=self.vclient,
            index_name='cohere_notes',
            text_key='text',
            attributes=[],
            create_schema_if_missing=True
        )

        return self.retriever

    # Search Method
    def retriever_search(self, query: str):
        # Perform a hybrid search
        result = self.retriever.invoke(
            input=query,
            where_filter={
                "path" : ['file_name'],
                "operator" : "Equal",
                "valueString" : self.file_name
            }
        )

        return result


