"""Observe actual rendered fonts and sizes; this is a check, not an exporter."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from PIL import Image

d=Path(__file__).parent
report={}
with sync_playwright() as p:
    browser=p.chromium.launch()
    for slug,height in [('structure',840),('keys',788)]:
        page=browser.new_page(viewport={'width':1360,'height':940})
        page.goto((d/f'{slug}.html').as_uri())
        page.evaluate('document.fonts.ready')
        client=page.context.new_cdp_session(page)
        client.send('DOM.enable'); client.send('CSS.enable')
        root=client.send('DOM.getDocument')['root']['nodeId']
        font_rows=[]
        for selector in ['svg text.title','svg text.mono']:
            nodes=client.send('DOM.querySelectorAll',{'nodeId':root,'selector':selector})['nodeIds']
            if nodes:
                font_rows.append({'selector':selector,'actual_fonts':client.send('CSS.getPlatformFontsForNode',{'nodeId':nodes[0]})['fonts']})
        layout=page.locator('svg').evaluate('e=>({width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height,viewBox:e.getAttribute("viewBox"),minWidth:getComputedStyle(e).minWidth})')
        title=page.locator('svg text.title').evaluate('e=>({fontSize:getComputedStyle(e).fontSize,fontWeight:getComputedStyle(e).fontWeight})')
        strokes=page.locator('svg [stroke-width]').evaluate_all('es=>es.map(e=>({tag:e.tagName,width:parseFloat(getComputedStyle(e).strokeWidth)}))')
        assert title['fontWeight']=='700' and 28<=float(title['fontSize'].removesuffix('px'))<=32
        assert any(e['tag']=='path' and 2<=e['width']<=2.5 for e in strokes)
        bounds=page.locator('svg text').evaluate_all('es=>es.map(e=>({text:e.textContent,x:e.getBBox().x,y:e.getBBox().y,w:e.getBBox().width,h:e.getBBox().height})).filter(b=>b.x<0||b.y<0||b.x+b.w>1280||b.y+b.h>'+str(height)+')')
        page.set_viewport_size({'width':390,'height':844})
        narrow=page.evaluate('({pageWidth:document.documentElement.clientWidth,scrollWidth:document.documentElement.scrollWidth,wrapperWidth:document.querySelector(".diagram-container").clientWidth,wrapperScrollWidth:document.querySelector(".diagram-container").scrollWidth})')
        report[slug]={'browser':browser.version,'display':layout,'png_pixels':list(Image.open(d/f'{slug}.png').size),'export_scale':2,'title':title,'actual_fonts':font_rows,'display_strokes_css_px':strokes,'text_outside_viewbox':bounds,'narrow_390px':narrow}
        assert layout['width']==1280 and layout['height']==height
        assert report[slug]['png_pixels']==[2560,height*2]
        assert not bounds and narrow['pageWidth']==narrow['scrollWidth']
        page.close()
    page=browser.new_page(viewport={'width':1360,'height':940})
    page.route('https://**/*',lambda route:route.abort())
    standalone=[]
    for slug in ['structure','keys']:
        page.goto((d/f'{slug}.svg').as_uri())
        page.evaluate('document.fonts.ready')
        client=page.context.new_cdp_session(page)
        client.send('DOM.enable'); client.send('CSS.enable')
        root=client.send('DOM.getDocument')['root']['nodeId']
        node=client.send('DOM.querySelector',{'nodeId':root,'selector':'text.title'})['nodeId']
        standalone.append({'slug':slug,'remote_requests_blocked':True,'fonts':client.send('CSS.getPlatformFontsForNode',{'nodeId':node})['fonts']})
    page.goto((d/'document/index.html').as_uri())
    page.evaluate('document.fonts.ready')
    report['document_embed']=page.locator('img').evaluate_all('es=>es.map(e=>({src:e.getAttribute("src"),width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height,loaded:e.complete&&e.naturalWidth>0}))')
    assert all(i['width']==1280 and i['loaded'] for i in report['document_embed'])
    page.screenshot(path=d/'preview/document.png',full_page=True)
    report['standalone_svg']=standalone
    browser.close()
(d/'render-observations.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
