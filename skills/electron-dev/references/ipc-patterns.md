# IPC Communication Patterns

This document explains the Inter-Process Communication (IPC) patterns used in Electron and best practices for secure, efficient communication between main and renderer processes.

## Overview

Electron uses a multi-process architecture:
- **Main Process**: Backend, has full access to Node.js and OS APIs
- **Renderer Process**: Frontend, runs in Chromium, should be sandboxed
- **Preload Script**: Bridge between main and renderer, runs before renderer loads

## Security Principles

### The Golden Rule
**Never give the renderer process direct access to Node.js or Electron APIs.**

This prevents:
- Remote code execution attacks
- Unauthorized file system access
- Process spawning by malicious code
- Access to sensitive system APIs

### Required Security Settings

```javascript
// In main.js when creating BrowserWindow
new BrowserWindow({
  webPreferences: {
    contextIsolation: true,      // ✅ Isolate contexts
    nodeIntegration: false,       // ✅ No Node.js in renderer
    sandbox: true,                // ✅ Sandboxed renderer
    preload: path.join(__dirname, 'preload.js'),
  },
});
```

## Communication Patterns

### Pattern 1: Request-Response (invoke/handle)

**Use when**: Renderer needs a response from main process

**Main Process (main.js)**:
```javascript
const { ipcMain } = require('electron');

// Handler returns a value
ipcMain.handle('get:userData', async (event, userId) => {
  // Validate input
  if (typeof userId !== 'string') {
    throw new Error('Invalid user ID');
  }
  
  // Process request
  const userData = await database.getUser(userId);
  return userData;
});
```

**Preload Script (preload.js)**:
```javascript
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  getUserData: (userId) => ipcRenderer.invoke('get:userData', userId),
});
```

**Renderer (renderer.js)**:
```javascript
async function loadUser(userId) {
  try {
    const userData = await window.api.getUserData(userId);
    console.log(userData);
  } catch (error) {
    console.error('Failed to load user:', error);
  }
}
```

### Pattern 2: One-Way Communication (send/on)

**Use when**: Main process needs to notify renderer (no response expected)

**Main Process**:
```javascript
// Send to specific window
mainWindow.webContents.send('notification:new', {
  title: 'New Message',
  body: 'You have a new message',
});

// Send to all windows
const { BrowserWindow } = require('electron');
BrowserWindow.getAllWindows().forEach(window => {
  window.webContents.send('app:update', updateData);
});
```

**Preload Script**:
```javascript
contextBridge.exposeInMainWorld('api', {
  onNotification: (callback) => {
    // Validate callback
    if (typeof callback !== 'function') {
      throw new Error('Callback must be a function');
    }
    
    const listener = (event, data) => callback(data);
    ipcRenderer.on('notification:new', listener);
    
    // Return cleanup function
    return () => {
      ipcRenderer.removeListener('notification:new', listener);
    };
  },
});
```

**Renderer**:
```javascript
// Subscribe to notifications
const unsubscribe = window.api.onNotification((data) => {
  showNotification(data.title, data.body);
});

// Clean up when done
window.addEventListener('beforeunload', () => {
  unsubscribe();
});
```

### Pattern 3: Streaming Data

**Use when**: Need to send multiple updates over time

**Main Process**:
```javascript
ipcMain.handle('file:watch', async (event, filePath) => {
  const watcher = fs.watch(filePath, (eventType, filename) => {
    // Send updates as they happen
    event.sender.send('file:update', { eventType, filename });
  });
  
  return { watchId: Date.now() };
});

ipcMain.handle('file:unwatch', async (event, watchId) => {
  // Clean up watcher
  watchers.get(watchId)?.close();
  watchers.delete(watchId);
});
```

**Preload**:
```javascript
contextBridge.exposeInMainWorld('api', {
  watchFile: async (path, callback) => {
    const listener = (event, data) => callback(data);
    ipcRenderer.on('file:update', listener);
    
    const result = await ipcRenderer.invoke('file:watch', path);
    
    return {
      ...result,
      unwatch: () => {
        ipcRenderer.removeListener('file:update', listener);
        ipcRenderer.invoke('file:unwatch', result.watchId);
      },
    };
  },
});
```

**Renderer**:
```javascript
const watcher = await window.api.watchFile('/path/to/file', (data) => {
  console.log('File changed:', data);
});

// Later, stop watching
watcher.unwatch();
```

## Input Validation

### Always Validate in Main Process

```javascript
ipcMain.handle('file:read', async (event, filePath) => {
  // ❌ BAD: Trust input directly
  // const content = await fs.readFile(filePath, 'utf-8');
  
  // ✅ GOOD: Validate input
  if (typeof filePath !== 'string') {
    throw new Error('File path must be a string');
  }
  
  if (!path.isAbsolute(filePath)) {
    throw new Error('File path must be absolute');
  }
  
  // Optionally: Check if path is within allowed directories
  const allowedDir = app.getPath('documents');
  if (!filePath.startsWith(allowedDir)) {
    throw new Error('Access denied');
  }
  
  const content = await fs.readFile(filePath, 'utf-8');
  return content;
});
```

### Validate in Preload Too

```javascript
// Double validation for defense in depth
contextBridge.exposeInMainWorld('api', {
  readFile: (filePath) => {
    if (typeof filePath !== 'string') {
      return Promise.reject(new Error('Invalid file path'));
    }
    return ipcRenderer.invoke('file:read', filePath);
  },
});
```

## Channel Whitelisting

Limit which IPC channels can be used:

```javascript
// Preload script
const ALLOWED_CHANNELS = [
  'file:read',
  'file:write',
  'dialog:open',
  'notification:show',
];

contextBridge.exposeInMainWorld('api', {
  invoke: (channel, ...args) => {
    if (!ALLOWED_CHANNELS.includes(channel)) {
      throw new Error(`Channel ${channel} not allowed`);
    }
    return ipcRenderer.invoke(channel, ...args);
  },
});
```

## Error Handling

### Return Structured Errors

```javascript
// Main process
ipcMain.handle('file:read', async (event, filePath) => {
  try {
    const content = await fs.readFile(filePath, 'utf-8');
    return { success: true, data: content };
  } catch (error) {
    // Don't expose internal error details
    return { 
      success: false, 
      error: 'Failed to read file',
      code: error.code, // Safe to expose error codes
    };
  }
});

// Renderer
const result = await window.api.readFile(path);
if (result.success) {
  console.log(result.data);
} else {
  console.error(result.error);
}
```

## Common Pitfalls

### ❌ Don't Expose Entire Modules

```javascript
// BAD: Gives renderer full file system access
contextBridge.exposeInMainWorld('fs', require('fs'));

// BAD: Exposes all of Electron
contextBridge.exposeInMainWorld('electron', require('electron'));
```

### ❌ Don't Use Remote Module

```javascript
// BAD: Remote module is deprecated and insecure
const { remote } = require('electron');
const { dialog } = remote;
```

### ❌ Don't Disable Security Features

```javascript
// BAD: Opens security vulnerabilities
new BrowserWindow({
  webPreferences: {
    nodeIntegration: true,        // ❌ Don't do this
    contextIsolation: false,      // ❌ Don't do this
    enableRemoteModule: true,     // ❌ Don't do this
  },
});
```

## Performance Tips

### Batch Operations

```javascript
// ❌ BAD: Multiple IPC calls
for (const file of files) {
  await window.api.processFile(file);
}

// ✅ GOOD: Single IPC call
await window.api.processFiles(files);
```

### Debounce Frequent Updates

```javascript
// Renderer
let debounceTimer;
window.api.onFileChange((data) => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    updateUI(data);
  }, 100);
});
```

### Use Transferable Objects for Large Data

```javascript
// For very large data, consider using MessagePort
// or write to temp file and pass path instead
```

## Testing IPC

```javascript
// In tests, you can mock the API
window.electronAPI = {
  readFile: jest.fn().mockResolvedValue({ success: true, data: 'test' }),
};
```

## Summary Checklist

- ✅ Use `contextIsolation: true`
- ✅ Use `nodeIntegration: false`
- ✅ Validate all inputs in main process
- ✅ Whitelist allowed IPC channels
- ✅ Return structured errors
- ✅ Clean up event listeners
- ✅ Use invoke/handle for request-response
- ✅ Use send/on for one-way communication
- ❌ Never expose full Node.js/Electron APIs
- ❌ Never trust renderer input without validation
