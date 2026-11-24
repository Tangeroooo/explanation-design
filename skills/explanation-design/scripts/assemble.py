#!/usr/bin/env python3
"""Validate and assemble authored plain-text blocks; does not assess truth or quality."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit

KINDS = {"fact": "사실", "inference": "추론", "proposal": "제안", "unknown": "미확인"}
ID = re.compile(r"[A-Za-z][A-Za-z0-9_-]*\Z")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def string(value, label):
    require(isinstance(value, str) and bool(value.strip()), f"{label}: nonempty string required")
    return value


def safe_url(value):
    string(value, "URL")
    require(not any(c.isspace() or ord(c) < 32 or c in '\\<>"\'' for c in value), "unsafe URL characters")
    parsed = urlsplit(value)
    require(parsed.scheme in ("", "https", "http") and not value.startswith("//"), "unsafe URL scheme")
    if parsed.scheme:
        require(bool(parsed.netloc) and not parsed.username and not parsed.password, "invalid HTTP URL")
    return value


def output_url(value, base, out):
    """Rebase source file links from manifest location to the output directory."""
    parsed = urlsplit(safe_url(value))
    if parsed.scheme or not parsed.path:
        return value
    target = (base / unquote(parsed.path)).resolve()
    require(target.is_file(), f"missing local source link: {value}")
    relative = quote(Path(os.path.relpath(target, out)).as_posix(), safe="/")
    return urlunsplit(("", "", relative, parsed.query, parsed.fragment))


def local_file(base, value, suffixes):
    string(value, "asset path")
    path = (base / value).resolve()
    require(not Path(value).is_absolute() and path.is_relative_to(base.resolve()), "asset escapes input directory")
    require(path.is_file() and path.suffix.lower() in suffixes, f"missing or unsupported asset: {value}")
    return path


def records(items, label):
    require(isinstance(items, list), f"{label}: list required")
    result = {}
    for item in items:
        require(isinstance(item, dict), f"{label}: object required")
        ident = item.get("id")
        require(isinstance(ident, str) and ID.fullmatch(ident), f"{label}: invalid id")
        require(ident not in result, f"{label}: duplicate id {ident}")
        result[ident] = item
    return result


def references(ids, known, label):
    require(isinstance(ids, list) and all(isinstance(x, str) and x in known for x in ids), f"{label}: unresolved reference")


def validate(doc, base):
    require(isinstance(doc, dict), "document must be an object")
    for key in ("title", "summary", "language"):
        string(doc.get(key), key)
    require(re.fullmatch(r"[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*", doc["language"]), "invalid language tag")
    sources = records(doc.get("sources"), "sources")
    claims = records(doc.get("claims"), "claims")
    sections = records(doc.get("sections"), "sections")
    require(bool(sections), "at least one section required")
    for source in sources.values():
        for key in ("label", "location", "version"):
            string(source.get(key), f"source.{key}")
        if "href" in source:
            safe_url(source["href"])
            parsed = urlsplit(source["href"])
            if not parsed.scheme and parsed.path:
                require((base / unquote(parsed.path)).is_file(), f"missing local source link: {source['href']}")
    for claim in claims.values():
        string(claim.get("text"), "claim.text")
        string(claim.get("basis"), "claim.basis")
        require(claim.get("kind") in KINDS, "invalid claim kind")
        references(claim.get("source_ids"), sources, "claim.source_ids")
        if claim["kind"] in ("fact", "inference"):
            require(bool(claim["source_ids"]), "fact/inference requires a source")
    for section in sections.values():
        string(section.get("heading"), "section.heading")
        require(isinstance(section.get("blocks"), list) and section["blocks"], "nonempty blocks required")
        for block in section["blocks"]:
            require(isinstance(block, dict), "block must be object")
            references(block.get("claim_ids", []), claims, "block.claim_ids")
            kind = block.get("type")
            if kind in ("paragraph", "code"):
                string(block.get("text"), "block.text")
                if kind == "code":
                    require(re.fullmatch(r"[a-zA-Z0-9_+-]*", block.get("language", "")), "invalid code language")
            elif kind == "list":
                require(isinstance(block.get("items"), list) and block["items"], "nonempty items required")
                for item in block["items"]:
                    string(item, "list item")
            elif kind == "table":
                headers, rows = block.get("headers"), block.get("rows")
                require(isinstance(headers, list) and headers and isinstance(rows, list), "table lists required")
                for header in headers:
                    string(header, "table header")
                for row in rows:
                    require(isinstance(row, list) and len(row) == len(headers), "ragged table")
                    for cell in row:
                        string(cell, "table cell")
            elif kind == "figure":
                local_file(base, block.get("path"), {".svg", ".png"})
                local_file(base, block.get("brief"), {".md"})
                string(block.get("alt"), "figure.alt")
                string(block.get("caption"), "figure.caption")
                if "display_width" in block:
                    require(type(block["display_width"]) is int and 64 <= block["display_width"] <= 16384, "display_width must be 64..16384 CSS pixels")
            else:
                raise ValueError(f"unknown block type: {kind}")
    return doc


def md(value):
    # Plain text input: no raw HTML, headings, links or injected table cells.
    return re.sub(r"([\\`*_{}\[\]()#+.!|>~-])", r"\\\1", html.escape(value, quote=False)).replace("\n", " ")


def copy_asset(base, value, out, folder):
    source = (base / value).resolve()
    data = source.read_bytes()
    name = hashlib.sha256(data).hexdigest()[:16] + source.suffix.lower()
    dest = out / folder / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return f"{folder}/{name}"


def assemble(doc, base, out):
    validate(doc, base)
    out = out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    h = html.escape
    hs = [f"<h1>{h(doc['title'])}</h1>", f"<p class='summary'>{h(doc['summary'])}</p>"]
    ms = [f"# {md(doc['title'])}", md(doc["summary"])]
    for section in doc["sections"]:
        hs.append(f"<section id='section-{section['id']}'><h2>{h(section['heading'])}</h2>")
        ms.append(f"## {md(section['heading'])}")
        for b in section["blocks"]:
            kind = b["type"]
            if kind == "paragraph":
                hs.append(f"<p>{h(b['text'])}</p>")
                ms.append(md(b["text"]))
            elif kind == "list":
                hs.append("<ul>" + "".join(f"<li>{h(x)}</li>" for x in b["items"]) + "</ul>")
                ms.append("\n".join(f"- {md(x)}" for x in b["items"]))
            elif kind == "code":
                hs.append(f"<pre><code>{h(b['text'])}</code></pre>")
                fence = "`" * max(3, max((len(x) + 1 for x in re.findall(r"`+", b["text"])), default=3))
                ms.append(f"{fence}{b.get('language', '')}\n{b['text']}\n{fence}")
            elif kind == "table":
                hs.append("<div class='scroll'><table><thead><tr>" + "".join(f"<th scope='col'>{h(x)}</th>" for x in b["headers"]) + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{h(x)}</td>" for x in row) + "</tr>" for row in b["rows"]) + "</tbody></table></div>")
                ms.append("\n".join(["| " + " | ".join(md(x) for x in b["headers"]) + " |", "| " + " | ".join("---" for _ in b["headers"]) + " |"] + ["| " + " | ".join(md(x) for x in row) + " |" for row in b["rows"]]))
            elif kind == "figure":
                asset = copy_asset(base, b["path"], out, "assets")
                brief = copy_asset(base, b["brief"], out, "briefs")
                width = f" width='{b['display_width']}'" if "display_width" in b else ""
                hs.append(f"<figure><div class='scroll' tabindex='0' role='region' aria-label='가로로 스크롤하여 전체 그림 보기'><img src='{asset}'{width} alt='{h(b['alt'], quote=True)}'></div><figcaption>{h(b['caption'])} <a href='{brief}'>제작 명세</a> · 넓은 그림은 가로로 스크롤해 전체를 볼 수 있습니다.</figcaption></figure>")
                ms.append(f"![{md(b['alt'])}]({asset})\n\n{md(b['caption'])} [제작 명세]({brief})")
            if b.get("claim_ids"):
                hs.append("<p class='claims'>" + " · ".join(f"<a href='#claim-{i}'>{i}</a>" for i in b["claim_ids"]) + "</p>")
                ms.append("근거 주장: " + ", ".join(f"[{i}](#claim-{i.lower()})" for i in b["claim_ids"]))
        hs.append("</section>")
    hs.append("<section><h2>주장과 근거</h2>")
    ms.append("## 주장과 근거")
    for c in doc["claims"]:
        refs = ", ".join(c["source_ids"]) or "없음"
        hs.append(f"<article id='claim-{c['id']}'><h3>{c['id']} · {KINDS[c['kind']]}</h3><p>{h(c['text'])}</p><p>{h(c['basis'])}</p><p>출처: {h(refs)}</p></article>")
        ms.extend([f"### claim-{c['id'].lower()}", f"{KINDS[c['kind']]}: {md(c['text'])}\n\n{md(c['basis'])}\n\n출처: {md(refs)}"])
    hs.append("</section><section><h2>출처</h2><ul>")
    ms.append("## 출처")
    for s in doc["sources"]:
        label = f"{s['id']} · {s['label']} · {s['location']} · {s['version']}"
        href = output_url(s["href"], base, out) if "href" in s else None
        hs.append("<li>" + (f"<a href='{h(href, quote=True)}'>{h(label)}</a>" if href else h(label)) + "</li>")
        ms.append(f"- [{md(label)}]({quote(href, safe=':/?#%=&@+;,~-._')})" if href else f"- {md(label)}")
    hs.append("</ul></section>")
    css = """*{box-sizing:border-box}body{margin:0;background:#fafaf7;color:#202c33;font:17px/1.75 system-ui,sans-serif}main{max-width:1000px;margin:auto;padding:48px 24px}h1{font-size:2rem;line-height:1.3}h2{margin-top:2.5rem}h3{font-size:1.05rem}p,li,td,th{overflow-wrap:anywhere}.summary{font-size:1.15rem;border-left:4px solid #176b62;padding:12px 20px}.claims,figcaption{font-size:.9rem;color:#4e5c64}.scroll{max-width:100%;overflow-x:auto}table{border-collapse:collapse;min-width:600px;width:100%}th,td{min-width:88px;padding:12px;text-align:left;border-bottom:1px solid #bbc7c7;vertical-align:top}pre{overflow:auto;padding:20px;background:#edf1f1}figure{margin:24px 0}img{display:block;max-width:none;height:auto}a{color:#155d78}article{border-top:1px solid #bbc7c7;padding:12px 0}@media print{img{max-width:100%}th,td{min-width:0;padding:6px}main{padding:0}.scroll{overflow:visible}table{min-width:0}pre{white-space:pre-wrap}figure,article{break-inside:avoid}}"""
    page = f"<!doctype html><html lang='{doc['language']}'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><meta http-equiv='Content-Security-Policy' content=\"default-src 'none'; img-src 'self' data:; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'\"><title>{h(doc['title'])}</title><style>{css}</style></head><body><main>{''.join(hs)}</main></body></html>"
    (out / "index.html").write_text(page, encoding="utf-8")
    (out / "explanation.md").write_text("\n\n".join(ms) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        doc = json.loads(args.input.read_text(encoding="utf-8"))
        validate(doc, args.input.parent)
        if not args.check:
            require(args.out is not None, "--out required unless --check")
            assemble(doc, args.input.parent, args.out)
        print("Structure valid" if args.check else f"Assembled: {args.out}")
    except (ValueError, OSError, TypeError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
