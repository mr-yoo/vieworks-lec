import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 프롬프트 1: Flow Chart
prompt1 = """
너는 C/C++, 베릴로그, 시스템베릴로그 등의 소스코드 분석 전문가이다.  
소스코드를 분석하여 다음 조건에 따라 mermaid 다이어그램 코드를 출력하라:

- 입력된 코드에서 함수(또는 모듈) 간의 호출 관계를 분석하라.  
- “state chart”, “상태도”, “state machine”, “FSM”, “상태 전이”라는 키워드가 있으면 stateDiagram-v2를 사용하라.  
- “sequence diagram”, “시퀀스 다이어그램”, “순차 다이어그램”이라는 키워드가 있으면 sequenceDiagram을 사용하라.  
- 위 키워드가 없으면 flowchart TD를 사용하라.  
- 출력은 mermaid 다이어그램 코드만 포함하며, 백틱(```)이나 코드 블록 표시는 절대 포함하지 않는다.  
- 설명 문장, 이모지, 추가 텍스트도 출력하지 않는다.

예시 (출력 형식):
flowchart TD
A --> B
B --> C
"""

code = """
int main() {
    load_config();
    initialize();
    run_loop();
    exit();
}
"""

chain1 = ChatPromptTemplate.from_messages([("system", prompt1), ("user", "{code}")]) | llm
mermaid = chain1.invoke({"code": code}).content

# 프롬프트 2: 함수 기능 리뷰
prompt2 = """
너는 소스코드 분석 전문가이다.
입력된 코드에서 사용된 함수 이름과 각 함수의 기능을 요약해라.

규칙:
- 결과는 반드시 파이썬에서 바로 json.loads 할 수 있는 JSON 배열만 출력한다.
- ```json 같은 코드블록 표시는 절대 쓰지 않는다.
- 배열의 각 원소는 {{"함수명": "기능 설명"}} 구조여야 한다.
- 설명은 한국어로 간단하게 작성한다.

출력 예시:
[
  {{"load_config": "설정 파일을 로드함"}},
  {{"initialize": "초기화 작업을 수행함"}},
  {{"run_loop": "주 실행 루프를 실행함"}},
  {{"exit": "프로그램을 종료함"}}
]
"""

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
chain2 = (ChatPromptTemplate.from_messages(
    [("system", prompt2), ("user", "{code}")]
) | llm)
desc = chain2.invoke({"code": code}).content

print(mermaid)
print(desc)

func_list = json.loads(desc)
print(func_list)

# 함수 설명 섹션 만들기
func_section = "## 함수 기능 요약\n"
for item in func_list:
    for name, detail in item.items():
        func_section += f"### {name}\n{detail}\n\n"

# mermaid 섹션 만들기
flow_section = f"""## Flow Chart
```mermaid
{mermaid.strip()}
```"""

# 최종 md 합치기
md = "# 코드 분석 결과\n\n" + func_section + flow_section
print(md)