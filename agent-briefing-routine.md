# MCE 아침 브리핑 Agent 루틴

이 파일은 Claude Code `/schedule` 루틴에 등록할 프롬프트입니다.
**등록 일정:** 매일 오전 08:00

---

## 루틴 프롬프트 (복사하여 사용)

```
다음 작업을 순서대로 수행해주세요:

── 1. 데이터 읽기 ──────────────────────────────
파일을 읽어주세요:
- G:\내 드라이브\Projects\MCE-Setup-Guide\dashboard-data.json

(파일이 없으면 "dashboard-data.json 없음, 대시보드를 열어 Agent 설정을 먼저 완료하세요"라고
briefing-data.json에 기록하고 종료)

── 2. 기존 processed_thread_ids 확인 ──────────
파일을 읽어주세요 (있으면):
- G:\내 드라이브\Projects\MCE-Setup-Guide\briefing-data.json

기존 processed_thread_ids 배열을 메모해두세요 (없으면 빈 배열 []).

── 3. 대시보드 데이터 분석 ─────────────────────
dashboard-data.json에서 다음을 분석하세요:

today = 오늘 날짜 (YYYY-MM-DD)

a) 오늘의 todos: todos 배열에서 date === today인 항목
   - 미완료(done:false) vs 완료(done:true) 개수
b) 임박 마감 todos: 오늘 ~ 3일 이내 마감, 미완료
c) 오픈 이슈: issues 배열에서 status !== 'resolved'
   - priority='high' 건수 별도 집계
d) STEPS 진행률: 전체 스텝 수 대비 done 건수, 현재 in-progress 스텝명
e) 최근 7일 커뮤니케이션 건수

── 4. Gmail 확인 ────────────────────────────────
mcp__claude_ai_Gmail__search_threads 사용:
- query: "newer_than:2d"
- 결과에서 threadId, subject, from, date 확인
- processed_thread_ids에 이미 있는 threadId는 스킵
- 신규 스레드만 highlights에 추가:
  "제목: {subject} | 발신: {from} | 날짜: {date}"
- 신규 threadId를 processed_thread_ids에 append

(주의: 본문 fetch 금지, 메타데이터만 사용)

── 5. Google Calendar 확인 ─────────────────────
mcp__claude_ai_Google_Calendar__list_events 사용:
- 오늘 일정 목록
- "HH:MM 일정명" 형태로 정리

── 6. Google Drive 날짜별 백업 ─────────────────
dashboard-data.json 내용을 Google Drive에 백업하세요.

mcp__claude_ai_Google_Drive__create_file 사용:
- 파일명: dashboard-data-{today}.json  (예: dashboard-data-2026-06-22.json)
- 부모 폴더 ID: 10QsEGHZgsZgLkvmw40hZwUE9MtwHpoIo
  (Google Drive › MCE-Setup-Guide › backups 폴더)
- 내용: dashboard-data.json 파일 내용 그대로

(백업 실패해도 계속 진행)

── 7. briefing-data.json 저장 ──────────────────
G:\내 드라이브\Projects\MCE-Setup-Guide\briefing-data.json 에 저장:

{
  "generatedAt": "ISO 날짜시각",
  "date": "YYYY-MM-DD",
  "summary": "한 줄 요약 (예: '오늘 할일 3개, 높은 우선순위 이슈 1건, 미팅 2개')",
  "insights": [
    "⚠️ 높은 우선순위 이슈 N건 오픈",
    "✅ 오늘 할일 N개 (완료 N개)",
    "📅 임박 마감 N개",
    "📈 구축 진행률 N%"
  ],
  "calendar": [
    "10:00 화상회의",
    "14:00 내부미팅"
  ],
  "gmailHighlights": [
    "제목: IP Warming 문의 | 발신: hong@client.com | 날짜: 2026-06-22"
  ],
  "todoCount": {"total": 5, "done": 2},
  "openIssueCount": {"high": 1, "medium": 2, "low": 0},
  "processed_thread_ids": ["thread_abc", "thread_xyz", ...]
}

processed_thread_ids는 기존 배열에 신규 ID를 누적 append. 절대 기존 ID 삭제 금지.
```

---

## 스케줄 등록 방법 (claude.ai 영구 등록)

> CronCreate(세션 한정, 7일 만료) 대신 **claude.ai 웹**에서 등록하면 세션 종료 후에도 유지됩니다.

1. [claude.ai](https://claude.ai) 접속
2. 새 대화 시작 → `/schedule` 입력
3. 아래 정보 입력:
   - **이름:** MCE 아침 브리핑
   - **일정:** 매일 08:00 (KST)
   - **프롬프트:** 위 `## 루틴 프롬프트` 코드블록 전체 복사·붙여넣기

---

## 출력 파일

| 파일 | 설명 |
|------|------|
| `briefing-data.json` | 매일 덮어쓰기 (processed_thread_ids 누적) |
| `dashboard-data-YYYY-MM-DD.json` | Google Drive backups 폴더에 날짜별 누적 |

---

## 대시보드 연동 흐름

1. 루틴이 매일 08:00 자동 실행 → `briefing-data.json` 갱신
2. MCE 대시보드 열기 → `🤖 브리핑` 탭 클릭
3. Agent 브리핑 섹션에 오늘 요약 자동 표시
4. 오늘 할일 / 이슈 현황 / 진행현황은 IndexedDB에서 실시간 표시

---

## 선행 조건

- 대시보드에서 `⚙️ Agent` 버튼 클릭 → 폴더 선택 완료
- `dashboard-data.json`이 프로젝트 폴더에 존재 (대시보드 열 때 자동 생성)
