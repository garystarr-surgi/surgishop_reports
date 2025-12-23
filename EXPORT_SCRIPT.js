// ============================================
// SURGISHOP REPORTS - BULK EXPORT SCRIPT
// ============================================
// Run this in your browser console on the SOURCE Frappe Cloud instance
// It will export all your custom reports as a single JSON file

// Step 1: List your 20 report names here
var reportNames = [
    "Regional Dashboard",
    "Monthly Pacing",
    "Director Dashboard",
    "Outbound Shipping",
    "Item Tracking Report",
    "Stock Status",
    // ADD YOUR OTHER 14 REPORT NAMES BELOW:
    // "Report Name 7",
    // "Report Name 8",
    // "Report Name 9",
    // etc...
];

// Step 2: Run this code
console.log('Starting export of ' + reportNames.length + ' reports...');

var allReports = [];
var counter = 0;
var errors = [];

reportNames.forEach(function(reportName) {
    frappe.call({
        method: 'frappe.desk.form.load.getdoc',
        args: {
            doctype: 'Report',
            name: reportName
        },
        callback: function(r) {
            counter++;
            
            if (r.message) {
                var doc = r.message;
                
                // Clean up fields for export
                delete doc.owner;
                delete doc.creation;
                delete doc.modified;
                delete doc.modified_by;
                delete doc.idx;
                delete doc.__islocal;
                delete doc.__unsaved;
                delete doc.doctype;
                
                // Mark as standard (from app)
                doc.is_standard = 'Yes';
                doc.docstatus = 0;
                
                allReports.push(doc);
                console.log('✓ Exported: ' + reportName);
            } else {
                errors.push(reportName);
                console.error('✗ Failed: ' + reportName);
            }
            
            // When all done, download
            if (counter === reportNames.length) {
                console.log('\n========================================');
                console.log('Export Complete!');
                console.log('Successfully exported: ' + allReports.length + ' reports');
                if (errors.length > 0) {
                    console.log('Failed to export: ' + errors.length + ' reports');
                    console.log('Failed reports: ' + errors.join(', '));
                }
                console.log('========================================\n');
                
                // Download as file
                var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(allReports, null, 2));
                var downloadAnchorNode = document.createElement('a');
                downloadAnchorNode.setAttribute("href", dataStr);
                downloadAnchorNode.setAttribute("download", "surgishop_reports_export.json");
                document.body.appendChild(downloadAnchorNode);
                downloadAnchorNode.click();
                downloadAnchorNode.remove();
                
                console.log('File downloaded: surgishop_reports_export.json');
                console.log('\nNext steps:');
                console.log('1. Save this file to your computer');
                console.log('2. Use the Python script to import reports into app structure');
            }
        }
    });
});
