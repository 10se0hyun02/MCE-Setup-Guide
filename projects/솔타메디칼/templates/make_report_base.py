"""
솔타메디칼 인터뷰 결과 보고서 베이스 템플릿 생성기
현업인터뷰결과보고서_V0.1_261013.pptx에서 표지(slide 1)만 추출해
templates/솔타_보고서_base.pptx로 저장한다.

실행: python make_report_base.py
"""

import shutil, zipfile, os
from lxml import etree

SRC = r"G:\내 드라이브\Projects\Project-Archive\projects\솔타메디칼\docs\솔타메디칼_현업인터뷰결과보고서_V0.1_261013.pptx"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(OUT_DIR, "솔타_보고서_base.pptx")

NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"

# 파일 전체 메모리 로드
files = {}
with zipfile.ZipFile(SRC, "r") as z:
    for name in z.namelist():
        try:
            files[name] = z.read(name)
        except Exception:
            files[name] = b""

# slides 2~8 제거
for i in range(2, 9):
    files.pop(f"ppt/slides/slide{i}.xml", None)
    files.pop(f"ppt/slides/_rels/slide{i}.xml.rels", None)

# presentation.xml: sldIdLst에서 slide2~8 참조 제거
PRES_PATH = "ppt/presentation.xml"
RELS_PATH = "ppt/_rels/presentation.xml.rels"
pres_root = etree.fromstring(files[PRES_PATH])
rels_root = etree.fromstring(files[RELS_PATH])

# rId → target 매핑
rid_to_target = {rel.get("Id"): rel.get("Target", "") for rel in rels_root}
target_to_rid = {v: k for k, v in rid_to_target.items()}

bad_targets = {f"slides/slide{i}.xml" for i in range(2, 9)}
bad_rids = {target_to_rid.get(t) for t in bad_targets} - {None}

# sldIdLst 정리
sldIdLst = pres_root.find(f"{{{NS_P}}}sldIdLst")
if sldIdLst is not None:
    for sldId in list(sldIdLst):
        rid = sldId.get(f"{{{NS_R}}}id")
        if rid in bad_rids:
            sldIdLst.remove(sldId)

# rels 정리
for rel in list(rels_root):
    if rel.get("Id") in bad_rids:
        rels_root.remove(rel)

files[PRES_PATH] = etree.tostring(pres_root, xml_declaration=True,
                                   encoding="UTF-8", standalone=True)
files[RELS_PATH] = etree.tostring(rels_root, xml_declaration=True,
                                   encoding="UTF-8", standalone=True)

# 출력
if os.path.exists(OUT):
    os.remove(OUT)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for name, data in files.items():
        z.writestr(name, data)

print(f"저장 완료: {OUT}")
print("슬라이드 구성: 1=표지(Cover)  →  이후 gen_interview_report.py 실행")
