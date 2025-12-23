#!/usr/bin/env python3
"""
Surgishop Print Formats - Import Script
========================================
This script takes the exported print formats JSON and creates the proper
folder structure for the Frappe app.

Usage:
    1. Export your print formats (similar to reports)
    2. Save the downloaded JSON file as 'surgishop_print_formats_export.json'
    3. Place it in the same directory as this script
    4. Run: python3 import_print_formats.py
"""

import os
import json
import re

def slugify(text):
    """Convert print format name to folder name (lowercase with underscores)"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '_', text)
    return text

def create_print_format_structure(print_formats, base_path='surgishop_reports'):
    """Create folder structure for all print formats"""
    
    created_formats = []
    
    for pf in print_formats:
        pf_name = pf['name']
        module = pf.get('module', 'Selling').lower()
        
        # Convert to folder name
        folder_name = slugify(pf_name)
        
        # Create folder structure
        pf_path = os.path.join(base_path, module, 'print_format', folder_name)
        os.makedirs(pf_path, exist_ok=True)
        
        # Create __init__.py at each level
        for level_path in [
            os.path.join(base_path, module),
            os.path.join(base_path, module, 'print_format'),
            pf_path
        ]:
            init_file = os.path.join(level_path, '__init__.py')
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    f.write('')
        
        # Set is_standard to Yes for app deployment
        pf['is_standard'] = 'Yes'
        pf['docstatus'] = 0
        
        # Save print format JSON
        json_path = os.path.join(pf_path, f'{folder_name}.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(pf, f, indent=1)
        
        created_formats.append({
            'name': pf_name,
            'module': module,
            'path': pf_path
        })
        
        print(f'[OK] Created: {pf_name} ({module})')
    
    return created_formats

def main():
    # Check if export file exists
    export_file = 'surgishop_print_formats_export.json'
    
    if not os.path.exists(export_file):
        print(f'Error: {export_file} not found!')
        print('\nPlease:')
        print('1. Export your print formats')
        print('2. Save the file as "surgishop_print_formats_export.json"')
        print('3. Place it in the same directory as this script')
        print('4. Run this script again')
        return
    
    # Load print formats
    print(f'Loading print formats from {export_file}...\n')
    with open(export_file, 'r', encoding='utf-8') as f:
        print_formats = json.load(f)
    
    print(f'Found {len(print_formats)} print formats\n')
    print('Creating folder structure...\n')
    
    # Create structure
    created = create_print_format_structure(print_formats)
    
    # Summary
    print('\n' + '='*60)
    print('IMPORT COMPLETE!')
    print('='*60)
    print(f'Total print formats: {len(created)}')
    print('='*60)
    
    print('\nNext steps:')
    print('1. Review the created files in surgishop_reports/')
    print('2. Update hooks.py to add print formats to fixtures')
    print('3. Commit and push to GitHub')
    print('4. Install/update app on target Frappe Cloud')
    print('5. Run migrate to sync print formats')
    print('\nDone!')

if __name__ == '__main__':
    main()

