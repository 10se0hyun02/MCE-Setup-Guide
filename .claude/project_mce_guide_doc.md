---
name: project-mce-guide-doc
description: "MCE Setup Guide 가이드 문서 — Custom Activity 중심, 슈어엠·CJ PDF 반영 내역"
metadata: 
  node_type: memory
  type: project
  lastUpdated: 2026-07-02
  originSessionId: 19001cfd-15c0-4a86-8533-83b760d3751c
---

## 파일 위치
- **메인 가이드:** `${GDRIVE_ROOT}\Projects\MCE-Setup-Guide\docs\journey-builder-custom-activity.html`
- **CJ 매뉴얼 원본(읽기용):** `${USER_HOME}\tmp_cj_pdf\extracted.txt` (1808줄, 3 PDF 합본)
- 경로 변수는 [[user-work-environment]] 참고

**Why:** Salesforce MCE Custom Activity(Journey Builder) 구현 시 참조 가이드  
**How to apply:** 슈어엠/CJ 관련 질문 시 이 문서 기준으로 답변

---

## 가이드 문서 TOC (주요 섹션)

- Custom Activity 개요 / R&R 협의 체크리스트
- DE(Data Extension) 설계
- Installed Package 등록
- 슈어엠 연동 (5개 서브섹션)
  - `#surem-msgtype` : 카카오 메시지 타입 (AT/AI/FT/FI/FW/FL/FC/FM/FA)
  - `#surem-failback` : Fail-Back 정책 (FAILED_TYPE: SMS/LMS/MMS/NO)
  - `#surem-callerid` : 발신번호 사전등록 법적 요건
  - `#surem-080` : 080 수신거부 적용 범위 (광고형만 해당, AT 제외)
  - `#surem-rsltcode` : 발송 결과 코드 12종 (0/A/V/M/B/I/G 등)
- Troubleshooting (전화번호 오류, 과금 부족, Fail-Back 미동작, 카카오 장애)

---

## CJ PDF 매뉴얼 요약 (슈어엠 적용 불가, 참고만)

| 파일 | 내용 | MCE 적용 여부 |
|------|------|---------------|
| api.pdf | 080 수신거부 API | 참고만 (슈어엠 방식 다름) |
| agent.pdf | CJAgent SMS DB INSERT 방식 | 적용 불가 (슈어엠은 REST API) |
| mplace.pdf | CJmplaceAgent 카카오 DB INSERT 방식 | 적용 불가 (구현 방식 상이) |

**핵심 차이:** CJ는 DB INSERT로 발송 트리거, 슈어엠은 REST API `/execute` 호출

### CJ PDF에서 가져온 실제 반영 내용
- 전화번호 포맷: 하이픈 없는 11자리 (`010XXXXXXXX`) → 가이드 DE 설계 섹션 반영
- 카카오 메시지 타입 코드 체계 (AT/FT 등) → `#surem-msgtype` 테이블에 반영
- Fail-Back 개념 (알림톡 실패 → SMS 전환) → `#surem-failback` 섹션에 반영
- 080 수신거부 적용 범위 (광고형만) → `#surem-080` 섹션에 반영

---

## 선오픈 공수 분석 (세스코 프로젝트)

출처: `세스코_기술협상_마케팅_별첨2. 선오픈 검토_밀버스_260602.xlsx`  
분석 파일: `${USER_HOME}\Desktop\MCE_선오픈_공수분석.txt`

| 항목 | MD | MM | 비율 |
|------|----|----|------|
| ① 솔루션 환경 구성 | 5 | 0.24 | 3% |
| ② 데이터 연계 체계 구축 | 30 | 1.43 | 17% |
| ③ 발송 채널 연계 구축 | 15 | 0.71 | 9% |
| ④ 타겟 세그먼트 구축 | 40 | 1.90 | 23% |
| ⑤ Journey Builder 시나리오 구축 | 66 | 3.14 | 38% |
| ⑥ 통합 테스트 및 안정화 | 18 | 0.86 | 10% |
| **소계 (MCE+)** | **174** | **8.29** | **100%** |

**리스크 포인트:**
- ④+⑤ = 106MD (전체의 61%) → 타겟 조건 확정 지연이 전체 병목
- ③(슈어엠 연동) 완료 전까지 ⑤(Journey 테스트) 불가
- ② 외부 의존성 가장 큼 (세스코 원천 시스템 협의)
