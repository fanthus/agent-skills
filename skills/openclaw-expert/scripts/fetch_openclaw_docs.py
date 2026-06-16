#!/usr/bin/env python3
"""
Fetch OpenClaw documentation and GitHub content for reference.
This script can be used to update the cached documentation periodically.
"""

import sys
import json
import requests
from pathlib import Path
from typing import Dict, List, Optional

def fetch_url(url: str) -> Optional[str]:
    """Fetch content from a URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

def fetch_github_readme(owner: str, repo: str) -> Optional[str]:
    """Fetch README from GitHub repository."""
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"
    content = fetch_url(url)
    if not content:
        # Try master branch if main doesn't exist
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md"
        content = fetch_url(url)
    return content

def save_content(content: str, filepath: Path) -> bool:
    """Save content to file."""
    try:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content, encoding='utf-8')
        return True
    except Exception as e:
        print(f"Error saving to {filepath}: {e}", file=sys.stderr)
        return False

def main():
    """Main function to fetch and save OpenClaw documentation."""
    script_dir = Path(__file__).parent
    refs_dir = script_dir.parent / "references"
    
    print("Fetching OpenClaw documentation...")
    
    # Fetch GitHub README
    readme = fetch_github_readme("openclaw", "openclaw")
    if readme:
        readme_path = refs_dir / "github_readme.md"
        if save_content(readme, readme_path):
            print(f"✅ Saved GitHub README to {readme_path}")
    
    print("\n📝 Note: For full documentation, users should visit:")
    print("   - https://docs.openclaw.ai/start/getting-started")
    print("   - https://github.com/openclaw/openclaw")
    print("\nThis script provides cached content for offline reference.")

if __name__ == "__main__":
    main()
