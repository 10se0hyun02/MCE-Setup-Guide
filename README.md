# MCE 구축 가이드 (index.html)

Marketing Cloud Engagement 구축 전 과정을 단계별로 정리한 단일 HTML 가이드 파일입니다.  
Claude Code로 지속적으로 수정·보완하는 것을 전제로 구성되어 있습니다.

---

## 파일 구조

```
mce-guide/
├── index.html      # 메인 가이드 (단일 파일, 이것만 관리)
├── README.md       # 이 파일 — 구조 설명 + 작업 로그
└── progress.md     # Claude Code 세션 간 이어가기용 체크포인트
```

---

## 현재 구현 상태

### 완료된 기능
- [x] 10단계 사이드바 네비게이션 (그룹별 묶음)
- [x] 단계별 체크리스트 (클릭 완료 처리 + 취소선)
- [x] 단계별 진행률 바 + 카운터 (예: 2 / 5)
- [x] 전체 진행률 (사이드바 하단)
- [x] 네비게이션 상태 아이콘 (⬜ / 🔵 / ✅)
- [x] 4종 callout 박스 (warning / danger / tip / note)
- [x] 코드블록 복사 버튼
- [x] 필드 구성 테이블 (tag: 필수/선택/시스템)
- [x] 키워드 검색 (체크리스트 + callout 대상)
- [x] 다크모드 대응

### 미완료 / 디벨롭 예정
- [ ] 각 단계 실제 내용 채우기 (현재는 기본 템플릿 수준)
- [ ] 클라이언트별 분기 (탭 또는 필터로 Sony / 초록우산 등 구분)
- [ ] 스크린샷 삽입 영역
- [ ] 트러블슈팅 섹션 추가
- [ ] 단계 완료 후 로컬스토리지 진행 상태 저장
- [ ] 인쇄/PDF 출력 스타일

---

## 구조 설명

### HTML 구조 패턴

**새 단계 추가 시 반드시 두 곳 동시 수정:**

```html
<!-- 1. 사이드바 nav-item 추가 -->
<div class="nav-item" onclick="showSection('s11')" id="nav-s11">
  <span class="nav-badge">11</span>
  <span>새 단계 이름</span>
  <span class="nav-status" id="status-s11">⬜</span>
</div>

<!-- 2. main 영역 section 추가 -->
<div class="section" id="s11">
  <div class="section-header">
    <div class="section-eyebrow">Step 11 · 그룹명</div>
    <div class="section-title">단계 제목</div>
    <div class="section-desc">설명</div>
    <div class="step-progress">
      <div class="step-progress-track">
        <div class="step-progress-fill" id="prog-s11" style="width:0%"></div>
      </div>
      <span class="step-progress-label" id="prog-label-s11">0 / N</span>
    </div>
  </div>
  <!-- 체크리스트, callout, 코드블록 등 -->
</div>
```

**JS의 SECTIONS 객체도 함께 추가:**
```js
const SECTIONS = {
  // ...기존 항목들...
  s11: { title: '새 단계 이름', group: '그룹명' }
};
```

---

### 컴포넌트 사용법

**체크리스트 항목:**
```html
<div class="check-item" onclick="toggle(this)">
  <input type="checkbox">
  <label>항목 내용</label>
</div>
```

**Callout 박스 (4종):**
```html
<div class="callout warning">  <!-- warning / danger / tip / note -->
  <span class="callout-icon">⚠️</span>  <!-- ⚠️ 🚫 💡 📌 -->
  <div><strong>제목:</strong> 내용</div>
</div>
```

**코드블록:**
```html
<div class="code-block">
  <div class="code-header">
    <span class="code-lang">SQL (Query Studio)</span>
    <button class="copy-btn" onclick="copyCode(this)">
      <svg ...>...</svg> 복사
    </button>
  </div>
  <div class="code-body">SELECT * FROM ...</div>
</div>
```

**테이블:**
```html
<table class="data-table">
  <thead><tr><th>필드명</th><th>타입</th><th>필수</th></tr></thead>
  <tbody>
    <tr>
      <td>ContactKey</td>
      <td>Text(36)</td>
      <td><span class="tag required">필수</span></td>  <!-- required / optional / system -->
    </tr>
  </tbody>
</table>
```

---

## Claude Code 작업 가이드

### 세션 시작 프롬프트 템플릿

```
README.md와 progress.md 읽고 현재 상태 파악해줘.
오늘 작업 목표: [여기에 작업 내용 입력]
index.html 기준으로 작업해줘.
```

### 작업 규칙

1. **항상 index.html 단일 파일 기준** — 외부 CSS/JS 파일 분리하지 않음
2. **새 단계 추가 시** — nav-item + section + SECTIONS 객체 동시 수정
3. **체크리스트 항목 수 변경 시** — `prog-label-sN`의 `0 / N` 숫자도 업데이트
4. **검색 대상 확장 시** — `searchIndex`에 push하는 selector 추가
5. **스타일 수정 시** — CSS 변수(`--bg-primary` 등) 기준으로만 색상 처리, 하드코딩 금지

### 자주 쓰는 Claude Code 명령

```bash
# 모델 확인 및 전환
/status
/model sonnet

# 현재 세션 진행 상황 체크포인트 저장 요청
"현재 작업 상태 progress.md에 업데이트해줘"
```

---

## 작업 로그

| 날짜 | 작업 내용 | 비고 |
|------|-----------|------|
| 2026-06-19 | 초기 구조 생성 (10단계, 기본 컴포넌트 세트) | Claude.ai에서 생성 |

---

## 디벨롭 아이디어 (백로그)

- **클라이언트 필터**: 상단에 클라이언트 탭 추가, 단계별로 클라이언트별 주의사항 분기
- **스크린샷 영역**: `<figure class="screenshot">` 컴포넌트 추가
- **진행 상태 저장**: localStorage로 체크박스 상태 유지 (브라우저 닫아도 유지)
- **트러블슈팅 섹션**: 자주 발생하는 에러별 해결법 별도 섹션으로 추가
- **인쇄 모드**: `@media print` 스타일로 PDF 출력 최적화
