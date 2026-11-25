"""Subset existing fonts to text in the authored sources; does not install fonts."""
from pathlib import Path
from fontTools import subset

d=Path(__file__).parent
text=(d/'make_sources.py').read_text()
for filename in ['NotoSansKR.ttf','DejaVuSansMono.ttf']:
    path=d/'fonts'/filename
    options=subset.Options()
    font=subset.load_font(str(path),options)
    sub=subset.Subsetter(options=options)
    sub.populate(text=text)
    sub.subset(font)
    subset.save_font(font,str(path),options)
    assert path.stat().st_size < 1000000
