#!/usr/bin/env python3
"""index.html -> artifact.html

Artifact 發佈時平台會自己包上 <!doctype html><head>…</head><body>，
所以要把外層骨架拆掉，只留 <title>/<link>/<style> + body 內容。
本機檔案和雲端版共用同一份原始碼，改 index.html 後重跑這支即可。
"""
import io, re, sys, pathlib

SRC = pathlib.Path(__file__).with_name("index.html")
OUT = pathlib.Path(__file__).with_name("artifact.html")

html = io.open(SRC, encoding="utf-8").read()

head = re.search(r"<head>(.*?)</head>", html, re.S)
body = re.search(r"<body>(.*?)</body>", html, re.S)
if not head or not body:
    sys.exit("找不到 <head> 或 <body>")

# charset / viewport 由平台的骨架提供，這裡丟掉避免重複
head_kept = "\n".join(
    ln for ln in head.group(1).strip().splitlines()
    if not re.match(r'\s*<meta\s+(charset|name="viewport")', ln)
)

out = head_kept.strip() + "\n" + body.group(1).strip() + "\n"
io.open(OUT, "w", encoding="utf-8").write(out)
print(f"{OUT.name}: {len(out):,} bytes")
