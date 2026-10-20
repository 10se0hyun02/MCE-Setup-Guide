"""
솔타메디칼 현업 인터뷰 기반 요건정의 PPT 생성기 (TEST)
구성: 표지 / 목차 / 마케팅팀 / 세일즈팀 / 방향성 Summary / 아키텍처 / 끝장표
폰트: Noto Sans KR
"""

import os
from pptx import Presentation
from pptx.util import Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "솔타메디칼_PPT_base.pptx")
OUT  = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "솔타메디칼_현업인터뷰기반요건정의_TEST_V0.1.pptx")

# ── 색상 ─────────────────────────────────────────────────────────────────
NAVY    = RGBColor(0x0E, 0x28, 0x41)
BLUE    = RGBColor(0x15, 0x60, 0x82)
BLUE_LT = RGBColor(0xD6, 0xE8, 0xF5)
GRAY_LT = RGBColor(0xF4, 0xF6, 0xF8)
GRAY_BD = RGBColor(0xD0, 0xD5, 0xDD)
ORANGE  = RGBColor(0xE9, 0x71, 0x32)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
DARK    = RGBColor(0x1A, 0x1A, 0x2E)
MID     = RGBColor(0x55, 0x55, 0x77)
AMBER   = RGBColor(0xF2, 0xB1, 0x34)
GREEN   = RGBColor(0x19, 0x6B, 0x24)

FONT = "Noto Sans KR"

# ── 레이아웃 기준값 (cm) ──────────────────────────────────────────────────
# 슬라이드 33.9 × 19.1 cm  /  B5 레이아웃 푸터 y≈17cm
MARGIN_L   = 1.601      # subtitle placeholder left와 동일 (측정값)
CONTENT_W  = 28.888     # subtitle width와 동일 (측정값)
CONTENT_TOP = 4.5       # 소제목(y≈2.5+높이) 아래 여백 확보
CONTENT_BOT = 16.4      # 푸터 위 여백 y

# ─────────────────────────────────────────────────────────────────────────
# 헬퍼
# ─────────────────────────────────────────────────────────────────────────

def _fmt_para(para, size, bold, color, align, line_sp=1.15):
    para.alignment = align
    para.space_before = Pt(0)
    para.space_after  = Pt(0)
    from pptx.util import Pt as _Pt
    from pptx.oxml.ns import qn
    pPr = para._pPr
    if pPr is None:
        pPr = para._p.get_or_add_pPr()
    lnSpc = pPr.get_or_add_lnSpc()
    spcPct = lnSpc.get_or_add_spcPct()
    spcPct.set("val", str(int(line_sp * 100000)))


def textbox(slide, text, l, t, w, h,
            size=11, bold=False, color=DARK, align=PP_ALIGN.LEFT,
            italic=False, line_sp=1.2):
    txb = slide.shapes.add_textbox(Cm(l), Cm(t), Cm(w), Cm(h))
    tf  = txb.text_frame
    tf.word_wrap = True
    para = tf.paragraphs[0]
    para.alignment = align
    run = para.add_run()
    run.text = text
    run.font.name  = FONT
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.color.rgb = color
    run.font.italic = italic
    return txb


def mlbox(slide, lines, l, t, w, h,
          size=11, bold=False, color=DARK, align=PP_ALIGN.LEFT, line_sp=1.3):
    """여러 줄 텍스트박스. lines: list[str] 또는 '\n' 포함 str."""
    if isinstance(lines, str):
        lines = lines.split("\n")
    txb = slide.shapes.add_textbox(Cm(l), Cm(t), Cm(w), Cm(h))
    tf  = txb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_before = Pt(1)
        p.space_after  = Pt(1)
        run = p.add_run()
        run.text = line
        run.font.name  = FONT
        run.font.size  = Pt(size)
        run.font.bold  = bold
        run.font.color.rgb = color
    return txb


def box(slide, l, t, w, h, fill,
        text="", size=11, tc=WHITE, bold=False, align=PP_ALIGN.LEFT,
        border=None, pad=0.25):
    """채색 사각형 + 텍스트. pad: 텍스트 안쪽 여백(cm)."""
    sh = slide.shapes.add_shape(1, Cm(l), Cm(t), Cm(w), Cm(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if border:
        sh.line.color.rgb = border
        sh.line.width = Pt(0.5)
    else:
        sh.line.fill.background()
    if text:
        tf = sh.text_frame
        tf.word_wrap = True
        tf.margin_left   = Cm(pad)
        tf.margin_right  = Cm(pad)
        tf.margin_top    = Cm(pad * 0.8)
        tf.margin_bottom = Cm(pad * 0.8)
        p = tf.paragraphs[0]
        p.alignment = align
        run = p.add_run()
        run.text = text
        run.font.name  = FONT
        run.font.size  = Pt(size)
        run.font.bold  = bold
        run.font.color.rgb = tc
    return sh


def mlbox_in_box(slide, lines, l, t, w, h, fill,
                 size=11, tc=DARK, pad=0.3):
    """채색 배경 + 여러 줄 텍스트."""
    sh = slide.shapes.add_shape(1, Cm(l), Cm(t), Cm(w), Cm(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.fill.background()
    tf = sh.text_frame
    tf.word_wrap = True
    tf.margin_left   = Cm(pad)
    tf.margin_right  = Cm(pad)
    tf.margin_top    = Cm(pad * 0.7)
    tf.margin_bottom = Cm(pad * 0.7)
    if isinstance(lines, str):
        lines = lines.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_before = Pt(1.5)
        p.space_after  = Pt(1.5)
        run = p.add_run()
        run.text = line
        run.font.name  = FONT
        run.font.size  = Pt(size)
        run.font.color.rgb = tc
    return sh


def hline(slide, l, t, w, color=GRAY_BD, thickness=0.04):
    sh = slide.shapes.add_shape(1, Cm(l), Cm(t), Cm(w), Cm(thickness))
    sh.fill.solid()
    sh.fill.fore_color.rgb = color
    sh.line.fill.background()
    return sh


def add_b5_slide(prs, title, subtitle):
    lmap = {l.name: l for l in prs.slide_master.slide_layouts}
    slide = prs.slides.add_slide(lmap["B5 - Graphic Footer - 3 Column"])
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == 0:
            ph.text = title
            for p in ph.text_frame.paragraphs:
                for r in p.runs:
                    r.font.name = FONT
        elif ph.placeholder_format.idx == 5:
            ph.text = subtitle
            for p in ph.text_frame.paragraphs:
                for r in p.runs:
                    r.font.name = FONT
    return slide


def two_col(slide, left_data, right_data):
    """
    2컬럼 공통 레이아웃.
    data = {"header": str, "header_color": RGB,
            "blocks": [{"title": str, "lines": [str], "title_color": RGB}]}
    """
    col_w = (CONTENT_W - 0.7) / 2   # 두 컬럼 균등 분할, 간격 0.7cm
    cols = [
        (MARGIN_L,                col_w),
        (MARGIN_L + col_w + 0.7,  col_w),
    ]
    for data, (cx, cw) in zip([left_data, right_data], cols):
        # 컬럼 헤더 바
        box(slide, cx, CONTENT_TOP, cw, 0.75,
            data["header_color"], data["header"],
            size=12, bold=True, tc=WHITE, align=PP_ALIGN.LEFT, pad=0.3)

        by = CONTENT_TOP + 0.75 + 0.4
        block_h = (CONTENT_BOT - by) / len(data["blocks"])

        for bi, blk in enumerate(data["blocks"]):
            # 블록 제목
            textbox(slide, blk["title"],
                    cx + 0.1, by, cw - 0.2, 0.6,
                    size=11, bold=True, color=blk.get("title_color", data["header_color"]))
            # 구분선
            hline(slide, cx + 0.1, by + 0.62, cw - 0.2, data["header_color"])
            # 내용
            mlbox(slide, blk["lines"],
                  cx + 0.2, by + 0.75, cw - 0.4,
                  block_h - 1.1,
                  size=10.5, color=DARK, line_sp=1.5)
            by += block_h


# ─────────────────────────────────────────────────────────────────────────
prs = Presentation(BASE)

# ── 1. 표지 ──────────────────────────────────────────────────────────────
cover = prs.slides[0]
for shape in cover.shapes:
    if not shape.has_text_frame:
        continue
    for para in shape.text_frame.paragraphs:
        for run in para.runs:
            run.font.name = FONT
            if "[보고서 제목]" in run.text:
                run.text = run.text.replace("[보고서 제목]", "현업 인터뷰 기반 요건정의")
            if "[YYYY.MM.DD]" in run.text:
                run.text = run.text.replace("[YYYY.MM.DD]", "2026.10")


# ── 2. 목차 ──────────────────────────────────────────────────────────────
s = add_b5_slide(prs, "목차", "현업 인터뷰 기반 요건정의 — 문서 구성")

items = [
    ("01", "마케팅팀 인터뷰 결과",          "HCP·소비자 마케팅 담당자 인터뷰 주요 발견 및 니즈"),
    ("02", "세일즈팀 인터뷰 결과",          "국내 영업 담당자 인터뷰 주요 발견 및 니즈"),
    ("03", "프로젝트 요건 방향성 Summary",  "인터뷰 기반 시나리오 선정 방향 및 우선순위"),
    ("04", "To-Be 아키텍처 (개요)",         "Data Cloud 중심 데이터 흐름 및 캠페인 채널 구성"),
]

total_h  = CONTENT_BOT - CONTENT_TOP          # 12.7 cm
row_h    = total_h / len(items)               # ~3.17 cm per item
gap_x    = 0.55                               # 번호 박스 오른쪽 간격

for i, (num, title, desc) in enumerate(items):
    t = CONTENT_TOP + i * row_h + 0.25

    # 번호 박스
    box(s, MARGIN_L, t, 1.6, row_h - 0.5, NAVY,
        num, size=22, bold=True, tc=WHITE, align=PP_ALIGN.CENTER)

    # 제목
    textbox(s, title,
            MARGIN_L + 1.6 + gap_x, t + 0.25,
            CONTENT_W - 1.6 - gap_x, 0.75,
            size=14, bold=True, color=DARK)

    # 구분선
    hline(s, MARGIN_L + 1.6 + gap_x, t + 1.1,
          CONTENT_W - 1.6 - gap_x, GRAY_BD)

    # 설명
    textbox(s, desc,
            MARGIN_L + 1.6 + gap_x, t + 1.25,
            CONTENT_W - 1.6 - gap_x, 0.7,
            size=11, color=MID)


# ── 3. 마케팅팀 인터뷰 ───────────────────────────────────────────────────
s = add_b5_slide(prs, "마케팅팀 인터뷰 결과",
                 "HCP 마케팅·콘텐츠 제작(RA/QA)  |  10.08 · 10.12 진행")

two_col(
    s,
    left_data={
        "header": "  현황 (AS-IS)",
        "header_color": BLUE,
        "blocks": [
            {"title": "Pain Point",
             "lines": [
                 "• 행사 초청·리마인드 · 사후 설문 등 과정 수작업 진행",
                 "• 마케팅 발송에 대한 인게이지먼트 데이터 미연동",
                 "• 수신 동의 고객 약 300~400명",
                 "• 웹사이트 DB ↔ Data Cloud 미연동",
                 "• 노쇼율 평균 20%, 만족도 회수율 20~30% (수기 관리중)",
             ]},
            {"title": "보유 데이터 & 심의 현황 (RAQA)",
             "lines": [
                 "• 수신 동의: 웹사이트 DB (8/29 이후부터 수집, B2B/B2C 구분)",
                 "• 행사 등록: 별도 DB 관리 (SF 미연동)",
                 "",
                 "[참고]▸ 콘텐츠 심의",
                 "• 이메일·카카오·문자 모두 심의 대상",
                 "• 심의 소요 3~4주 (행정 10일 + 에이전시)",
                 "• 유효기간 (추가 확인 필요) / 개인화 필드 재심의 불필요",
             ]},
        ],
    },
    right_data={
        "header": "  니즈 및 요건 (TO-BE)",
        "header_color": ORANGE,
        "blocks": [
            {"title": "주요 니즈",
             "lines": [
                 "• B2B 대상 캠페인 발송 자동화",
                 "  (예 : 행사 초청 → 리마인더 → 참석 확인 → 사후 설문)",
                 "• 세그먼트별 발송",
                 "  (잠재/신규/Active/업셀·크로스셀/이탈)",
                 "• 오픈율·클릭률 기반 넥스트 콘텐츠 연결 (CTA)",
                 "• 채널: 단문=카카오, 뉴스레터=이메일",
             ]},
            {"title": "확인 필요 (Open Items)",
             "lines": [
                 "• 웹사이트 DB → Data Cloud 연동 방식 확정",
                 "• 행사 등록 DB → 세일즈포스 연동 방식 결정",
                 "• 시나리오 콘텐츠 심의 일정 선반영",
                 "  (착수 즉시 에이전시 심의 요청 필요)",
             ]},
        ],
    },
)


# ── 4. 세일즈팀 인터뷰 ───────────────────────────────────────────────────
s = add_b5_slide(prs, "세일즈팀 인터뷰 결과",
                 "국내 영업 담당자  |  10.12 진행")

two_col(
    s,
    left_data={
        "header": "  현황 (AS-IS)",
        "header_color": BLUE,
        "blocks": [
            {"title": "Pain Point",
             "lines": [
                 "• 매출 데이터 SF 미연동 — 담당자·거래처별 추적 불가",
                 "• 소모품(팁) 매출: 총판 경유, SFDC 미입력",
                 "• 리드 상세 정보 엑셀 별도 관리 (SF에 숫자만)",
                 "• APAC 공용 org — KR 세팅 불일치, 타국 데이터 혼재",
             ]},
            {"title": "보유 데이터",
             "lines": [
                 "• Account: 고객사 전체 입력됨",
                 "• Opportunity: 장비 영업 단계 기록",
                 "  (초기 → 데모 → Closed Won/Lost)",
                 "• Task: 계정별 데일리 콜 기록",
                 "• 소모품 매출: 총판 경로, SF 미반영",
                 "• D365 일부 연동 (정확도 미확인)",
             ]},
        ],
    },
    right_data={
        "header": "  니즈 및 요건 (TO-BE)",
        "header_color": ORANGE,
        "blocks": [
            {"title": "주요 니즈",
             "lines": [
                 "• 담당자별·거래처별 매출 대시보드",
                 "• Opportunity 금액 연동 → 예상 매출 자동 집계",
                 "• 마케팅 메시지 선발송 후 영업 팔로업 연계",
             ]},
            {"title": "확인 필요 (Open Items)",
             "lines": [
                 "• 소모품(팁) 매출 → SF 연동 가능 여부",
                 "  (총판 경로 데이터 처리 방식 확인)",
             ]},
        ],
    },
)


# ── 5. 인터뷰 요건정의 Summary ────────────────────────────────────────────
s = add_b5_slide(prs, "인터뷰 요건정의 Summary",
                 "팀별 핵심 요건 및 공통 선결 과제")

two_col(
    s,
    left_data={
        "header": "  마케팅팀 핵심 요건",
        "header_color": BLUE,
        "blocks": [
            {"title": "자동화·커뮤니케이션 요건",
             "lines": [
                 "• 행사: 초청→리마인더→참석 확인→사후 설문 발송 자동화",
                 "  (KPI : 노쇼율 감소 / 참석자 만족도 향상 목표)",
                 "• 세그먼트별 발송",
                 "  잠재 / 신규 / Active / 업셀·크로스셀 / 이탈",
                 "• 오픈율·클릭률 기반 넥스트 콘텐츠 연결 (CTA)",
                 "• 마케팅 발송 채널: 단문=카카오 알림톡, 뉴스레터=이메일",
             ]},
            {"title": "콘텐츠 심의 제약 (RAQA)",
             "lines": [
                 "• 이메일·카카오·문자 전부 심의 필요",
                 "• 심의 소요 3~4주 → 시나리오 착수 즉시 준비 필요",
                 "• 개인화 필드(고객명·병원명) 재심의 불필요",
                 "  → 템플릿 1회 심의로 개인화 발송 가능",
             ]},
        ],
    },
    right_data={
        "header": "  세일즈팀 핵심 요건",
        "header_color": ORANGE,
        "blocks": [
            {"title": "대시보드·보고 요건",
             "lines": [
                 "• 담당자별·거래처별 매출 확인",
                 "• Opportunity 금액 연동 → 예상 매출 자동 집계",
                 "• MC 메시지 선발송 → 영업 팔로업 연계",
             ]},
            {"title": "공통 선결 과제 (Open Items)",
             "lines": [
                 "• 웹사이트 DB → Data Cloud 연동 방식 확정",
                 "• 행사 등록 DB → Salesforce 연동 방식 결정",
                 "• 수신 동의 모수 확보 (현 300~400명 → 목표 1,700명)",
                 "• 콘텐츠 심의 일정 고려한 마케팅 메시지 콘텐츠 제작",
             ]},
        ],
    },
)


# ── 6. 아키텍처 ──────────────────────────────────────────────────────────
s = add_b5_slide(prs, "To-Be 아키텍처 (개요)",
                 "Data Cloud 중심 데이터 통합 → MC Next 캠페인 → 채널 발송")

KAKAO_Y = RGBColor(0xF9, 0xE0, 0x00)
LINE_C  = RGBColor(0xCC, 0xCC, 0xCC)

# ── 범례 ─────────────────────────────────────────────────────────────────
leg_y = CONTENT_TOP + 0.05
leg_items = [("[기존]", NAVY), ("[+ 신규 구성]", BLUE),
             ("[미확정·확인 필요]", ORANGE), ("[범위 제외]", GRAY_BD)]
lw = (CONTENT_W - 0.6) / 4
for i, (leg_t, leg_c) in enumerate(leg_items):
    box(s, MARGIN_L + i*(lw+0.2), leg_y, lw, 0.48, leg_c,
        leg_t, size=9, bold=True, tc=WHITE, align=PP_ALIGN.CENTER, pad=0.15)

# ── 존 좌표 ──────────────────────────────────────────────────────────────
ZY = CONTENT_TOP + 0.65
ZH = 9.8
ZB = ZY + ZH

SOLTA_X = MARGIN_L;                SOLTA_W = 6.2
SF_X    = SOLTA_X + SOLTA_W + 0.5; SF_W    = 13.6
MIL_X   = SF_X + SF_W + 0.5;       MIL_W   = 3.6
CHAN_X  = MIL_X + MIL_W + 0.4
CHAN_W  = MARGIN_L + CONTENT_W - CHAN_X

# ── 도메인 배경 (통일된 연회색) ──────────────────────────────────────────
for _dx, _dw in [(SOLTA_X, SOLTA_W), (SF_X, SF_W), (MIL_X, MIL_W)]:
    box(s, _dx, ZY, _dw, ZH, GRAY_LT, border=GRAY_BD)

# 도메인 소제목 + 구분선
def domain_hdr(sld, x, y, w, title, color=NAVY):
    textbox(sld, title, x+0.2, y+0.1, w-0.4, 0.42, size=9, bold=True, color=color)
    hline(sld, x+0.2, y+0.58, w-0.4, color=LINE_C, thickness=0.03)

domain_hdr(s, SOLTA_X, ZY, SOLTA_W, "Solta Medical", NAVY)
domain_hdr(s, SF_X,    ZY, SF_W,    "Salesforce",    BLUE)
domain_hdr(s, MIL_X,   ZY, MIL_W,  "Milvus",        GREEN)
textbox(s, "채널", CHAN_X, ZY+0.1, CHAN_W, 0.42, size=9, bold=True, color=DARK)
hline(s, CHAN_X, ZY+0.58, CHAN_W, color=LINE_C, thickness=0.03)

# ── 컴포넌트 치수 ─────────────────────────────────────────────────────────
CW_S  = SOLTA_W - 0.6
CW_SF = (SF_W - 1.0) / 3
CH    = 1.75

# ── Solta 컴포넌트 ────────────────────────────────────────────────────────
SY = [ZY + 0.72 + i * (CH + 0.5) for i in range(4)]
box(s, SOLTA_X+0.3, SY[0], CW_S, CH, NAVY,   "영업 담당자\n(기존)",                size=10, tc=WHITE, align=PP_ALIGN.CENTER, pad=0.2)
box(s, SOLTA_X+0.3, SY[1], CW_S, CH, ORANGE, "채널톡\n(미확정·확인 필요)",         size=10, tc=WHITE, align=PP_ALIGN.CENTER, pad=0.2)
box(s, SOLTA_X+0.3, SY[2], CW_S, CH, NAVY,   "Web Site\n(Thermage.co.kr)\n(기존)", size=9,  tc=WHITE, align=PP_ALIGN.CENTER, pad=0.2)
box(s, SOLTA_X+0.3, SY[3], CW_S, CH, NAVY,   "홈페이지 DB\n(기존)",               size=10, tc=WHITE, align=PP_ALIGN.CENTER, pad=0.2)

# ── Salesforce 컴포넌트 ───────────────────────────────────────────────────
SC_X  = SF_X + 0.3
DC_X  = SC_X + CW_SF + 0.2
MCN_X = DC_X + CW_SF + 0.2

SC_Y  = ZY + 0.72
DC_Y  = SC_Y + CH + 0.5
MCN_Y = ZY + 0.72

box(s, SC_X,  SC_Y,  CW_SF, CH*2+0.5, NAVY, "Sales Cloud /\nService Cloud\n(기존)",              size=10, tc=WHITE, align=PP_ALIGN.CENTER, pad=0.2)
box(s, DC_X,  DC_Y,  CW_SF, CH*2,     BLUE, "Data Cloud\n(+ 신규 구성)",                         size=10, bold=True, tc=WHITE, align=PP_ALIGN.CENTER, pad=0.2)
box(s, MCN_X, MCN_Y, CW_SF, CH*3+1.0, BLUE, "Marketing Cloud\nNext (Advanced)\n(+ 신규 구성)",   size=10, bold=True, tc=WHITE, align=PP_ALIGN.CENTER, pad=0.2)

# ── Milvus ────────────────────────────────────────────────────────────────
MIL_CY = ZY + 1.8
box(s, MIL_X+0.3, MIL_CY, MIL_W-0.6, CH*2.8, BLUE, "miCRM\n\n(+ 신규 구성)", size=10, bold=True, tc=WHITE, align=PP_ALIGN.CENTER, pad=0.2)

# ── 채널 박스 ─────────────────────────────────────────────────────────────
CHAN_CH = 1.8
CHAN_CY = ZY + 0.72
box(s, CHAN_X, CHAN_CY,                    CHAN_W, CHAN_CH, BLUE,    "Email\n발송",    size=10, tc=WHITE, align=PP_ALIGN.CENTER, pad=0.2)
box(s, CHAN_X, CHAN_CY + CHAN_CH + 0.55,   CHAN_W, CHAN_CH, KAKAO_Y, "카카오\n알림톡", size=10, tc=DARK,  align=PP_ALIGN.CENTER, pad=0.2)
box(s, CHAN_X, CHAN_CY + (CHAN_CH+0.55)*2, CHAN_W, CHAN_CH, GRAY_BD, "SMS\n발송",     size=10, tc=DARK,  align=PP_ALIGN.CENTER, pad=0.2)

# ── 연결 레이블 (배경 박스로 가시성 확보) ────────────────────────────────
def conn(sld, x, y, text, w=2.6, dashed=False):
    tc_ = ORANGE if dashed else MID
    box(sld, x, y, w, 0.38, GRAY_LT, text, size=8, tc=tc_, align=PP_ALIGN.LEFT, pad=0.1, border=LINE_C)

ARR_X = SOLTA_X + SOLTA_W + 0.08
conn(s, ARR_X, SY[0]+CH/2-0.19, "→ 리드 생성")
conn(s, ARR_X, SY[1]+CH/2-0.19, "⤳ 리드 생성 (미확정)", dashed=True)
conn(s, ARR_X, SY[2]+0.1,       "→ 리드 생성")
conn(s, ARR_X, SY[2]+0.6,       "→ 웹 행동 데이터 (SDK)")
conn(s, ARR_X, SY[2]+1.1,       "→ 수신 동의 적재")

conn(s, SC_X,             SC_Y+CH*2+0.55, "↓ CRM 데이터 전달",    w=CW_SF)
conn(s, DC_X+CW_SF+0.1,  DC_Y+CH*0.55,   "→ 세그먼트 활성화")
conn(s, DC_X+CW_SF+0.1,  DC_Y+CH*1.3,    "← Email 반응")
conn(s, MCN_X+CW_SF+0.1, MCN_Y+CH*0.4,   "→ Email 직접 발송")
conn(s, MCN_X+CW_SF+0.1, MCN_Y+CH*1.5,   "→ 발송 연동")
conn(s, MIL_X-2.65,      MIL_CY+CH*2.8+0.1, "← 발송 이력 전송")

for _i in range(3):
    textbox(s, "▶", CHAN_X-0.5, CHAN_CY + _i*(CHAN_CH+0.55) + 0.65,
            0.45, 0.38, size=11, bold=True, color=GRAY_BD, align=PP_ALIGN.CENTER)

# ── 범위 제외 영역 ────────────────────────────────────────────────────────
OOS_Y = ZB + 0.2
box(s, MARGIN_L, OOS_Y, CONTENT_W, 0.55, GRAY_BD,
    "  [범위 제외]   D365 ↔ Sales Cloud / Service Cloud   |   D365 →(BYOD)→ Power BI   |   Power BI ··· Data Cloud",
    size=9, tc=WHITE, pad=0.2)
textbox(s, "※ 실선: 연동 확정  |  점선(⤳): 미확정  |  범위 제외 시스템은 점선 표기",
        MARGIN_L, OOS_Y+0.65, CONTENT_W, 0.4, size=8, color=MID, italic=True)


# ── 끝장표를 마지막으로 이동 ─────────────────────────────────────────────
sldIdLst = prs.slides._sldIdLst
ty = sldIdLst[1]
sldIdLst.remove(ty)
sldIdLst.append(ty)

# ── 저장 ─────────────────────────────────────────────────────────────────
prs.save(OUT)

verify = Presentation(OUT)
print(f"저장 완료: {OUT}")
print(f"슬라이드 수: {len(verify.slides)}")
for i, sl in enumerate(verify.slides):
    print(f"  [{i+1}] {sl.slide_layout.name}")
