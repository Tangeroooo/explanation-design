import json
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
report={}
with sync_playwright() as p:
 browser=p.chromium.launch()
 page=browser.new_page(viewport={'width':1280,'height':1088},device_scale_factor=1)
 for ext in ('html','svg'):
  page.route('http**/*', lambda route: route.abort())
  page.goto((root/f'component-handoff.{ext}').as_uri(),wait_until='networkidle')
  page.evaluate('document.fonts.ready')
  cdp=page.context.new_cdp_session(page)
  cdp.send('DOM.enable')
  cdp.send('CSS.enable')
  doc=cdp.send('DOM.getDocument')
  nodes=cdp.send('DOM.querySelectorAll',{'nodeId':doc['root']['nodeId'],'selector':'svg text'})['nodeIds']
  fonts=[]
  for node in nodes:
   f=cdp.send('CSS.getPlatformFontsForNode',{'nodeId':node})['fonts']
   fonts.extend(f)
  report[ext]={
    'fonts':sorted({(f['familyName'],f['isCustomFont']) for f in fonts}),
    'glyphs':sum(f['glyphCount'] for f in fonts),
    'checks':page.evaluate('''() => {
      const svg=document.querySelector('svg');
      const r=svg.getBoundingClientRect();
      const items=[...svg.querySelectorAll('text')].map(el=>{const b=el.getBoundingClientRect();return {text:el.textContent.trim(),x:b.x-r.x,y:b.y-r.y,w:b.width,h:b.height}});
      const outside=items.filter(b=>b.x<0||b.y<0||b.x+b.w>r.width||b.y+b.h>r.height);
      const overlaps=[]; for(let i=0;i<items.length;i++) for(let j=i+1;j<items.length;j++){const a=items[i],b=items[j];if(a.x<b.x+b.w&&a.x+a.w>b.x&&a.y<b.y+b.h&&a.y+a.h>b.y) overlaps.push([a.text,b.text]);}
      return {width:r.width,height:r.height,titleSize:getComputedStyle(svg.querySelector('text')).fontSize,titleWeight:getComputedStyle(svg.querySelector('text')).fontWeight,outside,overlaps,loadedFonts:[...document.fonts].map(f=>({family:f.family,status:f.status}))};
    }''')
  }
  cdp.detach()
 page.goto((root/'component-handoff.html').as_uri(),wait_until='networkidle')
 page.set_viewport_size({'width':390,'height':844})
 report['mobile']=page.evaluate('''() => ({viewport:innerWidth,document:document.documentElement.scrollWidth,wrapper:document.querySelector('.diagram-container').clientWidth,scrollWidth:document.querySelector('.diagram-container').scrollWidth,svg:document.querySelector('svg').getBoundingClientRect().width})''')
 browser.close()
report['png']={name:Image.open(root/name).size for name in ('component-handoff.png','preview/component-handoff-1x.png')}
(root/'render-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
assert all(not report[e]['checks']['outside'] and not report[e]['checks']['overlaps'] for e in ('html','svg'))
assert report['png']['component-handoff.png']==(2560,2176)
assert report['png']['preview/component-handoff-1x.png']==(1280,1088)
assert report['mobile']['document']==390 and report['mobile']['scrollWidth']==1280
