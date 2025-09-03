from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

prompt = """
너는 C/C++, 베릴로그, 시스템베릴로그 등의 소스코드 분석 전문가이다.  
소스코드를 분석하여 다음 조건에 따라 mermaid 차트를 출력하라:

- 입력된 코드에서 함수(또는 모듈) 간의 호출 관계를 분석하라.  
- “state chart”, “상태도”, “state machine”, “FSM”, “상태 전이”라는 키워드가 있으면 **stateDiagram-v2**를 사용하라.  
- “sequence diagram”, “시퀀스 다이어그램”, “순차 다이어그램”이라는 키워드가 있으면 **sequenceDiagram**을 사용하라.  
- 위 키워드가 없으면 **flowchart TD**를 사용하라.  
- 결과는 **오직 하나의 mermaid 코드 블록만 출력**하라.  
- 설명 문장, 이모지, 텍스트는 출력하지 않는다.  
- mermaid 블록은 삼중 백틱(```mermaid)으로 시작하고 종료한다.

예시:
```mermaid
flowchart TD
A --> B
B --> C
```
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