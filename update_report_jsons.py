#!/usr/bin/env python3
"""
Update Report JSON Files
========================
This script reads the exported reports JSON and updates each report's
JSON file with the complete data from the export.

Usage:
    1. Ensure surgishop_reports_export.json exists with actual report data
    2. Run: python update_report_jsons.py
"""

import os
import json
import re

def slugify(text):
    """Convert report name to folder name (lowercase with underscores)"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '_', text)
    return text

def find_report_json_path(report_name, base_path='surgishop_reports'):
    """Find the JSON file path for a given report name"""
    folder_name = slugify(report_name)
    
    # Search in all modules
    modules = ['accounts', 'selling', 'stock']
    
    for module in modules:
        report_path = os.path.join(base_path, module, 'report', folder_name)
        json_path = os.path.join(report_path, f'{folder_name}.json')
        
        if os.path.exists(json_path):
            return json_path, module
    
    return None, None

def update_report_jsons():
    """Update all report JSON files from the export file"""
    
    export_file = 'surgishop_reports_export.json'
    
    if not os.path.exists(export_file):
        print(f'Error: {export_file} not found!')
        print('\nPlease ensure the export file exists with report data.')
        return
    
    # Load reports from export
    print(f'Loading reports from {export_file}...\n')
    try:
        with open(export_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            
        # Check if it's just a placeholder
        if content == '[JSON_CONTENT_HERE]' or not content:
            print('Error: Export file appears to be empty or contains placeholder text.')
            print('Please export your reports first using EXPORT_SCRIPT.js')
            return
            
        reports = json.loads(content)
    except json.JSONDecodeError as e:
        print(f'Error: Invalid JSON in export file: {e}')
        return
    except Exception as e:
        print(f'Error reading export file: {e}')
        return
    
    if not isinstance(reports, list):
        print('Error: Export file should contain a JSON array of reports')
        return
    
    print(f'Found {len(reports)} reports in export file\n')
    
    updated = []
    not_found = []
    
    # Update each report's JSON file
    for report in reports:
        report_name = report.get('name')
        if not report_name:
            print('Warning: Found report without a name, skipping...')
            continue
        
        # Find the corresponding JSON file
        json_path, module = find_report_json_path(report_name)
        
        if not json_path:
            not_found.append(report_name)
            print(f'⚠ Could not find JSON file for: {report_name}')
            continue
        
        # Update the JSON file
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=1)
            updated.append(report_name)
            print(f'✓ Updated: {report_name}')
        except Exception as e:
            print(f'✗ Error updating {report_name}: {e}')
    
    # Summary
    print('\n' + '='*60)
    print('UPDATE COMPLETE!')
    print('='*60)
    print(f'Total reports in export: {len(reports)}')
    print(f'Successfully updated: {len(updated)}')
    print(f'Not found: {len(not_found)}')
    print('='*60)
    
    if not_found:
        print('\nReports not found in file structure:')
        for report_name in not_found:
            print(f'  - {report_name}')
        print('\nMake sure these reports exist in the surgishop_reports/ directory')
    
    print('\nDone!')

if __name__ == '__main__':
    update_report_jsons()

