---
name: appstore-competitor-analysis
description: Analyze App Store competitor landscapes and product opportunities for iOS app ideas. Use when Codex needs to evaluate an App Store product direction, compare competing apps, inspect market demand, pricing, reviews, subscriptions, revenue/download estimates, business metrics, positioning, negative feedback, or produce a product hypothesis, MVP scope, differentiation angle, and go/no-go recommendation for an app idea.
---

# App Store Competitor Analysis

## Overview

Use this skill to turn App Store competitor research into a product decision. Focus on whether a market has demand, whether users pay, where existing apps disappoint users, and whether a smaller, simpler, cheaper, or more focused app can enter.

The final output should be a testable product hypothesis and a rough business case, not only a feature comparison.

## Operating Mode

- Work in Chinese by default unless the user asks otherwise.
- Use concise Markdown that remains readable in source mode; prefer headings and lists over tables.
- Browse or otherwise verify current App Store-facing facts when the user asks for a real market, competitor set, prices, recent reviews, rankings, screenshots, release cadence, or "latest/current" evidence.
- When the user asks for business demand or commercial potential, collect numeric signals: price, IAP tiers, subscription terms, ratings count, review volume, category rank if available, update recency, age of app, visible ads, and any public revenue/download estimates.
- Search public channels for revenue and download clues when useful: App Store pages, App Store web search snippets, Sensor Tower/data.ai/Appfigures/AppMagic public pages or reports, developer blogs, maker revenue posts, press releases, investor filings, acquisition announcements, podcast/news interviews, and reputable SEO/ASO tools with public snippets.
- If the user provides competitor notes, reviews, URLs, screenshots, exports, or keyword lists, prioritize those materials and only browse to fill gaps.
- Separate facts from inference. Mark assumptions explicitly when evidence is thin.
- Do not present third-party revenue estimates or model-derived estimates as exact truth. Use ranges, name the source, and label confidence.
- Do not over-optimize for exhaustive coverage. Prefer enough evidence to decide the next validation step.

## Workflow

### 1. Clarify the user's constraints

Before judging competitors, identify the user's own boundary conditions:

- Solo or team capacity
- Development, design, content, marketing, operations, and support capabilities
- API, storage, model, or data costs
- Preferred business model: subscription, one-time purchase, ads, freemium, hybrid
- Long-term maintenance, compliance, customer support, and data risk tolerance
- Explicit "will not do" constraints

If constraints are missing and the user wants immediate progress, state reasonable assumptions and continue.

### 2. Check three market signals

Evaluate the direction only when there is evidence for all three signals:

- Demand signal: users search, download, review, and competitors still update.
- Payment signal: competitors use subscriptions, in-app purchases, one-time purchase, or visible monetization tied to the core need.
- Gap signal: repeated complaints reveal unresolved pain.

The best opportunity pattern is: users pay, and users are still dissatisfied.

### 3. Quantify business signals

For important competitors, record the hard numbers before interpreting:

- Store metrics: rating score, rating count, review count if visible, category, country/storefront, launch or first visible version date, latest update date, app size, supported platforms, and privacy/data collection claims.
- Monetization: free/paid download price, IAP list, subscription period, lifetime option, ad presence, paywall position, free limits, refund/subscription complaints.
- Public estimates: monthly downloads, monthly revenue, rank history, category rank, MAU/DAU, or grossing rank from any public source. Cite the source and date.
- Derived estimates when public revenue is missing:
  - Downloads range from rating count using an explicit rating-rate assumption, commonly `ratings / 3%` to `ratings / 0.3%`, with `ratings / 1%` as a middle scenario.
  - Gross one-time revenue range from estimated paid purchases times price or IAP conversion assumptions.
  - Subscription MRR/ARR range from estimated active subscribers times monthly or annual price.
  - Net developer revenue should be shown separately only when useful, using Apple commission assumptions such as 70% or 85% after platform fees.
- Unit economics: estimate what must be true to reach a target such as RMB 1k/10k/50k monthly gross revenue: required paid users, subscribers, conversion rate, or installs.

Use simple ranges over fake precision. If evidence is weak, say so and use the numbers only for directional comparison.

### 4. Segment competitors into three layers

Do not mix all competitors into one list. Classify them by strategic role:

- Head competitors: validate market size, willingness to pay, category expectations, trust signals, and premium ceiling.
- Mid-tier competitors: reveal lighter feature bundles, pricing patterns, narrower positioning, and feasible replication paths.
- Long-tail competitors: reveal niche scenarios, rough execution, underserved users, and low-quality opportunities.

Use the head layer to answer "does anyone pay for this?" Use the long tail to answer "where can a small product enter?"

### 5. Analyze beyond feature lists

For each important competitor, extract:

- Core pain solved
- Reason users pay
- Key numbers: price, IAP tiers, rating count, update recency, public or estimated revenue/download range
- Free limit or paywall position
- Reasons users praise it
- Reasons users criticize it
- Trust-building mechanisms
- Complexity that creates room for a simpler product
- Pricing friction or subscription resentment

Prefer extracting payment reasons, user dissatisfaction, and entry opportunities over building a broad feature matrix.

### 6. Prioritize negative reviews

Treat positive reviews as proof of market acceptance and negative reviews as opportunity evidence.

Look especially for repeated complaints about:

- Too expensive
- Too complex
- Too many ads
- Misleading subscription
- Data loss
- Hard export
- Instability
- Poor support
- A specific workflow or scenario being underserved

If multiple competitors are criticized for the same issue, treat it as a candidate entry point.

### 7. Form the product hypothesis

Convert research into one sentence:

> 做一个给 [细分用户] 用的 [轻工具]，解决他们在 [现有竞品/现有方案] 里遇到的 [高频痛点]，用 [差异化方式] 收费。

Also include:

- Target user
- Existing alternatives
- Main dissatisfaction
- Differentiation angle
- Monetization assumption
- Business target and required numbers
- MVP validation path

### 8. Decide whether it is worth building

Score the opportunity using six questions:

- Is the user pain strong enough?
- Is there real payment validation?
- Can the user build 80% of the core experience?
- Is there a clear differentiation point?
- Are acquisition keywords or channels reachable?
- Is maintenance risk controllable?

Also score the business case:

- Is there evidence that competitors make meaningful revenue, or at least that users pay at non-trivial prices?
- Can a small app plausibly reach the user's target revenue with realistic installs and conversion?
- Is the monetization model aligned with usage frequency, or will users resent it?

If at least four product answers are positive and the business case is plausible, recommend MVP validation. If fewer than four product answers are positive or the business case requires unrealistic conversion/acquisition, recommend narrowing the niche, changing positioning, or abandoning the direction.

## Output Format

Use this structure by default:

```markdown
# 竞品分析：[赛道/产品方向]

## 1. 我的约束
- 能力：
- 成本：
- 商业模式：
- 不做什么：

## 2. 赛道信号
- 需求信号：
- 付费信号：
- 缺口信号：

## 3. 关键指标
- 价格/IAP：
- 评分与评论：
- 更新频率：
- 排名/下载：
- 公开收入线索：
- 粗略收入估算：
- 证据可信度：

## 4. 竞品分层
- 头部竞品：
- 腰部竞品：
- 长尾竞品：

## 5. 关键发现
- 用户为什么付费：
- 用户主要不满：
- 竞品共同弱点：
- 能否达到目标收入：

## 6. 产品假设
做一个给 [细分用户] 用的 [轻工具]，解决 [痛点]，用 [差异化方式] 收费。

## 7. 是否值得做
- 痛点强度：
- 付费验证：
- 收入潜力：
- 实现难度：
- 差异化：
- 获客机会：
- 维护风险：
- 结论：

## 8. 下一步
- [ ] 下载体验核心竞品
- [ ] 收集差评并归类
- [ ] 记录价格和免费限制
- [ ] 查询公开收入/下载/排名线索
- [ ] 建立低/中/高三档收入估算
- [ ] 做 MVP 功能清单
- [ ] 验证关键词和商店页表达
```

## Quality Bar

- Make the decision useful even when evidence is incomplete.
- Prefer explicit numbers and ranges over vague words like "many", "cheap", or "popular" when public data allows.
- Avoid pretending a market is attractive only because many competitors exist.
- Avoid pretending estimated revenue is known fact; mark source and confidence.
- Avoid recommending a full-featured clone.
- Anchor the opportunity in a specific underserved user, repeated dissatisfaction, and an achievable MVP.
- End with concrete next steps that test the riskiest assumption first, especially willingness to pay and reachable acquisition volume.
