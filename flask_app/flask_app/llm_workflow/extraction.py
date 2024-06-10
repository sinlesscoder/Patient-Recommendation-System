from json import loads
from langchain_openai import ChatOpenAI
from langchain.pydantic_v1 import BaseModel

# Extraction Workflow
class Entities(BaseModel):
    # Define attributes
    date_of_birth: str
    date_of_admission: str
    chief_complaint: str
    medications: list[str]
    procedures: list[str]
    smoking_history: str

# Structured Output Flow
def structured_output(llm: ChatOpenAI, context: str) -> dict:
    # Define the LLM
    structured_llm = llm.with_structured_output(schema=Entities)

    # Get the result
    result = structured_llm.invoke(input=context).json()

    print(result)

    return loads(result)