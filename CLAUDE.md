# AI News Daily — Claude 工作规范

## Git 工作规范

所有变更必须直接提交并 push 到 `main` 分支，不使用特性分支。
无需等待用户明确许可，直接 `git push -u origin main`。

---

## 每次生成新一期的完整流程

### 1. 文件命名

新闻 HTML 文件命名格式为北京时间：`ai-news-YYYYMMDD-HHMM.html`
例：`ai-news-20260506-1554.html`

### 2. 内容页结构

每个新闻内容页必须包含：

**顶部固定导航条**（复制以下模板，填入正确的上一期/下一期链接）：

```html
<nav class="site-nav" aria-label="站点导航">
  <a class="nav-back" href="index.html">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
      <path d="M11 7H3M3 7L7 3M3 7L7 11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    返回列表
  </a>
  <span class="nav-title" aria-hidden="true">AI 行业快讯</span>
  <div class="nav-pager">
    <!-- 若有上一期，替换为 <a class="nav-pager-link" href="上一期文件名"> -->
    <span class="nav-pager-link disabled" aria-hidden="true">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        <path d="M9 3L5 7L9 11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      上一期
    </span>
    <!-- 若有下一期，替换为 <a class="nav-pager-link" href="下一期文件名"> -->
    <span class="nav-pager-link disabled" aria-hidden="true">
      下一期
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
        <path d="M5 3L9 7L5 11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </span>
  </div>
</nav>
```

导航条 CSS（加入页面 `<style>` 块）：

```css
.site-nav {
  position: fixed; top: 0; left: 0; right: 0; height: 48px;
  background: rgba(9,18,40,0.88); backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255,255,255,0.08);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 20px; z-index: 100;
}
.nav-back, .nav-pager-link {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 12px; font-weight: 500; color: #93c5fd;
  text-decoration: none; padding: 5px 10px; border-radius: 6px;
  transition: background .15s, color .15s; white-space: nowrap;
}
.nav-back:hover, .nav-pager-link:hover { background: rgba(255,255,255,0.08); color: #fff; }
.nav-back:focus-visible, .nav-pager-link:focus-visible { outline: 2px solid #60a5fa; outline-offset: 2px; }
.nav-title {
  font-size: 12px; font-weight: 600; color: rgba(255,255,255,0.5);
  letter-spacing: 0.06em; position: absolute; left: 50%; transform: translateX(-50%);
}
.nav-pager { display: flex; gap: 4px; }
.nav-pager-link.disabled { opacity: 0.25; pointer-events: none; }
body { padding-top: 48px; }
@media (max-width: 480px) { .nav-title { display: none; } }
```

**同时**，需要将刚生成的上一期文件的"下一期"按钮从 disabled 改为指向本期的链接。

### 3. 更新 index.html

每次新增一期时，按以下规则更新 `index.html`：

- 将当前 `.featured` 卡片内容**移入** `.archive-list` 的顶部，改用 `archive-card` 样式，期号不变
- 将新一期写成新的 `.featured` 卡片（含本期 6 个话题芯片）
- `archive-card` 中的 badge 使用 `badge-archive`（"往期"）

`index.html` 关键结构：

```html
<!-- 最新一期（每次替换这里） -->
<a class="featured" href="新文件名.html" ...>
  <div class="featured-top">
    <span class="featured-badge">最新一期</span>
    <span class="featured-num" aria-hidden="true">期号</span>
  </div>
  <div class="featured-title">AI 行业快讯 Top 10</div>
  <div class="featured-date">日期 · 北京时间 HH:MM</div>
  <div class="featured-topics">
    <span class="topic-chip">话题1</span>
    <!-- 共 6 个话题芯片 -->
  </div>
  <span class="featured-cta">阅读本期 →</span>
</a>

<!-- 往期（每次将上一期的 featured 移到这里） -->
<nav class="archive-list">
  <a class="archive-card" href="旧文件名.html" ...>
    <div class="archive-num">旧期号</div>
    <div>
      <div class="archive-title">AI 行业快讯 Top 10</div>
      <div class="archive-meta">
        <span class="archive-date">日期 · HH:MM</span>
        <div class="archive-topics-inline">
          <span class="chip-sm">话题1</span>
          <!-- 3-4 个话题 -->
        </div>
      </div>
    </div>
    <div class="archive-right">
      <span class="badge-archive">往期</span>
      <span class="archive-arrow">→</span>
    </div>
  </a>
</nav>
```

### 4. 提交规范

两次独立提交，message 格式：

```
Update AI news YYYY-MM-DD      # 新增内容页
Update AI news YYYY-MM-DD      # 更新 index.html
```

---

## 设计规范

- 内容页头图：深蓝渐变 `linear-gradient(140deg, #060d1f, #0c1f45, #0f3460, #1d4ed8)`
- 卡片布局：左侧彩色竖线区分分类，卡片含编号、分类标签、标题、摘要、来源、原文链接按钮
- 字体：`Instrument Serif`（标题）+ `IBM Plex Mono`（编号/元数据）+ `IBM Plex Sans`（正文）
- 支持移动端响应式，所有动画需有 `prefers-reduced-motion` 兜底
- 所有链接需有 `aria-label`，装饰性 SVG 需有 `aria-hidden="true"`
