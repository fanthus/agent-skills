## [ERR-20260520-001] skill-creator-generate-openai-yaml

**Logged**: 2026-05-20T19:43:32+08:00
**Priority**: low
**Status**: pending
**Area**: config

### Summary
`generate_openai_yaml.py` failed because the current Python environment does not include the `yaml` module.

### Details
While creating `ihuman-aixue-requirement-advisor`, the metadata generation script raised `ModuleNotFoundError: No module named 'yaml'`.

### Suggested Action
Use the bundled Python environment when available, install PyYAML for the active Python, or write `agents/openai.yaml` manually using the documented schema.

### Metadata
- Source: error
- Related Files: /Users/fanthus/.codex/skills/.system/skill-creator/scripts/generate_openai_yaml.py
- Tags: python, skill-creator, yaml
## [ERR-20260602-001] apply_patch

**Logged**: 2026-06-02T16:09:37+08:00
**Priority**: low
**Status**: pending
**Area**: docs

### Summary
Patch failed because the expected line omitted the leading Markdown list marker.

### Error
```
apply_patch verification failed: Failed to find expected lines in /Users/fanthus/.agents/skills/appstore-listing-writer/SKILL.md:
可根据需要生成中文、英文或多语言版本
```

### Context
- Operation attempted: updating the appstore-listing-writer skill output rules.
- The file contained `- 可根据需要生成中文、英文或多语言版本`, so the patch context did not match.

### Suggested Fix
Use exact file context from a fresh read, or make smaller patches around stable section headings.

### Metadata
- Reproducible: yes
- Related Files: /Users/fanthus/.agents/skills/appstore-listing-writer/SKILL.md

---
