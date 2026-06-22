# 주간 보고 초안 생성 Agent 루틴

대시보드 데이터를 읽어 고객사 공유용 주간 보고서 초안을 생성합니다.
**등록 일정:** 매주 금요일 17:00 (루틴) 또는 수동 실행

---

## 루틴 프롬프트 (복사하여 사용)

```
다음 작업을 순서대로 수행해주세요:

── 1. 데이터 읽기 ──────────────────────────────
파일을 읽어주세요:
- G:\내 드라이브\Projects\MCE-Setup-Guide\dashboard-data.json

── 2. 이번 주 범위 계산 ─────────────────────────
오늘 = 금요일 (또는 실행 당일)
이번 주 = 직전 월요일 ~ 오늘
날짜 범위: YYYY-MM-DD 형식

── 3. 보고서 데이터 수집 ────────────────────────

a) 전체 진행률
   - STEPS에서 done/in-progress/pending 각 건수
   - 현재 진행 중인 단계명

b) 이번 주 완료 항목
   - todos 중 done=true이고 date가 이번 주인 것
   - issues 중 status='resolved'이고 resolvedAt이 이번 주인 것

c) 이번 주 커뮤니케이션
   - communications 중 date가 이번 주인 것 (type, participants, summary)

d) 현안 이슈
   - status='open'인 이슈 중 priority='high'인 것

e) 다음 주 예정
   - todos 중 done=false이고 date가 다음 주인 것 (상위 5개)
   - 다음에 진행할 STEP

── 4. 보고서 파일 저장 ─────────────────────────
아래 두 곳에 저장:

로컬: G:\내 드라이브\Projects\MCE-Setup-Guide\weekly-report-{오늘날짜}.md
Drive: mcp__claude_ai_Google_Drive__create_file
  - 부모 폴더 ID: 1MJSX7EQBWKIaXFHyl2txkOG9XMXPAied (MCE-Setup-Guide)
  - 파일명: weekly-report-{오늘날짜}.md

보고서 포맷:
---
# MCE 구축 주간 현황 보고
**기간:** YYYY년 MM월 DD일 ~ MM월 DD일 (N주차)
**작성일:** YYYY년 MM월 DD일

## 전체 진행률
> 전체 N단계 중 N단계 완료 (N%)
> 현재 진행: {단계명}

[진행 바 텍스트: ████████░░░░ 67%]

## 이번 주 완료 사항
- 항목1
- 항목2

## 커뮤니케이션 이력
| 날짜 | 유형 | 주요 내용 |
|------|------|----------|
| MM/DD | 화상회의 | ... |

## 현안 사항
| 구분 | 내용 | 조치 계획 |
|------|------|----------|
| 이슈명 | 내용 | 계획 |

(현안 없으면 "현재 특이사항 없음" 표기)

## 다음 주 예정
- 예정1
- 예정2

---
*본 보고서는 MCE 구축 대시보드 데이터를 기반으로 자동 생성되었습니다.*
---
```

---

## 스케줄 등록 방법 (claude.ai 영구 등록)

1. [claude.ai](https://claude.ai) 접속
2. 새 대화 → `/schedule` 입력
3. 아래 정보 입력:
   - **이름:** MCE 주간 보고 초안
   - **일정:** 매주 금요일 17:00 (KST)
   - **프롬프트:** 위 루틴 프롬프트 전체 복사·붙여넣기

---

## 출력 파일

| 파일 | 설명 |
|------|------|
| `weekly-report-YYYY-MM-DD.md` | 로컬 저장 (검토 후 고객 전달) |
| Google Drive MCE-Setup-Guide 폴더 | 동일 파일 Drive 백업 |

---

## 활용 흐름

1. 금요일 17:00 루틴 자동 실행 → 보고서 초안 생성
2. 담당자가 내용 검토·수정
3. 고객사에 메일/Slack으로 공유
