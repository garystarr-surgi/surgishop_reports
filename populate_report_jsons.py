#!/usr/bin/env python3
"""
Populate Report JSON Files
==========================
This script reads from surgishop_reports_export.json and populates each 
report's JSON file with the complete data using the same logic as import_reports.py.

Usage:
    python populate_report_jsons.py
"""

import os
import json
import re

def slugify(text):
    """Convert report name to folder name (lowercase with underscores) - from import_reports.py"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '_', text)
    return text

def populate_report_json(report, base_path='surgishop_reports'):
    """Populate a report's JSON file with data from export - using import_reports.py logic"""
    report_name = report.get('name')
    if not report_name:
        return False, None, "No report name found"
    
    module = report.get('module', 'Selling').lower()
    folder_name = slugify(report_name)
    
    # Find the JSON file path (matching import_reports.py structure)
    json_path = os.path.join(base_path, module, 'report', folder_name, f'{folder_name}.json')
    
    if not os.path.exists(json_path):
        return False, json_path, f"JSON file not found at {json_path}"
    
    try:
        # Write the complete report JSON data (same as import_reports.py line 77)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=1)
        return True, json_path, None
    except Exception as e:
        return False, json_path, str(e)

def main():
    """Main function to populate all report JSON files"""
    # Check multiple possible locations for the export file
    possible_paths = [
        'surgishop_reports_export.json',
        'surgishop_reports/surgishop_reports_export.json',
        os.path.join('surgishop_reports', 'surgishop_reports_export.json')
    ]
    
    export_file = None
    for path in possible_paths:
        if os.path.exists(path):
            export_file = path
            break
    
    if not export_file:
        print('Error: Export file not found in any of these locations:')
        for path in possible_paths:
            print(f'  - {path}')
        print('\nPlease ensure the export file exists.')
        return
    
    print(f'Found export file at: {export_file}\n')
    
    # Load reports (same as import_reports.py)
    print(f'Loading reports from {export_file}...\n')
    try:
        with open(export_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Check for placeholder
        if content == '[JSON_CONTENT_HERE]' or not content:
            print('Error: Export file appears to be empty or contains placeholder.')
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
    
    print(f'Found {len(reports)} reports\n')
    print('Populating report JSON files...\n')
    
    # Populate each report's JSON file (using import_reports.py logic)
    updated = []
    errors = []
    
    for report in reports:
        report_name = report.get('name', 'Unknown')
        success, json_path, error_msg = populate_report_json(report)
        
        if success:
            updated.append(report_name)
            print(f'[OK] Populated: {report_name}')
        else:
            errors.append((report_name, json_path, error_msg))
            print(f'[FAIL] Failed: {report_name} - {error_msg}')
    
    # Summary
    print('\n' + '='*60)
    print('POPULATION COMPLETE!')
    print('='*60)
    print(f'Successfully populated: {len(updated)}/{len(reports)} reports')
    if errors:
        print(f'Errors: {len(errors)}')
    print('='*60)
    
    if errors:
        print('\nReports that could not be populated:')
        for report_name, json_path, error in errors:
            print(f'  - {report_name}: {error}')
    
    print('\nDone!')

if __name__ == '__main__':
    main()

