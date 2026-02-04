#!/usr/bin/env python3
"""
Project Structure Analyzer
Generates a comprehensive overview of a software project's architecture, entry points, and key files.
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple

class ProjectAnalyzer:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.ignore_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 
                           'dist', 'build', '.next', 'coverage', '.pytest_cache', 
                           'vendor', 'target', 'bin', 'obj'}
        self.config_files = {}
        self.entry_points = []
        self.file_stats = defaultdict(int)
        self.dependencies = {}
        
    def analyze(self) -> Dict:
        """Main analysis method"""
        self._scan_directory()
        self._identify_project_type()
        self._find_entry_points()
        self._analyze_config_files()
        self._analyze_dependencies()
        
        return {
            'project_type': self.project_type,
            'languages': dict(self.file_stats),
            'structure': self._get_tree_structure(),
            'entry_points': self.entry_points,
            'config_files': self.config_files,
            'dependencies': self.dependencies,
            'architecture_notes': self._generate_architecture_notes()
        }
    
    def _scan_directory(self, path: Path = None, depth: int = 0, max_depth: int = 5):
        """Recursively scan directory and collect file statistics"""
        if path is None:
            path = self.project_path
        
        if depth > max_depth:
            return
            
        try:
            for item in path.iterdir():
                if item.name.startswith('.') and item.name not in {'.env', '.env.example'}:
                    continue
                    
                if item.is_dir() and item.name not in self.ignore_dirs:
                    self._scan_directory(item, depth + 1, max_depth)
                elif item.is_file():
                    ext = item.suffix.lower()
                    self.file_stats[ext] += 1
        except PermissionError:
            pass
    
    def _identify_project_type(self):
        """Identify the type of project based on files and structure"""
        root_files = {f.name for f in self.project_path.iterdir() if f.is_file()}
        
        # Check for specific project types
        if 'package.json' in root_files:
            try:
                with open(self.project_path / 'package.json') as f:
                    pkg = json.load(f)
                    if 'dependencies' in pkg or 'devDependencies' in pkg:
                        deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                        if 'react' in deps or 'next' in deps:
                            self.project_type = 'React/Next.js Project'
                        elif 'vue' in deps:
                            self.project_type = 'Vue.js Project'
                        elif 'express' in deps:
                            self.project_type = 'Node.js/Express Project'
                        else:
                            self.project_type = 'Node.js Project'
            except:
                self.project_type = 'JavaScript Project'
        elif 'Cargo.toml' in root_files:
            self.project_type = 'Rust Project'
        elif 'go.mod' in root_files:
            self.project_type = 'Go Project'
        elif 'pom.xml' in root_files or 'build.gradle' in root_files:
            self.project_type = 'Java Project'
        elif 'requirements.txt' in root_files or 'pyproject.toml' in root_files or 'setup.py' in root_files:
            self.project_type = 'Python Project'
        elif 'Gemfile' in root_files:
            self.project_type = 'Ruby Project'
        elif '.csproj' in str(root_files):
            self.project_type = 'C# Project'
        else:
            # Fallback to most common file type
            if self.file_stats:
                most_common = max(self.file_stats.items(), key=lambda x: x[1])
                ext_map = {
                    '.py': 'Python Project',
                    '.js': 'JavaScript Project',
                    '.ts': 'TypeScript Project',
                    '.java': 'Java Project',
                    '.go': 'Go Project',
                    '.rs': 'Rust Project',
                    '.rb': 'Ruby Project',
                    '.php': 'PHP Project'
                }
                self.project_type = ext_map.get(most_common[0], 'Unknown Project Type')
            else:
                self.project_type = 'Unknown Project Type'
    
    def _find_entry_points(self):
        """Find likely entry points for the application"""
        entry_candidates = [
            'main.py', 'app.py', 'server.py', 'run.py', '__init__.py',
            'index.js', 'index.ts', 'server.js', 'app.js', 'main.js',
            'main.go', 'main.rs', 'Main.java', 'Program.cs',
            'index.html', 'index.php'
        ]
        
        for root, dirs, files in os.walk(self.project_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            for filename in files:
                if filename in entry_candidates:
                    rel_path = os.path.relpath(os.path.join(root, filename), self.project_path)
                    self.entry_points.append(rel_path)
    
    def _analyze_config_files(self):
        """Identify and categorize configuration files"""
        config_patterns = {
            'package.json': 'Node.js dependencies and scripts',
            'tsconfig.json': 'TypeScript configuration',
            'webpack.config.js': 'Webpack bundler configuration',
            'vite.config.js': 'Vite bundler configuration',
            'next.config.js': 'Next.js framework configuration',
            'requirements.txt': 'Python dependencies',
            'pyproject.toml': 'Python project metadata and dependencies',
            'setup.py': 'Python package setup',
            'Pipfile': 'Pipenv dependencies',
            'Cargo.toml': 'Rust dependencies and package info',
            'go.mod': 'Go module dependencies',
            'pom.xml': 'Maven dependencies',
            'build.gradle': 'Gradle build configuration',
            'Gemfile': 'Ruby dependencies',
            'composer.json': 'PHP dependencies',
            '.env': 'Environment variables',
            '.env.example': 'Example environment variables',
            'docker-compose.yml': 'Docker services configuration',
            'Dockerfile': 'Docker image definition',
            '.eslintrc': 'ESLint code quality rules',
            '.prettierrc': 'Prettier code formatting',
            'jest.config.js': 'Jest testing framework',
            'pytest.ini': 'Pytest configuration',
            'README.md': 'Project documentation'
        }
        
        for root, dirs, files in os.walk(self.project_path):
            # Only check root and first level
            if root != str(self.project_path) and os.path.dirname(root) != str(self.project_path):
                continue
            
            for filename in files:
                if filename in config_patterns:
                    rel_path = os.path.relpath(os.path.join(root, filename), self.project_path)
                    self.config_files[rel_path] = config_patterns[filename]
    
    def _analyze_dependencies(self):
        """Extract key dependencies from config files"""
        # Node.js
        pkg_json = self.project_path / 'package.json'
        if pkg_json.exists():
            try:
                with open(pkg_json) as f:
                    pkg = json.load(f)
                    deps = pkg.get('dependencies', {})
                    dev_deps = pkg.get('devDependencies', {})
                    self.dependencies['npm'] = {
                        'dependencies': list(deps.keys())[:10],  # Top 10
                        'devDependencies': list(dev_deps.keys())[:10]
                    }
            except:
                pass
        
        # Python
        req_txt = self.project_path / 'requirements.txt'
        if req_txt.exists():
            try:
                with open(req_txt) as f:
                    deps = [line.split('==')[0].split('>=')[0].strip() 
                           for line in f if line.strip() and not line.startswith('#')]
                    self.dependencies['pip'] = deps[:15]
            except:
                pass
    
    def _get_tree_structure(self, max_depth: int = 3) -> List[str]:
        """Generate a tree-like structure of the project"""
        tree = []
        
        def add_to_tree(path: Path, prefix: str = "", depth: int = 0):
            if depth >= max_depth:
                return
            
            try:
                items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
                items = [i for i in items if not i.name.startswith('.') and i.name not in self.ignore_dirs]
                
                for i, item in enumerate(items[:20]):  # Limit to 20 items per directory
                    is_last = i == len(items) - 1
                    current_prefix = "└── " if is_last else "├── "
                    tree.append(f"{prefix}{current_prefix}{item.name}{'/' if item.is_dir() else ''}")
                    
                    if item.is_dir():
                        extension_prefix = "    " if is_last else "│   "
                        add_to_tree(item, prefix + extension_prefix, depth + 1)
            except PermissionError:
                pass
        
        tree.append(f"{self.project_path.name}/")
        add_to_tree(self.project_path)
        return tree
    
    def _generate_architecture_notes(self) -> List[str]:
        """Generate architecture insights based on discovered patterns"""
        notes = []
        
        # Check for common architectural patterns
        src_exists = (self.project_path / 'src').exists()
        components_exists = (self.project_path / 'components').exists() or (self.project_path / 'src' / 'components').exists()
        
        if components_exists:
            notes.append("Frontend component-based architecture detected")
        
        if (self.project_path / 'api').exists() or (self.project_path / 'routes').exists():
            notes.append("API/routing layer present")
        
        if (self.project_path / 'models').exists() or (self.project_path / 'src' / 'models').exists():
            notes.append("Data models layer detected")
        
        if (self.project_path / 'tests').exists() or (self.project_path / 'test').exists():
            notes.append("Test suite present")
        
        if (self.project_path / 'docs').exists():
            notes.append("Documentation directory found")
        
        return notes

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python analyze_project.py <project_path>")
        sys.exit(1)
    
    project_path = sys.argv[1]
    analyzer = ProjectAnalyzer(project_path)
    results = analyzer.analyze()
    
    # Print formatted output
    print(f"\n{'='*60}")
    print(f"PROJECT ANALYSIS: {Path(project_path).name}")
    print(f"{'='*60}\n")
    
    print(f"Project Type: {results['project_type']}\n")
    
    print("File Distribution:")
    for ext, count in sorted(results['languages'].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {ext if ext else 'no extension'}: {count} files")
    
    print(f"\nEntry Points ({len(results['entry_points'])}):")
    for ep in results['entry_points'][:5]:
        print(f"  - {ep}")
    
    print(f"\nConfiguration Files ({len(results['config_files'])}):")
    for cf, desc in list(results['config_files'].items())[:10]:
        print(f"  - {cf}: {desc}")
    
    if results['dependencies']:
        print("\nKey Dependencies:")
        for pkg_mgr, deps in results['dependencies'].items():
            if isinstance(deps, dict):
                print(f"  {pkg_mgr} (production): {', '.join(deps.get('dependencies', [])[:5])}")
            else:
                print(f"  {pkg_mgr}: {', '.join(deps[:5])}")
    
    if results['architecture_notes']:
        print("\nArchitecture Notes:")
        for note in results['architecture_notes']:
            print(f"  - {note}")
    
    print("\nProject Structure:")
    for line in results['structure'][:30]:
        print(f"  {line}")

if __name__ == '__main__':
    main()
