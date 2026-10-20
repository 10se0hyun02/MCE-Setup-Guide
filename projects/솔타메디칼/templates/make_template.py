"""
솔타메디칼 PPT 기본 템플릿 생성기
킥오프 PPTX에서 표지(Cover) + 끝장표(Thank You)만 추출해
templates/솔타메디칼_PPT_base.pptx 로 저장한다.

실행: python make_template.py
"""

import shutil
import zipfile
import os
from lxml import etree

SRC = r"C:\Users\DELLA\Desktop\Della\업무파일\K. 솔타메디칼\Solta_Project_Kickoff Meeting_20260928.pptx"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(OUT_DIR, "솔타메디칼_PPT_base.pptx")

# ── ZIP 레벨에서 직접 조작 ──────────────────────────────────────────────────

shutil.copy2(SRC, OUT)

with zipfile.ZipFile(OUT, "r") as z:
    names = z.namelist()

# 남길 슬라이드: slide1(표지), slide8(Thank You)
# slide2~7 제거 → 그 사이에 slide2를 B5 빈 슬라이드로 재활용

KEEP_SLIDES = {"ppt/slides/slide1.xml", "ppt/slides/slide8.xml"}
REMOVE_SLIDES = {f"ppt/slides/slide{i}.xml" for i in range(2, 8)}
REMOVE_RELS = {f"ppt/slides/_rels/slide{i}.xml.rels" for i in range(2, 8)}

# 남길 slide8을 slide2로 리번호링
RENAME = {
    "ppt/slides/slide8.xml": "ppt/slides/slide2.xml",
    "ppt/slides/_rels/slide8.xml.rels": "ppt/slides/_rels/slide2.xml.rels",
}

NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"

# 모든 파일 메모리 로드
files: dict[str, bytes] = {}
with zipfile.ZipFile(OUT, "r") as z:
    for name in names:
        try:
            files[name] = z.read(name)
        except Exception:
            files[name] = b""

# 슬라이드 2~7 제거
for name in list(files.keys()):
    if name in REMOVE_SLIDES or name in REMOVE_RELS:
        del files[name]

# slide8 → slide2 리번호링
for old, new in RENAME.items():
    if old in files:
        files[new] = files.pop(old)

# presentation.xml 슬라이드 목록 갱신 (slide1, slide2만)
PRES_PATH = "ppt/presentation.xml"
pres_root = etree.fromstring(files[PRES_PATH])
sldIdLst = pres_root.find(f"{{{NS_P}}}sldIdLst")
if sldIdLst is not None:
    # 현재 sldId 목록 읽기
    current_ids = list(sldIdLst)
    # id 1 (slide1), id 8 (slide8→slide2) 만 남기고 나머지 제거
    # r:id 기준으로 필터
    keep_rids = set()
    for sldId in current_ids:
        rid = sldId.get(f"{{{NS_R}}}id")
        keep_rids.add(rid)  # 일단 전부 수집

    # presentation.xml.rels 에서 rid → target 매핑
    PRES_RELS_PATH = "ppt/_rels/presentation.xml.rels"
    rels_root = etree.fromstring(files[PRES_RELS_PATH])
    rid_to_target: dict[str, str] = {}
    for rel in rels_root:
        rid_to_target[rel.get("Id", "")] = rel.get("Target", "")

    # slide1, slide8(now slide2) 에 해당하는 rid 찾기
    target_to_rid = {v: k for k, v in rid_to_target.items()}
    keep_targets = {"slides/slide1.xml", "slides/slide8.xml"}
    good_rids = {target_to_rid.get(t) for t in keep_targets} - {None}

    # sldIdLst 정리
    for sldId in list(current_ids):
        rid = sldId.get(f"{{{NS_R}}}id")
        if rid not in good_rids:
            sldIdLst.remove(sldId)

    # presentation.xml.rels 에서 slide8 target → slide2 로 변경
    for rel in rels_root:
        if rel.get("Target") == "slides/slide8.xml":
            rel.set("Target", "slides/slide2.xml")

    files[PRES_RELS_PATH] = etree.tostring(rels_root, xml_declaration=True,
                                            encoding="UTF-8", standalone=True)

files[PRES_PATH] = etree.tostring(pres_root, xml_declaration=True,
                                   encoding="UTF-8", standalone=True)

# slide2 rels 도 내부 ../slides/slide8 참조를 ../slides/slide2 로 수정 (없으면 무시)
# (slide rels는 slideMaster/layout 참조라 변경 불필요)

# 출력
os.remove(OUT)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for name, data in files.items():
        z.writestr(name, data)

# ── 표지 텍스트 placeholder 교체 ─────────────────────────────────────────────
from pptx import Presentation
from pptx.util import Pt

prs = Presentation(OUT)
cover = prs.slides[0]

PARA_REPLACEMENTS = {
    "Salesforce Marketing Campaign": "[보고서 제목]",
    "설계 프로젝트 Kick-off Meeting": "",           # 부제 단락 삭제(빈 문자열)
    "2026. 09. 28": "[YYYY.MM.DD]",
}

for shape in cover.shapes:
    if not shape.has_text_frame:
        continue
    for para in shape.text_frame.paragraphs:
        # 단락 전체 텍스트 기준으로 매칭
        para_text = "".join(r.text for r in para.runs)
        for old, new in PARA_REPLACEMENTS.items():
            if old in para_text:
                # 첫 번째 run에 새 텍스트 넣고 나머지 run 비움
                if para.runs:
                    para.runs[0].text = new
                    for run in para.runs[1:]:
                        run.text = ""
                break

prs.save(OUT)

print(f"저장 완료: {OUT}")
print("슬라이드 구성: 1=표지(Cover)  2=끝장표(Thank You)")
print("사용법: PowerPoint에서 열어 [보고서 제목]/[날짜]를 수정하고")
print("       표지와 끝장표 사이에 B5 레이아웃 본문 슬라이드를 추가하세요.")
