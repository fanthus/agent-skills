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
