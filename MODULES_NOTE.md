# Modules.txt Note

## Current Status
The `modules.txt` file currently contains:
```
Accounts
Selling
Stock
```

## Important Information

### Standard Modules
Accounts, Selling, and Stock are **standard ERPNext modules**, not custom modules. Technically, they don't need to be listed in `modules.txt` - that file is typically for custom modules only.

### Why They're Listed
Based on your experience where adding modules, breaking the site, then removing them made reports work - it appears that:

1. **The migration/refresh process** triggered by the change is what actually fixed the discovery
2. Having them listed may help Frappe discover reports and print formats in your app's module folders
3. Some Frappe versions/configurations may require explicit module listing for discovery

### What to Do

**Option 1: Keep them listed (Recommended if it works)**
- If reports and print formats are working with modules listed, keep them
- No harm in having them there

**Option 2: Remove after migration**
- After running migrate and confirming everything works, you can remove them
- The reports/print formats should remain in the database even after removal
- If you remove them, just ensure you run migrate again

### Testing
1. Pull latest code with modules.txt
2. Run **Database → Migrate** on Frappe Cloud
3. Clear cache
4. Verify reports and print formats appear
5. If everything works, you can optionally remove modules from modules.txt later

### If Reports Still Don't Appear
1. Check that all JSON files have `"is_standard": "Yes"`
2. Verify the module folders exist: `surgishop_reports/{module}/report/` and `surgishop_reports/{module}/print_format/`
3. Run migrate multiple times
4. Check Frappe Cloud logs for errors
5. Try the force reload commands in TROUBLESHOOTING.md

