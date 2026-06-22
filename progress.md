# progress.md — 세션 체크포인트

> 새 세션 시작 시 이 파일을 먼저 읽으면 컨텍스트를 빠르게 복원할 수 있습니다.

---

## 현재 상태 (2026-06-19 최종 — 세션 5)

**프로젝트 파일:**
```
MCE-Setup-Guide/
  index.html       — MCE 구축 가이드 (범용 레퍼런스, ~1,980줄)
  dashboard.html   — 개인 업무 대시보드 (IndexedDB 기반, ~1,600줄)
  README.md        — 프로젝트 설명 + 컴포넌트 가이드
  progress.md      — 이 파일
  docs/
    contact-builder-de.html          — Contact Builder / DE 레퍼런스 (한국어)
    marketing-cloud-intelligence.html
    marketing-cloud-personalization.html
    einstein-analytics.html
```

---

## index.html 완료 현황

### Step 구성 (총 17단계, 네비게이션 배지 0~16)

| 배지 | ID | 제목 | 그룹 |
|---|---|---|---|
| 0 | s0 | 사전 준비 | 준비 |
| 1 | s1 | 계정 / BU 설정 | 계정 설정 |
| 2 | s_ftp | Enhanced FTP 설정 | 계정 설정 |
| 3 | s2 | 사용자 권한 설정 | 계정 설정 |
| 4 | s3 | Data Extension 설계 | 데이터 설계 |
| 5 | s4 | Contact Builder 설정 | 데이터 설계 |
| 6 | s5 | Sender Profile | 발송 설정 |
| 7 | s6 | Send Classification | 발송 설정 |
| 8 | s_ipw | IP Warming | 발송 설정 |
| 9 | s_cb | Content Builder | 콘텐츠 |
| 10 | s_cp | CloudPages | 콘텐츠 |
| 11 | s7 | Automation Studio | 자동화 |
| 12 | s8 | Journey Builder | 자동화 |
| 13 | s_tx | Transactional 발송 | 자동화 |
| 14 | s_dm | 데이터 관리 | 자동화 |
| 15 | s9 | 발송 테스트 | 검수 & 인계 |
| 16 | s10 | 운영 인계 | 검수 & 인계 |

### 완료된 기능
- [x] 17단계 사이드바 네비게이션 (그룹별 구분선)
- [x] 단계별 체크리스트 (클릭 완료 처리)
- [x] 전체/단계별 진행률 바
- [x] 네비게이션 상태 아이콘 (⬜/🔵/✅)
- [x] 4종 callout 박스 (warning/danger/tip/note)
- [x] 코드블록 복사 버튼
- [x] data-table 컴포넌트
- [x] 키워드 검색
- [x] 다크모드
- [x] 사이드바 하단 대시보드 링크 (→ dashboard.html)
- [x] s3, s4에서 contact-builder-de.html 문서 링크
- [x] 정확한 doc-link 2개만 유지 (distributing-marketing.html, einstein-analytics.html)

### CSS 변수 (index.html 기준, docs/*.html과 다름)
```css
--blue:#378ADD; --blue-bg:#E6F1FB; --blue-text:#185FA5;
--green:#1D9E75; --green-bg:#E1F5EE;
--amber:#BA7517; --amber-bg:#FAEEDA;
--red:#A32D2D; --red-bg:#FCEBEB;
--bg:#fff; --bg2:#f8f8f7; --bg3:#f2f2f0;
--text:#1a1a1a; --text2:#555; --text3:#999;
--border:rgba(0,0,0,.08); --border2:rgba(0,0,0,.14);
```
폰트: `system-ui, -apple-system, 'Noto Sans KR'` (docs/는 Pretendard)

---

## dashboard.html 완료 현황

### 아키텍처
- **저장소:** IndexedDB `MCEDashboardDB` v4
- **스키마:** `projects` / `communications` / `files` / `issues` / `notes` / `threads` / `todos`
- **프로젝트:** 단일 고객사 (`id: 'default'`), 멀티 프로젝트 확장 가능 구조
- **백업:** JSON 내보내기/가져오기 (파일 바이너리 제외, todos 포함)

### 완료된 기능

**헤더**
- [x] 고객사명, 기간, 담당자, MCE 에디션 표시 + ✏️ 편집
- [x] 다크/라이트 모드 수동 토글 (🌙/☀️, localStorage 유지)
- [x] MCE 가이드 링크, 내보내기/가져오기

**📊 진행현황 탭**
- [x] Step 0~16 그룹별 체크리스트
- [x] ⬜→🔵→✅ 3단계 클릭 토글
- [x] 전체 진행률 바
- [x] 각 스텝 "가이드 →" 링크 (index.html 해당 섹션)

**💬 커뮤니케이션 탭**
- [x] 날짜/방식/참석자/내용/결정사항 입력
- [x] 마크다운 서식 툴바 + 실시간 미리보기 (좌우 분할)
- [x] 카드 목록 (날짜 역순), 내용 검색
- [x] 카드 헤더 클릭 → 우측 스레드 패널

**📎 파일 탭**
- [x] 드래그&드롭 업로드 → ArrayBuffer → IndexedDB
- [x] 카테고리 필터 (요건정의/계약서/회의록/기획서/산출물/기타)
- [x] 다운로드 (Blob URL), 삭제

**⚠️ 이슈 탭**
- [x] 우선순위 (높음/보통/낮음), 상태 (오픈/진행중/완료), 카테고리
- [x] 마크다운 서식 툴바 + 실시간 미리보기
- [x] 상태 인라인 변경 (select)
- [x] 이슈 제목 클릭 → 우측 스레드 패널

**📝 노트 탭**
- [x] 노트 카드 목록, 검색, 추가/수정/삭제
- [x] 마크다운 서식 툴바 + 실시간 미리보기
- [x] 마크다운 렌더링 (H1/H2, 굵게, 기울임, 목록, 체크박스, 구분선, 코드)
- [x] 카드에서 체크박스 직접 클릭 토글 (IndexedDB 즉시 반영)
- [x] 노트 제목 클릭 → 우측 스레드 패널

**스레드 패널 (공통)**
- [x] 커뮤니케이션/이슈/노트 카드 클릭 시 우측 패널 슬라이드 오픈
- [x] 원본 내용 상단 표시 + 스레드 메시지 목록
- [x] 스레드 입력 (Ctrl+Enter 전송), 삭제
- [x] 선택된 카드 파란 테두리 강조

**📅 할일 탭**
- [x] 월 달력 (왼쪽): prev/next 달 네비게이션, 오늘 날짜 강조, 선택 날짜 파란 배경
- [x] 할일 있는 날짜에 파란 점(dot) 표시
- [x] 달력 날짜 클릭 → 오른쪽 해당 날짜 할일 목록으로 전환
- [x] 빠른 추가: 텍스트 입력 + Enter/버튼 (시간·담당자·마감일·메모 선택 입력)
- [x] [▾ 상세] 토글로 optional 필드 펼침/접기
- [x] 체크박스 클릭으로 완료/미완료 전환 (취소선 스타일)
- [x] ✏️ 수정 모달 (전 필드 편집), 🗑️ 삭제
- [x] 내보내기/가져오기 JSON에 todos 배열 포함

**todos 스키마:**
```javascript
{ id, projectId, date:'YYYY-MM-DD', content, time, assignee, deadline, memo, done:false, createdAt }
```

---

## 다음 세션 시작 프롬프트

```
README.md와 progress.md 읽고 현재 상태 파악해줘.
오늘 작업 목표: [여기에 작업 내용]
```

---

## 세션 로그

| 날짜 | 작업 내용 |
|------|-----------|
| 2026-06-19 세션 1 | 초기 구조 생성 (10단계) |
| 2026-06-19 세션 2 | 17단계 확장, s_ftp/s_cb/s_ipw/s_cp/s_tx/s_dm 추가, 스타일 정규화, doc-link 정리 |
| 2026-06-19 세션 3 | contact-builder-de.html 신규 생성 (DE/Contact Builder 한국어 레퍼런스) |
| 2026-06-19 세션 4 | dashboard.html 전체 구현 (IndexedDB, 5탭, 마크다운, 스레드 패널) |
| 2026-06-19 세션 5 | dashboard.html — 📅 할일 탭 추가 (달력+날짜별 할일, DB v4) |
