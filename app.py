import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# 페이지 기본 설정
st.set_page_config(
    page_title="빅데이터 모델 및 분석 챗봇",
    page_icon="🐉",
    layout="wide"
)

# 1. 화면 상단 제목
st.title("빅데이터 모델 및 분석 챗봇 🐉")

# 2. 사이드바 (화면 왼쪽): OpenAI API 키 입력 및 설정
with st.sidebar:
    st.header("🔑 설정")
    openai_api_key = st.text_input(
        "OpenAI API Key를 입력하세요",
        type="password",
        placeholder="sk-...",
        help="OpenAI 플랫폼에서 발급받은 API 키를 입력해 주세요."
    )
    
    # 모델 선택 (기본값: gpt-4o-mini)
    selected_model = st.selectbox(
        "사용할 모델 선택",
        ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
        index=0
    )
    
    # 대화 초기화 버튼
    if st.button("대화 내용 초기화"):
        st.session_state.messages = []
        st.rerun()

# 세션 상태(Session State)를 활용한 대화 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 기록 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. 사용자 입력 처리
if prompt := st.chat_input("질문을 입력하세요용..."):
    # API 키 입력 여부 확인
    if not openai_api_key:
        st.error("왼쪽 사이드바에 OpenAI API Key를 입력해야 대화를 시작할 수 있습니다용!")
        st.stop()

    # 사용자 메시지 화면에 표시 및 세션 저장
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # LangChain 및 OpenAI 연동 후 답변 생성
    with st.chat_message("assistant"):
        with st.spinner("답변을 생각하고 있습니다용..."):
            try:
                # ChatOpenAI 객체 생성
                llm = ChatOpenAI(
                    model_name=selected_model,
                    openai_api_key=openai_api_key,
                    temperature=0.7
                )

                # System Prompt 구축 (말끝마다 '용'을 붙이는 페르소나 설정)
                langchain_messages = [
                    SystemMessage(content="당신은 빅데이터 및 AI 전문 챗봇입니다. 친절하고 정확하게 답변하되, 질문에 답할 때 반드시 말 끝 마다 '용'을 붙여서 자연스럽고 귀엽게 작성해 주세요. (예: 안녕하세요용! 무엇을 도와드릴까요용?)")
                ]

                # 기존 대화 히스토리 구성
                for msg in st.session_state.messages:
                    if msg["role"] == "user":
                        langchain_messages.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        langchain_messages.append(AIMessage(content=msg["content"]))

                # LLM 호출 및 응답 받아오기
                response = llm.invoke(langchain_messages)
                assistant_response = response.content

                # 답변 출력 및 세션 저장
                st.markdown(assistant_response)
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})

            except Exception as e:
                st.error(f"오류가 발생했습니다용: {str(e)}")
