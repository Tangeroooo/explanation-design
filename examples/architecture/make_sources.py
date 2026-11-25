"""Fill the installed diagram-design HTML template; exports use its packaged tools."""
from pathlib import Path
import base64, re

D = Path(__file__).parent
template = (D / 'template.html').read_text()
fonts = ''
for family, name, weight in [('Noto Sans KR','NotoSansKR.ttf','100 900'), ('DejaVu Sans Mono','DejaVuSansMono.ttf','400')]:
    data = base64.b64encode((D/'fonts'/name).read_bytes()).decode()
    fonts += f'@font-face {{font-family:"{family}";src:url(data:font/ttf;base64,{data}) format("truetype");font-weight:{weight};}}\n'
css = '''
* {box-sizing:border-box;margin:0;padding:0}
body {font-family:"Noto Sans KR",sans-serif;background:#fbfcfe;color:#1f2a3c;padding:24px;}
.frame {width:1280px;max-width:100%;min-width:0;margin:auto;}
.diagram-container {width:100%;overflow-x:auto;}
svg {width:1280px;min-width:1280px;display:block;}
svg text {font-family:"Noto Sans KR",sans-serif;fill:#1f2a3c;font-size:16px;}
svg .mono {font-family:"DejaVu Sans Mono",monospace;}
svg .heading {font-size:18px;font-weight:700;}
svg .title {font-size:30px;font-weight:700;}
svg .small {font-size:14px;}
@media print {.diagram-container{overflow-x:visible} svg{min-width:0;width:100%}}
'''

def write(slug,title,desc,height,body):
    s=re.sub(r'  <link[^>]+>\n','',template)
    s=re.sub(r'<style>.*?</style>',lambda _: '<style>'+css+'</style>',s,flags=re.S)
    s=s.replace('lang="en"','lang="ko"').replace('<title>Diagram</title>',f'<title>{title}</title>')
    s=re.sub(r'    <p class="eyebrow">.*?</h1>', '',s, flags=re.S)
    svg=f'''<svg viewBox="0 0 1280 {height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="{slug}-title {slug}-desc">
    <title id="{slug}-title">{title}</title><desc id="{slug}-desc">{desc}</desc>
    <defs><marker id="arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#66748a"/></marker><marker id="arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#c46a17"/></marker><marker id="arrow-link" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#2462b8"/></marker></defs>
    <rect width="1280" height="{height}" fill="#fbfcfe"/>
    {body}</svg>'''
    svg=svg.replace('<defs>','<defs><style>'+fonts+'</style>',1)
    s=re.sub(r'<svg\b.*?</svg>',lambda _:svg,s,flags=re.S)
    (D/f'{slug}.html').write_text('\n'.join(line.rstrip() for line in s.splitlines())+'\n')

body='''
<text x="40" y="64" class="title">같은 서비스 안에서도 자원의 공유 범위는 다르다</text>
<text x="40" y="100">논리 서비스의 연결 하나가 프로세스 하나를 뜻하지 않는다.</text>
<rect x="40" y="136" width="904" height="568" rx="8" fill="#f1f4f8" stroke="#66748a" stroke-width="2"/>
<text x="64" y="172" class="heading">논리 서비스 <tspan class="mono">S</tspan> · 프로세스 두 개로 배포</text>
<rect x="64" y="200" width="600" height="432" rx="8" fill="#ffffff" stroke="#66748a" stroke-width="2"/>
<rect x="696" y="200" width="224" height="432" rx="8" fill="#ffffff" stroke="#66748a" stroke-width="2"/>
<text x="88" y="232" class="heading">프로세스 <tspan class="mono">P</tspan> · 내부 상세</text>
<text x="716" y="232" class="heading">프로세스 <tspan class="mono">Q</tspan></text>
<path d="M 944,388 H 1016" fill="none" stroke="#c46a17" stroke-width="2.5" marker-end="url(#arrow-accent)"/>
<rect x="948" y="340" width="64" height="36" fill="#fbfcfe"/>
<text x="980" y="355" text-anchor="middle" class="small">기록</text><text x="980" y="373" text-anchor="middle" class="small">갱신</text>
<rect x="1016" y="328" width="224" height="128" rx="6" fill="#fdeeee" stroke="#b83a30" stroke-width="2"/>
<text x="1040" y="360" class="heading">Catalog</text><line x1="1036" y1="376" x2="1220" y2="376" stroke="#b83a30" stroke-width="1"/>
<text x="1040" y="404" class="mono">record:P</text><text x="1040" y="432" class="mono">record:Q</text>
<text x="1016" y="496">Key 선택은 그림 2</text>
<rect x="88" y="252" width="552" height="56" rx="6" fill="#f2eefc" stroke="#6a4cc0" stroke-width="1.5"/>
<text x="364" y="286" text-anchor="middle" class="heading">Coordinator × 1</text>
'''
for i,x in enumerate([88,228,368,508]):
    dash=' stroke-dasharray="8,5"' if i==3 else ''
    body+=f'<line x1="{x+60}" y1="460" x2="{x+60}" y2="536" stroke="#66748a" stroke-width="2"{dash}/>'
    body+=f'<rect x="{x}" y="352" width="120" height="108" rx="6" fill="'+('#fff7df' if i==3 else '#fff4e8')+f'" stroke="'+('#b07d0a' if i==3 else '#c46a17')+f'" stroke-width="'+('3' if i==3 else '1.5')+f'"{dash}/>'
    body+=f'<text x="{x+60}" y="382" text-anchor="middle" class="heading">Worker {i+1}</text>'
    body+=f'<rect x="{x+12}" y="400" width="96" height="40" rx="4" fill="#eef1f6" stroke="#3c4a62" stroke-width="1.5"/><text x="{x+60}" y="426" text-anchor="middle" class="small">Mailbox</text>'
body+='''
<text x="528" y="336" class="small">추가 제안</text>
<rect x="88" y="536" width="552" height="64" rx="6" fill="#f1f4f8" stroke="#66748a" stroke-width="2"/>
<text x="364" y="562" text-anchor="middle" class="heading">공유 Pool × 1</text><text x="364" y="586" text-anchor="middle" class="small">P의 worker만 공유 · 네 번째 worker도 같은 pool 사용</text>
<text x="716" y="284" class="heading">현재 구성 유지</text>
<text x="716" y="328">Coordinator × 1</text><text x="716" y="376">Worker × 3</text><text x="716" y="408" class="small">각 worker에 mailbox 1개</text>
<line x1="716" y1="448" x2="900" y2="448" stroke="#c9d1dd" stroke-width="1"/>
<text x="716" y="496" class="heading">공유 Pool × 1</text><text x="716" y="528" class="small">Q의 worker끼리 공유</text><text x="716" y="556" class="small">P의 pool과 별개</text>
<text x="64" y="672">worker 수는 <tspan class="mono">P: 3 → 4</tspan>, <tspan class="mono">Q: 3</tspan> · pool 수는 프로세스마다 1개 유지</text>
<text x="40" y="748">Pool 용량·종류, coordinator의 메시지 전달 방식, 처리량 변화는 주어지지 않았다.</text>
<line x1="40" y1="780" x2="1240" y2="780" stroke="#c9d1dd" stroke-width="1"/>
<text x="40" y="812" class="small">범례 · 감싼 경계: 소속 범위   │   실선 연결: pool 공유   │   점선: 추가 제안   │   화살표: 서비스 수준의 기록 갱신 요약</text>
'''
write('structure','서비스와 프로세스의 공유 범위','서비스 S의 P와 Q는 별도 pool을 가지며 P에만 네 번째 worker와 mailbox를 추가하는 제안이다.',840,body)

body='''
<text x="40" y="64" class="title">같은 helper 코드여도, 인자가 달라지면 기록 대상이 달라진다</text>
<text x="40" y="100">공유하는 것은 소스 함수다. 하나의 실행 프로세스나 하나의 기록을 공유한다는 뜻은 아니다.</text>
<rect x="40" y="132" width="1200" height="96" rx="6" fill="#f1f4f8" stroke="#66748a" stroke-width="1.5"/>
<text x="64" y="164" class="heading">두 프로세스가 사용하는 소스 정의 · 실행 인스턴스 수를 나타내는 상자가 아님</text>
<text x="64" y="200" class="mono">update_record(node_id, value)  →  write("record:" + node_id, value)</text>
<rect x="40" y="264" width="576" height="356" rx="8" fill="#ffffff" stroke="#66748a" stroke-width="1.5"/>
<rect x="640" y="264" width="600" height="356" rx="8" fill="#ffffff" stroke="#66748a" stroke-width="1.5"/>
<text x="64" y="300" class="heading">평소 호출 · 서로 다른 key</text>
<text x="664" y="300" class="heading">별도 변경 제안 · Q도 P를 인자로 전달</text>
<rect x="436" y="328" width="156" height="256" rx="6" fill="#fdeeee" stroke="#b83a30" stroke-width="2"/>
<rect x="1060" y="328" width="156" height="256" rx="6" fill="#fdeeee" stroke="#b83a30" stroke-width="2"/>
<text x="456" y="356" class="heading">Catalog</text><text x="1080" y="356" class="heading">Catalog</text>
<path d="M 328,400 H 456" fill="none" stroke="#c46a17" stroke-width="2.5" marker-end="url(#arrow-accent)"/>
<path d="M 328,528 H 456" fill="none" stroke="#c46a17" stroke-width="2.5" marker-end="url(#arrow-accent)"/>
<path d="M 928,400 H 1080" fill="none" stroke="#c46a17" stroke-width="2.5" marker-end="url(#arrow-accent)"/>
<path d="M 928,528 H 1012 Q 1020,528 1020,520 V 432 Q 1020,424 1028,424 H 1080" fill="none" stroke="#b07d0a" stroke-width="3" stroke-dasharray="8,5" marker-end="url(#arrow)"/>
'''
for x in [64,664]:
    for y,p,arg in [(368,'P','P'),(496,'Q','Q' if x==64 else 'P')]:
        body+=f'<rect x="{x}" y="{y}" width="264" height="64" rx="6" fill="#fff4e8" stroke="#c46a17" stroke-width="1.5"/><text x="{x+16}" y="{y+26}" class="heading">프로세스 <tspan class="mono">{p}</tspan>의 호출</text><text x="{x+16}" y="{y+50}" class="mono">node_id = "{arg}"</text>'
for x,y,key in [(456,376,'P'),(456,504,'Q'),(1080,376,'P')]:
    body+=f'<rect x="{x}" y="{y}" width="116" height="64" rx="4" fill="#ffffff" stroke="#b83a30" stroke-width="1.5"/><text x="{x+58}" y="{y+38}" class="mono" text-anchor="middle">record:{key}</text>'
body+='''
<text x="1080" y="516" class="small">같은 key 갱신</text>
<text x="64" y="660">P의 worker 추가만으로 key는 바뀌지 않는다. Q의 인자를 바꾸면 기록 대상이 바뀐다.</text>
<text x="64" y="692">최종 값은 알 수 없다. 동시 갱신 순서·충돌 해결 규칙은 주어지지 않았다.</text>
<line x1="40" y1="728" x2="1240" y2="728" stroke="#c9d1dd" stroke-width="1"/>
<text x="40" y="760" class="small">범례 · 화살표: 인자로 결정되는 기록 대상   │   점선: 변경 제안   │   좌우: 같은 시스템의 조건 비교 · 실행 시간 순서 아님</text>
'''
write('keys','helper 인자와 기록 대상','평소 P와 Q는 다른 key를 갱신하지만 Q가 P를 전달하면 같은 record:P를 갱신하고 최종 값은 규칙이 주어지지 않아 알 수 없다.',788,body)
assert all((D/f'{s}.html').exists() for s in ['structure','keys'])
