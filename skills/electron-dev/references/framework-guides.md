# Framework Integration Guide

Guide for integrating popular frontend frameworks with Electron.

## React Integration

### Setup

```bash
# Create React app
npx create-react-app my-electron-app
cd my-electron-app

# Install Electron
npm install --save-dev electron electron-builder concurrently wait-on
```

### Project Structure

```
my-electron-app/
├── public/
│   └── electron.js          # Main process
├── src/
│   ├── App.js              # React app
│   ├── preload.js          # Preload script
│   └── index.js
└── package.json
```

### Package.json Configuration

```json
{
  "name": "my-electron-app",
  "version": "1.0.0",
  "main": "public/electron.js",
  "homepage": "./",
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "electron:dev": "concurrently \"npm start\" \"wait-on http://localhost:3000 && electron .\"",
    "electron:build": "npm run build && electron-builder"
  },
  "build": {
    "appId": "com.example.app",
    "files": [
      "build/**/*",
      "node_modules/**/*",
      "public/electron.js",
      "src/preload.js"
    ],
    "directories": {
      "buildResources": "public"
    }
  }
}
```

### Main Process (public/electron.js)

```javascript
const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, '../src/preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  // Development: Load from dev server
  // Production: Load from build folder
  const isDev = !app.isPackaged;
  
  if (isDev) {
    win.loadURL('http://localhost:3000');
    win.webContents.openDevTools();
  } else {
    win.loadFile(path.join(__dirname, '../build/index.html'));
  }
}

app.whenReady().then(createWindow);
```

### Using Electron APIs in React

```javascript
// src/App.js
import React, { useState } from 'react';

function App() {
  const [filePath, setFilePath] = useState('');
  
  const handleOpenFile = async () => {
    const paths = await window.electronAPI.openFileDialog();
    if (paths.length > 0) {
      setFilePath(paths[0]);
    }
  };
  
  return (
    <div>
      <button onClick={handleOpenFile}>Open File</button>
      <p>Selected: {filePath}</p>
    </div>
  );
}

export default App;
```

## Vue Integration

### Setup

```bash
# Create Vue app
npm create vue@latest my-electron-app
cd my-electron-app
npm install

# Install Electron
npm install --save-dev electron electron-builder
```

### electron-builder.json

```json
{
  "appId": "com.example.app",
  "productName": "My Electron App",
  "directories": {
    "output": "dist_electron"
  },
  "files": [
    "dist/**/*",
    "electron/**/*"
  ],
  "mac": {
    "category": "public.app-category.utilities"
  }
}
```

### Main Process

```javascript
// electron/main.js
const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  if (process.env.VITE_DEV_SERVER_URL) {
    win.loadURL(process.env.VITE_DEV_SERVER_URL);
  } else {
    win.loadFile(path.join(__dirname, '../dist/index.html'));
  }
}

app.whenReady().then(createWindow);
```

### Using in Vue Components

```vue
<!-- src/components/FileOpener.vue -->
<template>
  <div>
    <button @click="openFile">Open File</button>
    <p v-if="filePath">Selected: {{ filePath }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const filePath = ref('');

const openFile = async () => {
  const paths = await window.electronAPI.openFileDialog();
  if (paths.length > 0) {
    filePath.value = paths[0];
  }
};
</script>
```

## TypeScript Support

### TypeScript Definitions

```typescript
// src/types/electron.d.ts
interface ElectronAPI {
  openFileDialog: () => Promise<string[]>;
  readFile: (path: string) => Promise<{
    success: boolean;
    content?: string;
    error?: string;
  }>;
  writeFile: (path: string, content: string) => Promise<{
    success: boolean;
    error?: string;
  }>;
}

declare global {
  interface Window {
    electronAPI: ElectronAPI;
  }
}

export {};
```

### Using in TypeScript

```typescript
// src/App.tsx
import React, { useState } from 'react';

const App: React.FC = () => {
  const [content, setContent] = useState<string>('');
  
  const handleOpen = async () => {
    const paths = await window.electronAPI.openFileDialog();
    if (paths.length > 0) {
      const result = await window.electronAPI.readFile(paths[0]);
      if (result.success && result.content) {
        setContent(result.content);
      }
    }
  };
  
  return (
    <div>
      <button onClick={handleOpen}>Open File</button>
      <pre>{content}</pre>
    </div>
  );
};

export default App;
```

## State Management

### React + Redux

```javascript
// src/store/electronSlice.js
import { createSlice } from '@reduxjs/toolkit';

const electronSlice = createSlice({
  name: 'electron',
  initialState: {
    currentFile: null,
    fileContent: '',
  },
  reducers: {
    setCurrentFile: (state, action) => {
      state.currentFile = action.payload;
    },
    setFileContent: (state, action) => {
      state.fileContent = action.payload;
    },
  },
});

export const { setCurrentFile, setFileContent } = electronSlice.actions;
export default electronSlice.reducer;

// Usage in component
import { useDispatch } from 'react-redux';
import { setCurrentFile, setFileContent } from './store/electronSlice';

const dispatch = useDispatch();

const handleOpen = async () => {
  const paths = await window.electronAPI.openFileDialog();
  if (paths.length > 0) {
    dispatch(setCurrentFile(paths[0]));
    const result = await window.electronAPI.readFile(paths[0]);
    if (result.success) {
      dispatch(setFileContent(result.content));
    }
  }
};
```

### Vue + Pinia

```javascript
// src/stores/electron.js
import { defineStore } from 'pinia';

export const useElectronStore = defineStore('electron', {
  state: () => ({
    currentFile: null,
    fileContent: '',
  }),
  actions: {
    async openFile() {
      const paths = await window.electronAPI.openFileDialog();
      if (paths.length > 0) {
        this.currentFile = paths[0];
        const result = await window.electronAPI.readFile(paths[0]);
        if (result.success) {
          this.fileContent = result.content;
        }
      }
    },
  },
});
```

## Build Process

### Development Workflow

```bash
# React
npm run electron:dev

# Vue with electron-builder
npm run dev & npx electron .
```

### Production Build

```bash
# React
npm run electron:build

# Vue
npm run build && electron-builder
```

## Hot Reload in Development

### React

```javascript
// public/electron.js
if (isDev) {
  require('electron-reload')(__dirname, {
    electron: path.join(__dirname, '../node_modules', '.bin', 'electron'),
  });
}
```

### Vue

Vite has built-in HMR, just need to restart Electron when main process changes:

```javascript
// electron/main.js
if (process.env.NODE_ENV === 'development') {
  require('electron-reloader')(module, {
    debug: true,
    watchRenderer: false,
  });
}
```

## Common Issues

### Issue: White screen in production

**Solution**: Set `homepage` in package.json

```json
{
  "homepage": "./"
}
```

### Issue: Module not found errors

**Solution**: Check file paths are correct for packaged app

```javascript
// ❌ BAD
const filePath = './config.json';

// ✅ GOOD
const filePath = path.join(__dirname, 'config.json');
```

### Issue: DevTools not working

**Solution**: Install devtools extensions

```javascript
const { default: installExtension, REACT_DEVELOPER_TOOLS } = 
  require('electron-devtools-installer');

app.whenReady().then(() => {
  installExtension(REACT_DEVELOPER_TOOLS)
    .then((name) => console.log(`Added Extension: ${name}`))
    .catch((err) => console.log('Error:', err));
});
```

## Best Practices

1. **Separate Concerns**: Keep Electron code separate from framework code
2. **Environment Detection**: Handle dev vs production differently
3. **Type Safety**: Use TypeScript for better DX
4. **State Management**: Use framework's state management for UI state
5. **Testing**: Test framework code separately from Electron integration

## Templates

Pre-configured templates available:
- **electron-react-boilerplate**: Full-featured React setup
- **electron-vue**: Official Vue integration
- **electron-vite**: Modern Vite-based setup

Choose based on your needs and framework preference.
