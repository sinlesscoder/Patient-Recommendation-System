from langchain_openai import ChatOpenAI
from llm_workflow.extraction import structured_output
from llm_workflow.summarization import summary_chain
from llm_workflow.question_answer import qa_chain
from llm_workflow.basic_rag import BasicRAG

class Tasks(BasicRAG):
    # Constructor
    def __init__(self, file_name: str, file_text: str, model_name: str = 'gpt-4', port: int = 8450, grpc_port: int = 50050):
        # Inheritance
        super().__init__(file_name=file_name, file_text=file_text, port=port, grpc_port=grpc_port)

        # LLM Attribute
        self.llm = ChatOpenAI(model=model_name)

    # Method for extraction
    def extract_entities(self, text: str) -> dict:
        # Leverage structured output
        result = structured_output(llm=self.llm, context=text)

        print(type(result))
        print(result)

        return result
    
    # Method for summary
    def retrieve_summary(self, text: str) -> dict:
        # Leverage the summary function
        return summary_chain(llm=self.llm, context=text)
    
    # Method for Question Answering
    def question_answer(self, query: str) -> str:
        # Embedding
        self.openai_embedding()
        
        # Perform vector search based on chunks
        self.vector_etl()

        # Context for which to answer the question
        answer_context = self.get_top_chunk(query=query)

        # # Postprocess the List of Documents into a Combined String
        # prompt_context = "\n".join([ctx.page_content for ctx in answer_context])

        # Result
        result = qa_chain(llm=self.llm, context=answer_context)

        return result


        
