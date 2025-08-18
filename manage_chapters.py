#!/usr/bin/env python3
"""
Chapter Management Utility
Helps organize, view, and manage generated chapter files.
"""

import os
import sys
from pathlib import Path
import argparse
from datetime import datetime

def list_chapters(category=None):
    """List all chapter files, optionally filtered by category."""
    chapters_dir = Path("chapters")
    
    if not chapters_dir.exists():
        print("No chapters directory found.")
        return
    
    if category:
        category_dir = chapters_dir / category
        if not category_dir.exists():
            print(f"Category '{category}' not found.")
            print(f"Available categories: {', '.join([d.name for d in chapters_dir.iterdir() if d.is_dir()])}")
            return
        dirs_to_check = [category_dir]
    else:
        dirs_to_check = [d for d in chapters_dir.iterdir() if d.is_dir()]
    
    total_files = 0
    for category_dir in dirs_to_check:
        files = list(category_dir.glob("*.txt"))
        if files:
            print(f"\n📁 {category_dir.name.upper()} ({len(files)} files)")
            print("=" * 50)
            for file in sorted(files):
                # Get file info
                stat = file.stat()
                size = stat.st_size
                modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                
                print(f"  📄 {file.name}")
                print(f"     Size: {size:,} bytes | Modified: {modified}")
                
                # Show first few lines as preview
                try:
                    with open(file, 'r') as f:
                        lines = f.readlines()[:3]
                        for line in lines:
                            print(f"     > {line.strip()}")
                except:
                    print("     > (Unable to preview)")
                print()
            total_files += len(files)
    
    if total_files == 0:
        print("No chapter files found.")
    else:
        print(f"\nTotal: {total_files} chapter files")

def view_chapter(filename):
    """View contents of a specific chapter file."""
    chapters_dir = Path("chapters")
    
    # Search for the file in all subdirectories
    found_file = None
    for category_dir in chapters_dir.iterdir():
        if category_dir.is_dir():
            potential_file = category_dir / filename
            if potential_file.exists():
                found_file = potential_file
                break
            
            # Also try partial matching
            for file in category_dir.glob("*.txt"):
                if filename.lower() in file.name.lower():
                    found_file = file
                    break
    
    if not found_file:
        print(f"Chapter file '{filename}' not found.")
        print("Use 'python manage_chapters.py list' to see available files.")
        return
    
    print(f"📄 {found_file.name}")
    print(f"📁 Category: {found_file.parent.name}")
    print("=" * 60)
    
    try:
        with open(found_file, 'r') as f:
            content = f.read()
            print(content)
    except Exception as e:
        print(f"Error reading file: {e}")

def clean_empty_dirs():
    """Remove empty directories in the chapters folder."""
    chapters_dir = Path("chapters")
    removed = []
    
    for category_dir in chapters_dir.iterdir():
        if category_dir.is_dir():
            files = list(category_dir.glob("*"))
            if not files:
                category_dir.rmdir()
                removed.append(category_dir.name)
    
    if removed:
        print(f"Removed empty directories: {', '.join(removed)}")
    else:
        print("No empty directories found.")

def stats():
    """Show statistics about generated chapters."""
    chapters_dir = Path("chapters")
    
    if not chapters_dir.exists():
        print("No chapters directory found.")
        return
    
    total_files = 0
    total_size = 0
    categories = {}
    
    for category_dir in chapters_dir.iterdir():
        if category_dir.is_dir():
            files = list(category_dir.glob("*.txt"))
            if files:
                category_size = sum(f.stat().st_size for f in files)
                categories[category_dir.name] = {
                    'files': len(files),
                    'size': category_size
                }
                total_files += len(files)
                total_size += category_size
    
    print("📊 Chapter Statistics")
    print("=" * 50)
    print(f"Total Files: {total_files}")
    print(f"Total Size: {total_size:,} bytes ({total_size/1024:.1f} KB)")
    print()
    
    for category, data in sorted(categories.items()):
        print(f"📁 {category.upper()}")
        print(f"   Files: {data['files']}")
        print(f"   Size: {data['size']:,} bytes ({data['size']/1024:.1f} KB)")
        print()

def main():
    parser = argparse.ArgumentParser(description="Manage YouTube chapter files")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List chapter files')
    list_parser.add_argument('category', nargs='?', help='Filter by category (nbme_26, nbme_27, nbme_29, other)')
    
    # View command
    view_parser = subparsers.add_parser('view', help='View a specific chapter file')
    view_parser.add_argument('filename', help='Name of the chapter file to view')
    
    # Stats command
    subparsers.add_parser('stats', help='Show chapter statistics')
    
    # Clean command
    subparsers.add_parser('clean', help='Remove empty directories')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'list':
        list_chapters(args.category)
    elif args.command == 'view':
        view_chapter(args.filename)
    elif args.command == 'stats':
        stats()
    elif args.command == 'clean':
        clean_empty_dirs()

if __name__ == "__main__":
    main()
