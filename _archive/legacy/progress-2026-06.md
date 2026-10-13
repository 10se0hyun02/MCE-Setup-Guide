# progress.md — 세션 체크포인트

> 새 세션 시작 시 이 파일을 먼저 읽으면 컨텍스트를 빠르게 복원할 수 있습니다.

---

## 현재 상태 (2026-06-22 최종 — 세션 10)

**프로젝트 파일:**
```
MCE-Setup-Guide/
  index.html                    — MCE 구축 가이드 (범용 레퍼런스, Step 0~16)
  dashboard.html                — 개인 업무 대시보드 (IndexedDB v6, ~3,100줄)
  README.md                     — 프로젝트 설명 + 컴포넌트 가이드
  progress.md                   — 이 파일
  agent-briefing-routine.md     — 매일 08:00 브리핑 루틴
  agent-weekly-routine.md       — 매주 금 18:00 주간 분석 루틴
  agent-weekly-report-routine.md — 매주 금 17:00 고객사 보고서 루틴
  agent-meeting-routine.md      — 회의 후 수동 실행 루틴
  gmail-sync-routine.md         — Gmail 동기화 보조 루틴
  docs/
    contact-builder-de.html
    marketing-cloud-intelligence.html
    marketing-cloud-personalization.html
    einstein-analytics.html
```

---

## dashboard.html 완료 현황

### 아키텍처
- **저장소:** IndexedDB `MCEDashboardDB` **v6**
- **스키마:** `projects` / `communications` / `files` / `issues` / `notes` / `threads` / `todos` / `settings` / `meetings`
- **테마:** Tokyo Night (`:root` 라이트 + `@media dark` + `[data-theme="dark"]` / `[data-theme="light"]` 명시 토글)

### 탭 구조 (2-level nav)
```
메인: [🤖 브리핑] | — | [📊 MCE 구축 진행현황] | — | [📋 업무 기록]
업무 기록 하위: [📅 할일] [💬 커뮤니케이션] [⚠️ 이슈] [📝 노트] [🎙️ 회의록] [📎 파일]
```
- `WORKSPACE_TABS = new Set(['meeting','comm','files','issues','notes','todo'])`
- `renderTab()` 에서 서브탭 show/hide + 부모 '업무 기록' active 처리

### 완료된 기능

**🤖 브리핑 탭**
- [x] `briefing-data.json` / `weekly-data.json` File System Access API로 읽기
- [x] 2컬럼 그리드: 오늘 할일 + 이슈 / 진행현황 요약 + 주간 요약
- [x] [📥 회의록 가져오기] → `import-queue.json` 읽기 → 미리보기 모달 → IndexedDB 일괄 추가

**📊 MCE 구축 진행현황 탭**
- [x] Step 0~16 그룹별 체크리스트, ⬜→🔵→✅ 3단계 토글
- [x] 전체 진행률 바, 각 스텝 "가이드 →" 링크

**💬 커뮤니케이션 탭**
- [x] 카드/타임라인 뷰 토글
- [x] type별 색·아이콘 (이메일/전화/화상/대면/메시지)
- [x] Gmail 동기화 import (`gmail-sync.json` 읽어 미리보기 후 추가)
- [x] 마크다운 편집, 스레드 패널

**📎 파일 탭**
- [x] 드래그&드롭 업로드, 카테고리 필터+색, 파일명 검색, 이름 변경, 다운로드/삭제

**⚠️ 이슈 탭**
- [x] priority(high/medium/low) 색 구분, 인라인 상태 변경, 마크다운, 스레드

**📝 노트 탭**
- [x] 마크다운 렌더링, 체크박스 직접 토글, 스레드

**🎙️ 회의록 탭**
- [x] 좌측 목록 + 우측 에디터, 1.2초 자동저장 (IndexedDB `meetings`)
- [x] [📤 Agent 추출] → `meeting-draft.txt` → Claude 루틴 → `import-queue.json`

**📅 할일 탭**
- [x] Daily / Weekly / Monthly 3뷰
- [x] **미완료 이월:** 오늘 기준 과거 미완료 → 상단 amber 섹션, `originalDate` 보존
  - `rolloverTodo(id)`, `rolloverAllTodos()`, `rolloverTodoToDate(id, targetDate)`, `restoreTodo(id)`
- [x] **Weekly 요일별 색상:** 월=blue, 화=green, 수=amber, 목=red, 금=purple
  - `day-col-0`~`day-col-4` 클래스, `.todo-week-dow` 텍스트 + 카드 왼쪽 보더
  - 이월 카드(`.rolled-card`)는 amber 유지 (`:not(.rolled-card)` 조건)
- [x] **Weekly 양방향 드래그:** 컬럼↔이월섹션, JSON payload `{id, dir:'to-col'|'to-rollover'}`
- [x] `isCurrentWeek` 반드시 `colsHtml` 선언 앞에 위치 (const TDZ 버그 방지)

**공통**
- [x] 전체 검색 `Ctrl+K` / 🔍 버튼
- [x] `⚙️ Agent` 버튼 → 폴더 선택 → `syncDir` handle IndexedDB 저장
- [x] 탭 전환 시 `autoSaveDashboard()` → `dashboard-data.json` 자동 갱신
- [x] `showToast(msg)` 토스트 알림

### CSS 변수 (`dashboard.html` 전용 — Tokyo Night)
```css
/* 라이트 */
--blue:#2e7de9; --blue-bg:#dce8fb;
--green:#587539; --green-bg:#ddeec8;
--amber:#8c6c3e; --amber-bg:#f0e4cc;
--red:#c64343;   --red-bg:#f9dede;
--purple:#7847d4; --purple-bg:#ede5fa;   ← 2026-06-22 추가
/* 다크 */
--blue:#7aa2f7; --blue-bg:#1a2744;
--green:#9ece6a; --green-bg:#1a2b14;
--amber:#e0af68; --amber-bg:#2b200f;
--red:#f7768e;   --red-bg:#2b1520;
--purple:#bb9af7; --purple-bg:#2d1f5e;  ← 2026-06-22 추가
```

### Agent 동기화 파일 (`.gitignore` 적용)
| 파일 | 생성 주체 |
|------|-----------|
| `dashboard-data.json` | 대시보드 자동 저장 (탭 전환 시) |
| `briefing-data.json` | 매일 08:00 루틴 |
| `weekly-data.json` | 매주 금 18:00 루틴 |
| `meeting-draft.txt` | 회의록 탭 [Agent 추출] 버튼 |
| `import-queue.json` | 회의/Gmail 루틴 출력 → 브리핑 탭에서 가져오기 |

---

## index.html 완료 현황

### Step 구성 (총 17단계)
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

---

## ⚠️ search-index.json 갱신 규칙

`docs/*.html`을 신규 추가하거나 내용 수정 후 **반드시** 실행:

```bash
python generate-search-index.py
```

갱신 필요 조건: docs/*.html 신규 추가 / 내용 수정 / 섹션 id 변경
불필요 조건: index.html 수정 / dashboard.html 수정

---

## 다음 보완 후보
1. **Claude API 직접 연동** — API 키 Agent 설정 모달에 저장, 회의록 탭에서 직접 파싱
2. 커뮤니케이션 팔로업 날짜
3. D-day 배지 / 마감 경고
4. 일일 업무 로그
5. claude.ai `/schedule` 3개 루틴 등록 (프로젝트 시작 전날)

## 가이드 심화 현황 (2026-06-23~)

### 완료
- [x] `docs/ampscript-guide.html` — 변수/조건/반복/DE조회/문자열/날짜/수학 함수 + 실전 패턴 7종
  - 인삿말 개인화, 등급별 분기, 구매이력 테이블, NULL 처리, CloudPages 폼, 수신거부, 쿠폰 1:1 발급
- [x] `index.html` doc-link 추가 — Content Builder AMPscript 블록, CloudPages 수신거부, 발송 테스트 NULL 처리
- [x] `docs/audience-contact-builder.html` — Audience Builder 전체 + Contact Builder 심화 (Attribute Group, Cardinality, Synchronized DS, Contact Delete)
  - 출처: Salesforce 공식 문서 `engagement_audience_builder_and_contact_builder_6-23-2026.pdf` (185p)
- [x] `docs/marketing-cloud-account-engagement.html` — MCAE/Pardot 전체 가이드
  - MCE vs MCAE 비교, Prospect/Lists, Scoring/Grading, Engagement Studio, Forms/Form Handlers, 이메일 유형, CRM 동기화, Einstein, B2BMA 리포팅
  - 출처: Salesforce 공식 문서 `marketing_cloud_account_engagement_6-23-2026.pdf` (778p)
- [x] `index.html` doc-link 추가 (세션 11) — CB Cardinality, Contact Delete, JB Audience 트리거
- [x] `docs/journey-builder-automation-studio.html` — Automation Studio + Journey Builder 통합 가이드
  - AS: 시작소스 4종, Activity 12종(Type ID 포함), SQL Query 작성·최적화, Data Action 기준, Data View 15종
  - SQL 실전 패턴 5종: 바운스 이력, 30일 오픈, Journey 발송 집계, Journey 바운스 추출, 중간 테이블 분리
  - JB: Entry Source 6종, Canvas Activities(Send/Split/Wait/Update), 성능 최적화 원칙
  - Journey 실전 패턴 3종: Welcome Series, 생일 자동화(Wait by Attribute), Re-engagement(90일 비활성)
  - 출처: Salesforce 공식 문서 `engagement_journey_builder_and_automation_studio_6-23-2026.pdf` (497p)
- [x] `index.html` doc-link 추가 (세션 12) — AS Query/Data Action/시작소스, JB Entry/DE Entry/Split/Send/Wait

- [x] `docs/email-studio.html` — Email Studio 심화 가이드
  - Admin 설정 (SAP 3요소, Send Logging, Transactional Reconciliation, Auto-Suppression)
  - 구독자 상태 5종 (Active/Bounced/Held/Unsubscribed/Deleted)
  - Bounce 유형 4종 (Soft/Hard/Block/Technical) + 전환 조건
  - 수신거부 3단계 (List/Universal/FBL) + List-Unsubscribe Header (RFC 8058)
  - Lists vs Data Extensions 비교, Publication Lists
  - Triggered Sends 라이프사이클 (Draft→Active→Paused→Archived), List Detective
  - A/B Testing (4종 테스트, 5가지 상태, Test Distribution)
  - 발송 에러 코드 12종 + 집계 쿼리
  - 출처: Salesforce 공식 문서 `engagement_email_studio_6-23-2026.pdf` (366p)
- [x] `index.html` doc-link 추가 (세션 13) — SAP DKIM, Publication List, IP Warming Bounce, Transactional Triggered Send, 바운스 추출 쿼리

### 다음 예정
- [ ] `docs/automation-studio.html` → 삭제 예정 (journey-builder-automation-studio.html로 통합)
- [ ] `index.html` Step IPW 보강 — 일일 발송량 스케줄 표
- [ ] `docs/tracking-reporting.html` — Intelligence Reports, UTM 연동

---

## 다음 세션 시작 프롬프트

```
progress.md 읽고 현재 상태 파악해줘.
오늘 작업 목표: [여기에 작업 내용]
```

---

## 세션 로그

| 날짜 | 작업 내용 |
|------|-----------|
| 2026-06-19 세션 1 | 초기 구조 생성 (10단계) |
| 2026-06-19 세션 2 | 17단계 확장, 스타일 정규화, doc-link 정리 |
| 2026-06-19 세션 3 | contact-builder-de.html 신규 생성 |
| 2026-06-19 세션 4 | dashboard.html 전체 구현 (IndexedDB, 5탭, 마크다운, 스레드, DB v4) |
| 2026-06-19 세션 5 | 할일 탭 추가 (달력+날짜별 할일) |
| 2026-06-20 세션 6 | 파일탭 이름변경·검색, 전체 검색(Ctrl+K), 탭별 색·아이콘, 커뮤니케이션 Gmail 연동 |
| 2026-06-22 세션 7 | Agent 시스템 (File System Access API, autoSave, 브리핑 탭, DB v5→6) |
| 2026-06-22 세션 8 | 회의록 탭, 루틴 md 파일 4종, import-queue 파이프라인 |
| 2026-06-22 세션 9 | 2-level tab nav, 브리핑 독립, MCE 구축 진행현황 이름 변경, 미완료 이월·되돌리기, Weekly 양방향 드래그 |
| 2026-06-22 세션 10 | Weekly 요일별 색상 (월~금 blue/green/amber/red/purple), --purple CSS 변수 추가 |
| 2026-06-23 세션 11 | 가이드 심화: audience-contact-builder.html + marketing-cloud-account-engagement.html 신규 생성, index.html doc-link 3건 추가 |
| 2026-06-23 세션 12 | journey-builder-automation-studio.html 신규 생성 (AS+JB 통합, SQL 패턴 5종, Journey 패턴 3종), index.html doc-link 7건 추가 |
| 2026-06-23 세션 13 | email-studio.html 신규 생성 (구독자상태5종, Bounce4종, 수신거부3단계, Triggered Sends, A/B Testing, 에러코드12종), index.html doc-link 5건 추가 |
