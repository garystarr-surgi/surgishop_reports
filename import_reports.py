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
        
        # Save report JSON
        json_path = os.path.join(report_path, f'{folder_name}.json')
        with open(json_path, 'w') as f:
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
    print('Creating folder structure...\n')
    
    # Create structure
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

if __name__ == '__main__':
    main()
