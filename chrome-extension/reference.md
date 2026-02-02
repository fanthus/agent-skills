# Chrome Extension Reference

## Manifest V3 vs V2

| V2 | V3 |
|----|-----|
| `background.scripts` (persistent page) | `background.service_worker` (single JS file) |
| `browser_action` / `page_action` | `action` |
| Permissions mixed with host access | `permissions` + `host_permissions` |
| `web_accessible_resources` as array | `web_accessible_resources` as array of `{ resources, matches }` |

Service worker has no DOM; it is terminated when idle. Use `chrome.storage` for state; avoid long timers or open connections that assume a live script.

## Messaging

- **One-off**: `chrome.runtime.sendMessage(payload, (response) => {})`. Listener returns a value or `Promise` for the response; return `true` from listener to allow async reply.
- **Long-lived**: `chrome.runtime.connect()` / `chrome.tabs.connect(tabId)` for port; `port.postMessage` / `port.onMessage.addListener`.
- **Content ↔ background**: Content script uses `chrome.runtime.sendMessage`; background uses `chrome.tabs.sendMessage(tabId, payload)` to reach a content script in a tab.

## Storage

- `chrome.storage.local`: up to 10MB (or more with `unlimitedStorage`).
- `chrome.storage.sync`: synced across devices; quota ~100KB total, 8KB per item.
- `chrome.storage.session`: in-memory for the session (MV3).
- All are async: `chrome.storage.*.get/set/remove/clear`. Use `await` in async context.

## Tabs

- `chrome.tabs.query({ active: true, currentWindow: true })` → current tab.
- `chrome.tabs.create`, `chrome.tabs.update`, `chrome.tabs.remove`.
- `chrome.tabs.sendMessage(tabId, payload)` to content script; tab must have a matching content script loaded.
- Permission: `tabs` (read tab metadata) or `activeTab` (current tab only on user gesture).

## Scripting (Inject Scripts)

- `chrome.scripting.executeScript({ target: { tabId }, files: ["script.js"] })` or `func: () => { ... }` for one-off injection.
- `chrome.scripting.insertCSS({ target: { tabId }, files: ["style.css"] })`.
- Requires `scripting` and host permission (or `activeTab` when triggered from extension UI).

## Optional Permissions

Declare in manifest under `optional_permissions`; request at runtime with `chrome.permissions.request({ permissions: ["tabs"] })`. Check with `chrome.permissions.contains`.

## Official Docs

- [Chrome Extensions (developer.chrome.com)](https://developer.chrome.com/docs/extensions)
- [Manifest reference](https://developer.chrome.com/docs/extensions/reference/manifest)
- [Migration to MV3](https://developer.chrome.com/docs/extensions/develop/migrate/what-is-mv3)
