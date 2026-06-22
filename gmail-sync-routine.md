# Gmail 동기화 루틴 프롬프트

이 파일은 Claude Code `/schedule` 루틴에 등록할 프롬프트입니다.

---

## 루틴 프롬프트 (복사하여 사용)

```
다음 작업을 순서대로 수행해주세요:

1. 파일 읽기
   - G:\내 드라이브\Projects\MCE-Setup-Guide\gmail-config.json 읽기
   - domains 목록과 projectId 확인

2. 기존 sync 파일 확인 (중복 방지)
   - G:\내 드라이브\Projects\MCE-Setup-Guide\gmail-sync.json 이 있으면 읽어서
     기존 gmailThreadId 목록 수집

3. 각 도메인에 대해 Gmail 검색
   - mcp__claude_ai_Gmail__search_threads 사용
   - query: "from:@{도메인} newer_than:14d"
   - 각 검색 결과에서 threadId 추출

4. 신규 스레드만 처리 (기존 gmailThreadId 제외)
   - mcp__claude_ai_Gmail__get_thread 로 각 스레드 전체 가져오기
   - 다음 정보 추출:
     * date: 첫 번째 메시지의 날짜 (YYYY-MM-DD 형식)
     * participants: 발신자 이름 <이메일> 형식
     * subject: 메일 제목
     * gmailThreadId: 스레드 고유 ID
   - 본문 요약 (한국어, 3~5문장):
     * 주요 요청/내용 요약
     * 결정사항이 있으면 포함
     * 후속 액션이 있으면 포함

5. gmail-sync.json 업데이트
   - 기존 emails 배열에 신규 항목 추가 (prepend, 최신순)
   - syncedAt을 현재 시각으로 업데이트
   - G:\내 드라이브\Projects\MCE-Setup-Guide\gmail-sync.json 에 저장

출력 포맷 (gmail-sync.json):
{
  "syncedAt": "ISO 날짜시각",
  "emails": [
    {
      "gmailThreadId": "스레드ID",
      "date": "YYYY-MM-DD",
      "participants": "이름 <email@domain.com>",
      "subject": "메일 제목",
      "summary": "한국어 요약 3~5문장"
    }
  ]
}
```

---

## 스케줄 등록 방법

Claude Code에서:
```
/schedule
```
- 이름: MCE Gmail 동기화
- 일정: 매일 오전 9시 (또는 원하는 시간)
- 프롬프트: 위 루틴 프롬프트 붙여넣기

---

## 대시보드 사용 흐름

1. 루틴이 실행되면 `gmail-sync.json` 이 자동 업데이트됨
2. MCE 대시보드 열기 → 커뮤니케이션 탭
3. **📬 Gmail 동기화** 버튼 클릭
4. `gmail-sync.json` 파일 선택
5. 새 메일 미리보기 확인 → **가져오기** 클릭
6. 커뮤니케이션 탭에 이메일 기록 자동 추가
