# MCE 구축 가이드 + 업무 대시보드

Salesforce Marketing Cloud Engagement(MCE) 구축 전 과정을 정리한 레퍼런스 가이드와, 고객사별 프로젝트를 관리하는 개인 업무 대시보드로 구성됩니다.

---

## 파일 구조

```
MCE-Setup-Guide/
  index.html         — MCE 구축 가이드 (범용 레퍼런스, Step 0~16)
  dashboard.html     — 개인 업무 대시보드 (IndexedDB, 브라우저 내 저장)
  README.md          — 이 파일
  progress.md        — Claude Code 세션 간 이어가기용 체크포인트
  docs/
    contact-builder-de.html           — Contact Builder / DE 레퍼런스 (한국어)
    marketing-cloud-intelligence.html
    marketing-cloud-personalization.html
    einstein-analytics.html
```

---

## index.html — MCE 구축 가이드

### 개요
모든 고객사에 공통으로 사용하는 MCE 구축 단계별 레퍼런스 문서입니다.  
브라우저에서 바로 열면 사이드바 네비게이션 + 체크리스트 + 검색이 동작합니다.

### 17단계 구성 (Step 0~16)

| 그룹 | Step | 내용 |
|---|---|---|
| 준비 | 0 | 사전 준비 |
| 계정 설정 | 1~3 | 계정/BU, Enhanced FTP, 사용자 권한 |
| 데이터 설계 | 4~5 | Data Extension 설계, Contact Builder |
| 발송 설정 | 6~8 | Sender Profile, Send Classification, IP Warming |
| 콘텐츠 | 9~10 | Content Builder, CloudPages |
| 자동화 | 11~14 | Automation Studio, Journey Builder, Transactional 발송, 데이터 관리 |
| 검수 & 인계 | 15~16 | 발송 테스트, 운영 인계 |

### 주요 기능
- 단계별 체크리스트 (클릭 완료 처리, 진행률 바)
- 4종 callout 박스 (warning / danger / tip / note)
- 코드블록 복사 버튼, data-table 컴포넌트
- 키워드 검색, 다크모드
- 사이드바 하단 → dashboard.html 바로가기

### 컴포넌트 패턴

**체크리스트 항목:**
```html
<div class="check-item" onclick="toggle(this)">
  <input type="checkbox"><label>항목 내용</label>
</div>
```

**Callout 박스:**
```html
<div class="callout warning">   <!-- warning / danger / tip / note -->
  <span class="callout-icon">⚠️</span>
  <div><strong>제목:</strong> 내용</div>
</div>
```

**코드블록:**
```html
<div class="code-block">
  <div class="code-header">
    <span class="code-lang">SQL</span>
    <button class="copy-btn" onclick="copyCode(this)">복사</button>
  </div>
  <div class="code-body">SELECT * FROM _Sent</div>
</div>
```

**테이블:**
```html
<table class="data-table">
  <thead><tr><th>필드명</th><th>타입</th><th>구분</th></tr></thead>
  <tbody>
    <tr>
      <td>ContactKey</td><td>Text(36)</td>
      <td><span class="tag required">필수</span></td>
    </tr>
  </tbody>
</table>
```

**Block / Block-title (내용 그룹):**
```html
<div class="block">
  <div class="block-title">그룹 제목</div>
  <!-- 체크리스트, 테이블 등 -->
</div>
```

### 새 Step 추가 시 수정 위치 3곳

1. **사이드바 nav-item** (HTML)
2. **메인 section** (HTML, id=`sN`)
3. **SECTIONS 객체** (JS)

```js
const SECTIONS = {
  // ...기존...
  sN: { title: '새 단계명', group: '그룹명' }
};
```

### CSS 변수 (index.html 전용)
```css
--blue:#378ADD;  --blue-bg:#E6F1FB;  --blue-text:#185FA5;
--green:#1D9E75; --green-bg:#E1F5EE;
--amber:#BA7517; --amber-bg:#FAEEDA;
--red:#A32D2D;   --red-bg:#FCEBEB;
--bg:#fff; --bg2:#f8f8f7; --bg3:#f2f2f0;
--text:#1a1a1a; --text2:#555; --text3:#999;
```
> ⚠️ `docs/*.html`은 Pretendard + 다른 CSS 변수명 사용 — 혼용 금지

---

## dashboard.html — 업무 대시보드

### 개요
현재 진행 중인 MCE 구축 고객사 프로젝트를 관리하는 개인 업무 도구입니다.  
데이터는 **브라우저 IndexedDB에 저장**되며 외부 서버가 필요 없습니다.

### 저장 구조 (IndexedDB `MCEDashboardDB` v3)

| 스토어 | 키 | 용도 |
|---|---|---|
| projects | id | 프로젝트 정보 (고객사, 기간, 담당자, 에디션) |
| communications | id (idx: projectId) | 커뮤니케이션 이력 |
| files | id (idx: projectId) | 첨부파일 (ArrayBuffer) |
| issues | id (idx: projectId) | 이슈 트래커 |
| notes | id (idx: projectId) | 메모 카드 |
| threads | id (idx: parentId) | 카드별 스레드 메시지 |

### 주요 기능

| 탭 | 기능 |
|---|---|
| 📊 진행현황 | Step 0~16 상태 토글 (⬜/🔵/✅), 진행률 바, 가이드 링크 |
| 💬 커뮤니케이션 | 날짜/방식/참석자/내용/결정사항, 검색, 마크다운 편집 |
| 📎 파일 | 드래그 업로드, 카테고리 필터, 다운로드 |
| ⚠️ 이슈 | 우선순위/상태/카테고리, 인라인 상태 변경, 마크다운 편집 |
| 📝 노트 | 카드 목록, 검색, 마크다운 편집, 체크박스 인터랙션 |

**스레드 패널:** 커뮤니케이션/이슈/노트 카드를 클릭하면 우측에 Slack 스레드 형식의 패널이 열립니다.

**마크다운 지원 문법:**
```
# 제목 1    ## 제목 2
**굵게**    *기울임*    `코드`
- 목록      1. 번호 목록
- [ ] 체크박스    - [x] 완료
---  (구분선)
```

### 백업/복원
- **내보내기:** JSON 파일 다운로드 (파일 첨부 바이너리 제외)
- **가져오기:** JSON 파일 업로드로 복원 (파일 첨부는 재업로드 필요)

---

## Claude Code 작업 가이드

### 세션 시작 프롬프트
```
README.md와 progress.md 읽고 현재 상태 파악해줘.
오늘 작업 목표: [여기에 작업 내용]
```

### 작업 규칙
1. `index.html` / `dashboard.html` 모두 단일 파일 — 외부 CSS/JS 분리 금지
2. `docs/*.html` 은 Pretendard + 별도 CSS 변수 사용 (index.html 변수와 혼용 금지)
3. IndexedDB 스키마 변경 시 `DB_VERSION` 숫자 올리기 (현재 v3)
4. `dashboard.html` 수정 후 DB 버전을 올릴 경우 `onupgradeneeded` 마이그레이션 로직 확인

---

## 작업 로그

| 날짜 | 작업 내용 |
|------|-----------|
| 2026-06-19 | 초기 구조 생성 (10단계) |
| 2026-06-19 | 17단계로 확장, 스타일 정규화, doc-link 정리 |
| 2026-06-19 | `docs/contact-builder-de.html` 신규 생성 |
| 2026-06-19 | `dashboard.html` 전체 구현 (IndexedDB, 5탭, 마크다운, 스레드) |
