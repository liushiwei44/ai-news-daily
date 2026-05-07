#!/usr/bin/env python3
"""Build WeChat Work Markdown notification body from an ai-news-*.html file.

Usage:
    build_wechat_message.py <html_file> <issue_num> <datetime> <url>

Prints the rendered Markdown content to stdout.
"""
import sys
import re
import html as html_mod


def clean(s: str) -> str:
    s = html_mod.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def shorten(s: str, n: int) -> str:
    s = clean(s)
    return s[:n] + ("…" if len(s) > n else "")


def first_clause(s: str, max_len: int = 52) -> str:
    s = clean(s)
    for sep in ("。", "；"):
        idx = s.find(sep)
        if 0 < idx <= max_len:
            return s[: idx + 1]
    return shorten(s, max_len)


def main() -> None:
    html_path, issue_num, datetime_, url = sys.argv[1:5]

    with open(html_path, encoding="utf-8") as f:
        src = f.read()

    titles = re.findall(r'<div class="card-title">(.*?)</div>', src)
    summaries = re.findall(r'<p class="card-summary">(.*?)</p>', src, re.DOTALL)

    lines = [
        f"## 📡 AI 行业快讯 · No.{issue_num}",
        f'<font color="comment">{datetime_} BJT · 软件开发 / 模型前沿 / 中国动态</font>',
        "",
    ]

    for i, (t, s) in enumerate(zip(titles[:10], summaries[:10]), 1):
        lines.append(f'<font color="info">**{i:02d}** {shorten(t, 36)}</font>')
        lines.append(f'<font color="comment">　▸ {first_clause(s)}</font>')
        lines.append("")

    lines.append(f"**[→ 查看完整 Top 10 精选 ↗]({url})**")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
