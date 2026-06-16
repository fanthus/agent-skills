import SwiftUI

@main
struct AppNameApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .commands {
            CommandGroup(replacing: .newItem) {}
        }
    }
}

struct ContentView: View {
    var body: some View {
        NavigationSplitView {
            List {
                NavigationLink("Home", destination: HomeView())
                NavigationLink("Settings", destination: SettingsView())
            }
            .navigationTitle("Sidebar")
        } detail: {
            HomeView()
        }
        .frame(minWidth: 800, minHeight: 600)
    }
}

struct HomeView: View {
    var body: some View {
        VStack {
            Text("Welcome to Your macOS App")
                .font(.largeTitle)
            Text("Start building your app here")
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

struct SettingsView: View {
    var body: some View {
        Form {
            Section("General") {
                Toggle("Enable notifications", isOn: .constant(true))
            }
        }
        .formStyle(.grouped)
        .navigationTitle("Settings")
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}
