#!/usr/bin/env python3
"""Inspect local example pages and save screenshots; screenshots still require visual review."""
import argparse
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
PAGES={
    "diagram":ROOT/"examples/code/figures/delivery-flow.html",
    "code":ROOT/"examples/code/output/index.html",
    "design":ROOT/"examples/design/output/index.html",
    "data":ROOT/"examples/data/output/document/index.html",
}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=ROOT/'build/visual-review')
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    results=[]
    with sync_playwright() as p:
        browser=p.chromium.launch()
        try:
            for name,path in PAGES.items():
                for width in (1440,390):
                    page=browser.new_page(viewport={"width":width,"height":1000},device_scale_factor=1)
                    page.goto(path.resolve().as_uri(),wait_until='domcontentloaded')
                    try:page.wait_for_load_state('networkidle',timeout=20000)
                    except Exception:page.evaluate('window.stop()')
                    page.evaluate('document.fonts.ready')
                    row=page.evaluate('''() => ({
                      pageOverflow:document.documentElement.scrollWidth>innerWidth+1,
                      brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),
                      images:[...document.images].map(i=>({src:i.getAttribute('src'),naturalWidth:i.naturalWidth,expectedWidth:Number(i.getAttribute('width')||i.naturalWidth),width:i.getBoundingClientRect().width})),
                      shrunkImages:[...document.images].filter(i=>Number(i.getAttribute('width')||i.naturalWidth)>i.getBoundingClientRect().width+1).map(i=>i.getAttribute('src')),
                      localLinks:[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')),
                      svgTextOutside:[...document.querySelectorAll('svg text')].filter(t=>{let b=t.getBBox(),v=t.ownerSVGElement.viewBox.baseVal;return b.x<v.x-1||b.y<v.y-1||b.x+b.width>v.x+v.width+1||b.y+b.height>v.y+v.height+1}).map(t=>t.textContent),
                      svgScrollers:[...document.querySelectorAll('svg')].map(s=>({viewWidth:s.viewBox.baseVal.width,width:s.getBoundingClientRect().width,parentWidth:s.parentElement.clientWidth,parentScroll:s.parentElement.scrollWidth,overflowX:getComputedStyle(s.parentElement).overflowX})),
                      fonts:{title:getComputedStyle(document.querySelector('h1')).fontFamily,node:document.querySelector('.node-name')?getComputedStyle(document.querySelector('.node-name')).fontFamily:null,geist:document.fonts.check('600 12px Geist'),korean:document.fonts.check('600 12px "Noto Sans KR"')}
                    })''')
                    row.update(page=name,width=width)
                    row['missingLocalLinks']=[]
                    for href in row.pop('localLinks'):
                        u=urlsplit(href)
                        if not u.scheme and u.path and not (path.parent/unquote(u.path)).is_file():row['missingLocalLinks'].append(href)
                    page.screenshot(path=str(args.out/f'{name}-{width}.png'),full_page=True)
                    page.screenshot(path=str(args.out/f'{name}-{width}-top.png'))
                    for i,figure in enumerate(page.locator('figure').all()):
                        figure.screenshot(path=str(args.out/f'{name}-{width}-figure-{i}.png'))
                    # Inspect print sizing programmatically. This is not a printed-page visual review.
                    page.emulate_media(media='print')
                    row['printOverflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth+1')
                    results.append(row)
                    page.close()
        finally:browser.close()
    (args.out/'observations.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(results,ensure_ascii=False,indent=2))
    bad=any(r['pageOverflow'] or r['brokenImages'] or r['missingLocalLinks'] or r['svgTextOutside'] or r['shrunkImages'] for r in results)
    if bad:raise SystemExit(1)


if __name__=='__main__':main()
