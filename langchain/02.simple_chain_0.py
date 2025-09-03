from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "너는 친절하고 간결하게 답변하는 어시스턴트이다."),
    ("user", "{input}")
])

chain = prompt | llm

result = chain.invoke({"input": "지구에서 가장 큰 동물은 무엇이야?"})
print(result.content)
