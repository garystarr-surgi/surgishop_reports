# Surgishop Reports - Installation Guide

This guide walks you through exporting 20 reports from one Frappe Cloud instance and importing them to another.

## Step 1: Get Your Report Names

On your **SOURCE** Frappe Cloud instance, run this in the browser console (F12):

```javascript
frappe.call({
    method: 'frappe.client.get_list',
    args: {
        doctype: 'Report',
        filters: {
            is_standard: 'No'
        },
        fields: ['name', 'report_type', 'ref_doctype', 'module'],
        limit_page_length: 100,
        order_by: 'name'
    },
    callback: function(r) {
        console.log('========== YOUR CUSTOM REPORTS ==========');
        console.log('Copy these names into EXPORT_SCRIPT.js:\n');
        r.message.forEach(function(report) {
            console.log('"' + report.name + '",  // ' + report.report_type);
        });
        console.log('\nTotal: ' + r.message.length + ' reports');
    }
});
```

Copy the output.

## Step 2: Update Export Script

1. Open `EXPORT_SCRIPT.js`
2. Replace the `reportNames` array with your 20 report names
3. Save the file

## Step 3: Export Reports

1. On your **SOURCE** Frappe Cloud, open browser console (F12)
2. Copy the entire contents of `EXPORT_SCRIPT.js`
3. Paste into console and press Enter
4. Wait for "Export Complete!" message
5. File will download automatically as `surgishop_reports_export.json`

## Step 4: Import to App Structure

1. Save `surgishop_reports_export.json` in the `surgishop_reports/` directory
2. Run the import script:

```bash
cd surgishop_reports
python3 import_reports.py
```

This will create all folder structures and files automatically.

## Step 5: Review Script Reports

For any Script Reports, check the generated `.py` files:

```bash
# Example: Check Monthly Pacing report
cat surgishop_reports/selling/report/monthly_pacing/monthly_pacing.py
```

Make sure the Python code looks correct. If needed, manually copy the `report_script` content from the JSON file.

## Step 6: Update hooks.py

Edit `surgishop_reports/hooks.py` and add your 20 report names to the fixtures list:

```python
fixtures = [
    {
        "doctype": "Report",
        "filters": [
            [
                "name",
                "in",
                [
                    "Regional Dashboard",
                    "Monthly Pacing",
                    # ... add all 20 report names
                ]
            ]
        ]
    }
]
```

## Step 7: Initialize Git Repository

```bash
cd surgishop_reports
git init
git add .
git commit -m "Initial commit: 20 custom Surgishop reports"
```

## Step 8: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `surgishop_reports`
3. Description: "Custom ERPNext reports for Surgishop"
4. Make it Private (recommended)
5. Don't initialize with README (we already have one)
6. Click "Create repository"

## Step 9: Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/surgishop_reports.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 10: Install on Target Frappe Cloud

1. Log into your **TARGET** Frappe Cloud account
2. Go to your site dashboard
3. Click **Apps** tab
4. Click **Install App** → **From GitHub**
5. Enter repository URL: `https://github.com/YOUR_USERNAME/surgishop_reports`
6. Branch: `main`
7. Click **Install**

Wait for installation to complete (usually 2-5 minutes).

## Step 11: Verify Installation

1. On target site, go to **Report List**
2. Filter by **Module** = "Selling" (or your module)
3. You should see all 20 reports

## Troubleshooting

### Reports not showing up

Run migrate:
1. In Frappe Cloud dashboard, go to **Database** → **Migrate**
2. Or in console: `bench --site yoursite.com migrate`

### Script Report errors

Check the `.py` file for the report:
1. Make sure the code is properly indented
2. Ensure `return columns, data` is at the end
3. Variables should be defined at module level (not just inside functions)

### App not installing

Check these:
1. `setup.py` - Make sure all fields are correct
2. `__init__.py` - Should have `__version__ = '0.0.1'`
3. `modules.txt` - Should be empty (yes, empty)
4. All folders have `__init__.py` files

## Updating Reports

When you make changes:

```bash
# Make your changes to files
git add .
git commit -m "Update report X"
git push

# In Frappe Cloud:
# Go to Apps → Click "Update" next to surgishop_reports
```

## Need Help?

If you encounter issues:
1. Check the error logs in Frappe Cloud dashboard
2. Verify all file paths are correct
3. Make sure JSON files are valid (use a JSON validator)
4. Check that Script Reports have proper Python syntax

---

## File Structure Reference

```
surgishop_reports/
├── README.md
├── license.txt
├── setup.py
├── EXPORT_SCRIPT.js (helper script)
├── import_reports.py (helper script)
├── INSTALLATION.md (this file)
└── surgishop_reports/
    ├── __init__.py
    ├── hooks.py
    ├── modules.txt (empty)
    ├── config/
    │   ├── __init__.py
    │   └── desktop.py
    └── selling/ (or your module name)
        ├── __init__.py
        └── report/
            ├── __init__.py
            ├── regional_dashboard/
            │   ├── __init__.py
            │   ├── regional_dashboard.json
            │   └── regional_dashboard.py (if Script Report)
            ├── monthly_pacing/
            │   ├── __init__.py
            │   ├── monthly_pacing.json
            │   └── monthly_pacing.py
            └── ... (18 more reports)
```

Good luck! 🚀
