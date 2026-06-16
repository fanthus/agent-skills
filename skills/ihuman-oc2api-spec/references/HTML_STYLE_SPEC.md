# OC API HTML 展示样式规范

用于将 `markdown-it` 等工具生成的裸 HTML 片段包装成适合阅读的完整静态页面。HTML 内容必须以 Markdown 为唯一来源；包装层只能改变展示方式，不得增删接口、字段、枚举或表格内容。

## 生成顺序

1. 先生成并保存 `docs/API_DOC_OC_YYYYMMDD.md`。
2. 用 Markdown 生成同名 HTML 片段，例如 `markdown-it docs/API_DOC_OC_YYYYMMDD.md -o /tmp/API_DOC_OC_YYYYMMDD.fragment.html`。
3. 将 HTML 片段嵌入完整页面模板，输出 `docs/API_DOC_OC_YYYYMMDD.html`。
4. 删除临时片段文件。
5. 校验完整 HTML 页面结构和增强脚本语法。

## 页面结构

完整 HTML 必须包含：

- `<!doctype html>`、`<html lang="zh-CN">`、`<head>`、`<body>`。
- `meta charset="utf-8"` 和响应式 viewport。
- 页面标题：`SuperClass SDK OC 网络接口文档`。
- 一个左侧目录区：`.toc-panel`。
- 一个正文区：`.content > .doc`，正文内嵌 Markdown 转换出的 HTML 片段。
- 返回顶部链接。

## 推荐展示增强

使用内联 CSS 和少量原生 JavaScript，保证文件可直接双击打开，不依赖外部资源。

- 左侧固定目录：从正文中找到 `## 目录` 及其后续目录节点，移动到 `.toc-panel`。
- 表格包装：为所有 `table` 外层增加 `.table-wrap`，支持长字段横向滚动。
- 表头样式：`thead th` 使用稳定背景；在滚动表格内可 sticky。
- 代码展示：普通 `code` 用浅色标签样式，`pre code` 用深色代码块样式。
- HTTP Method：将单元格文本 `POST` 渲染为 `.method-badge`。
- 移动端：窄屏下目录改为顶部区域，正文单列布局。
- 打印：隐藏目录和返回顶部，表格取消阴影并适配纸面。

## 视觉约束

- 面向 SDK/API 文档，优先清晰、稳定、密集可扫读；避免营销页、装饰性大图和过度动画。
- 表格、代码块、目录项的圆角不超过 `8px`。
- 不使用外部字体、图片或 CDN。
- 避免单一大面积高饱和配色；推荐中性背景、白色正文面、青绿色或其他低饱和强调色。
- 正文字体不要随 viewport 宽度缩放；标题可使用 `clamp()`。
- 不要让长字段撑破页面：表格必须可横向滚动，字段 code 允许换行或在表格内滚动。

## 校验要求

生成后至少检查：

- HTML 以 `<!doctype html>` 开头，以 `</html>` 结束。
- `head`、`body`、`h1`、目录、表格均存在。
- 增强脚本通过语法检查，例如抽出 `<script>` 内容后执行 `node --check`。
- HTML 标签无明显未闭合问题。
- 表格数量与 Markdown 转换结果一致，或全部原始表格都能被 `.table-wrap` 接管。

## 最小模板要点

模板可自由调整，但必须包含这些选择器，方便后续维护：

```html
<aside class="toc-panel" aria-label="文档目录">
  <div class="toc-brand">...</div>
  <nav id="tocMount"></nav>
</aside>
<main class="content">
  <article class="doc" id="top">
    <!-- Markdown HTML fragment -->
  </article>
</main>
<a class="top-link" href="#top" aria-label="返回顶部">↑</a>
```

增强脚本的职责应保持有限：移动目录、包装表格、标记小节标题、渲染 `POST` 徽标和高亮当前目录项。不要在脚本里生成接口内容。
