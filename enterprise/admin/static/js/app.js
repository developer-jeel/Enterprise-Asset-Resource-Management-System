// Department Head Portal State & Interactivity Handler

// Initial Mock Data Structure
const INITIAL_DATABASE = {
  assets: [
    { id: 'AST-4902', name: 'MacBook Pro 16"', category: 'Laptops', employee: 'Sarah Connor', status: 'Allocated', location: 'HQ - Room 402', date: '2026-01-10', returnDate: '2027-01-10', sn: 'C02DF98XMD6M', value: '$2,499.00', condition: 'Excellent', lastAudit: '2026-05-15', notes: 'Primary development machine with 32GB RAM' },
    { id: 'AST-8291', name: 'Dell XPS 15', category: 'Laptops', employee: 'John Doe', status: 'Allocated', location: 'HQ - Room 402', date: '2026-02-15', returnDate: '2027-02-15', sn: 'DELL8892112Z', value: '$1,899.00', condition: 'Good', lastAudit: '2026-05-20', notes: 'Assigned for frontend development' },
    { id: 'AST-1029', name: 'iPhone 14 Pro', category: 'Phones', employee: 'Alice Johnson', status: 'Allocated', location: 'HQ - Room 405', date: '2026-03-01', returnDate: '2027-03-01', sn: 'IPH14P98821X', value: '$999.00', condition: 'Excellent', lastAudit: '2026-06-01', notes: 'QA testing device' },
    { id: 'AST-3810', name: 'iPad Air', category: 'Tablets', employee: 'Bob Smith', status: 'Allocated', location: 'HQ - Room 405', date: '2026-03-12', returnDate: '2027-03-12', sn: 'IPDA992811AB', value: '$599.00', condition: 'Good', lastAudit: '2026-06-10', notes: 'UI mockup presentations' },
    { id: 'AST-7762', name: 'LG UltraFine 27"', category: 'Monitors', employee: 'Sarah Connor', status: 'Allocated', location: 'HQ - Room 402', date: '2026-01-10', returnDate: '2027-01-10', sn: 'LGMON881029A', value: '$699.00', condition: 'Excellent', lastAudit: '2026-05-15', notes: 'Engineering team display' },
    { id: 'AST-9021', name: 'Ergonomic Chair', category: 'Chairs', employee: 'Charlie Brown', status: 'Allocated', location: 'HQ - Room 402', date: '2026-04-01', returnDate: '2027-04-01', sn: 'HERM8821990Z', value: '$1,200.00', condition: 'Excellent', lastAudit: '2026-06-15', notes: 'Herman Miller Aeron' },
    { id: 'AST-5521', name: 'Sony WH-1000XM4', category: 'Headsets', employee: 'David Miller', status: 'Allocated', location: 'HQ - Room 402', date: '2026-04-10', returnDate: '2027-04-10', sn: 'SONYXM49882B', value: '$349.00', condition: 'Good', lastAudit: '2026-06-20', notes: 'Noise cancelling' },
    { id: 'AST-6632', name: 'ThinkPad X1 Carbon', category: 'Laptops', employee: 'Eva Green', status: 'Allocated', location: 'HQ - Room 403', date: '2026-05-01', returnDate: '2027-05-01', sn: 'TPX1C990011Z', value: '$1,699.00', condition: 'Excellent', lastAudit: '2026-06-25', notes: 'Assigned for Product Owner roles' }
  ],
  allocations: [
    { id: 'AR-2091', employee: 'John Doe', asset: 'iPad Air 5th Gen', category: 'Tablets', date: '2026-07-10', status: 'Pending', remarks: '' },
    { id: 'AR-2092', employee: 'Alice Johnson', asset: 'Logitech MX Master 3', category: 'Accessories', date: '2026-07-09', status: 'Approved', remarks: 'Approved for design tasks.' },
    { id: 'AR-2093', employee: 'Bob Smith', asset: 'Standing Desk', category: 'Furniture', date: '2026-07-08', status: 'Pending', remarks: '' },
    { id: 'AR-2094', employee: 'Charlie Brown', asset: 'Samsung Galaxy S23', category: 'Phones', date: '2026-07-07', status: 'Pending', remarks: '' },
    { id: 'AR-2095', employee: 'Eva Green', asset: 'Mac Studio M2 Max', category: 'Desktops', date: '2026-07-06', status: 'Pending', remarks: '' },
    { id: 'AR-2096', employee: 'David Miller', asset: 'Keychron K2 Keyboard', category: 'Accessories', date: '2026-07-05', status: 'Rejected', remarks: 'Out of budget for this quarter.' }
  ],
  transfers: [
    { id: 'TR-8812', asset: 'AST-8291 (Dell XPS 15)', fromEmployee: 'John Doe', toEmployee: 'Alice Johnson', reason: 'Alice needs a testing laptop for local deployment', status: 'Pending', date: '2026-07-11', remarks: '' },
    { id: 'TR-8813', asset: 'AST-1029 (iPhone 14 Pro)', fromEmployee: 'Alice Johnson', toEmployee: 'Bob Smith', reason: 'Bob needs to test iOS specific layouts', status: 'Approved', date: '2026-07-10', remarks: 'Approved. Handover done.' },
    { id: 'TR-8814', asset: 'AST-3810 (iPad Air)', fromEmployee: 'Bob Smith', toEmployee: 'Charlie Brown', reason: 'Charlie needs to create UI design sketches', status: 'Pending', date: '2026-07-09', remarks: '' },
    { id: 'TR-8815', asset: 'AST-5521 (Sony WH-1000XM4)', fromEmployee: 'David Miller', toEmployee: 'Eva Green', reason: 'Eva needs headset for remote presentations', status: 'Pending', date: '2026-07-08', remarks: '' }
  ],
  bookings: [
    { id: 'BK-5011', resource: 'Meeting Room 204', date: '2026-07-14', start: '10:00 AM', end: '11:30 AM', purpose: 'Sprint Planning', department: 'Engineering', status: 'Active', notes: 'Requires projector setup' },
    { id: 'BK-5012', resource: 'Conference Hall B', date: '2026-07-15', start: '02:00 PM', end: '04:00 PM', purpose: 'All-hands Sync', department: 'Engineering', status: 'Active', notes: 'Includes catering for 15' },
    { id: 'BK-5013', resource: 'Projector Max', date: '2026-07-13', start: '09:00 AM', end: '12:00 PM', purpose: 'Architecture Review', department: 'Engineering', status: 'Active', notes: 'Ensure power adapter included' },
    { id: 'BK-5014', resource: 'Corporate Sedan', date: '2026-07-12', start: '01:00 PM', end: '05:00 PM', purpose: 'Client On-site Visit', department: 'Engineering', status: 'Active', notes: 'Driver allocated by admin' },
    { id: 'BK-5015', resource: 'Meeting Room 204', date: '2026-07-10', start: '11:00 AM', end: '12:00 PM', purpose: 'Design Review', department: 'Engineering', status: 'Completed', notes: 'Done' },
    { id: 'BK-5016', resource: 'Projector Max', date: '2026-07-09', start: '03:00 PM', end: '05:00 PM', purpose: 'QA Retro', department: 'Engineering', status: 'Completed', notes: 'Done' }
  ],
  timeline: [
    { id: 'TL-1', text: 'Sarah Connor approved Allocation Request #AR-2092', time: '10 mins ago', type: 'approval' },
    { id: 'TL-2', text: 'Sarah Connor booked Corporate Sedan for client visit', time: '2 hours ago', type: 'booking' },
    { id: 'TL-3', text: 'Asset #AST-1029 (iPhone 14 Pro) assigned to Alice Johnson', time: '1 day ago', type: 'asset' },
    { id: 'TL-4', text: 'Sarah Connor rejected Allocation Request #AR-2096', time: '2 days ago', type: 'rejection' }
  ]
};

// State functions
function getDB() {
  const db = localStorage.getItem('dept_portal_db');
  if (!db) {
    localStorage.setItem('dept_portal_db', JSON.stringify(INITIAL_DATABASE));
    return INITIAL_DATABASE;
  }
  return JSON.parse(db);
}

function saveDB(db) {
  localStorage.setItem('dept_portal_db', JSON.stringify(db));
}

// Toast alerts helper
function showToast(message, type = 'success') {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  let iconClass = 'ri-checkbox-circle-fill';
  if (type === 'danger') {
    iconClass = 'ri-error-warning-fill';
  } else if (type === 'warning') {
    iconClass = 'ri-alert-fill';
  }
  
  toast.innerHTML = `
    <i class="${iconClass}"></i>
    <span>${message}</span>
  `;
  
  container.appendChild(toast);
  
  // Slide animation trigger
  setTimeout(() => {
    toast.style.opacity = '1';
  }, 10);

  // Auto remove
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => {
      toast.remove();
    }, 300);
  }, 3500);
}

// Modal handling
let activeModalOverlay = null;

function openModal(modalId) {
  const overlay = document.getElementById(modalId);
  if (overlay) {
    overlay.classList.add('open');
    activeModalOverlay = overlay;
    document.body.style.overflow = 'hidden'; // Lock background scroll
  }
}

function closeModal(modalId) {
  const overlay = document.getElementById(modalId);
  if (overlay) {
    overlay.classList.remove('open');
    if (activeModalOverlay === overlay) {
      activeModalOverlay = null;
    }
    document.body.style.overflow = ''; // Unlock scroll
  }
}

// Event Listeners for closing modals
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && activeModalOverlay) {
    closeModal(activeModalOverlay.id);
  }
});

document.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal-overlay')) {
    closeModal(e.target.id);
  }
});

// App Engine Context
window.App = {
  getDB,
  saveDB,
  showToast,
  openModal,
  closeModal
};
