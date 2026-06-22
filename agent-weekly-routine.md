# MCE 주간 리뷰 Agent 루틴

이 파일은 Claude Code `/schedule` 루틴에 등록할 프롬프트입니다.
**등록 일정:** 매주 금요일 18:00

---

## 루틴 프롬프트 (복사하여 사용)

```
다음 작업을 순서대로 수행해주세요:

── 1. 데이터 읽기 ──────────────────────────────
파일을 읽어주세요:
- G:\내 드라이브\Projects\MCE-Setup-Guide\dashboard-data.json

(파일이 없으면 "dashboard-data.json 없음"이라는 메시지를 weekly-data.json에 기록하고 종료)

── 2. 이번 주 범위 계산 ─────────────────────────
오늘 = 금요일
이번 주 = 이번 주 월요일 ~ 오늘 (금요일)
다음 주 = 다음 주 월요일 ~ 다음 주 금요일

날짜 범위를 YYYY-MM-DD 형식으로 계산.

── 3. 주간 분석 ────────────────────────────────
dashboard-data.json에서:

a) 이번 주 커뮤니케이션
   - communications 배열에서 date가 이번 주 범위인 항목
   - type별 건수 집계 (이메일, 전화, 화상회의, 대면미팅, 메신저)

b) 이슈 현황
   - 이번 주 새로 등록된 이슈 (createdAt이 이번 주)
   - 이번 주 해결된 이슈 (status='resolved', updatedAt이 이번 주)
   - 현재 오픈 이슈 건수 및 priority 분포

c) 할일 완료율
   - todos에서 date가 이번 주인 항목
   - 완료(done:true) vs 전체

d) STEPS 변경
   - 이번 주에 상태가 변경된 스텝 (완료된 스텝 등)
   - 현재 진행중인 스텝, 다음 대기 스텝

e) 다음 주 주요 항목
   - todos에서 date가 다음 주 범위인 항목 (상위 5개)

── 4. weekly-data.json 저장 ────────────────────
G:\내 드라이브\Projects\MCE-Setup-Guide\weekly-data.json 에 저장:

{
  "weekLabel": "2026년 6월 4주차",
  "generatedAt": "ISO 날짜시각",
  "weekRange": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
  "summary": "이번 주 2~3문장 요약 (주요 진전, 해결된 이슈, 커뮤니케이션 현황 등)",
  "highlights": [
    "Step 5 완료",
    "이슈 2건 해결",
    "고객사 화상회의 2회"
  ],
  "nextActions": [
    "다음 주 Step 6 진행 예정",
    "회의록 작성 2건 필요",
    "고객사 요건 확인 필요"
  ],
  "stats": {
    "commCount": 3,
    "commByType": {"이메일": 2, "화상회의": 1},
    "issueNew": 1,
    "issueResolved": 2,
    "issueOpen": 3,
    "todosDone": 8,
    "todosTotal": 10
  }
}
```

---

## 스케줄 등록 방법 (claude.ai 영구 등록)

> CronCreate(세션 한정, 7일 만료) 대신 **claude.ai 웹**에서 등록하면 세션 종료 후에도 유지됩니다.

1. [claude.ai](https://claude.ai) 접속
2. 새 대화 시작 → `/schedule` 입력
3. 아래 정보 입력:
   - **이름:** MCE 주간 리뷰
   - **일정:** 매주 금요일 18:00 (KST)
   - **프롬프트:** 위 `## 루틴 프롬프트` 코드블록 전체 복사·붙여넣기

---

## 출력 파일

| 파일 | 설명 |
|------|------|
| `weekly-data.json` | 매주 금요일 덮어쓰기 |

---

## 대시보드 연동 흐름

1. 루틴이 매주 금요일 18:00 자동 실행 → `weekly-data.json` 갱신
2. MCE 대시보드 → `🤖 브리핑` 탭
3. 주간 요약 섹션에 이번 주 리뷰 자동 표시

---

## 선행 조건

- 대시보드에서 `⚙️ Agent` 버튼 클릭 → 폴더 선택 완료
- `dashboard-data.json`이 프로젝트 폴더에 존재 (대시보드 열 때 자동 생성)
