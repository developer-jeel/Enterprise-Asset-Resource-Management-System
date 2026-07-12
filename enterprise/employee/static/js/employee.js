// Employee Portal — State & Interaction Handler

const INITIAL_EMP_DATABASE = {
  employee: {
    id: 'EMP-004',
    name: 'Bob Smith',
    email: 'bob.s@assetflow.com',
    department: 'Engineering',
    role: 'Standard User',
    avatar: 'BS'
  },
  myAssets: [
    { id: 'AST-0201', name: 'MacBook Pro 14"', tag: 'AST-0201', category: 'Laptops', serial: 'C02GH12XMD9T', condition: 'Excellent', status: 'Allocated', department: 'Engineering', location: 'HQ-402', allocDate: '2025-06-01', returnDate: '2026-06-01', vendor: 'Apple Inc.', cost: 1999, warranty: '2028-06-01', notes: 'Primary workstation laptop' },
    { id: 'AST-0202', name: 'Dell 27" Monitor', tag: 'AST-0202', category: 'Monitors', serial: 'DELL4K2027XZ', condition: 'Good', status: 'Allocated', department: 'Engineering', location: 'HQ-402', allocDate: '2025-06-01', returnDate: '2026-06-01', vendor: 'Dell Inc.', cost: 520, warranty: '2027-06-01', notes: 'Secondary display' },
    { id: 'AST-0203', name: 'Logitech MX Master 3', tag: 'AST-0203', category: 'Accessories', serial: 'LOGI-MX3-0442', condition: 'Good', status: 'Allocated', department: 'Engineering', location: 'HQ-402', allocDate: '2025-07-10', returnDate: '2026-07-10', vendor: 'Logitech', cost: 99, warranty: '2027-07-10', notes: 'Wireless ergonomic mouse' },
    { id: 'AST-0204', name: 'iPhone 14 Pro', tag: 'AST-0204', category: 'Phones', serial: 'IPH14P9921AB', condition: 'Fair', status: 'Allocated', department: 'Engineering', location: 'HQ-402', allocDate: '2025-03-15', returnDate: '2026-03-15', vendor: 'Apple Inc.', cost: 999, warranty: '2027-03-15', notes: 'QA testing device — battery degraded' },
  ],
  bookings: [
    { id: 'BK-6001', resource: 'Meeting Room 204', type: 'Room', capacity: 10, date: '2026-07-14', start: '10:00 AM', end: '11:30 AM', purpose: 'Sprint Planning', status: 'Active', notes: 'Need projector setup' },
    { id: 'BK-6002', resource: 'Conference Hall B', type: 'Hall', capacity: 50, date: '2026-07-18', start: '02:00 PM', end: '04:00 PM', purpose: 'Design Review', status: 'Active', notes: '' },
    { id: 'BK-6003', resource: 'Projector Max', type: 'Equipment', capacity: 1, date: '2026-07-10', start: '09:00 AM', end: '12:00 PM', purpose: 'Demo session', status: 'Completed', notes: '' },
  ],
  resources: [
    { id: 'RES-01', name: 'Meeting Room 204', type: 'Room', capacity: 10, floor: 'Floor 2', icon: 'ri-building-line', availability: 'Available' },
    { id: 'RES-02', name: 'Conference Hall B', type: 'Hall', capacity: 50, floor: 'Ground Floor', icon: 'ri-community-line', availability: 'Partial' },
    { id: 'RES-03', name: 'Projector Max', type: 'Equipment', capacity: 1, floor: 'Portable', icon: 'ri-projector-2-line', availability: 'Available' },
    { id: 'RES-04', name: 'Corporate Sedan', type: 'Vehicle', capacity: 4, floor: 'Parking B', icon: 'ri-car-line', availability: 'Unavailable' },
    { id: 'RES-05', name: 'Training Room C', type: 'Room', capacity: 20, floor: 'Floor 3', icon: 'ri-building-4-line', availability: 'Available' },
    { id: 'RES-06', name: 'Video Camera Kit', type: 'Equipment', capacity: 1, floor: 'Portable', icon: 'ri-vidicon-line', availability: 'Partial' },
  ],
  maintenance: [
    { id: 'MR-8001', assetId: 'AST-0204', assetName: 'iPhone 14 Pro', priority: 'High', issue: 'Battery health at 68% — device not lasting through the workday. Requires battery replacement.', submittedDate: '2026-07-08', status: 'In Progress', technician: 'IT Support Team', remarks: 'Parts ordered. Repair scheduled for July 14.' },
    { id: 'MR-8002', assetId: 'AST-0201', assetName: 'MacBook Pro 14"', priority: 'Low', issue: 'Right speaker produces occasional crackling noise at high volumes. Mostly functional.', submittedDate: '2026-06-25', status: 'Resolved', technician: 'Mark Technical', remarks: 'Speaker replaced under warranty. Issue closed.' },
  ],
  requests: [
    { id: 'REQ-7001', type: 'Return', assetId: 'AST-0203', assetName: 'Logitech MX Master 3', reason: 'No longer needed — switching to built-in trackpad.', submittedDate: '2026-07-09', status: 'Pending', remarks: '' },
    { id: 'REQ-7002', type: 'Transfer', assetId: 'AST-0202', assetName: 'Dell 27" Monitor', toEmployee: 'Alice Johnson', toDept: 'Engineering', reason: 'Alice needs a second monitor for dual-screen dev setup.', submittedDate: '2026-07-07', status: 'Approved', remarks: 'Approved. Please coordinate handover by July 15.' },
    { id: 'REQ-7003', type: 'Return', assetId: 'AST-0204', assetName: 'iPhone 14 Pro', reason: 'Device condition degraded. Returning for replacement.', submittedDate: '2026-07-05', status: 'Rejected', remarks: 'Maintenance request already raised. Retain until repair complete.' },
  ],
  activities: [
    { text: 'Maintenance request MR-8001 status updated to In Progress', time: '1 hour ago', type: 'maintenance' },
    { text: 'Booking BK-6001 confirmed — Meeting Room 204 for Sprint Planning', time: '3 hours ago', type: 'booking' },
    { text: 'Transfer request REQ-7002 approved by Asset Manager', time: '1 day ago', type: 'transfer' },
    { text: 'Asset AST-0203 (Logitech MX Master 3) allocated to your account', time: '2 days ago', type: 'asset' },
    { text: 'Maintenance request MR-8002 resolved — speaker replaced', time: '4 days ago', type: 'maintenance' },
  ]
};

function getEmpDB() {
  const db = localStorage.getItem('employee_portal_db');
  if (!db) {
    localStorage.setItem('employee_portal_db', JSON.stringify(INITIAL_EMP_DATABASE));
    return JSON.parse(JSON.stringify(INITIAL_EMP_DATABASE));
  }
  return JSON.parse(db);
}

function saveEmpDB(db) {
  localStorage.setItem('employee_portal_db', JSON.stringify(db));
}

// Shared App shim
if (typeof window.App === 'undefined') {
  window.App = {
    showToast(message, type = 'success') {
      let c = document.getElementById('toastContainer');
      if (!c) { c = document.createElement('div'); c.id = 'toastContainer'; c.className = 'toast-container'; document.body.appendChild(c); }
      const t = document.createElement('div');
      t.className = `toast toast-${type}`;
      const icons = { success:'ri-checkbox-circle-fill', danger:'ri-error-warning-fill', warning:'ri-alert-fill', info:'ri-information-line' };
      t.innerHTML = `<i class="${icons[type]||icons.success}"></i><span>${message}</span>`;
      c.appendChild(t);
      setTimeout(() => { t.style.opacity = '0'; t.style.transform = 'translateY(10px)'; setTimeout(() => t.remove(), 300); }, 3500);
    },
    openModal(id) { const e = document.getElementById(id); if (e) { e.classList.add('open'); document.body.style.overflow = 'hidden'; } },
    closeModal(id) { const e = document.getElementById(id); if (e) { e.classList.remove('open'); document.body.style.overflow = ''; } }
  };
}

window.EmpApp = { getDB: getEmpDB, saveDB: saveEmpDB };
