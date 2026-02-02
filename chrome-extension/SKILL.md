---
name: chrome-extension
description: Build Chrome extensions using Manifest V3. Covers manifest structure, popup/options/background (service worker), content scripts, and chrome.* APIs. Use when creating or modifying a Chrome extension, browser extension, or Chrome plugin.
---

# Chrome Extension (Manifest V3)

## Quick Start

Use **Manifest V3** only. Do not use Manifest V2 (deprecated).

Minimal directory layout:

```
extension/
├── manifest.json
├── icons/           # 16, 48, 128 px
├── popup.html       # optional
├── popup.js
├── background.js    # service worker
├── content.js       # optional, injected into pages
└── options.html     # optional
```

## Manifest

Required fields and common keys:

```json
{
  "manifest_version": 3,
  "name": "Extension Name",
  "version": "1.0.0",
  "description": "Short description",
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  },
  "action": {
    "default_popup": "popup.html",
    "default_icon": "icons/icon16.png",
    "default_title": "Click for options"
  },
  "background": {
    "service_worker": "background.js"
  },
  "permissions": [],
  "host_permissions": []
}
```

- **permissions**: API access, e.g. `"storage"`, `"tabs"`, `"activeTab"`, `"scripting"`.
- **host_permissions**: URL patterns for content scripts / fetch, e.g. `"<all_urls>"` or `"https://example.com/*"`.
- **content_scripts**: Injected into matching pages; use `"matches"` and optionally `"run_at": "document_idle"` (default) / `"document_start"` / `"document_end"`.

## Background (Service Worker)

- Single file: `background.js`. No DOM, no `window`; use `chrome.*` APIs.
- Persists only while in use; avoid long-lived globals. Use `chrome.storage` for state.
- Listen for install/startup:

```javascript
chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed');
});
```

- Message from popup/content: `chrome.runtime.sendMessage` / `chrome.runtime.onMessage.addListener`. Return `true` from listener if replying asynchronously.

## Popup

- Popup is an HTML page; script it with a normal `<script src="popup.js">`. Lifecycle is short (closed when popup loses focus).
- To talk to background: `chrome.runtime.sendMessage`. To talk to content script: `chrome.tabs.sendMessage(tabId, payload)` (need `activeTab` or host permission and `chrome.tabs.query`).

## Content Scripts

- Run in page context but in an isolated world; no direct access to page JS. Share DOM.
- Inject via manifest:

```json
"content_scripts": [{
  "matches": ["https://example.com/*"],
  "js": ["content.js"],
  "run_at": "document_idle"
}]
```

- Or programmatically: `chrome.scripting.executeScript({ target: { tabId }, files: ["content.js"] })` (needs `scripting` and host/tab permission).
- To pass data: `chrome.runtime.sendMessage` to background; from page to content use custom events or `window.postMessage` (content script listens on `window`).

## Common APIs

| Need | Permission / API | Note |
|------|------------------|------|
| Persist data | `storage` | `chrome.storage.local` or `chrome.storage.sync` |
| Current tab | `activeTab` or `tabs` | `chrome.tabs.query({ active: true, currentWindow: true })` |
| Run script in tab | `scripting` + host/tab | `chrome.scripting.executeScript` |
| Notifications | `notifications` | `chrome.notifications.create` |
| Badge/text on icon | — | `chrome.action.setBadgeText` / `setBadgeBackgroundColor` |

Storage example:

```javascript
// Write
await chrome.storage.local.set({ key: 'value' });
// Read
const { key } = await chrome.storage.local.get('key');
```

## Loading and Debugging

1. Open `chrome://extensions/`, enable "Developer mode".
2. "Load unpacked" → select the extension folder (the one containing `manifest.json`).
3. Errors: "Errors" button on the card; background: "Service worker" link; popup/content: right‑click popup or page → Inspect.

## Checklist for New Extensions

- [ ] `manifest_version: 3` and all required fields (name, version, description, icons).
- [ ] `background.service_worker` (no `background.page` or V2 scripts).
- [ ] Permissions and `host_permissions` minimal and justified.
- [ ] Popup/options are plain HTML+JS; no bundler required for simple extensions.
- [ ] Content script `matches` are as narrow as needed.

## Additional Resources

- For detailed Chrome extension API reference and migration from V2, see [reference.md](reference.md).
