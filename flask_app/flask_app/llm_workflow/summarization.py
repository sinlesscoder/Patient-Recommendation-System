from json import loads
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.pydantic_v1 import BaseModel
from langchain_core.output_parsers.json import JsonOutputParser

# Pydantic Object
class SummaryResponse(BaseModel):
    problem: str
    main_complications: str
    recommendations: str

# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=SummaryResponse)

# Summary Prompt
template = """
    Task: Summarize the key findings from the note below, but please start off the summary with the exact problem that the patient has been admitted for.

    {format_instructions}

    {context}
"""

# Create the PromptTemplate
prompt = PromptTemplate(template=template, input_variables=['context'], partial_variables={'format_instructions' : parser.get_format_instructions()})

# Create a function
def summary_chain(llm: ChatOpenAI, context: str) -> dict:
    
    # Create the chain
    chain = LLMChain(llm=llm, prompt=prompt)

    # Create a result
    result = chain.invoke(input=context)

    print(result)

    return loads(result['text'])