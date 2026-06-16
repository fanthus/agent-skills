/**
 * Renderer Process JavaScript
 * 
 * BEST PRACTICES:
 * - Use async/await for cleaner async code
 * - Proper error handling with try/catch
 * - User feedback for all operations
 * - Clean up event listeners to prevent memory leaks
 */

// ============================================================================
// GLOBAL STATE
// ============================================================================

let currentFilePath = null;
let fileWatcher = null;

// ============================================================================
// INITIALIZATION
// ============================================================================

/**
 * Initialize app when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
  initializeUI();
  setupEventListeners();
  loadSystemInfo();
});

/**
 * Initialize UI elements
 */
function initializeUI() {
  // Display platform info
  document.getElementById('platform-info').textContent = window.electronAPI.platform;
  document.getElementById('env-info').textContent = window.electronAPI.isDev ? 'Development' : 'Production';
}

// ============================================================================
// EVENT LISTENERS
// ============================================================================

/**
 * Set up all event listeners
 * 
 * BEST PRACTICE: Centralize event listener setup for easier management
 */
function setupEventListeners() {
  // Custom title bar controls
  document.getElementById('minimize-btn')?.addEventListener('click', minimizeWindow);
  document.getElementById('maximize-btn')?.addEventListener('click', maximizeWindow);
  document.getElementById('close-btn')?.addEventListener('click', closeWindow);

  // File operations
  document.getElementById('open-file-btn').addEventListener('click', openFile);
  document.getElementById('save-file-btn').addEventListener('click', saveFile);

  // Window controls
  document.getElementById('window-minimize').addEventListener('click', minimizeWindow);
  document.getElementById('window-maximize').addEventListener('click', maximizeWindow);

  // Notifications
  document.getElementById('show-notification-btn').addEventListener('click', showNotification);

  // Drag and drop
  setupDragAndDrop();
}

// ============================================================================
// WINDOW CONTROLS
// ============================================================================

async function minimizeWindow() {
  try {
    await window.electronAPI.window.minimize();
  } catch (error) {
    console.error('Error minimizing window:', error);
  }
}

async function maximizeWindow() {
  try {
    await window.electronAPI.window.maximize();
  } catch (error) {
    console.error('Error maximizing window:', error);
  }
}

async function closeWindow() {
  try {
    await window.electronAPI.window.close();
  } catch (error) {
    console.error('Error closing window:', error);
  }
}

// ============================================================================
// FILE OPERATIONS
// ============================================================================

/**
 * Open file dialog and read selected file
 * 
 * UX: Provide feedback during async operations
 */
async function openFile() {
  const button = document.getElementById('open-file-btn');
  const fileInfo = document.getElementById('file-info');
  const fileContent = document.getElementById('file-content');

  try {
    // UX: Disable button during operation
    button.disabled = true;
    button.textContent = 'Opening...';

    // Open file dialog
    const filePaths = await window.electronAPI.openFileDialog();

    if (filePaths.length === 0) {
      fileInfo.textContent = 'No file selected';
      return;
    }

    // Read first selected file
    currentFilePath = filePaths[0];
    const result = await window.electronAPI.readFile(currentFilePath);

    if (result.success) {
      fileContent.value = result.content;
      fileInfo.innerHTML = `
        <strong>File:</strong> ${currentFilePath}<br>
        <strong>Size:</strong> ${result.content.length} characters
      `;
      
      // UX: Success feedback
      fileInfo.classList.add('success');
      setTimeout(() => fileInfo.classList.remove('success'), 2000);

      // Start watching file for changes
      watchFile(currentFilePath);
    } else {
      throw new Error(result.error);
    }
  } catch (error) {
    // ERROR HANDLING: Show user-friendly error message
    fileInfo.textContent = `Error: ${error.message}`;
    fileInfo.classList.add('error');
    console.error('Error opening file:', error);
  } finally {
    // UX: Re-enable button
    button.disabled = false;
    button.textContent = 'Open File';
  }
}

/**
 * Save file content
 * 
 * UX: Confirm before overwriting, provide feedback
 */
async function saveFile() {
  const button = document.getElementById('save-file-btn');
  const fileContent = document.getElementById('file-content');
  const fileInfo = document.getElementById('file-info');

  if (!currentFilePath) {
    fileInfo.textContent = 'No file opened. Open a file first.';
    fileInfo.classList.add('error');
    return;
  }

  try {
    button.disabled = true;
    button.textContent = 'Saving...';

    const result = await window.electronAPI.writeFile(
      currentFilePath,
      fileContent.value
    );

    if (result.success) {
      fileInfo.textContent = 'File saved successfully!';
      fileInfo.classList.add('success');
      setTimeout(() => fileInfo.classList.remove('success'), 2000);
    } else {
      throw new Error(result.error);
    }
  } catch (error) {
    fileInfo.textContent = `Error saving: ${error.message}`;
    fileInfo.classList.add('error');
    console.error('Error saving file:', error);
  } finally {
    button.disabled = false;
    button.textContent = 'Save File';
  }
}

/**
 * Watch file for external changes
 * 
 * UX: Notify user when file changes externally
 */
async function watchFile(filePath) {
  try {
    // Clean up previous watcher
    if (fileWatcher?.unwatch) {
      fileWatcher.unwatch();
    }

    // Start watching
    fileWatcher = await window.electronAPI.watchFile(filePath, (data) => {
      const fileInfo = document.getElementById('file-info');
      fileInfo.innerHTML = `
        <strong class="error">⚠️ File modified externally!</strong><br>
        Event: ${data.eventType}<br>
        Click "Open File" to reload.
      `;
    });
  } catch (error) {
    console.error('Error watching file:', error);
  }
}

// ============================================================================
// DRAG AND DROP
// ============================================================================

/**
 * Set up drag and drop functionality
 * 
 * UX: Visual feedback during drag operations
 */
function setupDragAndDrop() {
  const dropZone = document.getElementById('drop-zone');
  const dropResult = document.getElementById('drop-result');

  // Prevent default drag behaviors on the whole document
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    document.body.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  // Highlight drop zone when dragging over
  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
      dropZone.classList.add('drag-over');
    }, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
      dropZone.classList.remove('drag-over');
    }, false);
  });

  // Handle dropped files
  dropZone.addEventListener('drop', async (e) => {
    const files = e.dataTransfer.files;

    if (files.length === 0) return;

    // Display dropped file info
    const fileList = Array.from(files).map(file => 
      `<div>📄 ${file.name} (${formatFileSize(file.size)})</div>`
    ).join('');

    dropResult.innerHTML = `<strong>Dropped files:</strong><br>${fileList}`;

    // Read first file if it's a text file
    const firstFile = files[0];
    if (isTextFile(firstFile)) {
      try {
        // NOTE: In Electron, e.dataTransfer.files returns File objects with path property
        const filePath = firstFile.path;
        const result = await window.electronAPI.readFile(filePath);

        if (result.success) {
          currentFilePath = filePath;
          document.getElementById('file-content').value = result.content;
          document.getElementById('file-info').innerHTML = `
            <strong>Loaded from drag & drop:</strong> ${filePath}
          `;
        }
      } catch (error) {
        dropResult.innerHTML += `<br><span class="error">Error reading file: ${error.message}</span>`;
      }
    }
  }, false);
}

// ============================================================================
// NOTIFICATIONS
// ============================================================================

/**
 * Show native notification
 */
async function showNotification() {
  const title = document.getElementById('notification-title').value;
  const body = document.getElementById('notification-body').value;

  if (!title) {
    alert('Please enter a notification title');
    return;
  }

  try {
    const result = await window.electronAPI.showNotification({ title, body });

    if (result.success) {
      // Clear inputs on success
      document.getElementById('notification-title').value = '';
      document.getElementById('notification-body').value = '';
    } else {
      throw new Error(result.error);
    }
  } catch (error) {
    alert(`Error showing notification: ${error.message}`);
  }
}

// ============================================================================
// SYSTEM INFO
// ============================================================================

/**
 * Load system information
 */
async function loadSystemInfo() {
  // Platform info is already loaded in initializeUI
  // Add more system info as needed
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Check if file is likely a text file based on extension
 */
function isTextFile(file) {
  const textExtensions = [
    'txt', 'md', 'js', 'json', 'html', 'css', 'xml', 'csv',
    'log', 'yml', 'yaml', 'toml', 'ini', 'conf', 'sh', 'py',
  ];
  
  const extension = file.name.split('.').pop().toLowerCase();
  return textExtensions.includes(extension);
}

// ============================================================================
// CLEANUP
// ============================================================================

/**
 * Clean up when page unloads
 * 
 * BEST PRACTICE: Prevent memory leaks by cleaning up event listeners
 */
window.addEventListener('beforeunload', () => {
  if (fileWatcher?.unwatch) {
    fileWatcher.unwatch();
  }
});

// ============================================================================
// ERROR HANDLING
// ============================================================================

/**
 * Global error handler
 * 
 * ERROR HANDLING: Catch and log any unhandled errors
 */
window.addEventListener('error', (event) => {
  console.error('Unhandled error:', event.error);
  // In production, you might want to send this to an error tracking service
});

window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason);
});
