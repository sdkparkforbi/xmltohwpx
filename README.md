# 📝 Claude XML → HWPX 변환기

> Claude가 생성한 구조화된 XML을 한글(HWPX) 문서로 변환하는 도구

## 🚀 빠른 시작

### 설치 및 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 접속

### Streamlit Cloud 배포

1. GitHub 저장소에 `app.py`, `hwpx_generator.py`, `requirements.txt` 업로드
2. [share.streamlit.io](https://share.streamlit.io)에서 앱 배포
3. URL 공유하여 팀원들과 함께 사용

---

## 📋 사용법

### 1단계: Claude에게 XML 요청

Claude에게 다음과 같이 요청합니다:

```
다음 내용을 HWPX 변환용 XML로 작성해줘:

[변환할 내용]
```

### 2단계: XML을 변환기에 입력

Claude가 생성한 XML을 웹앱에 붙여넣습니다.

### 3단계: HWPX 다운로드

변환 버튼을 누르고 `.hwpx` 파일을 다운로드합니다.

한컴오피스 한/글 2010 이상에서 열 수 있습니다.

---

## 🏷️ XML 스키마

```xml
<document title="문서 제목" author="작성자">

  <!-- 제목 (level: 1=22pt, 2=16pt, 3=13pt) -->
  <heading level="1">대제목</heading>
  <heading level="2">중제목</heading>
  <heading level="3">소제목</heading>

  <!-- 본문 -->
  <paragraph>일반 본문</paragraph>
  <paragraph bold="true">굵은 본문</paragraph>
  <p>줄임형 문단</p>

  <!-- 표 -->
  <table header="true">
    <row>
      <cell>헤더1</cell>
      <cell>헤더2</cell>
    </row>
    <row>
      <cell>데이터1</cell>
      <cell>데이터2</cell>
    </row>
  </table>

  <!-- 목록 -->
  <list>
    <item>순서 없는 항목</item>
  </list>
  <list type="ordered">
    <item>순서 있는 항목</item>
  </list>

  <!-- 기타 -->
  <br/>    <!-- 빈 줄 -->
  <hr/>    <!-- 수평선 -->

</document>
```

### HTML 스타일 태그도 지원

```xml
<ol><li>순서 목록</li></ol>
<ul><li>불릿 목록</li></ul>
<tr><td>표 셀</td><th>헤더 셀</th></tr>
```

---

## 🏗️ HWPX 파일 구조

HWPX는 ZIP + XML 기반 개방형 문서 포맷입니다 (국가표준 KS X 6101):

```
document.hwpx (ZIP)
├── mimetype                    # "application/hwp+zip"
├── version.xml                 # OWPML 버전 정보
├── settings.xml                # 커서 위치 등 설정
├── META-INF/
│   ├── container.xml           # 루트 파일 목록
│   └── manifest.xml            # 전체 파일 매니페스트
├── Contents/
│   ├── content.hpf             # OPF 패키징 (메타데이터, 순서)
│   ├── header.xml              # 글자/문단 모양 정의 (스타일시트)
│   └── section0.xml            # 본문 내용 (문단, 표, 리스트)
└── Preview/
    └── PrvText.txt             # 미리보기 텍스트
```

### 스타일 매핑

| charPr ID | 용도 | 크기 | 스타일 |
|-----------|------|------|--------|
| 0 | 본문 | 10pt | Regular |
| 1 | 제목1 | 22pt | Bold |
| 2 | 제목2 | 16pt | Bold |
| 3 | 제목3 | 13pt | Bold |
| 4 | 굵은 본문 | 10pt | Bold |
| 5 | 표 내용 | 9pt | Regular |
| 6 | 표 헤더 | 9pt | Bold |

---

## 🔧 API 사용 (Python)

```python
from hwpx_generator import generate_hwpx

xml = """<document title="제목">
  <heading level="1">Hello HWPX</heading>
  <paragraph>한글 문서를 프로그래밍으로 생성합니다.</paragraph>
</document>"""

hwpx_bytes = generate_hwpx(xml, title="제목", author="작성자")

with open("output.hwpx", "wb") as f:
    f.write(hwpx_bytes)
```

---

## 📌 참고

- **HWPX 포맷 공식 문서**: [한컴테크 HWPX 구조](https://tech.hancom.com/hwpxformat/)
- **KS X 6101 표준**: [OWPML 표준](https://store.hancom.com/etc/hwpDownload.do)
- **호환성**: 한컴오피스 한/글 2010 이상

---

*피터(Peter) by Claude | 차의과학대학교 AI중심대학 추진위원회*
