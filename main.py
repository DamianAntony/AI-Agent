from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from tool import search_tool, wiki_tool
from langchain_core.exceptions import OutputParserException
import json
import re






load_dotenv()

class ResearchResponse(BaseModel):
  topic:str
  summary:str
  sources:str
  tools_used:str

llm = ChatGoogleGenerativeAI(
  model="gemini-2.5-flash",
  temperature=0.7,
  convert_system_message_to_human=True
)
# response = llm.invoke("Explain LangChain in one sentence")
# print(response.content)

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# fixing_parser=OutputFixingParser.from_llm(
#   parser=parser,
#   llm=llm
# )

prompt= ChatPromptTemplate.from_messages([
  ( 
   "system", """
You are a research assistant.

STRICT OUTPUT RULES (MANDATORY):
- After using tools and gathering information, you MUST return VALID JSON as your final response.
- You MUST NOT return plain text.
- You MUST NOT ask questions.
- You MUST NOT add explanations.
- You MUST NOT include markdown code blocks.

If tools succeed:
- Use their information to create a comprehensive summary.

If tools fail or return no data:
- Still return JSON.
- summary: explain that reliable information was not found.
- sources: "None"
- tools_used: list the tool attempted.

IMPORTANT: Your final response must be ONLY valid JSON matching this schema:
{format_instructions}

Do not wrap JSON in markdown code blocks. Return raw JSON only.
   """),
   ("placeholder","{chat_history}"),
   ("human","{query}"),
   ("placeholder","{agent_scratchpad}")
]).partial(format_instructions=parser.get_format_instructions())

# Create a simple LLM chain instead of tool-calling agent (for Google Generative AI compatibility)
chain = prompt | llm | parser

# user_query=input("Enter the research topic ")

user_input=input("What can I help you In Research ")

try:
    structured_output = chain.invoke({"query":user_input, "chat_history":[], "agent_scratchpad":[]})
except OutputParserException as e:
    print(f"⚠️ Parsing error: {e}")
    structured_output = ResearchResponse(
        topic=user_input,
        summary="Unable to parse structured response",
        sources="None",
        tools_used="Web_Search, Wikipedia"
    )

print("\n✅ Structured Output:")
print(structured_output)