# Electron Application

A production-ready Electron application template with security best practices, modern architecture, and comprehensive features.

## Features

✅ **Security First**
- Context isolation enabled
- No nodeIntegration in renderer
- Secure IPC communication via contextBridge
- Content Security Policy configured

✅ **File Operations**
- Read/write files with proper validation
- File watching for real-time updates
- Drag & drop support

✅ **System Integration**
- System tray with context menu
- Global keyboard shortcuts
- Native notifications
- Window management

✅ **Developer Experience**
- Clean, modular code structure
- Comprehensive comments explaining best practices
- Development and production modes
- Cross-platform support (macOS, Windows, Linux)

## Quick Start

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

### Build

```bash
# Build for all platforms
npm run build

# Platform-specific builds
npm run build:mac
npm run build:win
npm run build:linux
```

## Project Structure

```
├── src/
│   ├── main/           # Main process
│   │   └── main.js     # Main process entry point
│   ├── preload/        # Preload scripts
│   │   └── preload.js  # Secure API bridge
│   └── renderer/       # Renderer process
│       ├── index.html  # Main window HTML
│       ├── styles.css  # Styles
│       └── renderer.js # Renderer logic
├── assets/             # App icons and resources
├── package.json
└── README.md
```

## Security Best Practices

This template implements Electron security best practices:

1. **Context Isolation**: Renderer and main processes are isolated
2. **No Node Integration**: Renderer doesn't have direct access to Node.js
3. **Secure IPC**: All communication goes through validated preload script
4. **CSP Headers**: Content Security Policy prevents XSS attacks
5. **Input Validation**: All user input is validated before processing

## Customization

### Adding New IPC Handlers

1. Add handler in `src/main/main.js`:
```javascript
ipcMain.handle('my:handler', async (event, arg) => {
  // Your logic here
  return result;
});
```

2. Expose in `src/preload/preload.js`:
```javascript
contextBridge.exposeInMainWorld('electronAPI', {
  myFunction: (arg) => ipcRenderer.invoke('my:handler', arg),
});
```

3. Use in renderer `src/renderer/renderer.js`:
```javascript
const result = await window.electronAPI.myFunction(arg);
```

### Changing App Icons

Place your icons in the `assets/` directory:
- macOS: `icon.icns`
- Windows: `icon.ico`
- Linux: `icon.png`

Update paths in `package.json` build configuration.

## Resources

- [Electron Documentation](https://www.electronjs.org/docs)
- [Electron Security Checklist](https://www.electronjs.org/docs/tutorial/security)
- [electron-builder Documentation](https://www.electron.build/)

## License

MIT
