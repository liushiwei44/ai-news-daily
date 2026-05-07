#!/usr/bin/env python3
"""Build a punchy WeChat Work Markdown notification body.

Strategy: HTML card titles are already structured as
    "<HOOK>，<DETAIL>"  or  "<HOOK>：<DETAIL>"
We split at the first major punctuation and use:
  - HOOK   → punchy bold headline
  - DETAIL → click-worthy supporting fact

This is far more compelling than extracting the descriptive
opening sentence of the long card-summary paragraph.
"""
import sys
import re
import html as html_mod


CAT_EMOJI = {
    "cat-cn":    "🇨🇳",
    "cat-dev":   "💻",
    "cat-model": "🧠",
    "cat-biz":   "💰",
    "cat-ind":   "🏭",
    "cat-sec":   "🔒",
}


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", html_mod.unescape(s)).strip()


def split_title(title: str):
    """Find first major break and return (hook, detail)."""
    title = clean(title)
    for sep in ("：", "，", "；"):
        idx = title.find(sep)
        # 钩子至少 6 字，detail 至少 5 字才算有效切分
        if 6 <= idx and len(title) - idx > 5:
            return title[:idx], title[idx + 1:].strip()
    return title, ""


def truncate_detail(s: str, max_n: int = 44) -> str:
    """Trim detail to ≤max_n, prefer natural punctuation breaks."""
    s = clean(s)
    if len(s) <= max_n:
        return s
    for sep in ("，", "；", "、"):
        idx = s.rfind(sep, 18, max_n)
        if idx > 0:
            return s[:idx]
    return s[: max_n - 1] + "…"


def first_sentence(s: str, max_len: int = 44) -> str:
    """Fallback: extract first complete clause from card-summary."""
    s = clean(s)
    # 跳过以日期开头的引子，直奔事实
    s = re.sub(r"^\d+\s*年\s*\d+\s*月[^，]*[，,]\s*", "", s)
    s = re.sub(r"^\d+\s*月\s*\d+\s*日[，,：:]\s*", "", s)
    idx = s.find("。")
    if 0 < idx <= max_len:
        return s[:idx]
    return truncate_detail(s, max_len)


def main() -> None:
    html_path, issue_num, datetime_, url = sys.argv[1:5]
    with open(html_path, encoding="utf-8") as f:
        src = f.read()

    pattern = re.compile(
        r'<article class="card (cat-[\w-]+)".*?'
        r'<div class="card-title">(.*?)</div>.*?'
        r'<p class="card-summary">(.*?)</p>',
        re.DOTALL,
    )
    cards = pattern.findall(src)

    lines = [
        f"📡 **AI 行业快讯**  ·  No.{issue_num}",
        f'<font color="comment">{datetime_} BJT  |  软件开发 · 模型前沿 · 中国动态</font>',
        "",
    ]

    for i, (cat, title, summary) in enumerate(cards[:10], 1):
        emoji = CAT_EMOJI.get(cat, "📌")
        hook, detail = split_title(title)
        if detail:
            detail = truncate_detail(detail)
        else:
            detail = first_sentence(summary)

        # 第一行：橙色编号 + 分类 emoji + 加粗钩子标题
        lines.append(f'<font color="warning">{i:02d}</font> {emoji} **{hook}**')
        # 第二行：灰色 ▸ 引导符 + 简练摘要（不缩进，避免对齐问题）
        lines.append(f'<font color="comment">▸ {detail}</font>')
        lines.append("")

    lines.append(f"**[ 📖 阅读完整 Top 10 精选 → ]({url})**")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
