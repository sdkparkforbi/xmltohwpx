"""
Claude XML → HWPX 변환기 (Streamlit 웹앱)
==========================================
Claude가 생성한 XML을 한글(HWPX) 문서로 변환하는 도구입니다.
"""

import streamlit as st
import io
from datetime import datetime
from hwpx_generator import generate_hwpx, CLAUDE_XML_SCHEMA

# ============================================================
# 페이지 설정
# ============================================================

st.set_page_config(
    page_title="Claude XML → HWPX 변환기",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2em;
        font-weight: bold;
        color: #1a1a2e;
        margin-bottom: 0.2em;
    }
    .sub-header {
        font-size: 1.1em;
        color: #666;
        margin-bottom: 1.5em;
    }
    .stTextArea > div > div > textarea {
        font-family: 'D2Coding', 'Consolas', 'Monaco', monospace;
        font-size: 13px;
        line-height: 1.5;
    }
    .info-box {
        background-color: #f0f4ff;
        border-left: 4px solid #4361ee;
        padding: 12px 16px;
        margin: 12px 0;
        border-radius: 0 8px 8px 0;
    }
    .success-box {
        background-color: #f0fff4;
        border-left: 4px solid #2ecc71;
        padding: 12px 16px;
        margin: 12px 0;
        border-radius: 0 8px 8px 0;
    }
    .schema-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 16px;
        font-family: 'D2Coding', 'Consolas', monospace;
        font-size: 12px;
        white-space: pre-wrap;
    }
    div[data-testid="stDownloadButton"] button {
        background-color: #4361ee;
        color: white;
        font-size: 16px;
        padding: 12px 28px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# 사이드바 - 가이드
# ============================================================

with st.sidebar:
    st.markdown("## 📖 사용 가이드")
    
    st.markdown("""
    ### 1단계: Claude에게 XML 요청
    Claude에게 아래와 같이 요청하세요:
    
    > *"아래 내용을 HWPX 변환용 XML로 작성해줘"*
    """)
    
    st.markdown("### 2단계: XML 붙여넣기")
    st.markdown("Claude가 생성한 XML을 왼쪽 입력창에 붙여넣으세요.")
    
    st.markdown("### 3단계: 변환 및 다운로드")
    st.markdown("변환 버튼을 누르고 `.hwpx` 파일을 다운로드하세요.")
    
    st.divider()
    
    st.markdown("## 🏷️ 지원 태그")
    
    tag_data = {
        "`<heading level='1~3'>`": "제목 (22pt, 16pt, 13pt)",
        "`<paragraph>` / `<p>`": "본문 문단 (10pt)",
        "`<paragraph bold='true'>`": "굵은 본문",
        "`<table header='true'>`": "표 (헤더 행 포함)",
        "`<row>` / `<cell>`": "표 행/셀",
        "`<list>` / `<ul>`": "순서 없는 목록",
        "`<list type='ordered'>` / `<ol>`": "순서 있는 목록",
        "`<br/>`": "빈 줄",
        "`<hr/>`": "수평선",
    }
    
    for tag, desc in tag_data.items():
        st.markdown(f"- {tag}: {desc}")
    
    st.divider()
    st.markdown("### ⚙️ 문서 설정")
    
    paper_size = st.selectbox("용지 크기", ["A4 (210×297mm)"], index=0)
    font_family = st.selectbox("기본 글꼴", ["함초롬돋움", "함초롬바탕"], index=0)
    
    st.divider()
    st.caption("🤖 Claude XML → HWPX Generator v1.0")
    st.caption("피터(Peter) by Claude | 2026")


# ============================================================
# 메인 영역
# ============================================================

st.markdown('<div class="main-header">📝 Claude XML → HWPX 변환기</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Claude가 생성한 XML을 한글(HWPX) 문서로 변환합니다</div>', unsafe_allow_html=True)

# 문서 정보 입력
col_title, col_author = st.columns(2)
with col_title:
    doc_title = st.text_input("📄 문서 제목", value="", placeholder="예: AI 중심대학 연구개발계획서")
with col_author:
    doc_author = st.text_input("✍️ 작성자", value="", placeholder="예: 차의과학대학교")


# 탭: 직접 입력 / 예시 / 스키마 가이드
tab_input, tab_example, tab_schema = st.tabs(["📝 XML 입력", "📋 예시 보기", "📖 스키마 가이드"])

# ---- 예시 XML ----
EXAMPLE_XML = """<document title="AI 중심대학 추진 현황 보고서" author="차의과학대학교">

  <heading level="1">I. AI 중심대학 추진 현황</heading>
  
  <paragraph>차의과학대학교는 Bio Healthcare AI 특화 전략을 중심으로 AI 중심대학 사업을 추진하고 있습니다. 본 보고서에서는 현재까지의 추진 현황과 향후 계획을 정리합니다.</paragraph>

  <heading level="2">1. 주요 성과지표</heading>
  
  <table header="true">
    <row>
      <cell>성과지표</cell>
      <cell>현재 수준</cell>
      <cell>2030 목표</cell>
      <cell>비고</cell>
    </row>
    <row>
      <cell>AI 교과비율</cell>
      <cell>5.7%</cell>
      <cell>20%</cell>
      <cell>전교 대상</cell>
    </row>
    <row>
      <cell>AI 전임교원</cell>
      <cell>37명</cell>
      <cell>50명</cell>
      <cell>신규 채용 포함</cell>
    </row>
    <row>
      <cell>AI Ambassador</cell>
      <cell>11명</cell>
      <cell>20명</cell>
      <cell>비전공 교수 양성</cell>
    </row>
    <row>
      <cell>Fast Track 학생</cell>
      <cell>-</cell>
      <cell>40명/년</cell>
      <cell>신설 예정</cell>
    </row>
  </table>

  <heading level="2">2. 추진 전략</heading>
  
  <paragraph>차의과학대학교만의 차별화된 전략은 다음과 같습니다:</paragraph>
  
  <list>
    <item>의료 AI 특화: CHA 병원 네트워크(7개국 96개 센터) 연계 실전 데이터 기반 교육</item>
    <item>난임 AI 연구: 세계 최고 수준의 난임 치료 데이터 활용 AI 모델 개발</item>
    <item>줄기세포·재생의학 AI: 차별화된 바이오 의료 연구 인프라 활용</item>
    <item>정밀의료 AI: 맞춤형 진단·치료를 위한 AI 기술 개발</item>
  </list>

  <heading level="2">3. 교육과정 개편 방향</heading>

  <heading level="3">가. 전교적 AI 리터러시 강화</heading>
  <paragraph>차이름교양대학을 중심으로 전체 학생 대상 AI 기초 교육을 확대합니다. 현재 5.7%인 AI 교과 비율을 2030년까지 20%로 상향 조정할 계획입니다.</paragraph>

  <heading level="3">나. Fast Track 프로그램 신설</heading>
  <paragraph>매년 40명의 우수 학생을 선발하여 집중적인 AI 교육을 제공하는 Fast Track 프로그램을 신설합니다.</paragraph>
  
  <list type="ordered">
    <item>1학년: AI 기초 및 프로그래밍</item>
    <item>2학년: 머신러닝 및 데이터 사이언스</item>
    <item>3학년: Bio Healthcare AI 응용</item>
    <item>4학년: 캡스톤 프로젝트 및 현장 실습</item>
  </list>

  <hr/>

  <heading level="2">4. 향후 일정</heading>
  
  <table header="true">
    <row>
      <cell>시기</cell>
      <cell>주요 내용</cell>
    </row>
    <row>
      <cell>2026.03</cell>
      <cell>AI 중심대학 신청서 제출</cell>
    </row>
    <row>
      <cell>2026.06</cell>
      <cell>선정 결과 발표</cell>
    </row>
    <row>
      <cell>2026.09</cell>
      <cell>1차년도 사업 착수</cell>
    </row>
    <row>
      <cell>2027.03</cell>
      <cell>Fast Track 1기 입학</cell>
    </row>
  </table>

  <br/>
  <paragraph bold="true">본 보고서는 AI 중심대학 추진위원회의 검토를 거쳐 확정되었습니다.</paragraph>

</document>"""


with tab_input:
    xml_input = st.text_area(
        "Claude가 생성한 XML을 붙여넣으세요:",
        height=500,
        placeholder='<document title="문서 제목">\n  <heading level="1">제목</heading>\n  <paragraph>본문 내용...</paragraph>\n</document>',
        key="xml_input"
    )

with tab_example:
    st.code(EXAMPLE_XML, language="xml")
    if st.button("📋 이 예시로 변환하기", type="secondary"):
        st.session_state.xml_input = EXAMPLE_XML
        st.rerun()

with tab_schema:
    st.markdown("""
    ### Claude에게 요청할 때 사용할 프롬프트
    
    다음 프롬프트를 Claude에게 전달하면 변환 가능한 XML을 생성합니다:
    """)
    
    prompt_text = """다음 내용을 HWPX 변환용 XML로 작성해줘. 아래 스키마를 따라야 해:

- <document title="제목" author="작성자">로 감싸기
- <heading level="1~3">: 제목 (1=대, 2=중, 3=소)
- <paragraph>: 본문 / <paragraph bold="true">: 굵은 본문
- <table header="true"> + <row> + <cell>: 표
- <list> + <item>: 순서 없는 목록 / <list type="ordered">: 순서 있는 목록
- <br/>: 빈 줄 / <hr/>: 수평선

[여기에 변환할 내용을 작성]"""
    
    st.code(prompt_text, language="text")
    
    st.markdown("### 지원 태그 전체 목록")
    st.code(CLAUDE_XML_SCHEMA, language="text")


# ============================================================
# 변환 버튼
# ============================================================

st.divider()

col_btn, col_status = st.columns([1, 3])

with col_btn:
    convert_btn = st.button("🔄 HWPX로 변환", type="primary", use_container_width=True)

if convert_btn:
    xml_to_convert = xml_input.strip() if xml_input else ""
    
    if not xml_to_convert:
        st.error("⚠️ XML을 입력해주세요.")
    else:
        try:
            with st.spinner("변환 중..."):
                # 제목/작성자 추출 (입력 필드 우선, 없으면 XML에서)
                title = doc_title.strip() if doc_title.strip() else "문서"
                author = doc_author.strip() if doc_author.strip() else "Claude"
                
                # XML에서 title/author 추출 시도
                import xml.etree.ElementTree as ET
                try:
                    root = ET.fromstring(xml_to_convert)
                    if not doc_title.strip() and root.get("title"):
                        title = root.get("title")
                    if not doc_author.strip() and root.get("author"):
                        author = root.get("author")
                except:
                    pass
                
                # HWPX 생성
                hwpx_data = generate_hwpx(xml_to_convert, title=title, author=author)
            
            # 파일명 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = title.replace(" ", "_").replace("/", "_")[:30]
            filename = f"{safe_title}_{timestamp}.hwpx"
            
            st.markdown(f"""
            <div class="success-box">
                ✅ <strong>변환 완료!</strong><br>
                📄 문서: {title} | ✍️ 작성자: {author} | 📦 크기: {len(hwpx_data):,} bytes
            </div>
            """, unsafe_allow_html=True)
            
            # 다운로드 버튼
            st.download_button(
                label=f"📥 {filename} 다운로드",
                data=hwpx_data,
                file_name=filename,
                mime="application/hwp+zip",
                type="primary",
                use_container_width=True
            )
            
            # HWPX 내부 구조 미리보기
            with st.expander("🔍 HWPX 내부 구조 확인"):
                import zipfile
                buf = io.BytesIO(hwpx_data)
                with zipfile.ZipFile(buf, 'r') as zf:
                    for name in zf.namelist():
                        info = zf.getinfo(name)
                        st.text(f"  {name:45s} {info.file_size:>8,} bytes")
                    
                    st.markdown("---")
                    st.markdown("**section0.xml (본문):**")
                    section = zf.read("Contents/section0.xml").decode("utf-8")
                    st.code(section[:5000], language="xml")
            
        except ValueError as e:
            st.error(f"❌ 변환 오류: {e}")
        except Exception as e:
            st.error(f"❌ 예상치 못한 오류: {e}")
            import traceback
            st.code(traceback.format_exc())


# ============================================================
# 하단 정보
# ============================================================

st.divider()

st.markdown("""
<div style="text-align:center; color:#888; font-size:0.9em;">
    <p>💡 <strong>팁</strong>: 생성된 .hwpx 파일은 한컴오피스 한/글 2010 이상에서 열 수 있습니다.</p>
    <p>HWPX는 국가표준(KS X 6101) OWPML 기반 개방형 문서 포맷입니다.</p>
</div>
""", unsafe_allow_html=True)
