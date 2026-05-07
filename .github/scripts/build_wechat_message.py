#!/usr/bin/env python3
"""Build a richly-formatted WeChat Work Markdown notification body."""
import sys
import re
import html as html_mod


# 卡片分类 → emoji（与 HTML 中 cat-* class 对应）
CAT_EMOJI = {
    "cat-cn":    "🇨🇳",   # 中国动态
    "cat-dev":   "💻",   # 开发者工具
    "cat-model": "🧠",   # 模型前沿
    "cat-biz":   "💰",   # 商业 / 行业格局
    "cat-ind":   "🏭",   # 产业 / 报告
    "cat-sec":   "🔒",   # 安全
}


def clean(s: str) -> str:
    """合并空白、解码 HTML 实体。"""
    return re.sub(r"\s+", " ", html_mod.unescape(s)).strip()


def shorten_title(s: str, max_n: int = 38, min_n: int = 22) -> str:
    """在 [min_n, max_n] 区间内寻找自然断点（中文标点）截断标题。"""
    s = clean(s)
    if len(s) <= max_n:
        return s
    best = -1
    for sep in ("，", "：", "；", "、"):
        idx = s.rfind(sep, min_n, max_n)
        if idx > best:
            best = idx
    if best > 0:
        return s[:best]
    return s[: max_n - 1] + "…"


def first_sentence(s: str, max_len: int = 78) -> str:
    """优先取首个完整句子（句号截断）；否则在自然标点处截断。"""
    s = clean(s)
    idx = s.find("。")
    if 0 < idx <= max_len:
        return s[:idx]
    for sep in ("，", "；", "："):
        bi = s.rfind(sep, 30, max_len)
        if bi > 0:
            return s[:bi] + "…"
    return s[: max_len - 1] + "…"


def main() -> None:
    html_path, issue_num, datetime_, url = sys.argv[1:5]

    with open(html_path, encoding="utf-8") as f:
        src = f.read()

    # 一次性提取每张卡片的：分类、标题、摘要
    pattern = re.compile(
        r'<article class="card (cat-[\w-]+)".*?'
        r'<div class="card-title">(.*?)</div>.*?'
        r'<p class="card-summary">(.*?)</p>',
        re.DOTALL,
    )
    cards = pattern.findall(src)

    lines = [
        f"🤖 **AI 行业快讯**　·　No.{issue_num}",
        f'<font color="comment">📅 {datetime_} BJT　|　软件开发 · 模型前沿 · 中国动态</font>',
        "",
    ]

    for i, (cat, title, summary) in enumerate(cards[:10], 1):
        emoji = CAT_EMOJI.get(cat, "📌")
        t = shorten_title(title)
        s = first_sentence(summary)
        # 一行：橙色编号 + 分类 emoji + 加粗黑色标题
        lines.append(f'<font color="warning">{i:02d}</font>　{emoji}　**{t}**')
        # 二行：灰色首句摘要，全角空格缩进对齐编号下方
        lines.append(f'<font color="comment">　　　　{s}</font>')
        lines.append("")

    lines.append(f"**[　📖 阅读完整 Top 10 精选 ↗　]({url})**")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
