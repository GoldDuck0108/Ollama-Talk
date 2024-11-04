import streamlit as st
import subprocess
import time
import re
import random  # 이 부분을 추가하세요


# 텍스트 생성 함수
def generate_text_via_cli(prompt, model_name="gemma2:latest"):
    try:
        start_time = time.time()
        # ollama run 명령을 subprocess로 실행
        with st.spinner("텍스트를 생성 중입니다. 잠시만 기다려 주세요..."):
            result = subprocess.run(
                ["ollama", "run", model_name, prompt],
                capture_output=True,
                text=True
            )
        elapsed_time = time.time() - start_time
        
        # 결과 반환
        if result.returncode == 0:
            # 불필요한 진행 상황 메시지를 제거하기 위해 정규 표현식을 사용
            cleaned_output = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', result.stdout)
            return cleaned_output, elapsed_time
        else:
            st.error(f"모델 실행 오류: {result.stderr}")
            return None, elapsed_time
    except Exception as e:
        st.error(f"예상치 못한 오류가 발생했습니다: {str(e)}")
        return None, 0

# 텍스트 자동 삭제 설정 함수
def delete_text_after_timeout():
    if 'generated_text' in st.session_state and st.session_state['generated_text']:
        elapsed_time = time.time() - st.session_state['generated_text_time']
        if elapsed_time > 60:
            st.session_state['generated_text'] = ""

def main():
    st.set_page_config(page_title="🦙 Ollama 이야기 생성기", layout="wide")
    st.title("🦙 Ollama와 함께하는 대화")
    
    # Ollama 상태 확인 및 모델 설정
    with st.sidebar:
        st.header("🔧 설정해봐요!")
        
        # Ollama 상태 표시
        st.markdown("---")
        st.subheader("🛠️ Ollama 서버 상태")
        
        # 상태 표시를 위한 플레이스홀더
        status_indicator = st.empty()
        
        try:
            response = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True
            )
            if response.returncode == 0:
                status_indicator.success("✅ 서버에 잘 연결되었어요!")
            else:
                status_indicator.error("❌ 서버 연결에 실패했어요. 다시 확인해주세요.")
        except:
            status_indicator.error("❌ 서버에 연결할 수 없어요. Ollama가 실행 중인지 확인해 주세요.")
    
    model_name = "gemma2:latest"
    
    with st.sidebar:
        temperature = st.radio("🌟 창의성 선택하기", ["낮음", "보통", "높음"], index=1)
        max_length = st.radio("📝 답변 길이 선택하기", ["짧게", "중간", "길게"], index=1)
        
        # 재미있는 사실 표시하기
        st.markdown("---")
        st.subheader("🤔 재미있는 사실!")
        fun_facts = [
            "알고 계셨나요? 라마는 3개의 위를 가지고 있어요!",
            "흥미로운 사실! Ollama는 절대 지치지 않아요. AI니까요!",
            "AI 모델은 데이터를 바탕으로 훈련받아 사람처럼 대화할 수 있어요.",
            "라마는 사람에게 침을 뱉기도 해요. Ollama는 여러분을 도울 뿐이랍니다!",
            "AI는 절대 잠들지 않아요. 언제든 물어보세요!"
        ]
        st.info(random.choice(fun_facts))
    
    # 입력 영역
    prompt = st.text_area(
        "💬 Ollama에게 무엇을 물어볼까요?",
        placeholder="여기에 질문이나 대화를 입력해 주세요...",
        height=100
    )
    
    # 생성 버튼 및 Cmd+Enter 단축키 기능 추가
    if st.button("🚀 응답 받기 (Cmd+Enter)") or st.session_state.get('command_enter', False):
        if prompt:
            st.subheader("📝 입력한 프롬프트:")
            st.info(prompt)
            
            # 픽셀아트 이미지를 통한 시각적 대기 효과 추가
            st.image("https://via.placeholder.com/300x100?text=Ollama+is+thinking...+%F0%9F%8C%8C", caption="Ollama가 생각 중입니다. 잠시만 기다려 주세요...", use_column_width=True)
            
            # CLI 명령을 통해 텍스트 생성
            generated_text, elapsed_time = generate_text_via_cli(prompt, model_name)
            
            if generated_text:
                st.session_state['generated_text'] = generated_text
                st.session_state['generated_text_time'] = time.time()
                st.subheader("✨ Ollama의 답변 (1분 후 자동 삭제):")
                st.text_area("생성된 텍스트:", value=generated_text, height=300)
                st.info(f"⏱️ 응답 시간: {elapsed_time:.2f}초")
        else:
            st.warning("프롬프트를 입력해주세요!")

    # 키보드 이벤트 처리 (Cmd+Enter)
    def handle_keypress():
        st.session_state['command_enter'] = True

    st.text_input("텍스트 생성 단축키: Cmd+Enter로 Ollama와 대화를 시작해 보세요!", key='command_input', on_change=handle_keypress)
    
    # 텍스트 자동 삭제 처리
    delete_text_after_timeout()

if __name__ == "__main__":
    main()
