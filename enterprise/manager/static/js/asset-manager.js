// Asset Manager Portal — State & Interaction Handler

const INITIAL_AM_DATABASE = {
  assets: [
    { id: 'AST-0101', name: 'MacBook Pro 16"', category: 'Laptops', serial: 'C02DF98XMD6M', condition: 'Excellent', lifecycle: 'In Use', department: 'Engineering', employee: 'Sarah Connor', location: 'HQ-402', acquired: '2025-01-15', cost: 2499, warranty: '2028-01-15', vendor: 'Apple Inc.', notes: 'Primary dev machine' },
    { id: 'AST-0102', name: 'Dell XPS 15', category: 'Laptops', serial: 'DELL8892112Z', condition: 'Good', lifecycle: 'In Use', department: 'Engineering', employee: 'John Doe', location: 'HQ-402', acquired: '2025-02-10', cost: 1899, warranty: '2028-02-10', vendor: 'Dell Inc.', notes: 'Frontend dev machine' },
    { id: 'AST-0103', name: 'iPhone 14 Pro', category: 'Phones', serial: 'IPH14P98821X', condition: 'Excellent', lifecycle: 'In Use', department: 'Engineering', employee: 'Alice Johnson', location: 'HQ-405', acquired: '2025-03-01', cost: 999, warranty: '2027-03-01', vendor: 'Apple Inc.', notes: 'QA testing device' },
    { id: 'AST-0104', name: 'LG UltraFine 27"', category: 'Monitors', serial: 'LGMON881029A', condition: 'Excellent', lifecycle: 'In Use', department: 'Marketing', employee: 'Emma Watson', location: 'HQ-301', acquired: '2025-01-15', cost: 699, warranty: '2028-01-15', vendor: 'LG Electronics', notes: 'Design team display' },
    { id: 'AST-0105', name: 'Herman Miller Aeron', category: 'Furniture', serial: 'HERM8821990Z', condition: 'Good', lifecycle: 'In Use', department: 'Finance', employee: 'Robert Downey', location: 'HQ-201', acquired: '2025-04-01', cost: 1200, warranty: '2030-04-01', vendor: 'Herman Miller', notes: 'Ergonomic chair' },
    { id: 'AST-0106', name: 'Sony WH-1000XM5', category: 'Accessories', serial: 'SONYXM59882B', condition: 'Good', lifecycle: 'Storage', department: '—', employee: '—', location: 'Warehouse A', acquired: '2025-04-10', cost: 380, warranty: '2027-04-10', vendor: 'Sony Corp', notes: 'Spare headset unit' },
    { id: 'AST-0107', name: 'ThinkPad X1 Carbon', category: 'Laptops', serial: 'TPX1C990011Z', condition: 'Fair', lifecycle: 'Repair', department: 'Operations', employee: '—', location: 'IT Workshop', acquired: '2024-05-01', cost: 1699, warranty: '2027-05-01', vendor: 'Lenovo', notes: 'Sent for keyboard repair' },
    { id: 'AST-0108', name: 'iPad Air (5th Gen)', category: 'Tablets', serial: 'IPDA992811AB', condition: 'Excellent', lifecycle: 'In Use', department: 'Marketing', employee: 'Diana Prince', location: 'HQ-302', acquired: '2025-03-12', cost: 599, warranty: '2027-03-12', vendor: 'Apple Inc.', notes: 'Presentation device' },
  ],
  allocations: [
    { id: 'AR-3001', assetId: 'AST-0106', assetName: 'Sony WH-1000XM5', requestedBy: 'Charlie Brown', department: 'Engineering', requestDate: '2026-07-10', returnDate: '2027-07-10', purpose: 'Remote presentation work', status: 'Pending', remarks: '' },
    { id: 'AR-3002', assetId: 'AST-0101', assetName: 'MacBook Pro 16"', requestedBy: 'John Doe', department: 'Engineering', requestDate: '2026-07-09', returnDate: '2027-07-09', purpose: 'Additional dev machine', status: 'Approved', remarks: 'Approved for Q3 project sprint.' },
    { id: 'AR-3003', assetId: 'AST-0108', assetName: 'iPad Air (5th Gen)', requestedBy: 'Tony Stark', department: 'Finance', requestDate: '2026-07-08', returnDate: '2027-07-08', purpose: 'Client presentations', status: 'Pending', remarks: '' },
    { id: 'AR-3004', assetId: 'AST-0104', assetName: 'LG UltraFine 27"', requestedBy: 'Diana Prince', department: 'Marketing', requestDate: '2026-07-06', returnDate: '2027-06-06', purpose: 'Design workstation upgrade', status: 'Rejected', remarks: 'Asset currently assigned. Request deferred.' },
  ],
  transfers: [
    { id: 'TR-5001', assetId: 'AST-0103', assetName: 'iPhone 14 Pro', from: 'Alice Johnson (Engineering)', to: 'Bob Smith (QA)', reason: 'Bob needs device for mobile testing', requestDate: '2026-07-11', status: 'Pending', remarks: '' },
    { id: 'TR-5002', assetId: 'AST-0102', assetName: 'Dell XPS 15', from: 'John Doe (Engineering)', to: 'Eva Green (Operations)', reason: 'Eva needs a laptop for field deployment', requestDate: '2026-07-10', status: 'Approved', remarks: 'Transfer approved and handover completed.' },
    { id: 'TR-5003', assetId: 'AST-0105', assetName: 'Herman Miller Aeron', from: 'Robert Downey (Finance)', to: 'James Carter (HR)', reason: 'James relocated offices', requestDate: '2026-07-09', status: 'Pending', remarks: '' },
  ],
  maintenance: [
    { id: 'MNT-7001', assetId: 'AST-0107', assetName: 'ThinkPad X1 Carbon', priority: 'High', issue: 'Keyboard keys unresponsive — keys D, E, F not registering. Requires physical keyboard replacement.', reportedBy: 'Eva Green', reportDate: '2026-07-08', department: 'Operations', technician: '', status: 'Pending', estimatedDays: 3, remarks: '' },
    { id: 'MNT-7002', assetId: 'AST-0103', assetName: 'iPhone 14 Pro', priority: 'Medium', issue: 'Battery health degraded to 71%. Device not lasting through the workday. Battery replacement required.', reportedBy: 'Alice Johnson', reportDate: '2026-07-07', department: 'Engineering', technician: 'Mark Technical', status: 'Approved', estimatedDays: 2, remarks: 'Parts ordered, repair scheduled for July 14.' },
    { id: 'MNT-7003', assetId: 'AST-0104', assetName: 'LG UltraFine 27"', priority: 'Low', issue: 'Monitor occasionally flickering at full brightness. Firmware update required from LG support portal.', reportedBy: 'Emma Watson', reportDate: '2026-07-06', department: 'Marketing', technician: '', status: 'Pending', estimatedDays: 1, remarks: '' },
    { id: 'MNT-7004', assetId: 'AST-0101', assetName: 'MacBook Pro 16"', priority: 'Critical', issue: 'Liquid damage detected near charging port. Device not powering on. Urgent board-level repair required.', reportedBy: 'Sarah Connor', reportDate: '2026-07-10', department: 'Engineering', technician: '', status: 'Pending', estimatedDays: 7, remarks: '' },
  ],
  discrepancies: [
    { id: 'DISC-9001', auditId: 'AUD-2026-Q3', assetId: 'AST-0107', assetName: 'ThinkPad X1 Carbon', type: 'Location Mismatch', severity: 'Medium', description: 'Asset recorded at HQ-403 but physically found at IT Workshop. Location data needs updating.', detectedDate: '2026-07-05', status: 'Pending', resolution: '' },
    { id: 'DISC-9002', auditId: 'AUD-2026-Q3', assetId: 'AST-0106', assetName: 'Sony WH-1000XM5', type: 'Condition Mismatch', severity: 'Low', description: 'Asset marked "Excellent" in system but physical inspection reveals minor scratches on ear cups. Condition downgrade needed.', detectedDate: '2026-07-05', status: 'Pending', resolution: '' },
    { id: 'DISC-9003', auditId: 'AUD-2026-Q3', assetId: 'AST-MISSING-01', assetName: 'Logitech MX Keys', type: 'Missing Asset', severity: 'High', description: 'Asset with tag LOGI-MXK-011 listed in inventory but not found during physical audit. Last seen at HQ-402.', detectedDate: '2026-07-06', status: 'Resolved', resolution: 'Confirmed lost. Asset tagged for write-off and insurance claim filed.' },
    { id: 'DISC-9004', auditId: 'AUD-2026-Q3', assetId: 'AST-0108', assetName: 'iPad Air (5th Gen)', type: 'Condition Mismatch', severity: 'Medium', description: 'Screen has visible crack on lower-left corner. Condition in system shows Excellent but needs to be downgraded to Fair.', detectedDate: '2026-07-07', status: 'Pending', resolution: '' },
  ],
  returns: [
    { id: 'RET-4001', assetId: 'AST-0102', assetName: 'Dell XPS 15', employee: 'John Doe', department: 'Engineering', expectedReturn: '2026-07-10', actualReturn: '2026-07-11', conditionAtReturn: 'Good', conditionOriginal: 'Good', notes: 'Slight wear on keyboard. No functional issues.', status: 'Pending' },
    { id: 'RET-4002', assetId: 'AST-0103', assetName: 'iPhone 14 Pro', employee: 'Alice Johnson', department: 'Engineering', expectedReturn: '2026-07-08', actualReturn: '2026-07-08', conditionAtReturn: 'Fair', conditionOriginal: 'Excellent', notes: 'Battery significantly degraded. Screen in good shape.', status: 'Pending' },
    { id: 'RET-4003', assetId: 'AST-0105', assetName: 'Herman Miller Aeron', employee: 'Robert Downey', department: 'Finance', expectedReturn: '2026-07-12', actualReturn: '2026-07-12', conditionAtReturn: 'Excellent', conditionOriginal: 'Excellent', notes: 'Perfect condition. No issues noted.', status: 'Approved' },
  ],
  activities: [
    { text: 'Asset AST-0107 sent for keyboard repair (MNT-7001)', time: '30 mins ago', type: 'repair' },
    { text: 'Transfer TR-5002 approved – Dell XPS 15 handover to Eva Green', time: '2 hours ago', type: 'transfer' },
    { text: 'New asset AST-0108 registered – iPad Air 5th Gen', time: '1 day ago', type: 'register' },
    { text: 'Return RET-4003 approved – Herman Miller Aeron checked in', time: '2 days ago', type: 'return' },
    { text: 'Discrepancy DISC-9003 resolved – Logitech MX Keys marked missing', time: '3 days ago', type: 'audit' },
  ]
};

function getAMDB() {
  const db = localStorage.getItem('asset_manager_db');
  if (!db) {
    localStorage.setItem('asset_manager_db', JSON.stringify(INITIAL_AM_DATABASE));
    return JSON.parse(JSON.stringify(INITIAL_AM_DATABASE));
  }
  return JSON.parse(db);
}

function saveAMDB(db) {
  localStorage.setItem('asset_manager_db', JSON.stringify(db));
}

// Ensure App exists (fallback if app.js not yet loaded)
if (typeof window.App === 'undefined') {
  window.App = {
    showToast(message, type = 'success') {
      let container = document.getElementById('toastContainer');
      if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container';
        document.body.appendChild(container);
      }
      const toast = document.createElement('div');
      toast.className = `toast toast-${type}`;
      const icons = { success: 'ri-checkbox-circle-fill', danger: 'ri-error-warning-fill', warning: 'ri-alert-fill', info: 'ri-information-line' };
      toast.innerHTML = `<i class="${icons[type] || icons.success}"></i><span>${message}</span>`;
      container.appendChild(toast);
      setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateY(10px)'; setTimeout(() => toast.remove(), 300); }, 3500);
    },
    openModal(id) {
      const el = document.getElementById(id);
      if (el) { el.classList.add('open'); document.body.style.overflow = 'hidden'; }
    },
    closeModal(id) {
      const el = document.getElementById(id);
      if (el) { el.classList.remove('open'); document.body.style.overflow = ''; }
    }
  };
}

window.AssetManagerApp = { getDB: getAMDB, saveDB: saveAMDB };
