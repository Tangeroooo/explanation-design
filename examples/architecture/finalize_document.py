"""Add an offline Korean font and enough width to the assembled document."""
from pathlib import Path
import base64

d=Path(__file__).parent
path=d/'document/index.html'
html=path.read_text()
data=base64.b64encode((d/'fonts/NotoSansKR-document.ttf').read_bytes()).decode()
css='@font-face{font-family:"Noto Sans KR";src:url(data:font/ttf;base64,'+data+') format("truetype");font-weight:100 900;}body{font-family:"Noto Sans KR",sans-serif}main{max-width:1328px}'
html=html.replace("style-src 'unsafe-inline';", "style-src 'unsafe-inline'; font-src data:;")
html=html.replace('</style>',css+'</style>')
path.write_text(html)
assert 'font-src data:' in html
