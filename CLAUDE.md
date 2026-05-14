# AI News Daily — Claude 工作规范

## Git 工作流（重要 · 必须严格遵守）

本仓库通过 Claude Code Web 平台运行，平台会**强制为每个会话创建独立的 feature 分支**（形如 `claude/xxx-yyy-zzz`），并**禁止直接推送 main**。直接 `git push origin HEAD:main` 会返回 403 失败，不要再尝试。

### 标准发布流程（每次任务都要走完整闭环）

1. 在平台指定的 feature 分支上完成所有提交（`git commit`）。
2. `git push -u origin <feature-branch>` 推送到远程。
3. 平台会自动为该分支创建 Pull Request（如 PR #N），无需自己 `gh pr create`。
4. **任务的最后一步必须执行**：调用 GitHub MCP 工具 `mcp__github__merge_pull_request` 把 PR squash 合并到 main：
   - `merge_method`: `"squash"`
   - `commit_title`: 与本次任务的提交信息保持一致（如 `Update AI news 2026-05-14`）
5. 调用 `mcp__github__pull_request_read` 确认 `merged: true`，再向用户报告"已发布到 main"。

> ⚠️ **没有执行第 4 步 = 任务未完成**。只推到 feature 分支但没合并 PR，main 不会更新，GitHub Pages / 通知不会发布，用户会看不到结果。

### 不要再做的事

- 不要执行 `git push origin HEAD:main`（会 403）。
- 不要执行 `git checkout main && git merge ...` 然后推 main（同样会 403）。
- 不要等用户手动合并 PR——任务流程要求 Claude 自己合并完才算结束。

## 内容规范

### 时间变量
任务开始前先执行下面两条命令拿到当前北京时间，后续严格使用：
```bash
TZ='Asia/Shanghai' date '+%Y%m%d-%H%M'   # {TIME}，形如 20260514-0805
TZ='Asia/Shanghai' date '+%Y-%m-%d'      # {DATE}，形如 2026-05-14
```

### 设计规范（与现有页面保持一致）
- 字体：`Noto Serif SC`（卡片标题）· `IBM Plex Mono`（编号/元数据）· `IBM Plex Sans`（正文）
- 头图渐变：`linear-gradient(140deg, #060d1f, #0c1f45, #0f3460, #1d4ed8)`
- 卡片：左侧彩色竖线分类，含编号 · 分类标签 · 标题 · 摘要 · 来源 · 原文链接按钮
- 响应式布局 + `prefers-reduced-motion` + `aria-label` + 装饰性 SVG 加 `aria-hidden="true"`
- 顶部固定 `.site-nav`：左"返回列表"→ `index.html`；中"AI 行业快讯"；右"上一期 / 下一期"。本期作为最新一期，"下一期"按钮 `disabled`。
- 发布新一期时要同步把上一期 HTML 的"下一期"按钮从 `disabled` 改为指向本期文件。

### 提交信息
两次提交都使用 `Update AI news {DATE}`：
- 第一次：新增本期 HTML + 改上一期的"下一期"链接
- 第二次：更新 `index.html`（旧 featured 移入 archive，本期写为新 featured + 6 个话题芯片）
