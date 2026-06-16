# macOS SwiftUI Patterns Reference

## Navigation Patterns

### NavigationSplitView (Sidebar Navigation)
```swift
NavigationSplitView {
    List(selection: $selection) {
        NavigationLink("Item 1", value: 1)
        NavigationLink("Item 2", value: 2)
    }
} detail: {
    DetailView(item: selection)
}
.navigationSplitViewStyle(.balanced)
```

### Three-Column Navigation
```swift
NavigationSplitView {
    // Sidebar
    List { }
} content: {
    // Content list
    List { }
} detail: {
    // Detail view
    Text("Detail")
}
```

## Window Management

### Default Window Size
```swift
WindowGroup {
    ContentView()
}
.defaultSize(width: 800, height: 600)
```

### Window Position
```swift
WindowGroup {
    ContentView()
}
.defaultPosition(.center)
```

### Minimum Window Size
```swift
ContentView()
    .frame(minWidth: 600, minHeight: 400)
```

## Keyboard Shortcuts

### Command Menu
```swift
.commands {
    CommandMenu("Custom") {
        Button("Action") {
            performAction()
        }
        .keyboardShortcut("k", modifiers: [.command, .shift])
    }
}
```

### Common Shortcuts
```swift
.keyboardShortcut("n", modifiers: .command) // Cmd+N
.keyboardShortcut("w", modifiers: .command) // Cmd+W
.keyboardShortcut("s", modifiers: .command) // Cmd+S
.keyboardShortcut(.delete) // Delete key
.keyboardShortcut(.return) // Return key
```

### Replacing Default Commands
```swift
.commands {
    CommandGroup(replacing: .newItem) {
        Button("Custom New") { }
            .keyboardShortcut("n", modifiers: .command)
    }
}
```

## Toolbars

### Basic Toolbar
```swift
.toolbar {
    ToolbarItem(placement: .primaryAction) {
        Button(action: {}) {
            Label("Add", systemImage: "plus")
        }
    }
}
```

### Toolbar with Groups
```swift
.toolbar {
    ToolbarItemGroup {
        Button(action: {}) {
            Label("Bold", systemImage: "bold")
        }
        Button(action: {}) {
            Label("Italic", systemImage: "italic")
        }
    }
}
```

### Customizable Toolbar
```swift
.toolbar(id: "main") {
    ToolbarItem(id: "add", placement: .primaryAction) {
        Button("Add") { }
    }
    ToolbarItem(id: "remove", placement: .primaryAction) {
        Button("Remove") { }
    }
}
```

## Forms and Controls

### macOS Form Style
```swift
Form {
    Section("General") {
        TextField("Name:", text: $name)
        Toggle("Enabled", isOn: $enabled)
    }
}
.formStyle(.grouped)
```

### Picker Styles
```swift
Picker("Option", selection: $selection) {
    Text("One").tag(1)
    Text("Two").tag(2)
}
.pickerStyle(.menu) // Dropdown menu
.pickerStyle(.radioGroup) // Radio buttons
.pickerStyle(.segmented) // Segmented control
```

## Tables

### Basic Table
```swift
Table(items) {
    TableColumn("Name", value: \.name)
    TableColumn("Date", value: \.date)
}
```

### Table with Selection
```swift
Table(items, selection: $selection) {
    TableColumn("Name") { item in
        Text(item.name)
    }
}
```

## Menu Bar Integration

### Status Bar Item
```swift
class AppDelegate: NSObject, NSApplicationDelegate {
    var statusItem: NSStatusItem?
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        statusItem = NSStatusBar.system.statusItem(
            withLength: NSStatusItem.variableLength
        )
        
        if let button = statusItem?.button {
            button.image = NSImage(
                systemSymbolName: "star.fill",
                accessibilityDescription: "App"
            )
            button.action = #selector(statusItemClicked)
        }
    }
}
```

### Popover from Menu Bar
```swift
var popover = NSPopover()

func showPopover() {
    popover.contentViewController = NSHostingController(
        rootView: PopoverView()
    )
    popover.behavior = .transient
    
    if let button = statusItem?.button {
        popover.show(
            relativeTo: button.bounds,
            of: button,
            preferredEdge: .minY
        )
    }
}
```

## Settings Window

### Settings Scene
```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        
        Settings {
            SettingsView()
        }
    }
}
```

### Settings with Tabs
```swift
struct SettingsView: View {
    var body: some View {
        TabView {
            GeneralSettings()
                .tabItem {
                    Label("General", systemImage: "gearshape")
                }
            
            AdvancedSettings()
                .tabItem {
                    Label("Advanced", systemImage: "slider.horizontal.3")
                }
        }
        .frame(width: 450, height: 300)
    }
}
```

## macOS-Specific Modifiers

### Visual Effect Background
```swift
.background(.regularMaterial)
.background(.ultraThinMaterial)
.background(.thickMaterial)
```

### Focus Management
```swift
@FocusState private var focusedField: Field?

TextField("Name", text: $name)
    .focused($focusedField, equals: .name)
```

### Context Menu
```swift
.contextMenu {
    Button("Copy") { }
    Button("Paste") { }
    Divider()
    Button("Delete") { }
}
```

## File Operations

### File Import
```swift
.fileImporter(
    isPresented: $showFileImporter,
    allowedContentTypes: [.json, .text]
) { result in
    switch result {
    case .success(let url):
        // Handle file
    case .failure(let error):
        // Handle error
    }
}
```

### File Export
```swift
.fileExporter(
    isPresented: $showFileExporter,
    document: document,
    contentType: .json,
    defaultFilename: "export.json"
) { result in
    // Handle result
}
```

## App Lifecycle

### Launch at Login
```swift
import ServiceManagement

SMAppService.mainApp.register()
```

### Quit App
```swift
Button("Quit") {
    NSApplication.shared.terminate(nil)
}
```

## Color and Appearance

### System Colors
```swift
.foregroundColor(.primary)
.foregroundColor(.secondary)
.background(Color.accentColor)
```

### Accent Color
Set in Assets.xcassets or:
```swift
.tint(.blue)
```
