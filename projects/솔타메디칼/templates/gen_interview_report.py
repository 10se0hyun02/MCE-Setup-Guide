"""
솔타메디칼 현업 인터뷰 결과 보고서 생성기
기존 B5 템플릿(솔타메디칼_PPT_base.pptx) 기반
구성: 표지 / Summary / 인터뷰 개요 / 고객 여정 / 부서별 발견 / 데이터 AS-IS / 아키텍처 / 추천 시나리오
"""

import os
from pptx import Presentation
from pptx.util import Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "솔타메디칼_PPT_base.pptx")
OUT  = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "솔타메디칼_현업인터뷰결과보고서_V0.1.pptx")

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
TEAL_LT = RGBColor(0xE6, 0xF2, 0xF3)
TEAL    = RGBColor(0x0D, 0x6E, 0x79)
WARM_LT = RGBColor(0xFC, 0xE9, 0xE3)
COOL_LT = RGBColor(0xF3, 0xF5, 0xF8)
GREEN   = RGBColor(0x19, 0x6B, 0x24)

FONT = "Noto Sans KR"

# ── 레이아웃 기준값 (B5 기준, cm) ─────────────────────────────────────────
MARGIN_L   = 1.601
CONTENT_W  = 28.888
CONTENT_TOP = 4.5
CONTENT_BOT = 16.4

# ─────────────────────────────────────────────────────────────────────────
# 헬퍼 (gen_requirements.py와 동일)
# ─────────────────────────────────────────────────────────────────────────

def _fmt_para(para, size, bold, color, align, line_sp=1.15):
    para.alignment = align
    para.space_before = Pt(0)
    para.space_after  = Pt(0)
    pPr = para._pPr
    if pPr is None:
        pPr = para._p.get_or_add_pPr()
    lnSpc = etree.SubElement(pPr, qn("a:lnSpc"))
    spcPct = etree.SubElement(lnSpc, qn("a:spcPct"))
    spcPct.set("val", str(int(line_sp * 100000)))


def textbox(slide, text, l, t, w, h, size=11, bold=False,
            color=DARK, align=PP_ALIGN.LEFT, italic=False, line_sp=1.2):
    txb = slide.shapes.add_textbox(Cm(l), Cm(t), Cm(w), Cm(h))
    tf  = txb.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    para = tf.paragraphs[0]
    _fmt_para(para, size, bold, color, align, line_sp)
    run = para.add_run()
    run.text = text
    run.font.size   = Pt(size)
    run.font.bold   = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name   = FONT
    return txb


def mlbox(slide, lines, l, t, w, h, size=11, bold=False,
          color=DARK, align=PP_ALIGN.LEFT, line_sp=1.3):
    txb = slide.shapes.add_textbox(Cm(l), Cm(t), Cm(w), Cm(h))
    tf  = txb.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    for i, line in enumerate(lines):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        _fmt_para(para, size, bold, color, align, line_sp)
        run = para.add_run()
        run.text = line
        run.font.size  = Pt(size)
        run.font.bold  = bold
        run.font.color.rgb = color
        run.font.name  = FONT
    return txb


def box(slide, l, t, w, h, fill, text="", size=11, tc=WHITE,
        bold=False, align=PP_ALIGN.LEFT, border=None, pad=0.25, italic=False):
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
        tf.auto_size = None
        body = tf._txBody
        bodyPr = body.find(qn("a:bodyPr"))
        if bodyPr is None:
            bodyPr = etree.SubElement(body, qn("a:bodyPr"))
        pi = str(int(Cm(pad).emu / 914400 * 360000))
        bodyPr.set("lIns", pi); bodyPr.set("rIns", pi)
        bodyPr.set("tIns", pi); bodyPr.set("bIns", pi)
        bodyPr.set("anchor", "ctr")
        para = tf.paragraphs[0]
        _fmt_para(para, size, bold, tc, align)
        for i, seg in enumerate(text.split("\n")):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            if i > 0:
                _fmt_para(p, size, bold, tc, align)
            run = p.add_run()
            run.text = seg
            run.font.size   = Pt(size)
            run.font.bold   = bold
            run.font.italic = italic
            run.font.color.rgb = tc
            run.font.name   = FONT
    return sh


def hline(slide, l, t, w, color=GRAY_BD, thickness=0.04):
    sh = slide.shapes.add_shape(1, Cm(l), Cm(t), Cm(w), Cm(thickness))
    sh.fill.solid()
    sh.fill.fore_color.rgb = color
    sh.line.fill.background()
    return sh


def set_cell(cell, text, color=None, tc=DARK, size=10, bold=False,
             align=PP_ALIGN.LEFT):
    if color:
        try:
            cell.fill.solid()
            cell.fill.fore_color.rgb = color
        except Exception:
            pass
    tf = cell.text_frame
    tf.word_wrap = True
    for para in tf.paragraphs:
        for run in para.runs:
            run.text = ""
    tf.paragraphs[0].alignment = align
    run = tf.paragraphs[0].add_run()
    run.text = text
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.color.rgb = tc
    run.font.name  = FONT


def add_b5_slide(prs, title, subtitle):
    lmap  = {l.name: l for l in prs.slide_master.slide_layouts}
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


# ─────────────────────────────────────────────────────────────────────────
prs = Presentation(BASE)

# ── 표지 ─────────────────────────────────────────────────────────────────
cover = prs.slides[0]
for shape in cover.shapes:
    if not shape.has_text_frame:
        continue
    for para in shape.text_frame.paragraphs:
        for run in para.runs:
            run.font.name = FONT
            if "[보고서 제목]" in run.text:
                run.text = run.text.replace("[보고서 제목]", "현업 인터뷰 결과 보고 및 프로젝트 방향성")
            if "[YYYY.MM.DD]" in run.text:
                run.text = run.text.replace("[YYYY.MM.DD]", "2026.10")


# ═══════════════════════════════════════════════════════════════════════════
# 슬라이드 2  프로젝트 방향성 Summary
# ═══════════════════════════════════════════════════════════════════════════
s = add_b5_slide(prs, "프로젝트 방향성 Summary",
                 "재구매 성장을 위한 자동화 시나리오 3개를 설계합니다.")

CARDS = [
    ("1", "목표",
     ["장비 설치는 포화, 다음 성장 동력은 소모품(팁) 재구매",
      "세그먼트별 메시지로 세일즈를 끌어올리는 CRM 마케팅이 최우선 과제"]),
    ("2", "현황",
     ["고객 데이터가 홈페이지 DB · Salesforce · D365 · 엑셀에 흩어져 있고 Data Cloud와 미연동",
      "마케팅 수신 동의 HCP 약 300~400명, 팁 판매는 대리점 엑셀로만 관리"]),
    ("3", "방향",
     ["B2B 자동화 시나리오 3개 설계 프로젝트",
      "캠페인 내용은 솔타메디칼 코리아 내부 협의 후 전달"]),
    ("4", "요청",
     ["시나리오 3개 우선순위 결정 (10/17 제안)",
      "콘텐츠 심의 3~4주 소요되므로, 콘텐츠 Assets 우선 전달 필요"]),
]

CW = (CONTENT_W - 0.5) / 2
CH = (CONTENT_BOT - CONTENT_TOP - 0.5) / 2
CX = [MARGIN_L, MARGIN_L + CW + 0.5]
CY = [CONTENT_TOP, CONTENT_TOP + CH + 0.5]

for idx, (num, lbl, lines) in enumerate(CARDS):
    cx = CX[idx % 2]
    cy = CY[idx // 2]
    box(s, cx, cy, CW, CH, GRAY_LT, border=GRAY_BD, pad=0)
    box(s, cx+0.6, cy+0.6, 1.2, 1.2, BLUE, num,
        size=13, tc=WHITE, bold=True, align=PP_ALIGN.CENTER, pad=0)
    textbox(s, lbl, cx+2.2, cy+0.65, CW-2.8, 1.1,
            size=13, bold=True, color=DARK)
    mlbox(s, lines, cx+0.7, cy+2.2, CW-1.0, CH-2.8,
          size=10.5, color=DARK, line_sp=1.45)


# ═══════════════════════════════════════════════════════════════════════════
# 슬라이드 3  인터뷰 개요
# ═══════════════════════════════════════════════════════════════════════════
s = add_b5_slide(prs, "인터뷰 개요",
                 "4개 부서를 2일에 걸쳐 인터뷰했고, 사전 배포한 질문지에 솔타가 답을 달아 진행했습니다")

TBL_X, TBL_Y = MARGIN_L, CONTENT_TOP
TBL_W, TBL_H = CONTENT_W, 9.5

rows3 = [
    ["일자",        "부서",                  "주제"],
    ["10/8",        "RA/QA",                 "콘텐츠 심의 프로세스 · 사용 불가 표현 · 소요 기간"],
    ["10/8",        "IT",                    "고객 데이터 생성 이벤트 · 시스템별 보유 데이터 · 유입 경로"],
    ["10/12 오전",  "마케팅 (HCP · 소비자)", "고객 여정 · 채널 · 타겟 세그먼트 · 성과 지표 · 시나리오"],
    ["10/12 오후",  "세일즈",                "Salesforce 입력 현황 · 리드 관리 · KPI 대시보드"],
]
col3_w = [TBL_W * r for r in [0.15, 0.23, 0.62]]

tbl3 = s.shapes.add_table(5, 3, Cm(TBL_X), Cm(TBL_Y),
                           Cm(TBL_W), Cm(TBL_H)).table
for ci, cw in enumerate(col3_w):
    tbl3.columns[ci].width = Cm(cw)
for ri, row in enumerate(rows3):
    for ci, txt in enumerate(row):
        is_hdr = (ri == 0)
        set_cell(tbl3.cell(ri, ci), txt,
                 color=NAVY if is_hdr else (GRAY_LT if ri % 2 == 0 else WHITE),
                 tc=WHITE if is_hdr else DARK,
                 size=10.5, bold=is_hdr)

textbox(s, "※ 10/12 2부(소비자·정품 인증)는 녹음 없이 현장 메모로 정리",
        TBL_X, TBL_Y+TBL_H+0.3, TBL_W, 0.6,
        size=9, color=MID, italic=True)


# ═══════════════════════════════════════════════════════════════════════════
# 슬라이드 4  HCP 고객 여정과 접점
# ═══════════════════════════════════════════════════════════════════════════
s = add_b5_slide(prs, "HCP 고객 여정과 접점",
                 "장비를 도입한 뒤에도 팁(소모품)을 계속 사야 유지되는 구조 — 반복 구매의 중심은 팁")

STAGES = [
    ("문제 인식",  "학회 · 심포지엄\n디지털·의료 매체 광고\n브랜드 캠페인",          NAVY,   COOL_LT),
    ("정보 탐색",  "홈페이지 (HCP 로그인)\n세미나 · 담당 영업사원",                   NAVY,   COOL_LT),
    ("평가",       "영업사원 방문 상담·데모\n임상 자료·교육",                          NAVY,   COOL_LT),
    ("도입·구매",  "세일즈 계약\n설치 · 초기 제품 교육",                               NAVY,   COOL_LT),
    ("정착",       "뉴 유저 워크숍\nTTT · 학술 세미나",                                NAVY,   COOL_LT),
    ("반복 구매",  "팁 재구매\n600→900샷 업셀\n아이팁 크로스셀",                       ORANGE, WARM_LT),
    ("추천",       "MTL 포럼\nKOL 관리 · 서티 카드",                                  GREEN,  TEAL_LT),
]

N = len(STAGES)
COL_W  = (CONTENT_W - (N-1) * 0.15) / N   # ≈ 3.98
PITCH  = COL_W + 0.15
HDR_H  = 1.85
CARD_H = 5.8
HDR_Y  = CONTENT_TOP
CARD_Y = HDR_Y + HDR_H + 0.15

for i, (stage, detail, hdr_fill, card_fill) in enumerate(STAGES):
    x = MARGIN_L + i * PITCH
    box(s, x, HDR_Y, COL_W, HDR_H, hdr_fill,
        stage, size=10, tc=WHITE, bold=True, align=PP_ALIGN.CENTER, pad=0.2)
    box(s, x, CARD_Y, COL_W, CARD_H, card_fill,
        detail, size=9.5, tc=DARK, align=PP_ALIGN.LEFT, pad=0.25, border=GRAY_BD)

note = ("이탈 시점    "
        "도입 전 — 관심은 보였으나 상담·데모로 이어지지 않음   ·   "
        "도입 초기 — 사용법·교육 부족으로 팁 구매 저조   ·   "
        "기존 고객 — 3~6개월 미구매는 이탈 위험, 6개월 이상은 휴면 (카피캣 제품으로 이동 우려)")
box(s, MARGIN_L, CARD_Y+CARD_H+0.3, CONTENT_W, 2.5, TEAL_LT,
    note, size=10, tc=DARK, align=PP_ALIGN.LEFT, pad=0.3)


# ═══════════════════════════════════════════════════════════════════════════
# 슬라이드 5  부서별 핵심 발견
# ═══════════════════════════════════════════════════════════════════════════
s = add_b5_slide(prs, "부서별 핵심 발견",
                 "마케팅은 행사·교육 운영의 수작업, 세일즈는 매출 데이터의 엑셀 의존이 가장 큰 불편")

DEPTS = [
    ("마케팅", BLUE, [
        "행사·교육이 가장 반응 좋은 활동이지만 모객이 최대 과제 — 등록이 행사 하루 전에 몰림",
        "디지털 채널은 카카오 채널이 메인, 고객 데이터와는 미연계",
        "홍보는 최소 2개월 전부터 티저 → Save the Date → 초청장 → 리마인더 순",
    ]),
    ("세일즈", NAVY, [
        "영업 약 20명이 Salesforce에 Task · Opportunity · Contact 입력",
        "매출·소모품 매출은 Salesforce에 없어 엑셀로 따로 보고",
        "APAC과 같은 org를 써서 KR 담당자·거래처 정렬이 불편",
    ]),
    ("IT", TEAL, [
        "장비 출고 → Install Base 등록이 현재 유일한 자동 연동",
        "홈페이지 DB에 B2B·B2C 리드·수신 동의가 구분 적재, Data Cloud와 미연동",
        "오더는 D365, Salesforce 연동은 내년 예정",
    ]),
    ("RA/QA", GREEN, [
        "이메일·카카오·문자 발송물 모두 심의 대상 (문구 포함)",
        "개인화 필드(고객명·병원명)는 바뀌어도 재심의 불필요",
        "행정 약 12일, 에이전시 경유로 실제 3~4주",
    ]),
]

DCW = (CONTENT_W - 0.5) / 2
DCH = (CONTENT_BOT - CONTENT_TOP - 0.5) / 2
DCX = [MARGIN_L, MARGIN_L + DCW + 0.5]
DCY = [CONTENT_TOP, CONTENT_TOP + DCH + 0.5]

for idx, (dept, dept_c, bullets) in enumerate(DEPTS):
    cx = DCX[idx % 2]
    cy = DCY[idx // 2]
    box(s, cx, cy, DCW, DCH, GRAY_LT, border=GRAY_BD, pad=0)
    box(s, cx+0.25, cy+0.25, DCW-0.5, 1.0, dept_c, dept,
        size=12, tc=WHITE, bold=True, align=PP_ALIGN.LEFT, pad=0.25)
    lines = ["• " + b for b in bullets]
    mlbox(s, lines, cx+0.35, cy+1.45, DCW-0.7, DCH-1.7,
          size=10.5, color=DARK, line_sp=1.4)


# ═══════════════════════════════════════════════════════════════════════════
# 슬라이드 6  고객 데이터 AS-IS
# ═══════════════════════════════════════════════════════════════════════════
s = add_b5_slide(prs, "고객 데이터 AS-IS",
                 "시나리오에 쓸 데이터가 4곳 이상에 흩어져 있어, 시나리오별로 '있는 데이터'를 먼저 확인해야 합니다")

TBL6_W, TBL6_H = CONTENT_W, 9.0
rows6 = [
    ["데이터",                                 "현재 위치",                        "관리",       "마케팅 활용"],
    ["HCP 리드 · 마케팅 수신 동의",             "홈페이지 DB",                      "마케팅",     "● 연동 필요"],
    ["Account · Contact · Opportunity · Task", "Salesforce",                       "영업",       "● 활용 가능"],
    ["장비 출고 (시리얼 · 품목)",               "Salesforce Install Base (자동)",   "본사",       "● 활용 가능"],
    ["오더",                                    "D365",                             "—",          "● 연동 필요"],
    ["소모품(팁) 병원별 판매",                  "대리점 일 단위 엑셀",              "영업 · CO",  "● 데이터 없음"],
    ["교육 이수 · 서티 · 행사 참석 · 설문",    "수기",                             "마케팅",     "● 데이터 없음"],
]
STATUS_C = {"● 연동 필요": ORANGE, "● 활용 가능": GREEN, "● 데이터 없음": GRAY_BD}
col6_w   = [TBL6_W * r for r in [0.30, 0.30, 0.15, 0.25]]

tbl6 = s.shapes.add_table(7, 4, Cm(MARGIN_L), Cm(CONTENT_TOP),
                           Cm(TBL6_W), Cm(TBL6_H)).table
for ci, cw in enumerate(col6_w):
    tbl6.columns[ci].width = Cm(cw)
for ri, row in enumerate(rows6):
    for ci, txt in enumerate(row):
        cell = tbl6.cell(ri, ci)
        is_hdr = (ri == 0)
        if ci == 3 and txt in STATUS_C:
            set_cell(cell, txt, color=STATUS_C[txt],
                     tc=WHITE, size=10.5, bold=True, align=PP_ALIGN.CENTER)
        else:
            set_cell(cell, txt,
                     color=NAVY if is_hdr else (GRAY_LT if ri % 2 == 0 else WHITE),
                     tc=WHITE if is_hdr else DARK,
                     size=10.5, bold=is_hdr)

textbox(s, "※ 소비자 정품 인증 데이터도 홈페이지 DB에 있으나, 마케팅 의견에 따라 이번에는 B2B(HCP) 우선",
        MARGIN_L, CONTENT_TOP+TBL6_H+0.25, CONTENT_W, 0.6,
        size=9, color=MID, italic=True)


# ═══════════════════════════════════════════════════════════════════════════
# 슬라이드 7  To-Be 아키텍처 (개요)
# ═══════════════════════════════════════════════════════════════════════════
s = add_b5_slide(prs, "To-Be 아키텍처 (개요)",
                 "흩어진 고객 데이터를 Data Cloud로 모아 세그먼트를 만들고, Marketing Cloud에서 채널별로 발송합니다")

# 구역 좌표 (B5 폭 기준)
SRC_X,  SRC_W  = MARGIN_L,       6.0
DC_X,   DC_W   = MARGIN_L+6.8,   5.0
MCN_X,  MCN_W  = MARGIN_L+12.6,  5.0
CHAN_X, CHAN_W  = MARGIN_L+18.4,  6.5
HCP_X,  HCP_W  = MARGIN_L+25.3,  5.19  # → 1.601+25.3+5.19=32.09→우여백ok (합=28.888이내)

AY = CONTENT_TOP + 0.1   # 아키텍처 시작 y
SH = 0.65                # 섹션 헤더 높이
BOX_TOP = AY + SH + 0.3  # 박스 시작 y

# 섹션 헤더
for lbl, sx, sw in [("데이터 원천", SRC_X, SRC_W), ("통합·세그먼트", DC_X, DC_W),
                     ("캠페인·저니", MCN_X, MCN_W), ("채널", CHAN_X, CHAN_W+0.5+HCP_W)]:
    box(s, sx, AY, sw if "채널" not in lbl else CHAN_W+0.5+HCP_W, SH, NAVY,
        lbl, size=9.5, tc=WHITE, bold=True, align=PP_ALIGN.CENTER, pad=0.15)

# 데이터 원천 박스 (4개 세로 배열)
SRC_ITEMS = [
    ("홈페이지 DB\nHCP 리드 · 수신 동의",         WHITE,   True),
    ("Sales Cloud\nAccount · Contact · Install Base", WHITE, True),
    ("D365\n오더 (SF 연동 내년 예정)",             COOL_LT, False),
    ("대리점 엑셀\n팁 판매 (확보 방안 검토)",       COOL_LT, False),
]
sb_h = (CONTENT_BOT - BOX_TOP - 0.3*3) / 4
sy = BOX_TOP
for txt, fill, confirmed in SRC_ITEMS:
    border = GRAY_BD if confirmed else ORANGE
    box(s, SRC_X, sy, SRC_W, sb_h, fill, txt,
        size=9.5, tc=DARK, align=PP_ALIGN.LEFT, pad=0.2, border=border)
    sy += sb_h + 0.3

# 화살표
mid_y = BOX_TOP + (CONTENT_BOT - BOX_TOP) / 2 - 0.3
textbox(s, "→", SRC_X+SRC_W+0.1, mid_y-0.8, 0.6, 0.6, size=16, bold=True, color=MID)
textbox(s, "⤳", SRC_X+SRC_W+0.1, mid_y+0.3, 0.6, 0.6, size=16, bold=True, color=ORANGE)

# Data Cloud
dc_h = CONTENT_BOT - BOX_TOP
box(s, DC_X, BOX_TOP, DC_W, dc_h, TEAL_LT,
    "Data Cloud\n\n통합 프로필\n세그먼트",
    size=11, tc=DARK, bold=True, align=PP_ALIGN.CENTER, pad=0.3, border=TEAL)

textbox(s, "→", DC_X+DC_W+0.05, BOX_TOP+dc_h/2-0.3, 0.7, 0.6, size=16, bold=True, color=MID)

# Marketing Cloud Next
box(s, MCN_X, BOX_TOP, MCN_W, dc_h * 0.65, TEAL_LT,
    "Marketing Cloud\nNext\n\n시나리오(저니) 3개",
    size=11, tc=DARK, bold=True, align=PP_ALIGN.CENTER, pad=0.3, border=TEAL)
box(s, MCN_X, BOX_TOP + dc_h*0.65 + 0.3, MCN_W, dc_h*0.35-0.3, TEAL_LT,
    "Sales Cloud Task\n영업 담당자 팔로업",
    size=10, tc=DARK, align=PP_ALIGN.CENTER, pad=0.25, border=GRAY_BD)

textbox(s, "→", MCN_X+MCN_W+0.05, BOX_TOP+dc_h*0.3-0.3, 0.7, 0.6, size=16, bold=True, color=MID)

# 채널 박스
ch_box_h = (dc_h - 0.3*2) / 3
cy_ch = BOX_TOP
for txt, fill in [("카카오\n알림톡·친구톡", TEAL_LT),
                   ("SMS · LMS",             TEAL_LT),
                   ("이메일",                 TEAL_LT)]:
    box(s, CHAN_X, cy_ch, CHAN_W, ch_box_h, fill, txt,
        size=10, tc=DARK, align=PP_ALIGN.CENTER, pad=0.2, border=TEAL)
    cy_ch += ch_box_h + 0.3

textbox(s, "→", CHAN_X+CHAN_W+0.05, BOX_TOP+dc_h/2-0.3, 0.5, 0.6, size=16, bold=True, color=MID)

# HCP
box(s, HCP_X, BOX_TOP+dc_h/2-1.0, HCP_W, 2.0, WHITE, "HCP",
    size=13, tc=DARK, bold=True, align=PP_ALIGN.CENTER, pad=0.3, border=GRAY_BD)

# 피드백 텍스트
textbox(s, "← 발송·반응 데이터 → Data Cloud",
        DC_X, CONTENT_BOT-0.8, DC_W+0.5+MCN_W, 0.7,
        size=9, color=MID, italic=True, align=PP_ALIGN.CENTER)

# 범례
for i, (leg_txt, leg_fill, leg_tc) in enumerate([
    ("■ 신규 구성",   TEAL_LT, TEAL),
    ("■ 기존 시스템", WHITE,   DARK),
    ("■ 범위 외",     COOL_LT, MID),
]):
    lx = MARGIN_L + i * 5.5
    box(s, lx, CONTENT_BOT+0.15, 4.8, 0.6, leg_fill, leg_txt,
        size=9, tc=leg_tc, pad=0.15, border=GRAY_BD)


# ═══════════════════════════════════════════════════════════════════════════
# 슬라이드 8  추천 시나리오
# ═══════════════════════════════════════════════════════════════════════════
s = add_b5_slide(prs, "추천 시나리오",
                 "행사와 온보딩은 바로 설계 가능하고, 팁 리텐션은 데이터 확보 방안과 함께 결정이 필요합니다")

SCEN = [
    ("A",  BLUE,    "행사 모객 · 참석 관리",
     "트리거  행사 D-60부터 사후 팔로업까지",
     ["티저 → Save the Date → 초청장 (등록 CTA)",
      "미등록자 리마인더 2회, 등록자 D-1 참석 리마인더",
      "참석자 설문 → 다음 프로그램 / 불참자 자료 요약"],
     "KPI  노쇼율 · 설문 회수율 · 등록률"),
    ("B",  BLUE,    "신규 장비 도입 90일 온보딩",
     "트리거  Install Base 신규 장비 등록 시",
     ["환영 · 담당 영업사원 안내 → 사용 가이드",
      "뉴 유저 워크숍 초대 (A와 연결)",
      "D+90 팁 미구매 시 영업 담당자 Task 생성"],
     "KPI  90일 내 첫 팁 재구매율 · 워크숍 참석률"),
    ("?",  GRAY_BD, "팁 리텐션 · 윈백 (후보)",
     "트리거  3~6개월 미구매 / 6개월 이상 휴면",
     ["카피캣 대응으로 우선순위 높음",
      "병원별 팁 구매 데이터가 Salesforce에 없음",
      "대리점 엑셀 정기 적재 가능 여부 확인 필요"],
     "KPI  재구매율 · 휴면 전환율"),
]

SCW = (CONTENT_W - 0.5*2) / 3
SCH = CONTENT_BOT - CONTENT_TOP
SCX = [MARGIN_L + i*(SCW+0.5) for i in range(3)]

for idx, (badge, badge_c, title_s, trigger, bullets, kpi) in enumerate(SCEN):
    cx = SCX[idx]
    cy = CONTENT_TOP
    box(s, cx, cy, SCW, SCH, GRAY_LT, border=GRAY_BD, pad=0)
    box(s, cx+0.5, cy+0.5, 1.2, 1.2, badge_c, badge,
        size=14, tc=WHITE, bold=True, align=PP_ALIGN.CENTER, pad=0)
    textbox(s, title_s, cx+2.1, cy+0.5, SCW-2.6, 1.1,
            size=12, bold=True, color=DARK)
    hline(s, cx+0.3, cy+1.95, SCW-0.6, color=GRAY_BD)
    textbox(s, trigger, cx+0.5, cy+2.1, SCW-0.7, 1.3,
            size=10, color=BLUE, bold=True, line_sp=1.3)
    hline(s, cx+0.3, cy+3.6, SCW-0.6, color=GRAY_BD)
    lines = ["• " + b for b in bullets]
    mlbox(s, lines, cx+0.5, cy+3.8, SCW-0.7, SCH-5.8,
          size=10.5, color=DARK, line_sp=1.4)
    hline(s, cx+0.3, cy+SCH-1.8, SCW-0.6, color=GRAY_BD)
    textbox(s, kpi, cx+0.5, cy+SCH-1.65, SCW-0.7, 1.4,
            size=10, color=NAVY, bold=True, line_sp=1.3)


# ── 끝장표 마지막으로 이동 ────────────────────────────────────────────────
sldIdLst = prs.slides._sldIdLst
ty = sldIdLst[1]
sldIdLst.remove(ty)
sldIdLst.append(ty)

# ── 저장 ─────────────────────────────────────────────────────────────────
prs.save(OUT)
verify = Presentation(OUT)
print(f"저장 완료: {OUT}")
print(f"슬라이드 수: {len(verify.slides)}")
for i, sld in enumerate(verify.slides):
    print(f"  [{i+1}] {sld.slide_layout.name}")
