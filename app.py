# app.py - 마음의 나침반 완전 수정 버전
# ------------------------------------------
# 마음의 나침반: Streamlit 단일 앱 엔트리
# - 세션 상태 기반 라우팅(`current_page`)
# - 주요 페이지: 메인 / 감정 탐색 / 감정 달력 / 미래 편지
# - 데이터는 로컬 JSON/TXT 파일로 저장/로드
# ------------------------------------------

import streamlit as st
import json
import os
from datetime import datetime, date, timedelta
import calendar
import pandas as pd
import uuid

# 페이지 설정
st.set_page_config(
    page_title="마음의 나침반",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일 적용
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #4A90E2 0%, #7B68EE 50%, #9370DB 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(74, 144, 226, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin-bottom: 0;
        opacity: 0.95;
    }
    
    .positive-message {
        background: linear-gradient(90deg, #98FB98, #90EE90);
        padding: 1.5rem;
        border-radius: 12px;
        color: #2d5a2d;
        margin: 1rem 0;
        border-left: 5px solid #32CD32;
    }
    
    .stButton > button {
        width: 100%;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# 감정별 색깔 정의
EMOTION_COLORS = {
    "행복": "#FFD700",      # 황금색
    "평온": "#87CEEB",      # 하늘색
    "무기력": "#A9A9A9",    # 회색
    "불안": "#FF6B6B",      # 연한 빨강
    "슬픔": "#4169E1",      # 파랑
    "화남": "#FF4500",      # 주황빨강
    "희망": "#98FB98",      # 연두색
    "감사": "#DDA0DD"       # 자두색
}

# 데이터 로드/저장 함수들
def load_insights():
    """통찰 데이터 로드"""
    try:
        if os.path.exists("data/insights.json"):
            with open("data/insights.json", "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            os.makedirs("data", exist_ok=True)
            default_insights = {
                "lethargy": {
                    "keywords": {
                        "돌덩이": {
                            "response": "마치 무거운 돌덩이를 끌고 다니는 것 같은 기분이시군요.",
                            "next_question": "그 무거운 돌덩이를 잠시 내려놓을 수 있는 순간은 언제인가요?"
                        }
                    }
                },
                "anxiety": {
                    "keywords": {
                        "바람": {
                            "response": "마음이 바람에 흔들리는 것처럼 불안정하시군요.",
                            "next_question": "마음이 가장 안정되는 순간은 언제인가요?"
                        }
                    }
                }
            }
            with open("data/insights.json", "w", encoding="utf-8") as f:
                json.dump(default_insights, f, ensure_ascii=False, indent=2)
            return default_insights
    except Exception as e:
        print(f"통찰 데이터 로드 오류: {e}")
        return {}

def load_contents():
    """콘텐츠 데이터 로드"""
    try:
        if os.path.exists("data/contents.json"):
            with open("data/contents.json", "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            os.makedirs("data", exist_ok=True)
            default_contents = {
                "lethargy": [
                    {
                        "title": "무기력에서 벗어나는 5가지 방법",
                        "description": "에너지가 없고 의욕이 생기지 않을 때 도움이 되는 실용적인 방법들을 소개합니다.",
                        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                        "tags": ["#무기력", "#실용적조언", "#5분미만"],
                        "duration": "4분 30초"
                    }
                ],
                "anxiety": [
                    {
                        "title": "불안할 때 도움되는 호흡법",
                        "description": "불안감을 줄이는 효과적인 호흡 기법을 배워보세요.",
                        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                        "tags": ["#불안", "#호흡법", "#실용적조언"],
                        "duration": "6분 20초"
                    }
                ]
            }
            with open("data/contents.json", "w", encoding="utf-8") as f:
                json.dump(default_contents, f, ensure_ascii=False, indent=2)
            return default_contents
    except Exception as e:
        print(f"콘텐츠 로드 오류: {e}")
        return {}

def load_emotion_calendar():
    """감정 달력 데이터 로드"""
    try:
        if os.path.exists("emotion_calendar.json"):
            with open("emotion_calendar.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except:
        return {}

def save_emotion_calendar(calendar_data):
    """감정 달력 데이터 저장"""
    try:
        with open("emotion_calendar.json", "w", encoding="utf-8") as f:
            json.dump(calendar_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"저장 중 오류: {e}")

def save_emotion_record(text):
    """감정 기록 저장"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("records.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {text}\n")
    except Exception as e:
        st.error(f"기록 저장 오류: {e}")

def load_letters():
    """편지 데이터 로드"""
    try:
        if os.path.exists("future_letters.json"):
            with open("future_letters.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return {"letters": []}
    except:
        return {"letters": []}

def save_letters(letters_data):
    """편지 데이터 저장"""
    try:
        with open("future_letters.json", "w", encoding="utf-8") as f:
            json.dump(letters_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"편지 저장 오류: {e}")

def get_new_letters_count():
    """새로 도착한 편지 수 확인"""
    try:
        letters_data = load_letters()
        today = date.today()
        
        new_count = 0
        for letter in letters_data["letters"]:
            delivery_date = datetime.strptime(letter["delivery_date"], "%Y-%m-%d").date()
            if delivery_date <= today and not letter.get("is_read", False):
                new_count += 1
        
        return new_count
    except:
        return 0

# 메인 페이지
def main_page():
    """메인 홈페이지"""
    st.markdown("""
    <div class="main-header">
        <h1>🧭 마음의 나침반</h1>
        <p>당신의 감정을 이해하고, 성장하는 길을 찾아보세요</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="
            background: #ffffff;
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #e0e0e0;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            color: #333333;
        ">
            <h3 style="color: #4A90E2; margin-bottom: 1rem;">🎯 감정 탐색하기</h3>
            <p style="color: #666666; line-height: 1.6;">오늘 마음의 상태를 깊이 있게 탐색하고 맞춤형 조언을 받아보세요</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 감정 탐색 시작하기", key="start_exploration_main", type="primary", use_container_width=True):
            st.session_state["current_page"] = "emotion_exploration"
            # 세션 초기화
            for key in ["selected_emotion", "chat_step", "user_word", "timing"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="
            background: #ffffff;
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #e0e0e0;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            color: #333333;
        ">
            <h3 style="color: #4A90E2; margin-bottom: 1rem;">🌈 색깔 달력</h3>
            <p style="color: #666666; line-height: 1.6;">매일의 감정을 색깔로 기록하고 나만의 감정 패턴을 발견해보세요</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎨 감정 달력 보기", key="view_calendar_main", type="primary", use_container_width=True):
            st.session_state["current_page"] = "emotion_calendar"
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div style="
            background: #ffffff;
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #e0e0e0;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            color: #333333;
        ">
            <h3 style="color: #4A90E2; margin-bottom: 1rem;">💌 미래 편지</h3>
            <p style="color: #666666; line-height: 1.6;">현재의 마음을 미래의 나에게 전하는 특별한 편지를 써보세요</p>
        </div>
        """, unsafe_allow_html=True)
        
        new_letters = get_new_letters_count()
        if new_letters > 0:
            button_text = f"💌 편지함 ({new_letters}통 도착!)"
        else:
            button_text = "💌 미래 편지 쓰기"
        
        if st.button(button_text, key="view_letters_main", type="primary", use_container_width=True):
            st.session_state["current_page"] = "future_letter"
            st.rerun()
    
    with col4:
        st.markdown("""
        <div style="
            background: #ffffff;
            padding: 2rem;
            border-radius: 15px;
            border: 2px solid #e0e0e0;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            color: #333333;
        ">
            <h3 style="color: #4A90E2; margin-bottom: 1rem;">📊 나의 통계</h3>
            <p style="color: #666666; line-height: 1.6;">감정 기록과 성장 과정을 한눈에 확인해보세요</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📈 통계 보기", key="view_stats_main", type="secondary", use_container_width=True):
            st.info("📊 통계 기능은 곧 추가될 예정이에요!")
    
    show_recent_records()

def show_recent_records():
    """최근 감정 기록 표시"""
    st.subheader("📝 최근 감정 기록")
    
    try:
        if os.path.exists("records.txt"):
            with open("records.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
                if lines:
                    recent_lines = lines[-3:]
                    for line in reversed(recent_lines):
                        if line.strip():
                            st.write(f"• {line.strip()}")
                else:
                    st.info("아직 기록된 감정이 없어요. 첫 번째 여정을 시작해보세요! 😊")
        else:
            st.info("아직 기록된 감정이 없어요. 첫 번째 여정을 시작해보세요! 😊")
    except Exception as e:
        st.info("아직 기록된 감정이 없어요. 첫 번째 여정을 시작해보세요! 😊")

# 감정 탐색 페이지
def emotion_exploration_page():
    """감정 탐색 기능"""
    st.title("🎯 감정 탐색하기")
    st.markdown("*당신의 마음을 깊이 있게 이해해보세요*")
    
    # 초기 감정 선택
    if "selected_emotion" not in st.session_state:
        st.subheader("어떤 감정을 느끼고 계신가요?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("😴 무기력함", key="lethargy_btn", type="primary", use_container_width=True):
                st.session_state.selected_emotion = "lethargy"
                st.session_state.chat_step = 1
                st.rerun()
        
        with col2:
            if st.button("😰 불안함", key="anxiety_btn", type="primary", use_container_width=True):
                st.session_state.selected_emotion = "anxiety"
                st.session_state.chat_step = 1
                st.rerun()
    else:
        run_emotion_chat()

def run_emotion_chat():
    """감정 탐색 채팅"""
    emotion = st.session_state.selected_emotion
    step = st.session_state.get("chat_step", 1)
    
    emotion_name = "무기력" if emotion == "lethargy" else "불안"
    st.subheader(f"💭 {emotion_name} 감정 탐색")
    
    # 단계 1: 은유적 단어 입력 받기 → 사용자 입력 후 2단계로 진행
    if step == 1:
        st.write("마음이 힘드시는군요. 조금 더 자세히 이야기해볼까요?")
        st.write("지금 느끼시는 감정을 한 단어로 표현한다면 어떤 것일까요?")
        
        user_input = st.text_input("예: 돌덩이, 안개, 무거운 짐 같은...", key="emotion_word")
        
        if st.button("다음", key="next1") and user_input:
            st.session_state.user_word = user_input
            st.session_state.chat_step = 2
            st.rerun()
    
    # 단계 2: 감정이 시작된 맥락/시점 서술 받기 → 3단계로 진행
    elif step == 2:
        word = st.session_state.user_word
        st.write(f"'{word}' 같은 감정이시는군요.")
        st.write("언제부터 이런 기분을 느끼셨나요?")
        
        user_input = st.text_area("시간, 상황, 계기 등을 자유롭게 적어주세요", key="emotion_timing")
        
        if st.button("다음", key="next2") and user_input:
            st.session_state.timing = user_input
            st.session_state.chat_step = 3
            st.rerun()
    
    # 단계 3: 통찰, 추천, 기록(완료 후 홈 이동)
    elif step == 3:
        st.write("🌟 통찰의 시간")
        provide_insight()
        recommend_content()
        final_emotion_record()

def provide_insight():
    """개인화된 통찰 제공"""
    word = st.session_state.get("user_word", "")
    emotion = st.session_state.selected_emotion
    
    st.markdown("""
    <div class="positive-message">
        <h4>💝 당신을 위한 따뜻한 메시지</h4>
    </div>
    """, unsafe_allow_html=True)
    
    if emotion == "lethargy":
        insight = f"""
        '{word}' 같은 무기력함을 느끼고 계시는군요. 
        
        이런 감정은 우리가 잠시 멈춰서 자신을 돌아보라는 신호일 수 있어요. 
        마치 휴대폰 배터리가 부족할 때 충전이 필요하듯, 
        당신의 마음도 지금 재충전의 시간이 필요한 것 같아요.
        
        작은 것부터 시작해보세요. 오늘 할 수 있는 가장 작은 일 하나만이라도요. 
        그것이 당신의 첫 번째 작은 승리가 될 거예요. ✨
        """
    else:
        insight = f"""
        '{word}' 같은 불안함을 느끼고 계시는군요.
        
        불안은 우리가 무언가를 소중히 여기고 있다는 증거예요. 
        완전히 무관심하다면 불안하지도 않을 테니까요.
        
        지금 이 순간, 당신이 할 수 있는 일에 집중해보세요. 
        미래는 현재의 작은 선택들로 만들어진답니다. 
        심호흡을 하고, 한 걸음씩 나아가세요. 🌱
        """
    
    st.write(insight)

def recommend_content():
    """콘텐츠 추천"""
    st.subheader("🎬 당신을 위한 추천 콘텐츠")
    
    emotion = st.session_state.selected_emotion
    
    default_contents = {
        "lethargy": [
            {
                "title": "무기력에서 벗어나는 5가지 방법",
                "description": "에너지가 없고 의욕이 생기지 않을 때 도움이 되는 실용적인 방법들을 소개합니다.",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "tags": ["#무기력", "#실용적조언", "#5분미만"],
                "duration": "4분 30초"
            },
            {
                "title": "작은 습관의 힘",
                "description": "큰 변화보다는 작은 습관부터 시작하는 방법에 대해 이야기합니다.",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "tags": ["#습관", "#자기계발"],
                "duration": "8분 15초"
            }
        ],
        "anxiety": [
            {
                "title": "불안할 때 도움되는 호흡법",
                "description": "불안감을 줄이는 효과적인 호흡 기법을 배워보세요.",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "tags": ["#불안", "#호흡법", "#실용적조언"],
                "duration": "6분 20초"
            },
            {
                "title": "걱정 많은 마음 다스리기",
                "description": "과도한 걱정에서 벗어나는 심리학적 접근법을 소개합니다.",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "tags": ["#걱정", "#심리학"],
                "duration": "7분 45초"
            }
        ]
    }
    
    try:
        contents = load_contents()
        # 데이터 파일이 없거나 해당 감정 키가 없으면 안전한 기본 추천 사용
        if not contents or emotion not in contents:
            contents = default_contents
    except:
        contents = default_contents
    
    if emotion in contents:
        for i, content in enumerate(contents[emotion][:3]):
            with st.expander(f"🎥 {content['title']}"):
                st.write(f"**설명:** {content['description']}")
                st.write(f"**시간:** {content['duration']}")
                st.write(f"**태그:** {' '.join(content['tags'])}")
                st.markdown(f"[🔗 영상 보러가기]({content['url']})")

def final_emotion_record():
    """최종 감정 기록"""
    st.subheader("📝 오늘의 마음 기록하기")
    
    final_text = st.text_area(
        "이 모든 과정을 거친 지금, 당신의 마음을 한 문장으로 표현해보세요 ✍️",
        placeholder="예: 비록 무겁지만 이해받는 느낌이 들어서 조금 마음이 가벼워졌어요"
    )
    
    if st.button("💾 마음 기록하기", type="primary"):
        if final_text.strip():
            save_emotion_record(final_text.strip())
            
            st.markdown("""
            <div class="positive-message">
                <h4>🎉 기록 완료!</h4>
                <p>당신의 소중한 마음이 기록되었어요. 오늘도 자신과 마주한 용기 있는 당신에게 박수를 보내요! 👏</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
            
            if st.button("🏠 홈으로 돌아가기"):
                for key in ["selected_emotion", "chat_step", "user_word", "timing"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.session_state["current_page"] = "main"
                st.rerun()

# 감정 달력 페이지
def emotion_calendar_page():
    """감정 색깔 달력 페이지"""
    st.title("🌈 감정 색깔 달력")
    st.markdown("*매일의 감정을 색깔로 기록하고, 나만의 감정 패턴을 발견해보세요*")
    
    tab1, tab2, tab3 = st.tabs(["📅 달력 보기", "🎨 오늘 기록", "📊 내 통계"])
    
    with tab1:
        display_emotion_calendar()
    
    with tab2:
        show_emotion_selector()
    
    with tab3:
        show_emotion_statistics()

def display_emotion_calendar():
    """감정 달력 표시"""
    calendar_data = load_emotion_calendar()
    
    # 현재 날짜 표시
    today = date.today()
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #4A90E2, #7B68EE);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
    ">
        <h3>📅 오늘은 {today.strftime('%Y년 %m월 %d일')} ({['월', '화', '수', '목', '금', '토', '일'][today.weekday()]}요일)</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        current_year = st.selectbox("년도", range(2020, 2030), 
                                   index=datetime.now().year - 2020)
    with col2:
        current_month = st.selectbox("월", range(1, 13), 
                                    index=datetime.now().month - 1)
    
    cal = calendar.monthcalendar(current_year, current_month)
    
    st.write(f"### {current_year}년 {current_month}월 감정 달력")
    
    # 범례 추가
    st.markdown("""
    <div style="
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    ">
        <h5>🎨 달력 사용법</h5>
        <p>• <strong>색깔 원:</strong> 감정이 기록된 날 (마우스를 올리면 내용 확인)</p>
        <p>• <strong>회색 원:</strong> 감정이 기록되지 않은 날</p>
        <p>• <strong>오늘:</strong> {today.strftime('%m월 %d일')} - 새로운 감정을 기록해보세요!</p>
    </div>
    """, unsafe_allow_html=True)
    
    days = ['월', '화', '수', '목', '금', '토', '일']
    cols = st.columns(7)
    for i, day in enumerate(days):
        with cols[i]:
            st.write(f"**{day}**")
    
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.write("")
                else:
                    date_str = f"{current_year}-{current_month:02d}-{day:02d}"
                    
                    # 오늘 날짜인지 확인
                    is_today = date_str == today.strftime("%Y-%m-%d")
                    
                    if date_str in calendar_data:
                        emotion_data = calendar_data[date_str]
                        color = emotion_data["color"]
                        
                        # 오늘이면 특별한 스타일
                        border_style = "3px solid #FFD700" if is_today else "2px solid #ddd"
                        
                        st.markdown(f"""
                        <div style="
                            width: 40px; 
                            height: 40px; 
                            background-color: {color}; 
                            border-radius: 50%; 
                            display: flex; 
                            align-items: center; 
                            justify-content: center; 
                            margin: 5px auto;
                            border: {border_style};
                            cursor: pointer;
                            position: relative;
                        " title="{emotion_data['emotion']}: {emotion_data['note']}">
                            <strong style="color: {'white' if color != '#FFD700' else 'black'};">{day}</strong>
                            {f'<div style="position: absolute; top: -5px; right: -5px; background: #FFD700; border-radius: 50%; width: 12px; height: 12px; font-size: 10px; display: flex; align-items: center; justify-content: center;">✨</div>' if is_today else ''}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # 오늘이면 특별한 스타일
                        if is_today:
                            st.markdown(f"""
                            <div style="
                                width: 40px; 
                                height: 40px; 
                                background-color: #fff; 
                                border-radius: 50%; 
                                display: flex; 
                                align-items: center; 
                                justify-content: center; 
                                margin: 5px auto;
                                border: 3px solid #FFD700;
                                animation: pulse 2s infinite;
                            ">
                                <strong style="color: #FFD700;">{day}</strong>
                            </div>
                            <style>
                            @keyframes pulse {{
                                0% {{ box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.7); }}
                                70% {{ box-shadow: 0 0 0 10px rgba(255, 215, 0, 0); }}
                                100% {{ box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }}
                            }}
                            </style>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="
                                width: 40px; 
                                height: 40px; 
                                background-color: #f0f0f0; 
                                border-radius: 50%; 
                                display: flex; 
                                align-items: center; 
                                justify-content: center; 
                                margin: 5px auto;
                                border: 1px solid #ddd;
                            ">
                                {day}
                            </div>
                            """, unsafe_allow_html=True)
    
    # 이번 달 통계 요약
    current_month_data = {}
    for date_key, record in calendar_data.items():
        try:
            record_date = datetime.strptime(date_key, "%Y-%m-%d")
            if record_date.year == current_year and record_date.month == current_month:
                current_month_data[date_key] = record
        except:
            continue
    
    if current_month_data:
        st.markdown("---")
        st.subheader(f"📊 {current_year}년 {current_month}월 요약")
        
        month_emotions = {}
        for record in current_month_data.values():
            emotion = record["emotion"]
            month_emotions[emotion] = month_emotions.get(emotion, 0) + 1
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🗓️ 이번 달 기록", len(current_month_data))
        
        with col2:
            if month_emotions:
                most_emotion = max(month_emotions, key=month_emotions.get)
                st.metric("😊 가장 많은 감정", most_emotion)
        
        with col3:
            completion_rate = (len(current_month_data) / calendar.monthrange(current_year, current_month)[1]) * 100
            st.metric("📈 기록 완성도", f"{completion_rate:.1f}%")

def show_emotion_selector():
    """감정 선택 UI"""
    col1, col2 = st.columns(2)
    
    with col1:
        selected_emotion = st.selectbox(
            "어떤 감정인가요?",
            list(EMOTION_COLORS.keys())
        )
    
    with col2:
        default_color = EMOTION_COLORS[selected_emotion]
        st.markdown(f"""
        <div style="width: 60px; height: 60px; background-color: {default_color}; 
             border-radius: 50%; margin: 10px 0; border: 2px solid #ddd;">
        </div>
        """, unsafe_allow_html=True)
    
    custom_color = st.color_picker("원하는 색깔로 바꿔보세요", default_color)
    
    emotion_note = st.text_area(
        "오늘의 마음을 한 문장으로 적어보세요 ✍️",
        placeholder="예: 오늘은 새로운 도전을 시작하는 설레는 마음이었어요"
    )
    
    if st.button("💾 오늘의 감정 저장하기", type="primary"):
        if emotion_note.strip():
            calendar_data = load_emotion_calendar()
            today = date.today().strftime("%Y-%m-%d")
            
            calendar_data[today] = {
                "emotion": selected_emotion,
                "note": emotion_note.strip(),
                "color": custom_color,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            save_emotion_calendar(calendar_data)
            st.success("✨ 오늘의 감정이 색깔 달력에 저장되었어요!")
            st.balloons()
        else:
            st.warning("감정을 한 문장으로 적어주세요 😊")

def show_emotion_statistics():
    """감정 통계 표시"""
    calendar_data = load_emotion_calendar()
    
    if not calendar_data:
        st.info("아직 기록된 감정이 없어요. 첫 번째 감정을 기록해보세요! 😊")
        return
    
    emotion_counts = {}
    for record in calendar_data.values():
        emotion = record["emotion"]
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    most_common_emotion = max(emotion_counts, key=emotion_counts.get)
    total_records = len(calendar_data)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📅 총 기록 일수", total_records)
    
    with col2:
        st.metric("😊 가장 많은 감정", most_common_emotion)
    
    with col3:
        streak = calculate_streak(calendar_data)
        st.metric("🔥 연속 기록", f"{streak}일")
    
    if emotion_counts:
        st.subheader("📊 감정 분포")
        emotion_df = pd.DataFrame(list(emotion_counts.items()), 
                                 columns=['감정', '횟수'])
        st.bar_chart(emotion_df.set_index('감정'))

def calculate_streak(calendar_data):
    """연속 기록 일수 계산"""
    if not calendar_data:
        return 0
    
    dates = sorted(calendar_data.keys(), reverse=True)
    streak = 0
    current_date = date.today()
    # 최신 날짜부터 하루씩 이어지는지 확인하며 연속 기록 수(streak)를 계산
    for date_str in dates:
        record_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        if (current_date - record_date).days == streak:
            streak += 1
            current_date = record_date
        else:
            break
    
    return streak

# 미래 편지 페이지
def future_letter_page():
    """미래 편지 페이지"""
    st.title("💌 미래의 나에게 편지쓰기")
    st.markdown("*현재의 마음을 미래의 나에게 전해보세요*")
    
    tab1, tab2 = st.tabs(["✍️ 편지 쓰기", "📪 편지함"])
    
    with tab1:
        show_simple_letter_writing()
    
    with tab2:
        show_simple_mailbox()

def show_simple_letter_writing():
    """간단화된 편지 쓰기"""
    st.subheader("💝 마음을 담은 편지 쓰기")
    
    letter_content = st.text_area(
        "미래의 나에게 하고 싶은 말을 써보세요",
        placeholder="""안녕, 미래의 나!

지금은 조금 힘든 시간을 보내고 있어. 
하지만 이 편지를 읽고 있는 너는 분명 많이 성장했을 거야.

오늘 나는 이런 마음이야...

그때의 너에게 이 말을 전하고 싶어...

사랑해, 과거의 나가 💕""",
        height=200
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        delivery_option = st.selectbox(
            "언제 받고 싶나요?",
            ["1주일 후", "한 달 후", "3개월 후", "1년 후"]
        )
        
        days_map = {"1주일 후": 7, "한 달 후": 30, "3개월 후": 90, "1년 후": 365}
        delivery_date = date.today() + timedelta(days=days_map[delivery_option])
    
    with col2:
        st.info(f"📅 배송 예정일\n{delivery_date.strftime('%Y년 %m월 %d일')}")
    
    if st.button("💌 편지 보내기", type="primary"):
        if letter_content.strip():
            letters_data = load_letters()
            
            new_letter = {
                "id": str(uuid.uuid4()),
                "title": "",
                "content": letter_content.strip(),
                "write_date": date.today().strftime("%Y-%m-%d"),
                "delivery_date": delivery_date.strftime("%Y-%m-%d"),
                "is_read": False,
                "read_date": None,
                "write_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            letters_data["letters"].append(new_letter)
            save_letters(letters_data)
            
            st.success("✨ 편지가 성공적으로 보내졌어요!")
            st.balloons()
            
            days_until = (delivery_date - date.today()).days
            st.info(f"🚚 {days_until}일 후에 편지가 도착할 예정이에요!")

def show_simple_mailbox():
    """간단화된 편지함"""
    letters_data = load_letters()
    today = date.today()
    
    deliverable = []
    waiting = []
    
    for letter in letters_data["letters"]:
        delivery_date = datetime.strptime(letter["delivery_date"], "%Y-%m-%d").date()
        if delivery_date <= today:
            deliverable.append(letter)
        else:
            waiting.append(letter)
    
    col1, col2 = st.columns(2)
    with col1:
        unread_count = len([l for l in deliverable if not l["is_read"]])
        st.metric("📬 새 편지", unread_count)
    
    with col2:
        st.metric("⏰ 배송 대기", len(waiting))
    
    if deliverable:
        st.subheader("📬 도착한 편지들")
        
        for letter in sorted(deliverable, key=lambda x: x["delivery_date"], reverse=True):
            write_date = datetime.strptime(letter["write_date"], "%Y-%m-%d")
            status = "🆕 새 편지" if not letter["is_read"] else "✅ 읽음"
            
            with st.expander(f"{status} - {write_date.strftime('%Y.%m.%d')}의 나로부터"):
                st.write(letter["content"])
                
                if not letter["is_read"]:
                    if st.button("읽음으로 표시", key=f"mark_read_{letter['id']}"):
                        for l in letters_data["letters"]:
                            if l["id"] == letter["id"]:
                                l["is_read"] = True
                                l["read_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                break
                        save_letters(letters_data)
                        st.success("편지를 읽으셨군요! 💕")
                        st.rerun()
    else:
        st.info("아직 도착한 편지가 없어요. 첫 번째 편지를 써보세요! ✍️")

# 메인 앱 실행
def main():
    # 세션 상태 초기화
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "main"
    
    # 사이드바 네비게이션
    st.sidebar.title("🧭 마음의 나침반")
    
    # 새 편지 알림
    try:
        new_letters = get_new_letters_count()
        if new_letters > 0:
            st.sidebar.markdown(f"""
            <div style="
                background: linear-gradient(90deg, #FFE4E1, #FFF0F5);
                padding: 0.8rem;
                border-radius: 8px;
                border-left: 4px solid #FF69B4;
                margin: 1rem 0;
            ">
                <h4>💌 새 편지 도착!</h4>
                <p>{new_letters}통의 편지가 기다리고 있어요!</p>
            </div>
            """, unsafe_allow_html=True)
    except:
        pass
    
    # 현재 페이지 확인
    current_page = st.session_state.get("current_page", "main")
    
    # 사이드바 메뉴
    menu_options = ["🏠 홈", "🎯 감정 탐색", "🌈 감정 달력", "💌 미래 편지"]
    
    if current_page == "main":
        default_index = 0
    elif current_page == "emotion_exploration":
        default_index = 1
    elif current_page == "emotion_calendar":
        default_index = 2
    elif current_page == "future_letter":
        default_index = 3
    else:
        default_index = 0
    
    selected_menu = st.sidebar.selectbox(
        "메뉴 선택",
        menu_options,
        index=default_index
    )
    
    # 사이드바에서 메뉴 선택 시 페이지 변경
    if selected_menu == "🏠 홈" and current_page != "main":
        st.session_state["current_page"] = "main"
        st.rerun()
    elif selected_menu == "🎯 감정 탐색" and current_page != "emotion_exploration":
        st.session_state["current_page"] = "emotion_exploration"
        # 세션 초기화
        for key in ["selected_emotion", "chat_step", "user_word", "timing"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    elif selected_menu == "🌈 감정 달력" and current_page != "emotion_calendar":
        st.session_state["current_page"] = "emotion_calendar"
        st.rerun()
    elif selected_menu == "💌 미래 편지" and current_page != "future_letter":
        st.session_state["current_page"] = "future_letter"
        st.rerun()
    
    # 페이지 표시
    try:
        if current_page == "main":
            main_page()
        elif current_page == "emotion_exploration":
            emotion_exploration_page()
        elif current_page == "emotion_calendar":
            emotion_calendar_page()
        elif current_page == "future_letter":
            future_letter_page()
        else:
            st.session_state["current_page"] = "main"
            st.rerun()
    except Exception as e:
        st.error(f"페이지 로드 중 오류가 발생했어요: {str(e)}")
        st.info("홈 페이지로 돌아가려면 새로고침해주세요.")
        if st.button("🏠 홈으로 돌아가기"):
            st.session_state["current_page"] = "main"
            st.rerun()

if __name__ == "__main__":
    main()
