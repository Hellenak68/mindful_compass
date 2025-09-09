# app.py - 마음의 나침반 통합 앱 (8개 감정 확장 + 개선된 콘텐츠 시스템)

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
    
    .emotion-card {
        background: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }
    
    .emotion-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .positive-message {
        background: linear-gradient(90deg, #98FB98, #90EE90);
        padding: 1.5rem;
        border-radius: 12px;
        color: #2d5a2d;
        margin: 1rem 0;
        border-left: 5px solid #32CD32;
    }
    
    .emotion-button {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        text-align: center;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .emotion-button:hover {
        border-color: #4A90E2;
        transform: scale(1.02);
    }
    
    /* 버튼 스타일 개선 */
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

# 감정별 색깔 정의 (8개로 확장)
EMOTION_COLORS = {
    "행복": "#FFD700",      # 황금색
    "평온": "#87CEEB",      # 하늘색
    "무기력": "#A9A9A9",    # 회색
    "불안": "#FF6B6B",      # 연한 빨강
    "슬픔": "#4169E1",      # 파랑
    "화남": "#FF4500",      # 주황빨강
    "희망": "#98FB98",      # 연두색
    "감사": "#DDA0DD",      # 자주색
    "외로움": "#6f42c1",    # 보라색
    "분노": "#fd7e14",      # 주황색
    "스트레스": "#e83e8c",  # 핫핑크
    "혼란": "#17a2b8",      # 청록색
    "좌절": "#28a745"       # 녹색
}

# 8개 확장 감정 정의
EMOTIONS_CONFIG = {
    "무기력": {
        "icon": "😴",
        "description": "에너지가 없고 아무것도 하기 싫음",
        "color": "#6c757d",
        "keywords": ["덩어리", "안개", "무거운 짐"]
    },
    "불안": {
        "icon": "😰", 
        "description": "걱정되고 초조하며 불안함",
        "color": "#dc3545",
        "keywords": ["바람", "파도", "뒤틀림"]
    },
    "외로움": {
        "icon": "😔",
        "description": "혼자라는 느낌, 고립감",
        "color": "#6f42c1",
        "keywords": ["섬", "구멍", "텅 빔"]
    },
    "분노": {
        "icon": "😤",
        "description": "화가 나고 짜증나며 억울함",
        "color": "#fd7e14",
        "keywords": ["불", "폭발", "압박"]
    },
    "슬픔": {
        "icon": "😢",
        "description": "우울하고 기분이 가라앉음",
        "color": "#20c997",
        "keywords": ["비", "가라앉음", "어둠"]
    },
    "스트레스": {
        "icon": "😵",
        "description": "압박감과 긴장감, 과부하",
        "color": "#e83e8c",
        "keywords": ["조임", "짓눌림", "터질 것 같음"]
    },
    "혼란": {
        "icon": "🤯",
        "description": "무엇을 해야 할지 모르겠음",
        "color": "#17a2b8",
        "keywords": ["미로", "소용돌이", "뒤엉킴"]
    },
    "좌절": {
        "icon": "😩",
        "description": "뜻대로 되지 않아 답답함",
        "color": "#28a745",
        "keywords": ["막힘", "부딪힘", "갇힘"]
    }
}

# 데이터 로드/저장 함수들
def load_contents():
    """콘텐츠 데이터 로드 - 예외 처리 강화"""
    try:
        if os.path.exists("data/contents.json"):
            with open("data/contents.json", "r", encoding="utf-8") as f:
                contents = json.load(f)
                return contents
        else:
            return create_default_contents()
    except Exception as e:
        st.error(f"콘텐츠 로드 오류: {e}")
        return create_default_contents()

def create_default_contents():
    """각 감정별 1개씩 예시 콘텐츠 생성"""
    os.makedirs("data", exist_ok=True)
    
    default_contents = {
        "무기력": [
            {
                "id": "lethargy_001",
                "title": "20대 무기력증, 이렇게 극복했어요",
                "description": "무기력한 상태에서 벗어나는 작은 시작들",
                "channel": "써니즈",
                "url": "https://www.youtube.com/watch?v=sample1",
                "duration": "12:30",
                "tags": ["무기력", "20대", "극복"],
                "content_type": "위로"
            }
        ],
        "불안": [
            {
                "id": "anxiety_001",
                "title": "불안할 때 3분 마음챙김",
                "description": "즉시 사용 가능한 불안 완화 호흡법",
                "channel": "마인드풀TV",
                "url": "https://www.youtube.com/watch?v=sample2",
                "duration": "5:30",
                "tags": ["불안", "호흡법", "마음챙김"],
                "content_type": "실용팁"
            }
        ],
        "외로움": [
            {
                "id": "loneliness_001",
                "title": "혼자여도 괜찮아, 외로움 다독이기",
                "description": "외로움을 적이 아닌 친구로 받아들이는 방법",
                "channel": "하루의 사랑작업",
                "url": "https://www.youtube.com/watch?v=sample3",
                "duration": "14:20",
                "tags": ["외로움", "수용", "위로"],
                "content_type": "위로"
            }
        ],
        "분노": [
            {
                "id": "anger_001",
                "title": "화날 때 감정 조절하는 법",
                "description": "분노를 건설적으로 표현하고 다루는 방법",
                "channel": "김상윤",
                "url": "https://www.youtube.com/watch?v=sample4",
                "duration": "11:15",
                "tags": ["분노", "감정조절", "소통"],
                "content_type": "실용팁"
            }
        ],
        "슬픔": [
            {
                "id": "sadness_001",
                "title": "슬플 때 마음을 달래는 방법",
                "description": "슬픔을 받아들이고 위로받는 시간",
                "channel": "나탐",
                "url": "https://www.youtube.com/watch?v=sample5",
                "duration": "16:40",
                "tags": ["슬픔", "위로", "수용"],
                "content_type": "위로"
            }
        ],
        "스트레스": [
            {
                "id": "stress_001",
                "title": "직장인 스트레스 해소법",
                "description": "바쁜 일상 속에서 실천할 수 있는 스트레스 관리",
                "channel": "김주환",
                "url": "https://www.youtube.com/watch?v=sample6",
                "duration": "13:40",
                "tags": ["스트레스", "직장인", "해소법"],
                "content_type": "실용팁"
            }
        ],
        "혼란": [
            {
                "id": "confusion_001",
                "title": "인생의 방향을 잃었을 때",
                "description": "혼란스러운 시기를 지나는 지혜",
                "channel": "러브포레스토",
                "url": "https://www.youtube.com/watch?v=sample7",
                "duration": "18:30",
                "tags": ["혼란", "방향", "지혜"],
                "content_type": "통찰"
            }
        ],
        "좌절": [
            {
                "id": "frustration_001",
                "title": "실패와 좌절을 성장으로 바꾸기",
                "description": "좌절 경험을 통한 성장과 학습",
                "channel": "정신과의사정우열",
                "url": "https://www.youtube.com/watch?v=sample8",
                "duration": "15:25",
                "tags": ["좌절", "성장", "실패"],
                "content_type": "성장"
            }
        ]
    }
    
    with open("data/contents.json", "w", encoding="utf-8") as f:
        json.dump(default_contents, f, ensure_ascii=False, indent=2)
    
    return default_contents

def load_emotion_calendar():
    """감정 달력 데이터 로드"""
    if os.path.exists("emotion_calendar.json"):
        with open("emotion_calendar.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_emotion_calendar(calendar_data):
    """감정 달력 데이터 저장"""
    with open("emotion_calendar.json", "w", encoding="utf-8") as f:
        json.dump(calendar_data, f, ensure_ascii=False, indent=2)

def save_emotion_record(text):
    """감정 기록 저장"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("records.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {text}\n")

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
        <div class="emotion-card">
            <h3>🎯 감정 탐색하기</h3>
            <p>오늘 마음의 상태를 깊이 있게 탐색하고 맞춤형 조언을 받아보세요</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 감정 탐색 시작하기", key="start_exploration", type="primary"):
            st.session_state.page = "emotion_exploration"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="emotion-card">
            <h3>🌈 색깔 달력</h3>
            <p>매일의 감정을 색깔로 기록하고 나만의 감정 패턴을 발견해보세요</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎨 감정 달력 보기", key="view_calendar", type="primary"):
            st.session_state.page = "emotion_calendar"
            st.rerun()
    
    # 최근 기록 표시
    show_recent_records()

def show_recent_records():
    """최근 감정 기록 표시"""
    st.subheader("📝 최근 감정 기록")
    
    try:
        with open("records.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            if lines:
                # 최근 3개 기록만 표시
                recent_lines = lines[-3:]
                for line in reversed(recent_lines):
                    if line.strip():
                        st.write(f"• {line.strip()}")
            else:
                st.info("아직 기록된 감정이 없어요. 첫 번째 여정을 시작해보세요!")
    except FileNotFoundError:
        st.info("아직 기록된 감정이 없어요. 첫 번째 여정을 시작해보세요!")

# 감정 탐색 페이지 (8개 감정으로 확장)
def emotion_exploration_page():
    """감정 탐색 기능 - 8개 감정 지원"""
    st.title("🎯 감정 탐색하기")
    st.markdown("*당신의 마음을 깊이 있게 이해해보세요*")
    
    # 초기 감정 선택
    if "selected_emotion" not in st.session_state:
        st.subheader("어떤 감정을 느끼고 계신가요?")
        
        # 2x4 그리드로 배치
        col1, col2 = st.columns(2)
        
        emotions_list = list(EMOTIONS_CONFIG.items())
        
        for i in range(0, len(emotions_list), 2):
            with col1:
                if i < len(emotions_list):
                    emotion, data = emotions_list[i]
                    if st.button(
                        f"{data['icon']} {emotion}\n{data['description']}", 
                        key=f"emotion_{emotion}",
                        use_container_width=True
                    ):
                        st.session_state.selected_emotion = emotion
                        st.session_state.emotion_data = data
                        st.session_state.chat_step = 1
                        st.rerun()
            
            with col2:
                if i+1 < len(emotions_list):
                    emotion, data = emotions_list[i+1]
                    if st.button(
                        f"{data['icon']} {emotion}\n{data['description']}", 
                        key=f"emotion_{emotion}",
                        use_container_width=True
                    ):
                        st.session_state.selected_emotion = emotion
                        st.session_state.emotion_data = data
                        st.session_state.chat_step = 1
                        st.rerun()
    
    else:
        # 선택된 감정에 따른 대화형 탐색
        run_emotion_chat()

def run_emotion_chat():
    """감정 탐색 채팅 - 개선된 버전"""
    emotion = st.session_state.selected_emotion
    emotion_data = st.session_state.get("emotion_data", {})
    step = st.session_state.get("chat_step", 1)
    
    st.subheader(f"💭 {emotion} 감정 탐색")
    
    # 진행 상황 표시
    progress = min(step / 3, 1.0)
    st.progress(progress)
    st.caption(f"단계 {step}/3")
    
    if step == 1:
        st.markdown(f"""
        <div style="background: {emotion_data.get('color', '#6c757d')}20; 
                    padding: 15px; border-radius: 10px; margin: 10px 0;">
            <h4>{emotion_data.get('icon', '💭')} {emotion}을 느끼고 계시는군요</h4>
            <p>마음이 힘드시는군요. 조금 더 자세히 들어볼까요?</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("**지금 느끼시는 감정을 한 단어로 표현한다면 어떤 것일까요?**")
        
        # 감정별 맞춤 키워드 제안
        emotion_keywords = emotion_data.get('keywords', ["무거움", "답답함", "불편함"])
        
        # 빠른 선택 옵션
        st.write("빠른 선택:")
        cols = st.columns(len(emotion_keywords))
        
        for i, keyword in enumerate(emotion_keywords):
            with cols[i]:
                if st.button(keyword, key=f"quick_{keyword}"):
                    st.session_state.user_word = keyword
                    st.session_state.chat_step = 2
                    st.rerun()
        
        # 직접 입력
        user_input = st.text_input(
            "또는 직접 입력:", 
            placeholder="예: 덩어리, 안개, 무거운 짐 같은...",
            key="emotion_word"
        )
        
        if st.button("다음", key="next1") and user_input:
            st.session_state.user_word = user_input
            st.session_state.chat_step = 2
            st.rerun()
    
    elif step == 2:
        word = st.session_state.user_word
        st.write(f"'{word}' 같은 감정이시는군요.")
        st.write("**언제부터 이런 기분을 느끼셨나요?**")
        
        # 시점 선택 옵션
        timing_options = [
            "방금 전부터", "오늘 아침부터", "며칠 전부터", 
            "일주일 이상", "오래전부터"
        ]
        
        selected_timing = st.radio("시점을 선택해주세요:", timing_options, horizontal=True)
        
        # 상황 입력
        user_input = st.text_area(
            "그 시점에 무슨 일이 있었는지 간단히 알려주세요:",
            placeholder="예: 과제 마감, 친구와 다툼, 취업 스트레스, 특별한 일 없었음...",
            height=100,
            key="emotion_timing"
        )
        
        if st.button("다음", key="next2") and user_input:
            st.session_state.timing = selected_timing
            st.session_state.context = user_input
            st.session_state.chat_step = 3
            st.rerun()
    
    elif step == 3:
        st.write("🌟 통찰의 시간")
        
        # 개인화된 통찰 제공
        provide_enhanced_insight()
        
        # 콘텐츠 추천
        recommend_content()
        
        # 감정 기록하기
        final_emotion_record()

def provide_enhanced_insight():
    """향상된 개인화 통찰 제공"""
    emotion = st.session_state.selected_emotion
    word = st.session_state.get("user_word", "")
    timing = st.session_state.get("timing", "")
    context = st.session_state.get("context", "")
    
    st.markdown("""
    <div class="positive-message">
        <h4>💝 당신을 위한 따뜻한 이해</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # 감정별 맞춤 통찰
    insights = get_emotion_insights(emotion, word, timing, context)
    
    st.write(insights['main_message'])
    
    # 추가 격려 메시지
    st.info(f"💡 {insights['encouragement']}")

def get_emotion_insights(emotion, word, timing, context):
    """감정별 맞춤 통찰 생성"""
    
    base_insights = {
        "무기력": {
            "main_message": f"'{word}' 같은 무기력함을 느끼고 계시는군요. 이런 감정은 우리가 잠시 멈춰서 자신을 돌아보라는 신호일 수 있어요. 마치 휴대폰 배터리가 부족할 때 충전이 필요하듯, 당신의 마음도 지금 재충전의 시간이 필요한 것 같아요.",
            "encouragement": "작은 것부터 시작해보세요. 오늘 할 수 있는 가장 작은 일 하나만이라도요."
        },
        "불안": {
            "main_message": f"'{word}' 같은 불안함을 느끼고 계시는군요. 불안은 우리가 무언가를 소중히 여기고 있다는 증거예요. 완전히 무관심하다면 불안하지도 않을 테니까요.",
            "encouragement": "지금 이 순간, 당신이 할 수 있는 일에 집중해보세요. 미래는 현재의 작은 선택들로 만들어집니다."
        },
        "외로움": {
            "main_message": f"'{word}' 같은 외로움을 느끼고 계시는군요. 외로움은 연결을 원하는 자연스러운 감정이에요. 혼자라는 느낌이 들 때도 당신을 이해하고 응원하는 마음들이 있다는 것을 기억해주세요.",
            "encouragement": "외로움도 당신의 소중한 일부입니다. 이 감정을 통해 진정한 연결의 의미를 더 깊이 이해하게 될 거예요."
        },
        "분노": {
            "main_message": f"'{word}' 같은 분노를 느끼고 계시는군요. 화가 나는 것은 당신이 무언가 중요한 것을 지키려 한다는 뜻이에요. 그 분노 뒤에 숨은 소중한 가치를 발견해보세요.",
            "encouragement": "분노를 억누르지 마세요. 건강한 방식으로 표현하고, 그 에너지를 긍정적 변화로 바꿀 수 있어요."
        },
        "슬픔": {
            "main_message": f"'{word}' 같은 슬픔을 느끼고 계시는군요. 슬픔은 우리가 잃은 것의 소중함을 알려주는 감정이에요. 충분히 슬퍼하는 것도 치유의 과정입니다.",
            "encouragement": "눈물은 마음을 정화하는 자연스러운 과정이에요. 슬픔을 통해 더 깊은 공감과 사랑을 배우게 될 거예요."
        },
        "스트레스": {
            "main_message": f"'{word}' 같은 스트레스를 느끼고 계시는군요. 스트레스는 우리가 성장하고 도전하고 있다는 신호이기도 해요. 하지만 지금은 잠시 속도를 늦춰도 괜찮아요.",
            "encouragement": "완벽하지 않아도 괜찮습니다. 숨을 고르고, 우선순위를 정리해보세요."
        },
        "혼란": {
            "main_message": f"'{word}' 같은 혼란을 느끼고 계시는군요. 혼란은 새로운 이해와 성장의 전단계일 수 있어요. 지금 당장 모든 답을 알 필요는 없어요.",
            "encouragement": "한 번에 하나씩 정리해보세요. 작은 명확함들이 모여 큰 이해가 됩니다."
        },
        "좌절": {
            "main_message": f"'{word}' 같은 좌절감을 느끼고 계시는군요. 좌절은 당신이 목표를 향해 노력하고 있다는 증거예요. 포기하지 않고 여기까지 온 자신을 인정해주세요.",
            "encouragement": "모든 위대한 성취는 수많은 좌절을 딛고 만들어집니다. 잠시 쉬어가도 괜찮아요."
        }
    }
    
    return base_insights.get(emotion, {
        "main_message": "힘든 감정을 느끼고 계시는군요. 이런 감정도 당신의 소중한 일부예요.",
        "encouragement": "지금 이 순간을 있는 그대로 받아들여보세요."
    })

def recommend_content():
    """개선된 콘텐츠 추천 - 오류 방지"""
    st.subheader("🎬 당신을 위한 추천 콘텐츠")
    
    emotion = st.session_state.selected_emotion
    contents = load_contents()
    
    if emotion in contents and len(contents[emotion]) > 0:
        st.success(f"{emotion} 관련 콘텐츠를 찾았습니다!")
        
        for i, content in enumerate(contents[emotion][:3]):  # 최대 3개
            with st.expander(f"🎥 {content['title']}", expanded=(i==0)):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**설명:** {content['description']}")
                    st.write(f"**채널:** {content['channel']}")
                    st.write(f"**시간:** {content['duration']}")
                    if 'tags' in content:
                        st.write(f"**태그:** {' '.join(content['tags'])}")
                
                with col2:
                    st.markdown(f"[▶️ 시청하기]({content['url']})")
                    
                    # 피드백 수집
                    if st.button(f"도움됐어요", key=f"helpful_{emotion}_{i}"):
                        save_content_feedback(content.get('title', ''), True)
                        st.success("피드백 감사합니다!")
    else:
        st.warning(f"{emotion} 관련 콘텐츠가 아직 준비되지 않았습니다.")
        st.info("곧 다양한 콘텐츠를 추가할 예정입니다. 다른 감정을 선택해보시거나 나중에 다시 방문해주세요.")

def save_content_feedback(content_title, is_helpful):
    """콘텐츠 피드백 저장"""
    try:
        feedback_file = "content_feedback.json"
        
        if os.path.exists(feedback_file):
            with open(feedback_file, "r", encoding="utf-8") as f:
                feedbacks = json.load(f)
        else:
            feedbacks = {"feedbacks": []}
        
        new_feedback = {
            "content_title": content_title,
            "is_helpful": is_helpful,
            "emotion": st.session_state.get("selected_emotion", "unknown"),
            "timestamp": datetime.now().isoformat(),
            "session_id": st.session_state.get("session_id", "anonymous")
        }
        
        feedbacks["feedbacks"].append(new_feedback)
        
        with open(feedback_file, "w", encoding="utf-8") as f:
            json.dump(feedbacks, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"피드백 저장 오류: {e}")

def final_emotion_record():
    """최종 감정 기록"""
    st.subheader("📝 오늘의 마음 기록하기")
    
    final_text = st.text_area(
        "이 모든 과정을 거친 지금, 당신의 마음을 한 문장으로 표현해보세요 ✏️",
        placeholder="예: 비록 무겁지만 이해받는 느낌이 들어서 조금 마음이 가벼워졌어요",
        key="final_record"
    )
    
    if st.button("💾 마음 기록하기", type="primary"):
        if final_text.strip():
            save_emotion_record(final_text.strip())
            
            st.markdown("""
            <div class="positive-message">
                <h4>🎉 기록 완료!</h4>
                <p>당신의 소중한 마음이 기록되었어요. 오늘도 자신과 마주한 용기 있는 당신에게 박수를 보내요!</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
            
            if st.button("🏠 홈으로 돌아가기"):
                # 세션 초기화
                for key in ["selected_emotion", "chat_step", "user_word", "timing", "context", "emotion_data"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.session_state.page = "main"
                st.rerun()

# 감정 달력 페이지 (기존 코드 유지)
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
    
    # 현재 년월 선택
    col1, col2 = st.columns(2)
    with col1:
        current_year = st.selectbox("년도", range(2020, 2030), 
                                   index=datetime.now().year - 2020)
    with col2:
        current_month = st.selectbox("월", range(1, 13), 
                                    index=datetime.now().month - 1)
    
    # 달력 생성
    cal = calendar.monthcalendar(current_year, current_month)
    
    st.write(f"### {current_year}년 {current_month}월")
    
    # 요일 헤더
    days = ['월', '화', '수', '목', '금', '토', '일']
    cols = st.columns(7)
    for i, day in enumerate(days):
        with cols[i]:
            st.write(f"**{day}**")
    
    # 달력 날짜 표시
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.write("")
                else:
                    date_str = f"{current_year}-{current_month:02d}-{day:02d}"
                    
                    if date_str in calendar_data:
                        emotion_data = calendar_data[date_str]
                        color = emotion_data["color"]
                        
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
                            border: 2px solid #ddd;
                            cursor: pointer;
                        " title="{emotion_data['emotion']}: {emotion_data['note']}">
                            <strong>{day}</strong>
                        </div>
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
        "오늘의 마음을 한 문장으로 적어보세요 ✏️",
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
            st.warning("감정을 한 문장으로 적어주세요")

def show_emotion_statistics():
    """감정 통계 표시"""
    calendar_data = load_emotion_calendar()
    
    if not calendar_data:
        st.info("아직 기록된 감정이 없어요. 첫 번째 감정을 기록해보세요!")
        return
    
    # 기본 통계
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
    
    # 감정별 분포
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
    
    for date_str in dates:
        record_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        if (current_date - record_date).days == streak:
            streak += 1
            current_date = record_date
        else:
            break
    
    return streak

# 미래 편지 기능
def load_letters():
    """편지 데이터 로드"""
    if os.path.exists("future_letters.json"):
        with open("future_letters.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {"letters": []}

def save_letters(letters_data):
    """편지 데이터 저장"""
    with open("future_letters.json", "w", encoding="utf-8") as f:
        json.dump(letters_data, f, ensure_ascii=False, indent=2)

def get_new_letters_count():
    """새로 도착한 편지 수 확인"""
    letters_data = load_letters()
    today = date.today()
    
    new_count = 0
    for letter in letters_data["letters"]:
        delivery_date = datetime.strptime(letter["delivery_date"], "%Y-%m-%d").date()
        if delivery_date <= today and not letter.get("is_read", False):
            new_count += 1
    
    return new_count

def future_letter_page():
    """미래 편지 페이지"""
    st.title("💌 미래의 나에게 편지쓰기")
    st.markdown("*현재의 마음을 미래의 나에게 전해보세요*")
    
    tab1, tab2 = st.tabs(["✏️ 편지 쓰기", "📪 편지함"])
    
    with tab1:
        show_simple_letter_writing()
    
    with tab2:
        show_simple_mailbox()

def show_simple_letter_writing():
    """편지 쓰기"""
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
    """편지함"""
    letters_data = load_letters()
    today = date.today()
    
    # 읽을 수 있는 편지들
    deliverable = []
    waiting = []
    
    for letter in letters_data["letters"]:
        delivery_date = datetime.strptime(letter["delivery_date"], "%Y-%m-%d").date()
        if delivery_date <= today:
            deliverable.append(letter)
        else:
            waiting.append(letter)
    
    # 통계
    col1, col2 = st.columns(2)
    with col1:
        unread_count = len([l for l in deliverable if not l["is_read"]])
        st.metric("📬 새 편지", unread_count)
    
    with col2:
        st.metric("⏰ 배송 대기", len(waiting))
    
    # 도착한 편지들
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
        st.info("아직 도착한 편지가 없어요. 첫 번째 편지를 써보세요! ✏️")

# 메인 앱 실행
def main():
    # 사이드바 네비게이션
    st.sidebar.title("🧭 마음의 나침반")
    
    # 새 편지 알림
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
    
    page = st.sidebar.selectbox(
        "메뉴 선택",
        ["🏠 홈", "🎯 감정 탐색", "🌈 감정 달력", "💌 미래 편지"]
    )
    
    # 페이지 라우팅
    if page == "🏠 홈":
        st.session_state.page = "main"
    elif page == "🎯 감정 탐색":
        st.session_state.page = "emotion_exploration"
    elif page == "🌈 감정 달력":
        st.session_state.page = "emotion_calendar"
    elif page == "💌 미래 편지":
        st.session_state.page = "future_letter"
    
    # 페이지 표시
    current_page = st.session_state.get("page", "main")
    
    if current_page == "main":
        main_page()
    elif current_page == "emotion_exploration":
        emotion_exploration_page()
    elif current_page == "emotion_calendar":
        emotion_calendar_page()
    elif current_page == "future_letter":
        future_letter_page()

if __name__ == "__main__":
    main()
    