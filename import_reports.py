#!/usr/bin/env python3
"""
Surgishop Reports - Import Script
==================================
This script takes the exported reports JSON and creates the proper
folder structure for the Frappe app.

Usage:
    1. Export your reports using EXPORT_SCRIPT.js
    2. Save the downloaded JSON file as 'surgishop_reports_export.json'
    3. Place it in the same directory as this script
    4. Run: python3 import_reports.py
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

def update_existing_report_json(report, base_path='surgishop_reports'):
    """Update an existing report's JSON file with data from export"""
    report_name = report['name']
    module = report.get('module', 'Selling').lower()
    
    # Convert to folder name
    folder_name = slugify(report_name)
    
    # Find the JSON file
    json_path = os.path.join(base_path, module, 'report', folder_name, f'{folder_name}.json')
    
    if os.path.exists(json_path):
        # Update the JSON file with full report data
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=1)
        return True, json_path
    return False, json_path

def create_report_structure(reports, base_path='surgishop_reports'):
    """Create folder structure for all reports"""
    
    created_reports = []
    script_reports = []
    query_reports = []
    
    for report in reports:
        report_name = report['name']
        report_type = report.get('report_type', 'Report Builder')
        module = report.get('module', 'Selling').lower()
        
        # Convert to folder name
        folder_name = slugify(report_name)
        
        # Create folder structure
        report_path = os.path.join(base_path, module, 'report', folder_name)
        os.makedirs(report_path, exist_ok=True)
        
        # Create __init__.py at each level
        for level_path in [
            os.path.join(base_path, module),
            os.path.join(base_path, module, 'report'),
            report_path
        ]:
            init_file = os.path.join(level_path, '__init__.py')
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    f.write('')
        
        # Save report JSON (this will update if file already exists)
        json_path = os.path.join(report_path, f'{folder_name}.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=1)
        
        # If Script Report, create Python file
        if report_type == 'Script Report':
            py_path = os.path.join(report_path, f'{folder_name}.py')
            
            # Extract report_script if it exists
            report_script = report.get('report_script', '')
            
            if report_script:
                # Create Python file with the script
                py_content = f'''# Copyright (c) 2025, Surgishop
# License: MIT

import frappe

def execute(filters=None):
    """
    {report_name}
    """
    {report_script}
    
    # Ensure we return the right format
    return columns, data
'''
            else:
                # Create placeholder
                py_content = f'''# Copyright (c) 2025, Surgishop
# License: MIT

import frappe

def execute(filters=None):
    """
    {report_name}
    
    TODO: Add your report logic here
    This is a placeholder - copy your script from the JSON file's report_script field
    """
    columns = []
    data = []
    
    return columns, data
'''
            
            with open(py_path, 'w') as f:
                f.write(py_content)
            
            script_reports.append(report_name)
        else:
            query_reports.append(report_name)
        
        created_reports.append({
            'name': report_name,
            'type': report_type,
            'module': module,
            'path': report_path
        })
        
        print(f'✓ Created: {report_name} ({report_type})')
    
    return created_reports, script_reports, query_reports

def main():
    # Check if export file exists
    export_file = 'surgishop_reports_export.json'
    
    if not os.path.exists(export_file):
        print(f'Error: {export_file} not found!')
        print('\nPlease:')
        print('1. Run EXPORT_SCRIPT.js in your browser console on the source Frappe Cloud')
        print('2. Save the downloaded file as "surgishop_reports_export.json"')
        print('3. Place it in the same directory as this script')
        print('4. Run this script again')
        return
    
    # Load reports
    print(f'Loading reports from {export_file}...\n')
    with open(export_file, 'r') as f:
        reports = json.load(f)
    
    print(f'Found {len(reports)} reports\n')
    print('Processing reports (creating/updating JSON files)...\n')
    
    # Create/update structure (this will overwrite existing JSON files with full data)
    created, script_reports, query_reports = create_report_structure(reports)
    
    # Summary
    print('\n' + '='*60)
    print('IMPORT COMPLETE!')
    print('='*60)
    print(f'Total reports: {len(created)}')
    print(f'  - Query Reports: {len(query_reports)}')
    print(f'  - Script Reports: {len(script_reports)}')
    print('='*60)
    
    if script_reports:
        print('\nScript Reports that may need manual review:')
        for report in script_reports:
            print(f'  - {report}')
        print('\nNote: Check each Script Report\'s .py file and ensure the')
        print('report_script content is properly formatted.')
    
    print('\nNext steps:')
    print('1. Review the created files in surgishop_reports/')
    print('2. For Script Reports, verify the Python code is correct')
    print('3. Initialize git: git init')
    print('4. Add files: git add .')
    print('5. Commit: git commit -m "Initial commit with 20 reports"')
    print('6. Create GitHub repo and push')
    print('7. Install app on target Frappe Cloud from GitHub')
    print('\nDone!')

def update_existing_reports():
    """Update existing report JSON files with data from export file"""
    export_file = 'surgishop_reports_export.json'
    
    if not os.path.exists(export_file):
        print(f'Error: {export_file} not found!')
        return
    
    # Load reports
    print(f'Loading reports from {export_file}...\n')
    try:
        with open(export_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            
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
    print('Updating existing JSON files...\n')
    
    updated = []
    not_found = []
    
    for report in reports:
        report_name = report.get('name')
        if not report_name:
            continue
        
        success, json_path = update_existing_report_json(report)
        if success:
            updated.append(report_name)
            print(f'✓ Updated: {report_name}')
        else:
            not_found.append(report_name)
            print(f'⚠ Not found: {report_name} (expected at {json_path})')
    
    print('\n' + '='*60)
    print('UPDATE COMPLETE!')
    print('='*60)
    print(f'Successfully updated: {len(updated)}')
    print(f'Not found: {len(not_found)}')
    print('='*60)
    
    if not_found:
        print('\nReports not found (they may need to be created first):')
        for report_name in not_found:
            print(f'  - {report_name}')

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--update':
        update_existing_reports()
    else:
        main()
