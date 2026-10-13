# 프로젝트 목표
내가 담당하는 고객사 프로젝트(운영·구축·설계 등)의 업무 히스토리 아카이브. 프로젝트별 폴더에 업무 로그·회의록·산출물을 쌓고, `dashboard.html`(단일 HTML, IndexedDB)로 할일·이슈·커뮤니케이션·노트를 관리한다.

# 폴더 구조
- `projects/{고객사}/` — 프로젝트 단위 아카이브. `project.md`(성격·기간 등 메타), `workflow.md`(프로젝트별 업무 플로우), `history.md`(날짜별 로그), `meetings/`, `docs/`, `reports/`
- `projects/_template/` — 새 프로젝트 생성용 템플릿, `projects/README.md` — 프로젝트 목록(성격 포함)
- `dashboard.html` — 업무 아카이브 앱 (DB_VERSION 관리)
- `_sync/` — 대시보드 ⚙️ Agent 동기화 폴더 (dashboard-data.json, backups/, import-queue.json, meeting-draft.txt, gmail-sync.json). 자동 생성 파일만 둔다
- `routines/` — Agent 루틴 프롬프트 (briefing, weekly, weekly-report, meeting, gmail-sync)
- `tools/` — 로컬 프록시(`slack-proxy.js`, 포트 3099)와 실행 스크립트
- `_archive/legacy/` — 이전 구조의 기록 파일 (수정하지 않음)
- MCE 가이드 문서는 별도 프로젝트 `../MCE-Guide/`로 분리됨 (대시보드의 가이드 링크가 이 경로를 가리킴)

# 작업 규칙
- 업무 기록 요청 → 해당 `projects/{고객사}/history.md`에 최신 날짜가 위로 오도록 추가. 회의록은 `meetings/YYYY-MM-DD-제목.md`, 산출물은 `docs/`에 두고 history에서 링크
- 프로젝트 작업 시작 → `project.md` → `workflow.md` → `history.md` 최근 항목 순으로 읽고, 현재 단계와 다음 할 일을 먼저 제안
- 작업 종료 → history 초안과 함께 `workflow.md` 갱신 제안(이번에 확정된 처리 방식·반복 패턴). 사람이 확인한 것만 반영
- `workflow.md`의 "자동 처리 허용" 목록에 있는 작업만 묻지 않고 진행. 나머지는 확인 후 진행
- 새 프로젝트 → `_template/` 복사 후 `project.md`의 성격(운영/구축/설계/컨설팅)·기간 기입, `projects/README.md` 표에 추가
- 대시보드 기능 추가·수정은 `dashboard.html` 파일 하나만 수정 (단일 파일 구조 유지, 별도 프레임워크 도입하지 않음)
- IndexedDB 스키마 변경 시 `DB_VERSION` 증가 + 마이그레이션 로직 확인
- 루틴 파일의 경로는 `G:\내 드라이브\Projects\Project-Archive\_sync\` 기준
- 이 프로젝트는 golden/outputs 구조를 적용하지 않음

# AI ↔ 사람 경계
- 할일/이슈/커뮤니케이션 데이터 입력과 실제 업무 판단은 사람 몫. history·회의록은 사람이 확인한 내용만 기록
- 대시보드 구조·기능 변경은 AI가 제안하고 사람이 확인 후 반영
- 삭제는 undoStack으로 되돌릴 수 있지만, IndexedDB 스키마 변경처럼 되돌리기 어려운 작업은 사전에 영향 설명 필요

# 금지사항
- Gmail/Slack 등 외부 시스템에 직접 게시 금지 — 초안까지만 준비
- 고객사 민감 정보를 대시보드·아카이브 문서에 원문 그대로 노출하지 않음
- `projects/솔타메디칼/kickoff-reference.md`는 원문 레퍼런스이므로 수정 금지
