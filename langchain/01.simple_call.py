from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

result = llm.invoke("안녕")

print("content:", result.content)
print("id:", result.id)
print("type:", result.type)
print("response_metadata:", result.response_metadata)
print("usage_metadata:", result.usage_metadata)