---
name: macos-swiftui-dev
description: Create macOS applications using SwiftUI. Use when building macOS apps from scratch, including window-based apps, menu bar apps, apps with sidebar navigation, or when adding macOS-specific features like keyboard shortcuts, toolbars, and native UI components. Triggers on requests like "Build me a macOS app", "Create a SwiftUI app for Mac", "Make a menu bar app", or "Add keyboard shortcuts to my macOS app".
---

# macOS SwiftUI Development

## Overview

Create native macOS applications using SwiftUI with proper structure, navigation patterns, and macOS-specific UI components.

## Project Structure

Create files in the working directory with the following structure:

```
AppName/
├── AppName/
│   ├── AppNameApp.swift          # Main app entry point
│   ├── ContentView.swift         # Main content view
│   ├── Views/                    # Additional views
│   └── Models/                   # Data models
└── Info.plist                    # App configuration
```

## App Type Selection

Choose the appropriate template based on the user's request:

### Window-Based Apps
Use `assets/templates/BasicWindowApp.swift` when creating:
- Standard macOS applications with windows
- Apps with sidebar navigation
- Document-based applications
- Multi-window applications

### Menu Bar Apps
Use `assets/templates/MenuBarApp.swift` when creating:
- Apps that live in the menu bar
- Status bar utilities
- Background monitoring tools
- Quick-access tools

## Quick Start Workflows

### Creating a Basic Window App

1. Copy the BasicWindowApp.swift template from `assets/templates/`
2. Rename the struct and update app name references
3. Customize the ContentView with the desired layout
4. Add NavigationSplitView for sidebar navigation if needed
5. Include Info.plist from `assets/templates/Info.plist`

Example:
```swift
// Copy and modify BasicWindowApp.swift
@main
struct MyMacApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

### Creating a Menu Bar App

1. Copy the MenuBarApp.swift template from `assets/templates/`
2. Update the app name and status bar icon
3. Customize the PopoverContentView with desired UI
4. Modify SettingsView for app preferences
5. Use Info-MenuBar.plist (with LSUIElement set to true)

Key components:
- `@NSApplicationDelegateAdaptor` for AppDelegate
- NSStatusItem for menu bar presence
- NSPopover for displaying UI
- Settings scene for preferences window

### Adding Keyboard Shortcuts

Add to the App struct:
```swift
.commands {
    CommandMenu("Actions") {
        Button("New Item") {
            createNewItem()
        }
        .keyboardShortcut("n", modifiers: .command)
        
        Button("Delete") {
            deleteItem()
        }
        .keyboardShortcut(.delete)
    }
}
```

## Reference Documentation

Consult these references for detailed patterns and examples:

- **`references/swiftui-patterns.md`**: Comprehensive SwiftUI patterns for macOS including navigation, windows, forms, tables, toolbars, and more
- **`references/menubar-apps.md`**: Complete guide for menu bar app development including popovers, menus, icons, and launch at login

## Common Patterns

### Navigation with Sidebar
```swift
NavigationSplitView {
    List {
        NavigationLink("Section 1", destination: Section1View())
        NavigationLink("Section 2", destination: Section2View())
    }
} detail: {
    Text("Select an item")
}
```

### Toolbar
```swift
.toolbar {
    ToolbarItem(placement: .primaryAction) {
        Button("Add") {
            addItem()
        }
    }
}
```

### Settings Window
```swift
Settings {
    SettingsView()
}
```

### Forms
```swift
Form {
    Section("General") {
        TextField("Name:", text: $name)
        Toggle("Enabled", isOn: $enabled)
    }
}
.formStyle(.grouped)
```

## macOS-Specific Considerations

1. **Window Sizing**: Always set minimum window sizes with `.frame(minWidth:minHeight:)`
2. **Menu Bar**: Use template images for automatic dark mode support
3. **Keyboard Navigation**: Ensure all interactive elements support keyboard access
4. **Settings**: Provide a Settings scene for user preferences
5. **Info.plist**: Use `LSUIElement: true` for menu bar-only apps
6. **SF Symbols**: Use system symbols for consistent iconography

## Workflow

1. Determine app type (window-based or menu bar)
2. Copy appropriate template from `assets/templates/`
3. Customize app name and bundle identifier
4. Build out UI using SwiftUI components
5. Add keyboard shortcuts and menus as needed
6. Consult reference files for specific patterns
7. Include proper Info.plist configuration

## Resources

### assets/templates/
- `BasicWindowApp.swift` - Standard window-based app with sidebar navigation
- `MenuBarApp.swift` - Complete menu bar app with popover and settings
- `Info.plist` - Standard app configuration
- `Info-MenuBar.plist` - Menu bar app configuration (LSUIElement: true)

### references/
- `swiftui-patterns.md` - Comprehensive SwiftUI patterns for macOS
- `menubar-apps.md` - Menu bar app development guide
