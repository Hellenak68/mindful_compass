# 🧭 마음의 나침반 (Mindful Compass)

개인 맞춤형 감정 관리 웹 애플리케이션

## 🌟 주요 기능

### 🎯 감정 탐색하기
- 무기력감, 불안감 등 어려운 감정을 3단계 대화로 탐색
- 개인화된 통찰과 맞춤형 콘텐츠 추천
- 감정 기록 저장으로 성장 과정 추적

### 🌈 감정 색깔 달력
- 매일의 감정을 색깔로 시각화
- 감정 패턴 분석과 연속 기록 확인
- 월별 감정 통계 제공

### 💌 미래 편지 쓰기
- 현재의 나에서 미래의 나에게 편지 전송
- 1주일~1년 후 받을 수 있는 시간 여행 기능
- 과거 편지를 통한 성장 확인

### 📊 감정 통계
- 전체 기록 분석
- 가장 많은 감정 패턴 확인
- 연속 기록 달성 현황

## 🚀 라이브 데모

**웹사이트:** [마음의 나침반 체험하기](https://mindful-compass.streamlit.app)

> 💡 **팁:** GitHub에 push할 때마다 자동으로 업데이트됩니다!

## 🛠️ 로컬 실행 방법

### 1. 저장소 클론
```bash
git clone https://github.com/Hellenak68/mindful_compass.git
cd mindful_compass
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 앱 실행
```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속하세요.

## 📁 프로젝트 구조

```
mindful_compass/
├── app.py                 # 메인 애플리케이션
├── requirements.txt       # Python 의존성
├── data/                  # 앱 데이터 폴더
│   ├── insights.json     # 감정 통찰 데이터
│   └── contents.json     # 추천 콘텐츠 데이터
├── emotion_calendar.json  # 감정 달력 데이터
├── future_letters.json   # 미래 편지 데이터
├── records.txt           # 감정 기록 텍스트
├── tests/                # 테스트 파일
├── .github/workflows/    # CI/CD 설정
└── README.md            # 이 파일
```

## 🧪 개발자를 위한 정보

### 테스트 실행
```bash
pytest tests/
```

### 코드 스타일 검사
```bash
flake8 .
```

### CI/CD
- GitHub Actions를 통한 자동 테스트
- Streamlit Community Cloud 자동 배포
- 매 push마다 린트, 테스트, 배포 자동 실행

## 🎨 기술 스택

- **Frontend**: Streamlit (Python 웹 프레임워크)
- **Data Storage**: JSON/TXT 파일 (로컬 저장)
- **Styling**: Custom CSS + Streamlit 컴포넌트
- **Deployment**: Streamlit Community Cloud
- **CI/CD**: GitHub Actions

## 📝 사용법

1. **홈페이지**에서 원하는 기능 선택
2. **감정 탐색**: 현재 감정 상태를 3단계로 탐색하고 맞춤 조언 받기
3. **감정 달력**: 매일의 감정을 색깔로 기록하고 패턴 확인
4. **미래 편지**: 미래의 나에게 편지 쓰고 정해진 날짜에 받기
5. **사이드바 메뉴**로 언제든 페이지 이동 가능

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 Apache 2.0 라이선스 하에 배포됩니다.

## 📞 문의

프로젝트에 대한 질문이나 제안이 있으시면 GitHub Issues를 통해 연락주세요.

---

**마음의 나침반**과 함께 더 건강한 감정 관리를 시작해보세요! 🌱
