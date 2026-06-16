# Electron Security Guide

Comprehensive security best practices for Electron applications.

## Security Fundamentals

### Threat Model

Electron applications face unique security challenges:
- **Web content risks**: XSS, CSRF, malicious scripts
- **Node.js access**: Unrestricted file system and process access
- **Native API exposure**: System-level capabilities
- **Update mechanisms**: Potential for malicious updates
- **External content**: Loading untrusted remote content

### Defense in Depth

Apply multiple layers of security:
1. Secure defaults in configuration
2. Input validation and sanitization
3. Least privilege principle
4. Process isolation
5. Content Security Policy
6. Regular security updates

## Configuration Checklist

### BrowserWindow Security Settings

```javascript
const secureWindow = new BrowserWindow({
  width: 1200,
  height: 800,
  webPreferences: {
    // ✅ CRITICAL: Enable context isolation
    contextIsolation: true,
    
    // ✅ CRITICAL: Disable node integration
    nodeIntegration: false,
    
    // ✅ RECOMMENDED: Enable sandbox
    sandbox: true,
    
    // ✅ REQUIRED: Use preload script
    preload: path.join(__dirname, 'preload.js'),
    
    // ✅ RECOMMENDED: Enable web security
    webSecurity: true,
    
    // ✅ RECOMMENDED: Disable remote module (deprecated anyway)
    enableRemoteModule: false,
    
    // ✅ RECOMMENDED: Disable navigation on drag/drop
    navigateOnDragDrop: false,
    
    // ✅ OPTIONAL: Disable dev tools in production
    devTools: process.env.NODE_ENV === 'development',
  },
});
```

### Content Security Policy

```javascript
// Set CSP in main process
session.defaultSession.webRequest.onHeadersReceived((details, callback) => {
  callback({
    responseHeaders: {
      ...details.responseHeaders,
      'Content-Security-Policy': [
        "default-src 'self';",
        "script-src 'self';",
        "style-src 'self' 'unsafe-inline';",  // Only if needed
        "img-src 'self' data: https:;",
        "font-src 'self';",
        "connect-src 'self';",
        "media-src 'self';",
        "object-src 'none';",
        "base-uri 'self';",
        "form-action 'self';",
        "frame-ancestors 'none';",
        "upgrade-insecure-requests;",
      ].join(' '),
    },
  });
});
```

Or in HTML meta tag:
```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';">
```

## Input Validation

### File Path Validation

```javascript
const path = require('path');
const { app } = require('electron');

function validateFilePath(filePath) {
  // Check type
  if (typeof filePath !== 'string') {
    throw new Error('File path must be a string');
  }
  
  // Require absolute path (prevents path traversal)
  if (!path.isAbsolute(filePath)) {
    throw new Error('File path must be absolute');
  }
  
  // Normalize path (removes .., ., etc.)
  const normalizedPath = path.normalize(filePath);
  
  // Check if within allowed directory
  const allowedDir = app.getPath('documents');
  if (!normalizedPath.startsWith(allowedDir)) {
    throw new Error('Access denied: Path outside allowed directory');
  }
  
  // Prevent null byte injection
  if (filePath.includes('\0')) {
    throw new Error('Invalid file path: null byte detected');
  }
  
  return normalizedPath;
}

// Usage
ipcMain.handle('file:read', async (event, filePath) => {
  const safePath = validateFilePath(filePath);
  return await fs.readFile(safePath, 'utf-8');
});
```

### URL Validation

```javascript
function validateURL(urlString) {
  try {
    const url = new URL(urlString);
    
    // Whitelist protocols
    const allowedProtocols = ['https:', 'http:'];
    if (!allowedProtocols.includes(url.protocol)) {
      throw new Error('Protocol not allowed');
    }
    
    // Optionally whitelist domains
    const allowedDomains = ['example.com', 'api.example.com'];
    if (!allowedDomains.includes(url.hostname)) {
      throw new Error('Domain not allowed');
    }
    
    return url.href;
  } catch (error) {
    throw new Error('Invalid URL');
  }
}
```

### Command Injection Prevention

```javascript
// ❌ BAD: Direct shell execution with user input
const { exec } = require('child_process');
exec(`convert ${userInput}.jpg ${userInput}.png`);  // VULNERABLE!

// ✅ GOOD: Use array arguments, no shell
const { execFile } = require('child_process');
execFile('convert', [
  `${userInput}.jpg`,
  `${userInput}.png`
], { shell: false });

// ✅ BETTER: Validate and sanitize input first
function sanitizeFilename(filename) {
  // Remove or replace dangerous characters
  return filename.replace(/[^a-z0-9_-]/gi, '_');
}

const safeInput = sanitizeFilename(userInput);
execFile('convert', [`${safeInput}.jpg`, `${safeInput}.png`]);
```

## Navigation and Window Security

### Prevent Unwanted Navigation

```javascript
// Prevent all navigation
mainWindow.webContents.on('will-navigate', (event, url) => {
  event.preventDefault();
  console.log('Navigation blocked:', url);
});

// Allow only specific domains
mainWindow.webContents.on('will-navigate', (event, url) => {
  const allowedOrigins = ['https://example.com'];
  const { origin } = new URL(url);
  
  if (!allowedOrigins.includes(origin)) {
    event.preventDefault();
    console.log('Navigation blocked:', url);
  }
});
```

### Prevent New Window Creation

```javascript
// Block all new windows
mainWindow.webContents.setWindowOpenHandler(() => {
  return { action: 'deny' };
});

// Or open links in external browser
const { shell } = require('electron');

mainWindow.webContents.setWindowOpenHandler(({ url }) => {
  // Open external links in default browser
  if (url.startsWith('https://')) {
    shell.openExternal(url);
  }
  return { action: 'deny' };
});
```

## Remote Content

### Loading Remote Content Safely

If you must load remote content:

```javascript
// Create a separate, more restrictive window for remote content
const remoteWindow = new BrowserWindow({
  webPreferences: {
    contextIsolation: true,
    nodeIntegration: false,
    sandbox: true,              // ✅ Sandbox remote content
    webSecurity: true,
    allowRunningInsecureContent: false,
    enableRemoteModule: false,
    preload: path.join(__dirname, 'remote-preload.js'),
  },
});

// Only allow loading from specific origins
remoteWindow.webContents.session.webRequest.onBeforeRequest(
  { urls: ['*://*/*'] },
  (details, callback) => {
    const { url } = details;
    const allowedOrigins = ['https://trusted-domain.com'];
    
    try {
      const { origin } = new URL(url);
      if (allowedOrigins.includes(origin)) {
        callback({});  // Allow
      } else {
        callback({ cancel: true });  // Block
      }
    } catch {
      callback({ cancel: true });
    }
  }
);
```

### Never Load Untrusted Content in Privileged Windows

```javascript
// ❌ BAD: Loading user-provided URL in main window
mainWindow.loadURL(userProvidedURL);

// ✅ GOOD: Validate URL first
const safeURL = validateURL(userProvidedURL);
restrictedWindow.loadURL(safeURL);
```

## Secure Updates

### Code Signing

```javascript
// In electron-builder config (package.json)
{
  "build": {
    "mac": {
      "identity": "Developer ID Application: Your Name (TEAM_ID)"
    },
    "win": {
      "certificateFile": "path/to/cert.pfx",
      "certificatePassword": "password"  // Use env var in production!
    }
  }
}
```

### Update Verification

```javascript
const { autoUpdater } = require('electron-updater');

// Verify signature before installing updates
autoUpdater.on('update-downloaded', (info) => {
  // Signature is automatically verified by electron-updater
  // if code signing is properly configured
  
  dialog.showMessageBox({
    type: 'info',
    title: 'Update Ready',
    message: 'A new version has been downloaded. Restart to update?',
    buttons: ['Restart', 'Later'],
  }).then((result) => {
    if (result.response === 0) {
      autoUpdater.quitAndInstall();
    }
  });
});
```

## Dependency Security

### Audit Dependencies Regularly

```bash
# Check for known vulnerabilities
npm audit

# Fix automatically (if possible)
npm audit fix

# Use tools like Snyk
npm install -g snyk
snyk test
```

### Lock Dependencies

```json
// package.json
{
  "dependencies": {
    "electron": "28.0.0",  // ✅ Lock to specific version
    "some-package": "^2.0.0"  // ❌ Can auto-update (consider locking)
  }
}
```

## Encryption

### Storing Sensitive Data

```javascript
const keytar = require('keytar');

// Store credentials in system keychain
async function saveCredentials(service, account, password) {
  await keytar.setPassword(service, account, password);
}

async function getCredentials(service, account) {
  return await keytar.getPassword(service, account);
}

// ❌ BAD: Don't store secrets in localStorage or files
// localStorage.setItem('api-key', apiKey);

// ✅ GOOD: Use system keychain
await saveCredentials('MyApp', 'api-key', apiKey);
```

### Encrypting Data at Rest

```javascript
const crypto = require('crypto');

// Encrypt sensitive data before storing
function encrypt(text, password) {
  const algorithm = 'aes-256-gcm';
  const key = crypto.scryptSync(password, 'salt', 32);
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(algorithm, key, iv);
  
  const encrypted = Buffer.concat([
    cipher.update(text, 'utf8'),
    cipher.final(),
  ]);
  
  const authTag = cipher.getAuthTag();
  
  return Buffer.concat([iv, authTag, encrypted]).toString('hex');
}

function decrypt(encryptedHex, password) {
  const algorithm = 'aes-256-gcm';
  const key = crypto.scryptSync(password, 'salt', 32);
  const buffer = Buffer.from(encryptedHex, 'hex');
  
  const iv = buffer.slice(0, 16);
  const authTag = buffer.slice(16, 32);
  const encrypted = buffer.slice(32);
  
  const decipher = crypto.createDecipheriv(algorithm, key, iv);
  decipher.setAuthTag(authTag);
  
  return decipher.update(encrypted) + decipher.final('utf8');
}
```

## Logging and Monitoring

### Safe Logging

```javascript
// ❌ BAD: Logging sensitive data
console.log('User password:', password);
console.log('API token:', token);

// ✅ GOOD: Redact sensitive information
function sanitizeForLogging(obj) {
  const sensitiveKeys = ['password', 'token', 'apiKey', 'secret'];
  const sanitized = { ...obj };
  
  for (const key of sensitiveKeys) {
    if (key in sanitized) {
      sanitized[key] = '[REDACTED]';
    }
  }
  
  return sanitized;
}

console.log('User data:', sanitizeForLogging(userData));
```

## Production Checklist

Before releasing:

- [ ] Context isolation enabled
- [ ] Node integration disabled
- [ ] Sandbox enabled
- [ ] Preload script validates all IPC calls
- [ ] CSP configured
- [ ] All user inputs validated
- [ ] No sensitive data in logs
- [ ] Dependencies audited
- [ ] Code signed
- [ ] Auto-update configured with signature verification
- [ ] DevTools disabled in production
- [ ] Navigation restricted
- [ ] New window creation controlled
- [ ] HTTPS enforced for remote content
- [ ] Secrets stored in system keychain
- [ ] Error messages don't leak sensitive info

## Resources

- [Electron Security Checklist](https://www.electronjs.org/docs/tutorial/security)
- [OWASP Electron Security](https://github.com/doyensec/electronegativity)
- [Security Best Practices](https://www.electronjs.org/docs/tutorial/security)

## Common Vulnerabilities

### CVE Examples

1. **Remote Code Execution via XSS**
   - Cause: nodeIntegration enabled
   - Fix: Disable nodeIntegration

2. **Path Traversal**
   - Cause: Unsanitized file paths
   - Fix: Validate and normalize paths

3. **Command Injection**
   - Cause: Unsanitized input to shell commands
   - Fix: Use execFile with array args

4. **Unsafe Navigation**
   - Cause: No navigation restrictions
   - Fix: Implement will-navigate handler

Remember: **Security is not a feature, it's a requirement.**
