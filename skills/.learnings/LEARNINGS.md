## [LRN-20260520-001] skill-live-doc-source

**Logged**: 2026-05-20T20:05:45+08:00
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
For product-advisor skills, the user expects embedded document links to be read live, not copied into the skill as stale snapshots.

### Details
When adding Feishu product documentation to `ihuman-aixue-requirement-advisor`, storing a summarized copy in `references/product-requirements.md` did not match the user's intent. The desired behavior is to store the source link and reading workflow, then fetch the latest document content during each relevant request.

### Suggested Action
For skills backed by changing product documents, store source registries and live-reading rules. Only create snapshots when explicitly requested.

### Metadata
- Source: user_feedback
- Related Files: /Users/fanthus/.agents/skills/ihuman-aixue-requirement-advisor/references/product-requirements.md
- Tags: skills, product-docs, feishu, live-source

---
