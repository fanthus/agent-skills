#!/usr/bin/env python3
"""
Generate React Native component boilerplate
Usage: python generate_component.py ComponentName [--screen] [--typescript]
"""

import sys
import os
from pathlib import Path

def generate_component(name: str, is_screen: bool = False, use_typescript: bool = True):
    """Generate a React Native component with proper structure"""
    
    ext = 'tsx' if use_typescript else 'jsx'
    type_import = ': React.FC' if use_typescript else ''
    
    component_template = f'''import React from 'react';
import {{ View, Text, StyleSheet }} from 'react-native';

{"interface " + name + "Props {}" if use_typescript else ""}

export const {name}{type_import}{" = ({ }) => {" if use_typescript else " = () => {"}
  return (
    <View style={{styles.container}}>
      <Text style={{styles.text}}>{name}</Text>
    </View>
  );
{"}" if use_typescript else "};"}

const styles = StyleSheet.create({{
  container: {{
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  }},
  text: {{
    fontSize: 18,
    fontWeight: '600',
  }},
}});
'''

    screen_template = f'''import React from 'react';
import {{ View, Text, StyleSheet, SafeAreaView }} from 'react-native';
{"import type { NativeStackScreenProps } from '@react-navigation/native-stack';" if use_typescript else ""}

{"type Props = NativeStackScreenProps<RootStackParamList, '" + name + "'>;" if use_typescript else ""}

export const {name}Screen{type_import}{" = ({ navigation, route }: Props) => {" if use_typescript else " = ({ navigation, route }) => {"}
  return (
    <SafeAreaView style={{styles.container}}>
      <View style={{styles.content}}>
        <Text style={{styles.title}}>{name}</Text>
      </View>
    </SafeAreaView>
  );
{"}" if use_typescript else "};"}

const styles = StyleSheet.create({{
  container: {{
    flex: 1,
    backgroundColor: '#fff',
  }},
  content: {{
    flex: 1,
    padding: 16,
  }},
  title: {{
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 16,
  }},
}});
'''

    template = screen_template if is_screen else component_template
    filename = f"{name}{'Screen' if is_screen else ''}.{ext}"
    
    # Determine output directory
    output_dir = 'screens' if is_screen else 'components'
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    file_path = output_path / filename
    
    # Write file
    with open(file_path, 'w') as f:
        f.write(template)
    
    print(f"✅ Created {file_path}")
    
    # Create index file if it doesn't exist
    index_path = output_path / f'index.{ext[:-1]}'
    export_line = f"export {{ {name}{'Screen' if is_screen else ''} }} from './{name}{'Screen' if is_screen else ''}';\n"
    
    if index_path.exists():
        with open(index_path, 'a') as f:
            f.write(export_line)
        print(f"✅ Added export to {index_path}")
    else:
        with open(index_path, 'w') as f:
            f.write(export_line)
        print(f"✅ Created {index_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_component.py ComponentName [--screen] [--typescript]")
        sys.exit(1)
    
    name = sys.argv[1]
    is_screen = '--screen' in sys.argv
    use_typescript = '--typescript' in sys.argv or '--ts' in sys.argv or True  # Default to TS
    
    generate_component(name, is_screen, use_typescript)

if __name__ == '__main__':
    main()
