---
name: project-mce-dashboard
description: MCE Setup Guide 단일파일 대시보드 구성 현황 — 구현된 탭·기능·Agent 루틴·파일 경로
metadata: 
  node_type: memory
  type: project
  originSessionId: 5830ba7a-bdcb-47c8-bdb0-ad5d28e5b171
  lastUpdated: 2026-07-03
---

## 파일 위치
- **메인 파일:** `${GDRIVE_ROOT}\Projects\MCE-Setup-Guide\dashboard.html` (단일 HTML, IndexedDB 저장)
- **MCE 가이드 문서:** `${GDRIVE_ROOT}\Projects\MCE-Setup-Guide\docs\journey-builder-custom-activity.html`
- **선오픈 공수 분석:** `${USER_HOME}\Desktop\MCE_선오픈_공수분석.txt`
- 경로 변수는 [[user-work-environment]] 참고
- **루틴 설명:** `agent-briefing-routine.md`, `agent-weekly-routine.md`
- **Agent 출력 파일:** `briefing-data.json`, `weekly-data.json`, `dashboard-data.json`, `gmail-sync.json`

**Why:** Salesforce MCE 구축 프로젝트 전용 대시보드, 백엔드 없이 단일 파일로 운영  
**How to apply:** 기능 추가 요청 시 이 파일만 수정. DB_VERSION 현재 7.

---

## 탭 구조 (2-level nav)

메인 탭바: `🤖 브리핑` | 구분선 | `📊 MCE 구축 진행현황` | 구분선 | `📋 업무 기록`  
업무 기록 하위탭: `📅 할일` > `💬 커뮤니케이션` > `⚠️ 이슈` > `📝 노트` > `🎙️ 회의록` > `📎 파일` > `✂️ 스니펫`

| 탭 | 주요 기능 |
|----|-----------|
| 🤖 브리핑 | **로컬 IndexedDB 전용** — KPI 4개(할일완료·이슈·진행률·마감임박) + 오늘할일·미해결이슈·진행현황·이번주요약 |
| 📊 MCE 구축 진행현황 | STEPS 그룹별 상태 관리 (pending/in-progress/done) |
| 💬 커뮤니케이션 | 카드/타임라인 토글, Gmail 동기화 import, type별 색·아이콘 |
| 📎 파일 | 카테고리 필터+색, 파일명 검색, 이름 변경 |
| ⚠️ 이슈 | priority(high/medium/low) 색 구분, status: **발견/처리/완료** |
| 📝 노트 | 드래그앤드롭 순서 변경, 카테고리 필터, 스레드 편집 |
| 📅 할일 | Daily/Weekly/Monthly 뷰, **미완료 이월** (originalDate 보존, 개별/전체 이월·되돌리기), **Weekly 요일별 색상** |
| 🎙️ 회의록 | 좌측 목록 + 우측 에디터(실시간 파싱 패널), 1.2초 자동저장 |
| ✂️ 스니펫 | 카드 그리드, 카테고리 필터, 복사 횟수 추적 |

---

## 2026-07-03 주요 변경사항

### 브리핑 탭 완전 재설계
- **Agent 폴더 의존 제거**: `briefing-data.json`, `weekly-data.json`, `import-queue.json` 읽기 삭제
- **로컬 데이터만으로 브리핑 생성** (IndexedDB: todos, issues, communications)
- **KPI 카드 4개** (full-width): 오늘 할일 완료율 / 미해결 이슈 수 / MCE 진행률% / 이번 주 마감 임박
  - 이슈 고우선순위 또는 마감 임박 시 amber 강조(`.kpi-warn`)
- **이번 주 요약** 로컬 계산: 이번 주 커뮤니케이션 건수, 완료 이슈, 완료 할일, 마감 임박 목록
- 기본 진입 탭을 `briefing`으로 변경 (`currentTab = 'briefing'`)
- 브리핑 콘텐츠: `max-width:1400px; margin:0 auto` 가운데 정렬

### 이슈 상태 레이블 변경
- `open` → **발견**, `in-progress` → **처리**, `resolved` → **완료**
- 브리핑 섹션명: "오픈 이슈" → **"미해결 이슈"** (발견+처리 합계)
- 이슈 탭 필터 버튼 텍스트도 동일하게 변경

### 탭 내비게이션 디자인 개선
- 메인·서브탭 모두 `justify-content:center` 가운데 정렬
- 언더라인 액티브 → **pill 배경** 방식 (`background:var(--blue-bg); border-radius:7px`)
- 호버 시 배경 전환 애니메이션 추가

### 스니펫 탭 레이아웃 통일
- `.snippet-layout` 독자 래퍼 → `.list-pane` + `.tab-toolbar` 구조로 교체 (다른 탭과 동일)
- 카드 최소 너비 280→300px, 간격 12→14px
- 빈 상태 이미지: `flex:1` → `min-height:50vh` (list-pane 내에서 가운데 표시)
- `.pane-resizer` + `.thread-pane` 추가

---

## 핵심 구현 세부사항

### 브리핑 탭 데이터 흐름 (2026-07-03~)
```
IndexedDB todos/issues/communications → renderBriefing() →
  이번 주 범위 계산(월~일) → KPI 계산 → 섹션 렌더
```
- `urgentTodos`: `t.deadline || t.date`로 fallback (todo에 별도 deadline 필드 존재)
- `weekResolvedIssues`: `i.updatedAt`이 timestamp(숫자) 또는 ISO string 혼용 → `new Date(i.updatedAt)`으로 통일 처리
- `steps` 진행률: `project?.steps` 참조, STEPS 배열의 `s.title` 필드 사용 (`s.name` 아님)

### 이슈 탭 스키마
- `status`: `'open'` | `'in-progress'` | `'resolved'`  (내부 값 변경 없음, 표시 레이블만 변경)
- `priority`: `'high'` | `'medium'` | `'low'`

### 회의록 파싱 (parseMeetingItems)
- 마커: `이슈:` → issues[], `할일:`/`액션:` → todos[], `결정:` → decisions[]
- `@이름` → assignee, `~날짜` → deadline 파싱
- 결정 항목 → 노트탭 `category:'결정사항'`으로 저장 (제목에 `[결정]` prefix 없음)

### 삭제 취소 (undoStack)
- 모든 삭제 전 `pushUndo(store, item, label, refreshFn)` 호출
- `Ctrl+Z` → `undoLast()` → `db.put()`으로 복원
- 스택 최대 20개

### 노트 IndexedDB 스키마
```
notes store: { id, projectId, title, category, content, order, createdAt, updatedAt }
threads store: { id, parentId, projectId, content, createdAt, updatedAt }
```

### 미완료 이월 (Daily 뷰)
- 오늘 날짜 선택 시 과거 미완료 항목을 상단 amber 섹션으로 표시
- 이월 시 `originalDate` 필드에 원래 날짜 저장 → 되돌리기 가능
- `rolloverTodo(id)`, `rolloverAllTodos()`, `restoreTodo(id)` 함수

### Agent 동기화 (File System Access API)
- 헤더 `⚙️ Agent` 버튼 → 폴더 선택 → `syncDir` handle을 IndexedDB `settings` store에 저장
- 탭 전환 시마다 `autoSaveDashboard()` → `dashboard-data.json` 자동 갱신 (브리핑 탭은 제외)
- `readSyncFile(filename)` 함수는 코드에 남아 있음 (autoSaveDashboard 등에서 사용 가능)

### 등록된 CronCreate 루틴 (세션 한정, 7일 만료)
- **#89033777** 매일 08:03 → `briefing-data.json` 생성 (현재 브리핑에서 미사용)
- **#fa1ab169** 매주 금 18:07 → `weekly-data.json` 생성 (현재 브리핑에서 미사용)

### Weekly 뷰 요일별 색상
- 월~금 컬럼에 `day-col-0`~`day-col-4` 클래스 (토·일 제외)
- 월=blue, 화=green, 수=amber, 목=red, 금=purple
- CSS `--purple`/`--purple-bg` 변수 4곳 모두 추가

### 전체 검색
- `Ctrl+K` 또는 헤더 🔍 버튼 → 모든 탭 데이터 교차 검색

---

## Agent 루틴 파일 목록

| 파일 | 용도 | 트리거 |
|---|---|---|
| `agent-briefing-routine.md` | 매일 브리핑 + Drive 날짜별 백업 | claude.ai 매일 08:00 |
| `agent-weekly-routine.md` | 내부용 주간 데이터 분석 | claude.ai 매주 금 18:00 |
| `agent-weekly-report-routine.md` | 고객사 공유용 주간 보고서 초안 | claude.ai 매주 금 17:00 |
| `agent-meeting-routine.md` | meeting-draft.txt 읽어 추출 | 회의 후 수동 실행 |

- Google Drive backups 폴더 ID: `10QsEGHZgsZgLkvmw40hZwUE9MtwHpoIo`

## 다음 보완 후보
1. **Claude API 직접 연동** (회의록 추출 완전 자동화)
2. 커뮤니케이션 팔로업 날짜
3. D-day 배지 / 마감 경고
4. 일일 업무 로그
