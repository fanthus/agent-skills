---
name: appstore-competitor-analysis
description: Analyze App Store competitor landscapes and product opportunities for iOS app ideas. Use when Codex needs to evaluate an App Store product direction, compare competing apps, inspect market demand, pricing, reviews, subscriptions, positioning, negative feedback, or produce a product hypothesis, MVP scope, differentiation angle, and go/no-go recommendation for an app idea.
---

# App Store Competitor Analysis

## Overview

Use this skill to turn App Store competitor research into a product decision. Focus on whether a market has demand, whether users pay, where existing apps disappoint users, and whether a smaller, simpler, cheaper, or more focused app can enter.

The final output should be a testable product hypothesis, not only a feature comparison.

## Operating Mode

- Work in Chinese by default unless the user asks otherwise.
- Use concise Markdown that remains readable in source mode; prefer headings and lists over tables.
- Browse or otherwise verify current App Store-facing facts when the user asks for a real market, competitor set, prices, recent reviews, rankings, screenshots, release cadence, or "latest/current" evidence.
- If the user provides competitor notes, reviews, URLs, screenshots, exports, or keyword lists, prioritize those materials and only browse to fill gaps.
- Separate facts from inference. Mark assumptions explicitly when evidence is thin.
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

### 3. Segment competitors into three layers

Do not mix all competitors into one list. Classify them by strategic role:

- Head competitors: validate market size, willingness to pay, category expectations, trust signals, and premium ceiling.
- Mid-tier competitors: reveal lighter feature bundles, pricing patterns, narrower positioning, and feasible replication paths.
- Long-tail competitors: reveal niche scenarios, rough execution, underserved users, and low-quality opportunities.

Use the head layer to answer "does anyone pay for this?" Use the long tail to answer "where can a small product enter?"

### 4. Analyze beyond feature lists

For each important competitor, extract:

- Core pain solved
- Reason users pay
- Free limit or paywall position
- Reasons users praise it
- Reasons users criticize it
- Trust-building mechanisms
- Complexity that creates room for a simpler product
- Pricing friction or subscription resentment

Prefer extracting payment reasons, user dissatisfaction, and entry opportunities over building a broad feature matrix.

### 5. Prioritize negative reviews

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

### 6. Form the product hypothesis

Convert research into one sentence:

> 做一个给 [细分用户] 用的 [轻工具]，解决他们在 [现有竞品/现有方案] 里遇到的 [高频痛点]，用 [差异化方式] 收费。

Also include:

- Target user
- Existing alternatives
- Main dissatisfaction
- Differentiation angle
- Monetization assumption
- MVP validation path

### 7. Decide whether it is worth building

Score the opportunity using six questions:

- Is the user pain strong enough?
- Is there real payment validation?
- Can the user build 80% of the core experience?
- Is there a clear differentiation point?
- Are acquisition keywords or channels reachable?
- Is maintenance risk controllable?

If at least four answers are positive, recommend MVP validation. If fewer than four are positive, recommend narrowing the niche, changing positioning, or abandoning the direction.

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

## 3. 竞品分层
- 头部竞品：
- 腰部竞品：
- 长尾竞品：

## 4. 关键发现
- 用户为什么付费：
- 用户主要不满：
- 竞品共同弱点：

## 5. 产品假设
做一个给 [细分用户] 用的 [轻工具]，解决 [痛点]，用 [差异化方式] 收费。

## 6. 是否值得做
- 痛点强度：
- 付费验证：
- 实现难度：
- 差异化：
- 获客机会：
- 维护风险：
- 结论：

## 7. 下一步
- [ ] 下载体验核心竞品
- [ ] 收集差评并归类
- [ ] 记录价格和免费限制
- [ ] 做 MVP 功能清单
- [ ] 验证关键词和商店页表达
```

## Quality Bar

- Make the decision useful even when evidence is incomplete.
- Avoid pretending a market is attractive only because many competitors exist.
- Avoid recommending a full-featured clone.
- Anchor the opportunity in a specific underserved user, repeated dissatisfaction, and an achievable MVP.
- End with concrete next steps that test the riskiest assumption first.
