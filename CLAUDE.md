# 프로젝트 목표
Salesforce MCE(Marketing Cloud Engagement) 구축 프로젝트 운영을 위한 단일 파일 대시보드 + 가이드 문서. 백엔드 없이 로컬(IndexedDB)에서 진행현황·이슈·커뮤니케이션·노트·할일을 관리한다.

# 컨텍스트 경로
- 메인 파일: `dashboard.html` (단일 HTML, IndexedDB 저장, DB_VERSION 관리)
- MCE 가이드 문서: `docs/journey-builder-custom-activity.html`
- Agent 루틴 문서: `agent-briefing-routine.md`, `agent-weekly-routine.md`, `agent-weekly-report-routine.md`, `agent-meeting-routine.md`
- 관련 memory: `.claude/project_mce_dashboard.md`, `.claude/project_mce_guide_doc.md` (이 프로젝트 폴더 기준 상대경로)

# 작업 규칙
- 기능 추가·수정 요청은 `dashboard.html` 파일 하나만 수정 (단일 파일 구조 유지, 별도 프레임워크 도입하지 않음)
- IndexedDB 스키마 변경 시 `DB_VERSION` 증가 + 마이그레이션 로직 확인
- 가이드 문서 관련 질문·수정은 `journey-builder-custom-activity.html` 기준으로 답변
- 이 프로젝트는 golden/outputs 구조를 적용하지 않음 — 반복 산출물 생성형이 아니라 코드를 직접 편집하는 대시보드 앱이기 때문

# AI ↔ 사람 경계
- 할일/이슈/커뮤니케이션 데이터 입력과 실제 업무 판단은 사람 몫
- 대시보드 구조·기능 변경은 AI가 제안하고 사람이 확인 후 반영
- 삭제는 undoStack으로 되돌릴 수 있지만, IndexedDB 스키마 변경처럼 되돌리기 어려운 작업은 사전에 영향 설명 필요

# 금지사항
- Gmail/Slack 등 외부 시스템에 직접 게시 금지 — 초안까지만 준비
- 고객사(세스코 등) 민감 정보를 대시보드나 가이드 문서에 원문 그대로 노출하지 않음