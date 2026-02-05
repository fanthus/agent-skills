/**
 * Electron Preload Script
 * 
 * SECURITY BEST PRACTICES:
 * 1. Use contextBridge to expose ONLY necessary APIs to renderer
 * 2. Never expose entire Node.js or Electron APIs
 * 3. Validate and sanitize all data passed between processes
 * 4. Use invoke/handle pattern for request-response communication
 * 5. Use send/on pattern for one-way or streaming communication
 * 
 * This script runs in an isolated context with access to both:
 * - Renderer process DOM APIs
 * - Limited Node.js/Electron APIs (specified in main process)
 */

const { contextBridge, ipcRenderer } = require('electron');

// ============================================================================
// EXPOSE SAFE APIs TO RENDERER
// ============================================================================

/**
 * BEST PRACTICE: Create a namespaced API object
 * This prevents pollution of the global window object
 */
contextBridge.exposeInMainWorld('electronAPI', {
  
  // ==========================================================================
  // FILE OPERATIONS
  // ==========================================================================
  
  /**
   * Open file dialog and select files
   * Returns: Promise<string[]> - Array of selected file paths
   */
  openFileDialog: () => ipcRenderer.invoke('dialog:openFile'),

  /**
   * Read file content
   * @param {string} filePath - Absolute path to file
   * Returns: Promise<{success: boolean, content?: string, error?: string}>
   */
  readFile: (filePath) => {
    // VALIDATION: Ensure filePath is a string
    if (typeof filePath !== 'string') {
      return Promise.reject(new Error('File path must be a string'));
    }
    return ipcRenderer.invoke('file:read', filePath);
  },

  /**
   * Write content to file
   * @param {string} filePath - Absolute path to file
   * @param {string} content - Content to write
   * Returns: Promise<{success: boolean, error?: string}>
   */
  writeFile: (filePath, content) => {
    // VALIDATION: Type checking
    if (typeof filePath !== 'string' || typeof content !== 'string') {
      return Promise.reject(new Error('Invalid arguments'));
    }
    return ipcRenderer.invoke('file:write', filePath, content);
  },

  /**
   * Watch file or directory for changes
   * @param {string} filePath - Path to watch
   * @param {Function} callback - Called when file changes
   * Returns: Promise<{success: boolean, watcherId?: number, error?: string}>
   */
  watchFile: async (filePath, callback) => {
    // VALIDATION
    if (typeof filePath !== 'string' || typeof callback !== 'function') {
      throw new Error('Invalid arguments');
    }

    // Set up listener for file change events
    const listener = (event, data) => {
      callback(data);
    };
    
    ipcRenderer.on('file:changed', listener);

    // Start watching
    const result = await ipcRenderer.invoke('file:watch', filePath);
    
    // Return cleanup function
    return {
      ...result,
      unwatch: () => {
        ipcRenderer.removeListener('file:changed', listener);
      },
    };
  },

  // ==========================================================================
  // WINDOW OPERATIONS
  // ==========================================================================

  /**
   * Window control methods
   */
  window: {
    minimize: () => ipcRenderer.invoke('window:minimize'),
    maximize: () => ipcRenderer.invoke('window:maximize'),
    close: () => ipcRenderer.invoke('window:close'),
  },

  // ==========================================================================
  // NOTIFICATIONS
  // ==========================================================================

  /**
   * Show native notification
   * @param {Object} options - Notification options
   * @param {string} options.title - Notification title
   * @param {string} options.body - Notification body
   * Returns: Promise<{success: boolean, error?: string}>
   */
  showNotification: (options) => {
    // VALIDATION: Ensure options is an object with required fields
    if (!options || typeof options !== 'object') {
      return Promise.reject(new Error('Options must be an object'));
    }
    if (!options.title || typeof options.title !== 'string') {
      return Promise.reject(new Error('Title is required'));
    }
    
    return ipcRenderer.invoke('notification:show', options);
  },

  // ==========================================================================
  // EVENT LISTENERS
  // ==========================================================================

  /**
   * Listen to events from main process
   * 
   * BEST PRACTICE: Provide cleanup function to prevent memory leaks
   */
  on: (channel, callback) => {
    // VALIDATION: Whitelist allowed channels
    const validChannels = ['file:changed', 'app:update'];
    
    if (!validChannels.includes(channel)) {
      throw new Error(`Invalid channel: ${channel}`);
    }
    
    if (typeof callback !== 'function') {
      throw new Error('Callback must be a function');
    }

    const listener = (event, ...args) => callback(...args);
    ipcRenderer.on(channel, listener);

    // Return cleanup function
    return () => {
      ipcRenderer.removeListener(channel, listener);
    };
  },

  /**
   * Remove event listener
   */
  off: (channel, callback) => {
    const validChannels = ['file:changed', 'app:update'];
    
    if (!validChannels.includes(channel)) {
      throw new Error(`Invalid channel: ${channel}`);
    }

    ipcRenderer.removeListener(channel, callback);
  },

  // ==========================================================================
  // UTILITY FUNCTIONS
  // ==========================================================================

  /**
   * Get app version and other metadata
   * Useful for "About" dialogs
   */
  getAppInfo: () => ipcRenderer.invoke('app:getInfo'),

  /**
   * Platform information
   * Returns: 'darwin' | 'win32' | 'linux'
   */
  platform: process.platform,

  /**
   * Check if running in development mode
   */
  isDev: process.env.NODE_ENV === 'development',
});

// ============================================================================
// SECURITY NOTES
// ============================================================================

/**
 * WHY THIS APPROACH IS SECURE:
 * 
 * 1. CONTEXTBRIDGE: Creates a secure bridge between isolated contexts
 *    - Renderer can't access Node.js/Electron directly
 *    - Only explicitly exposed APIs are available
 * 
 * 2. VALIDATION: All inputs are validated before passing to main process
 *    - Type checking prevents injection attacks
 *    - Whitelisting prevents unauthorized IPC calls
 * 
 * 3. NO DIRECT ACCESS: Renderer never gets direct access to:
 *    - File system (fs module)
 *    - Child processes
 *    - Native modules
 *    - Full Electron API
 * 
 * 4. PRINCIPLE OF LEAST PRIVILEGE:
 *    - Expose only what's needed
 *    - Each API has a specific, limited purpose
 *    - No generic "execute anything" APIs
 * 
 * ANTI-PATTERNS TO AVOID:
 * ❌ Don't: contextBridge.exposeInMainWorld('fs', require('fs'))
 * ❌ Don't: contextBridge.exposeInMainWorld('electron', require('electron'))
 * ❌ Don't: Enable nodeIntegration in webPreferences
 * ❌ Don't: Disable contextIsolation
 * ✅ Do: Expose specific, validated APIs like shown above
 */
