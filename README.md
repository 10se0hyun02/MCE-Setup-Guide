# Project-Archive — 업무 히스토리 아카이브

담당 고객사 프로젝트(운영·구축·설계 등)의 업무 기록을 프로젝트 단위로 보관하고,
`dashboard.html`로 할일·이슈·커뮤니케이션·노트를 관리합니다.

## 구조

```
Project-Archive/
  dashboard.html          업무 아카이브 앱 (단일 HTML, IndexedDB MCEDashboardDB)
  projects/
    README.md             프로젝트 목록 (고객사·성격·기간·상태)
    _template/            새 프로젝트 템플릿
    {고객사}/
      project.md          성격(운영/구축/설계/컨설팅)·기간·역할·범위
      history.md          날짜별 업무 로그 (최신이 위)
      meetings/           회의록 YYYY-MM-DD-제목.md
      docs/               산출물·받은 자료
      reports/            주간 보고서 (weekly-report 루틴 출력)
  _sync/                  대시보드 ⚙️ Agent 동기화 폴더 (git 제외, 자동 생성)
    dashboard-data.json   탭 전환 시 자동 저장
    backups/              날짜별 백업 (7일 보관)
    import-queue.json     회의/메일 루틴 → 대시보드 가져오기 대기
    meeting-draft.txt     회의록 탭 [Agent 추출] 출력
    gmail-sync.json       Gmail 동기화 루틴 출력
  routines/               Agent 루틴 프롬프트
  tools/                  slack-proxy.js (localhost:3099), start-proxy-silent.vbs
  _archive/legacy/        이전 구조(MCE-Setup-Guide) 시절 기록
```

MCE 구축 가이드(index.html, docs/, 원문 PDF)는 `../MCE-Guide/`로 분리되었습니다.

## 데이터 흐름

```
대시보드 → _sync/dashboard-data.json → 루틴(briefing/weekly/weekly-report)
회의록 탭 → _sync/meeting-draft.txt → agent-meeting-routine → _sync/import-queue.json → 대시보드 가져오기
gmail-sync-routine → _sync/gmail-sync.json → 커뮤니케이션 탭 Gmail 동기화
weekly-report 루틴 → projects/{고객사}/reports/
```

## 기록 규칙
- 업무 로그는 `projects/{고객사}/history.md`에 `## YYYY-MM-DD` 단위로 추가
- 회의록·산출물은 해당 폴더에 두고 history에서 링크
- 고객사 민감 정보는 원문 그대로 남기지 않음
