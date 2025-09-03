from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

prompt = """너는 소스코드 분석 전문가이다.
사용된 함수의 이름과 각 함수의 기능을 리뷰해서 JSON 리스트 형태로 반환한다.

규칙:
- 결과는 반드시 파이썬 리스트 형식으로 출력한다.
- 리스트의 각 원소는 "함수명": "기능 설명" 구조로 작성한다.
- 설명은 한국어로 간단하게 작성한다.

출력 예시:
[
  "load": "파일에서 데이터를 읽음",
  "write": "데이터를 파일로 씀"
]
"""

code = """
int main() {
    load_config();
    initialize();
    run_loop();
    exit();
}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", prompt),
    ("user", "{code}")
])

chain = prompt | llm
result = chain.invoke({"code", code})
print(result.content)