from json import loads
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

# Summary Prompt
template = """
    Task: Answer the question based on the context below.

    {context}
"""

# Create the PromptTemplate
prompt = PromptTemplate(template=template, input_variables=['context'])

# question-answer helper function
def qa_chain(llm: ChatOpenAI, context: str) -> dict:
    
    # Create the chain
    chain = LLMChain(llm=llm, prompt=prompt)

    # Create a result
    result = chain.invoke(input=context)

    print(result)

    return result['text']