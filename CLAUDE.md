# AI News Daily — Claude 工作规范

## Git
所有变更直接提交并 push 到 `main` 分支，不使用特性分支，无需确认。

## 设计规范（与现有页面保持一致）
- 字体：`Noto Serif SC`（卡片标题）· `IBM Plex Mono`（编号/元数据）· `IBM Plex Sans`（正文）
- 头图渐变：`linear-gradient(140deg, #060d1f, #0c1f45, #0f3460, #1d4ed8)`
- 卡片：左侧彩色竖线分类，含编号 · 分类标签 · 标题 · 摘要 · 来源 · 原文链接按钮
- 响应式布局 + `prefers-reduced-motion` + `aria-label` + 装饰性 SVG 加 `aria-hidden="true"`
