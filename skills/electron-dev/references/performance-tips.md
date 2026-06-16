# Electron Performance Optimization

Best practices for building fast, responsive Electron applications.

## Performance Principles

1. **Fast Startup**: Users expect apps to launch quickly
2. **Smooth UI**: 60fps for all interactions
3. **Low Memory**: Efficient memory usage prevents crashes
4. **Responsive**: Never block the main thread
5. **Battery Friendly**: Minimize CPU/GPU usage on laptops

## Startup Optimization

### Lazy Window Creation

```javascript
// ❌ BAD: Show window immediately (causes white flash)
const win = new BrowserWindow({ show: true });
win.loadURL('...');

// ✅ GOOD: Show when ready
const win = new BrowserWindow({ 
  show: false,
  backgroundColor: '#ffffff',  // Match your app's bg color
});

win.once('ready-to-show', () => {
  win.show();
});

win.loadURL('...');
```

### Defer Non-Critical Initialization

```javascript
app.whenReady().then(() => {
  // Critical: Create window immediately
  createMainWindow();
  
  // Non-critical: Defer to after window is shown
  setTimeout(() => {
    setupAutoUpdater();
    loadUserPreferences();
    startBackgroundSync();
  }, 1000);
});
```

### V8 Snapshots

```javascript
// In package.json
{
  "build": {
    "asar": true,  // Enable ASAR packaging for faster loading
  }
}
```

### Reduce Bundle Size

```bash
# Use production build
NODE_ENV=production npm run build

# Analyze bundle size
npm install --save-dev webpack-bundle-analyzer
```

## Main Process Performance

### Offload Heavy Work to Utilities

```javascript
const { utilityProcess } = require('electron');

// ❌ BAD: Heavy work in main process blocks UI
ipcMain.handle('process:data', async (event, data) => {
  const result = heavyProcessing(data);  // Blocks everything!
  return result;
});

// ✅ GOOD: Use utility process
ipcMain.handle('process:data', async (event, data) => {
  const child = utilityProcess.fork(
    path.join(__dirname, 'worker.js')
  );
  
  return new Promise((resolve) => {
    child.postMessage({ data });
    child.on('message', (result) => {
      resolve(result);
      child.kill();
    });
  });
});
```

Worker script (worker.js):
```javascript
process.parentPort.on('message', ({ data }) => {
  const result = heavyProcessing(data);
  process.parentPort.postMessage(result);
});
```

### Debounce Frequent Operations

```javascript
let debounceTimer;

ipcMain.handle('search', async (event, query) => {
  // ❌ BAD: Search on every keystroke
  // return await searchDatabase(query);
  
  // ✅ GOOD: Debounce search
  return new Promise((resolve) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(async () => {
      const results = await searchDatabase(query);
      resolve(results);
    }, 300);
  });
});
```

### Cache Expensive Operations

```javascript
const cache = new Map();

ipcMain.handle('get:config', async (event, key) => {
  // Check cache first
  if (cache.has(key)) {
    return cache.get(key);
  }
  
  // Load and cache
  const value = await loadConfigFromDisk(key);
  cache.set(key, value);
  
  return value;
});

// Clear cache when needed
ipcMain.on('config:updated', () => {
  cache.clear();
});
```

## Renderer Process Performance

### Virtualize Long Lists

```javascript
// ❌ BAD: Render 10,000 items
<ul>
  {items.map(item => (
    <li key={item.id}>{item.name}</li>
  ))}
</ul>

// ✅ GOOD: Use virtual scrolling (react-window, react-virtualized)
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={600}
  itemCount={items.length}
  itemSize={35}
  width="100%"
>
  {({ index, style }) => (
    <div style={style}>{items[index].name}</div>
  )}
</FixedSizeList>
```

### Throttle Scroll Events

```javascript
let ticking = false;

window.addEventListener('scroll', () => {
  if (!ticking) {
    window.requestAnimationFrame(() => {
      handleScroll();
      ticking = false;
    });
    ticking = true;
  }
});
```

### Use Web Workers for Heavy Computation

```javascript
// main thread
const worker = new Worker('worker.js');

worker.postMessage({ data: largeDataset });

worker.onmessage = (event) => {
  const result = event.data;
  updateUI(result);
};

// worker.js
self.onmessage = (event) => {
  const processed = heavyComputation(event.data);
  self.postMessage(processed);
};
```

### Minimize DOM Manipulation

```javascript
// ❌ BAD: Causes multiple reflows
for (let i = 0; i < items.length; i++) {
  const div = document.createElement('div');
  div.textContent = items[i];
  container.appendChild(div);  // Reflow on each append!
}

// ✅ GOOD: Batch DOM updates
const fragment = document.createDocumentFragment();
for (let i = 0; i < items.length; i++) {
  const div = document.createElement('div');
  div.textContent = items[i];
  fragment.appendChild(div);
}
container.appendChild(fragment);  // Single reflow

// ✅ BETTER: Use innerHTML (if safe from XSS)
container.innerHTML = items.map(item => 
  `<div>${escapeHtml(item)}</div>`
).join('');
```

## Memory Management

### Clean Up Event Listeners

```javascript
class Component {
  constructor() {
    this.handleResize = this.handleResize.bind(this);
  }
  
  mount() {
    window.addEventListener('resize', this.handleResize);
  }
  
  unmount() {
    // ✅ CRITICAL: Remove listener to prevent leaks
    window.removeEventListener('resize', this.handleResize);
  }
}
```

### Avoid Memory Leaks in IPC

```javascript
// ❌ BAD: Listener never cleaned up
window.electronAPI.on('data:update', (data) => {
  updateUI(data);
});

// ✅ GOOD: Store cleanup function
const cleanup = window.electronAPI.on('data:update', (data) => {
  updateUI(data);
});

// Call when component unmounts
window.addEventListener('beforeunload', cleanup);
```

### Limit Cache Size

```javascript
class LRUCache {
  constructor(maxSize = 100) {
    this.cache = new Map();
    this.maxSize = maxSize;
  }
  
  set(key, value) {
    // Remove oldest if at capacity
    if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    
    this.cache.set(key, value);
  }
  
  get(key) {
    if (!this.cache.has(key)) return null;
    
    // Move to end (most recently used)
    const value = this.cache.get(key);
    this.cache.delete(key);
    this.cache.set(key, value);
    
    return value;
  }
}
```

### Monitor Memory Usage

```javascript
// In renderer
console.log('Memory:', performance.memory);

// In main process
setInterval(() => {
  const usage = process.memoryUsage();
  console.log('Memory usage:', {
    rss: `${Math.round(usage.rss / 1024 / 1024)}MB`,
    heapUsed: `${Math.round(usage.heapUsed / 1024 / 1024)}MB`,
  });
}, 10000);
```

## IPC Performance

### Batch IPC Calls

```javascript
// ❌ BAD: Multiple IPC calls
for (const item of items) {
  await window.electronAPI.saveItem(item);
}

// ✅ GOOD: Single batched call
await window.electronAPI.saveItems(items);
```

### Avoid Large Data Transfers

```javascript
// ❌ BAD: Transfer large data through IPC
const imageData = canvas.toDataURL();  // Large base64 string
await window.electronAPI.saveImage(imageData);

// ✅ GOOD: Write to temp file, send path
const tempPath = await window.electronAPI.getTempPath('image.png');
// Write directly to file in renderer if possible
// Or send smaller chunks
await window.electronAPI.saveImagePath(tempPath);
```

### Use Streaming for Large Files

```javascript
// Instead of loading entire file into memory
ipcMain.handle('file:read', async (event, filePath) => {
  const stream = fs.createReadStream(filePath);
  
  stream.on('data', (chunk) => {
    event.sender.send('file:chunk', chunk.toString());
  });
  
  stream.on('end', () => {
    event.sender.send('file:complete');
  });
});
```

## GPU Acceleration

### Enable Hardware Acceleration

```javascript
// Default is enabled, but can be force-enabled
app.commandLine.appendSwitch('enable-gpu-rasterization');
app.commandLine.appendSwitch('enable-accelerated-2d-canvas');

// Disable if causing issues (rare)
// app.disableHardwareAcceleration();
```

### Optimize Animations

```css
/* Use transform and opacity for smooth animations */
.animated {
  /* ✅ GOOD: GPU-accelerated */
  transform: translateX(100px);
  opacity: 0.5;
  transition: transform 0.3s, opacity 0.3s;
  
  /* Force GPU layer */
  will-change: transform, opacity;
}

/* ❌ AVOID: Causes layout/paint */
.animated-bad {
  left: 100px;  /* Triggers layout */
  background: red;  /* Triggers paint */
}
```

### Reduce Repaints

```javascript
// ❌ BAD: Multiple style changes = multiple repaints
element.style.width = '100px';
element.style.height = '100px';
element.style.border = '1px solid black';

// ✅ GOOD: Batch with CSS class
element.className = 'resized';

// Or use cssText
element.style.cssText = 'width: 100px; height: 100px; border: 1px solid black;';
```

## Network Optimization

### Cache API Responses

```javascript
const responseCache = new Map();

async function fetchWithCache(url) {
  if (responseCache.has(url)) {
    return responseCache.get(url);
  }
  
  const response = await fetch(url);
  const data = await response.json();
  
  responseCache.set(url, data);
  
  // Auto-expire cache after 5 minutes
  setTimeout(() => responseCache.delete(url), 5 * 60 * 1000);
  
  return data;
}
```

### Prefetch Data

```javascript
// Prefetch likely needed data
window.addEventListener('mouseover', (e) => {
  if (e.target.dataset.prefetch) {
    fetchWithCache(e.target.dataset.prefetch);
  }
});
```

## Build Optimization

### Production Build Settings

```javascript
// electron-builder config
{
  "build": {
    "asar": true,
    "compression": "maximum",
    "removePackageScripts": true,
    "files": [
      "!node_modules/**/*",
      "node_modules/required-module/**/*"
    ]
  }
}
```

### Tree Shaking

```javascript
// ✅ Use ES6 imports for tree shaking
import { specificFunction } from 'library';

// ❌ Avoid CommonJS (includes entire module)
const library = require('library');
```

## Profiling

### Chrome DevTools

```javascript
// In renderer, open DevTools
// Performance tab → Record → Analyze

// Main process debugging
app.commandLine.appendSwitch('remote-debugging-port', '9222');
// Navigate to chrome://inspect in Chrome
```

### Custom Performance Marks

```javascript
performance.mark('start-render');

// ... rendering code ...

performance.mark('end-render');
performance.measure('render', 'start-render', 'end-render');

const measure = performance.getEntriesByName('render')[0];
console.log(`Render took ${measure.duration}ms`);
```

## Checklist

- [ ] Windows show only when ready-to-show
- [ ] Heavy work offloaded to utility processes
- [ ] Frequent operations debounced/throttled
- [ ] Long lists virtualized
- [ ] Event listeners cleaned up
- [ ] IPC calls batched
- [ ] Large data avoided in IPC
- [ ] Animations use transform/opacity
- [ ] API responses cached
- [ ] Production build optimized
- [ ] Memory usage monitored

## Tools

- **electron-devtools-installer**: React/Redux DevTools
- **electron-reload**: Auto-reload on changes
- **webpack-bundle-analyzer**: Analyze bundle size
- **Chrome DevTools**: Performance profiling

Remember: **Measure before optimizing. Profile to find bottlenecks.**
