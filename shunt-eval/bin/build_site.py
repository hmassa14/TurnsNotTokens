#!/usr/bin/env python3
"""Wrap shunt-eval/post.html (an HTML fragment) into a standalone page at the repo root for GitHub Pages.

Usage: python3 shunt-eval/bin/build_site.py   (writes ./index.html; figure paths point at shunt-eval/figures/post/)
"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = open(os.path.join(ROOT, 'shunt-eval', 'post.html')).read()
src = src.replace('src="figures/post/', 'src="shunt-eval/figures/post/')
title = re.search(r'<title>(.*?)</title>', src).group(1)
head, body = src.split('<main>', 1)
head = head.replace('<title>%s</title>' % title, '')
page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{head}
<style>body {{ margin:0; }} img {{ max-width:100%; }}</style>
</head>
<body>
<main>{body}
<p class="byline" style="margin-top:48px">Source, harness and every run: <a href="https://github.com/hmassa14/TurnsNotTokens">github.com/hmassa14/TurnsNotTokens</a></p>
</body>
</html>
'''
open(os.path.join(ROOT, 'index.html'), 'w').write(page)
print('index.html written', len(page))
