# Menu Bar Apps Reference

## Menu Bar App Architecture

Menu bar apps (status bar apps) are macOS applications that appear in the system menu bar at the top of the screen. They typically don't have a dock icon and run in the background.

## Essential Components

### 1. App Delegate Setup

```swift
import SwiftUI

@main
struct MenuBarApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        Settings {
            SettingsView()
        }
    }
}
```

### 2. Status Item Creation

```swift
class AppDelegate: NSObject, NSApplicationDelegate {
    var statusItem: NSStatusItem?
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        statusItem = NSStatusBar.system.statusItem(
            withLength: NSStatusItem.variableLength
        )
        
        if let button = statusItem?.button {
            // Set icon
            button.image = NSImage(
                systemSymbolName: "star.fill",
                accessibilityDescription: "Menu Bar App"
            )
            button.action = #selector(handleClick)
            button.target = self
        }
    }
}
```

## Display Options

### Option 1: Popover

Best for: Interactive content, forms, mini-interfaces

```swift
var popover = NSPopover()

func showPopover() {
    popover.contentSize = NSSize(width: 300, height: 400)
    popover.behavior = .transient // Closes when clicking outside
    popover.contentViewController = NSHostingController(
        rootView: PopoverContentView()
    )
    
    if let button = statusItem?.button {
        popover.show(
            relativeTo: button.bounds,
            of: button,
            preferredEdge: .minY
        )
    }
}

@objc func handleClick() {
    if popover.isShown {
        popover.performClose(nil)
    } else {
        showPopover()
    }
}
```

### Option 2: Menu

Best for: Simple lists, actions, traditional menu structure

```swift
func setupMenu() {
    let menu = NSMenu()
    
    menu.addItem(NSMenuItem(
        title: "Action 1",
        action: #selector(action1),
        keyEquivalent: "1"
    ))
    menu.addItem(NSMenuItem.separator())
    menu.addItem(NSMenuItem(
        title: "Quit",
        action: #selector(quit),
        keyEquivalent: "q"
    ))
    
    statusItem?.menu = menu
}
```

### Option 3: Window

Best for: Full-featured interfaces that need more space

```swift
var window: NSWindow?

func showWindow() {
    let contentView = NSHostingController(rootView: MainView())
    
    window = NSWindow(
        contentRect: NSRect(x: 0, y: 0, width: 400, height: 500),
        styleMask: [.titled, .closable, .miniaturizable, .resizable],
        backing: .buffered,
        defer: false
    )
    window?.contentViewController = contentView
    window?.title = "Menu Bar App"
    window?.makeKeyAndOrderFront(nil)
}
```

## Info.plist Configuration

For menu bar apps without a dock icon, set `LSUIElement` to `true`:

```xml
<key>LSUIElement</key>
<true/>
```

For apps that should appear in the dock as well, set to `false` or omit.

## Icon Guidelines

### SF Symbols
```swift
button.image = NSImage(
    systemSymbolName: "clock.fill",
    accessibilityDescription: "Time Tracker"
)
```

### Custom Icons
- Template images (black/transparent) work best
- Recommended size: 22x22 pixels for @1x
- Use PDF or PNG assets with @2x and @3x variants

```swift
if let image = NSImage(named: "MenuBarIcon") {
    image.isTemplate = true // Adapts to light/dark mode
    button.image = image
}
```

## Popover Behaviors

```swift
popover.behavior = .transient       // Closes on outside click (default)
popover.behavior = .semitransient   // Closes on app deactivation
popover.behavior = .applicationDefined // Manual control
```

## Common Patterns

### Timer-based Updates

```swift
struct PopoverView: View {
    @State private var currentTime = Date()
    let timer = Timer.publish(every: 1, on: .main, in: .common).autoconnect()
    
    var body: some View {
        VStack {
            Text(currentTime, style: .time)
        }
        .onReceive(timer) { input in
            currentTime = input
        }
    }
}
```

### Status Item with Text

```swift
if let button = statusItem?.button {
    button.title = "Active"
}
```

### Dynamic Icon Updates

```swift
func updateIcon(active: Bool) {
    let iconName = active ? "checkmark.circle.fill" : "circle"
    statusItem?.button?.image = NSImage(
        systemSymbolName: iconName,
        accessibilityDescription: nil
    )
}
```

## Best Practices

1. **Keep popovers small**: 300-400px width is typical
2. **Use transient behavior**: Let users dismiss easily
3. **Provide quit option**: Always include a way to quit
4. **Use template images**: For automatic dark mode support
5. **Consider system settings**: Some users hide menu bar items
6. **Test on notch**: Ensure icon placement works on notched displays
7. **Keyboard accessibility**: Support keyboard navigation in popovers

## Launch at Login

```swift
import ServiceManagement

// Check if enabled
let isEnabled = SMAppService.mainApp.status == .enabled

// Enable
try? SMAppService.mainApp.register()

// Disable
try? SMAppService.mainApp.unregister()
```

Add to Settings view:
```swift
Toggle("Launch at login", isOn: $launchAtLogin)
    .onChange(of: launchAtLogin) { newValue in
        if newValue {
            try? SMAppService.mainApp.register()
        } else {
            try? SMAppService.mainApp.unregister()
        }
    }
```

## Troubleshooting

**Popover doesn't close on outside click**: Ensure `behavior` is `.transient`

**Icon too large/small**: Use 22x22pt base size for menu bar icons

**App shows in dock**: Check `LSUIElement` is set to `true` in Info.plist

**Popover appears in wrong position**: Use `.minY` for preferred edge to appear below menu bar
