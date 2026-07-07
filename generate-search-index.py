#!/usr/bin/env python3
"""
generate-search-index.py
docs/*.html → search-index.json 변환 스크립트

사용법:
  python generate-search-index.py

docs/ 파일을 수정하거나 새 파일을 추가한 후 반드시 실행하세요.
출력: search-index.json (index.html 전체검색에 사용)
"""
import json, re, os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
OUT_FILE = os.path.join(BASE_DIR, 'search-index.json')

SKIP_EXTENSIONS = {'.py', '.json', '.md', '.txt'}

def strip_tags(html):
    text = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', html, flags=re.S | re.I)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_page_title(html):
    m = re.search(r'<h1[^>]*class="[^"]*doc-title[^"]*"[^>]*>(.*?)</h1>', html, re.S | re.I)
    if m:
        return strip_tags(m.group(1))
    m = re.search(r'<title>(.*?)</title>', html, re.S | re.I)
    if m:
        t = strip_tags(m.group(1))
        return re.sub(r'\s*[—–-]+\s*MCE.*$', '', t).strip()
    return ''

def extract_sections(html, filename):
    entries = []
    page_title = get_page_title(html)

    # <section id="..."> 블록 추출
    pattern = re.compile(
        r'<section\s[^>]*\bid=["\']([^"\']+)["\'][^>]*>(.*?)</section>',
        re.S | re.I
    )
    for m in pattern.finditer(html):
        sec_id = m.group(1)
        sec_html = m.group(2)

        # 첫 번째 h2/h3 제목
        h_match = re.search(r'<h[23][^>]*>(.*?)</h[23]>', sec_html, re.S | re.I)
        sec_title = strip_tags(h_match.group(1)) if h_match else sec_id

        # 텍스트 추출 (nav/sidebar 제외)
        # sidebar 블록 제거 (nav.sidebar)
        body = re.sub(r'<nav[^>]*>.*?</nav>', '', sec_html, flags=re.S | re.I)
        text = strip_tags(body)

        # 최대 600자
        if len(text) > 600:
            text = text[:600] + '…'

        entries.append({
            'file': f'docs/{filename}',
            'pageTitle': page_title,
            'sectionId': sec_id,
            'sectionTitle': sec_title,
            'text': text,
        })

    return entries


def main():
    if not os.path.isdir(DOCS_DIR):
        print(f'ERROR: docs 디렉터리를 찾을 수 없습니다: {DOCS_DIR}', file=sys.stderr)
        sys.exit(1)

    index = []
    files = sorted(f for f in os.listdir(DOCS_DIR) if f.endswith('.html'))

    for fname in files:
        path = os.path.join(DOCS_DIR, fname)
        with open(path, encoding='utf-8', errors='replace') as f:
            html = f.read()
        entries = extract_sections(html, fname)
        print(f'  {fname}: {len(entries)}개 섹션')
        index.extend(entries)

    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f'\n완료: {len(index)}개 항목 → {OUT_FILE}')


if __name__ == '__main__':
    main()
