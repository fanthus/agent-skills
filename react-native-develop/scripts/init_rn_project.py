#!/usr/bin/env python3
"""
Initialize a React Native project with best practices structure
Usage: python init_rn_project.py <project-name>
"""

import sys
import os
from pathlib import Path

def create_directory_structure(base_path: Path):
    """Create the recommended directory structure"""
    directories = [
        'src',
        'src/components',
        'src/screens',
        'src/navigation',
        'src/services',
        'src/hooks',
        'src/utils',
        'src/constants',
        'src/types',
        'assets',
        'assets/images',
        'assets/fonts',
    ]
    
    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created {directory}/")

def create_theme_file(base_path: Path):
    """Create theme constants file"""
    theme_content = '''export const colors = {
  primary: '#007AFF',
  secondary: '#5856D6',
  success: '#34C759',
  danger: '#FF3B30',
  warning: '#FF9500',
  background: '#FFFFFF',
  backgroundSecondary: '#F2F2F7',
  text: '#000000',
  textSecondary: '#8E8E93',
  border: '#C6C6C8',
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

export const typography = {
  h1: { fontSize: 32, fontWeight: 'bold' as const },
  h2: { fontSize: 24, fontWeight: 'bold' as const },
  h3: { fontSize: 20, fontWeight: '600' as const },
  body: { fontSize: 16, fontWeight: 'normal' as const },
  caption: { fontSize: 12, fontWeight: 'normal' as const },
};

export const borderRadius = {
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  full: 9999,
};

export const shadows = {
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.18,
    shadowRadius: 1.0,
    elevation: 1,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.23,
    shadowRadius: 2.62,
    elevation: 4,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.30,
    shadowRadius: 4.65,
    elevation: 8,
  },
};
'''
    
    file_path = base_path / 'src/constants/theme.ts'
    with open(file_path, 'w') as f:
        f.write(theme_content)
    print(f"✅ Created src/constants/theme.ts")

def create_navigation_file(base_path: Path):
    """Create basic navigation setup"""
    nav_content = '''import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

export const AppNavigator = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        {/* Add your screens here */}
      </Stack.Navigator>
    </NavigationContainer>
  );
};
'''
    
    file_path = base_path / 'src/navigation/AppNavigator.tsx'
    with open(file_path, 'w') as f:
        f.write(nav_content)
    print(f"✅ Created src/navigation/AppNavigator.tsx")

def create_api_service(base_path: Path):
    """Create API service template"""
    api_content = '''const API_BASE = process.env.API_BASE_URL || 'https://api.example.com';

interface RequestConfig {
  headers?: Record<string, string>;
  params?: Record<string, any>;
}

export const api = {
  get: async <T>(endpoint: string, config?: RequestConfig): Promise<T> => {
    const url = new URL(`${API_BASE}${endpoint}`);
    if (config?.params) {
      Object.entries(config.params).forEach(([key, value]) => {
        url.searchParams.append(key, String(value));
      });
    }

    const response = await fetch(url.toString(), {
      headers: config?.headers,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    return response.json();
  },

  post: async <T>(endpoint: string, data: any, config?: RequestConfig): Promise<T> => {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...config?.headers,
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    return response.json();
  },

  put: async <T>(endpoint: string, data: any, config?: RequestConfig): Promise<T> => {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...config?.headers,
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    return response.json();
  },

  delete: async <T>(endpoint: string, config?: RequestConfig): Promise<T> => {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'DELETE',
      headers: config?.headers,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    return response.json();
  },
};
'''
    
    file_path = base_path / 'src/services/api.ts'
    with open(file_path, 'w') as f:
        f.write(api_content)
    print(f"✅ Created src/services/api.ts")

def create_storage_service(base_path: Path):
    """Create storage service template"""
    storage_content = '''import AsyncStorage from '@react-native-async-storage/async-storage';

export const storage = {
  get: async <T>(key: string): Promise<T | null> => {
    try {
      const value = await AsyncStorage.getItem(key);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      console.error('Storage get error:', error);
      return null;
    }
  },

  set: async <T>(key: string, value: T): Promise<void> => {
    try {
      await AsyncStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error('Storage set error:', error);
    }
  },

  remove: async (key: string): Promise<void> => {
    try {
      await AsyncStorage.removeItem(key);
    } catch (error) {
      console.error('Storage remove error:', error);
    }
  },

  clear: async (): Promise<void> => {
    try {
      await AsyncStorage.clear();
    } catch (error) {
      console.error('Storage clear error:', error);
    }
  },
};
'''
    
    file_path = base_path / 'src/services/storage.ts'
    with open(file_path, 'w') as f:
        f.write(storage_content)
    print(f"✅ Created src/services/storage.ts")

def create_custom_hooks(base_path: Path):
    """Create useful custom hooks"""
    hooks_content = '''import { useState, useEffect } from 'react';

export const useAsync = <T,>(asyncFn: () => Promise<T>, immediate = true) => {
  const [state, setState] = useState<{
    loading: boolean;
    data: T | null;
    error: Error | null;
  }>({
    loading: immediate,
    data: null,
    error: null,
  });

  const execute = async () => {
    setState({ loading: true, data: null, error: null });
    try {
      const data = await asyncFn();
      setState({ loading: false, data, error: null });
      return data;
    } catch (error) {
      setState({ loading: false, data: null, error: error as Error });
      throw error;
    }
  };

  useEffect(() => {
    if (immediate) {
      execute();
    }
  }, []);

  return { ...state, execute };
};
'''
    
    file_path = base_path / 'src/hooks/useAsync.ts'
    with open(file_path, 'w') as f:
        f.write(hooks_content)
    print(f"✅ Created src/hooks/useAsync.ts")

def create_readme(base_path: Path, project_name: str):
    """Create project README"""
    readme_content = f'''# {project_name}

A React Native application built with best practices.

## Project Structure

```
{project_name}/
├── src/
│   ├── components/       # Reusable UI components
│   ├── screens/          # Screen-level components
│   ├── navigation/       # Navigation setup
│   ├── services/         # API calls, storage, etc.
│   ├── hooks/            # Custom React hooks
│   ├── utils/            # Helper functions
│   ├── constants/        # Colors, sizes, config
│   └── types/            # TypeScript types
├── assets/               # Images, fonts, etc.
├── android/              # Native Android code
├── ios/                  # Native iOS code
└── package.json
```

## Getting Started

### Prerequisites

- Node.js >= 14
- React Native CLI
- Xcode (for iOS)
- Android Studio (for Android)

### Installation

```bash
npm install
# or
yarn install
```

### Running

```bash
# iOS
npm run ios

# Android
npm run android
```

## Development

### Creating Components

Use the component generator script:

```bash
python scripts/generate_component.py ComponentName
python scripts/generate_component.py ScreenName --screen
```

### Theme Configuration

Edit `src/constants/theme.ts` to customize:
- Colors
- Spacing
- Typography
- Border radius
- Shadows

## Built With

- React Native
- TypeScript
- React Navigation
- AsyncStorage
'''
    
    file_path = base_path / 'README.md'
    with open(file_path, 'w') as f:
        f.write(readme_content)
    print(f"✅ Created README.md")

def main():
    if len(sys.argv) < 2:
        print("Usage: python init_rn_project.py <project-name>")
        sys.exit(1)
    
    project_name = sys.argv[1]
    base_path = Path(project_name)
    
    if base_path.exists():
        print(f"❌ Directory {project_name} already exists")
        sys.exit(1)
    
    print(f"🚀 Initializing React Native project: {project_name}")
    
    # Create base directory
    base_path.mkdir()
    
    # Create directory structure
    create_directory_structure(base_path)
    
    # Create configuration files
    create_theme_file(base_path)
    create_navigation_file(base_path)
    create_api_service(base_path)
    create_storage_service(base_path)
    create_custom_hooks(base_path)
    create_readme(base_path, project_name)
    
    print(f"\n✅ Project {project_name} initialized successfully!")
    print(f"\nNext steps:")
    print(f"1. cd {project_name}")
    print(f"2. Initialize React Native: npx react-native init {project_name}")
    print(f"3. Move the src/ folder into the React Native project")
    print(f"4. Install dependencies: npm install @react-navigation/native @react-navigation/native-stack")

if __name__ == '__main__':
    main()
