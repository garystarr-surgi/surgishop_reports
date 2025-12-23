# Troubleshooting: Reports Not Appearing on Frappe Cloud

If your reports aren't appearing after installing the app, follow these steps:

## Step 1: Run Database Migrate (REQUIRED)

After installing or updating the app, you **must** run migrate to sync reports from the file system:

1. In Frappe Cloud dashboard, go to your site
2. Click **Database** → **Migrate**
3. Wait for migration to complete
4. Refresh your browser

**Alternative:** If you have console access:
```bash
bench --site [your-site] migrate
```

## Step 2: Clear Cache

1. In Frappe Cloud dashboard, go to your site
2. Click **Database** → **Clear Cache**
3. Or use console: `bench --site [your-site] clear-cache`

## Step 3: Verify App Installation

1. Check that the app shows as "Installed" (not "Attention Required")
2. If it shows "Attention Required", reinstall the app from GitHub
3. Make sure you're using the latest code from the `main` branch

## Step 4: Check Report Files

Verify that the report JSON files exist and have correct structure:

1. Reports should be in: `surgishop_reports/{module}/report/{report_name}/{report_name}.json`
2. Each JSON file should have `"is_standard": "Yes"`
3. Each JSON file should have the correct `"module"` field (Accounts, Selling, or Stock)

## Step 5: Check Modules

The `modules.txt` file should contain:
```
Accounts
Selling
Stock
```

## Step 6: Verify Reports in Database

Run this in the Frappe console to check if reports are being discovered:

```python
import frappe
reports = frappe.get_all('Report', filters={'module': ['in', ['Accounts', 'Selling', 'Stock']], 'is_standard': 'Yes'}, fields=['name', 'module'])
for r in reports:
    print(f"{r.name} - {r.module}")
```

## Step 7: Force Reload Reports

If reports still don't appear, force reload them:

```python
import frappe
from frappe.modules import import_module

# Reload the app modules
frappe.reload_doc('surgishop_reports', 'module', 'accounts')
frappe.reload_doc('surgishop_reports', 'module', 'selling')
frappe.reload_doc('surgishop_reports', 'module', 'stock')

# Sync reports
frappe.db.commit()
```

## Common Issues

### Issue: Reports show in Report List but don't run
- Check that Script Reports have valid Python code in the `.py` files
- Check that Query Reports have valid SQL in the `query` field

### Issue: Module not found errors
- Ensure `modules.txt` contains the module names
- Ensure module folders exist with `__init__.py` files

### Issue: Reports appear but are empty
- Check that the report JSON structure is correct
- Verify filters and columns are properly defined

## Still Not Working?

1. Check the Frappe Cloud site logs for errors
2. Try uninstalling and reinstalling the app
3. Verify all files were pushed to GitHub correctly
4. Check that you're on the latest commit from `main` branch

