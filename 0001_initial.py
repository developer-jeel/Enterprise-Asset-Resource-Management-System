{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Maintenance Management — AssetFlow Asset Manager</title>
  <meta name="description" content="Review and approve asset maintenance requests in AssetFlow ERP.">
  <link href="https://cdn.jsdelivr.net/npm/remixicon@4.2.0/fonts/remixicon.css" rel="stylesheet"/>
  <link rel="stylesheet" href="{% static 'css/main.css' %}">
  <link rel="stylesheet" href="{% static 'css/asset-manager.css' %}">
</head>
<body>

<aside class="sidebar">
  <div class="sidebar-brand">
    <div class="sidebar-logo">AF</div>
    <div class="sidebar-brand-text">
      <span class="sidebar-app-name">AssetFlow</span>
      <span class="sidebar-app-sub">Asset Manager</span>
    </div>
  </div>
  <nav class="sidebar-nav">
    <a href="{% url 'manager_index' %}" class="nav-link"><i class="ri-dashboard-line"></i> Dashboard</a>
    <a href="{% url 'manager_assets' %}" class="nav-link"><i class="ri-box-3-line"></i> Asset Directory</a>
    <a href="{% url 'manager_transfers' %}" class="nav-link"><i class="ri-shuffle-line"></i> Allocation & Transfer</a>
    <a href="{% url 'manager_maintenance' %}" class="nav-link active"><i class="ri-tools-line"></i> Maintenance</a>
    <a href="{% url 'manager_discrepancies' %}" class="nav-link"><i class="ri-error-warning-line"></i> Discrepancies</a>
    <a href="{% url 'manager_returns' %}" class="nav-link"><i class="ri-arrow-go-back-line"></i> Returns</a>
  </nav>
  <div class="sidebar-footer">
    <div class="user-profile">
      <div class="user-avatar">AM</div>
      <div class="user-info">
        <span class="user-name">{{ request.user.username }}</span>
        <span class="user-role">Asset Manager</span>
      </div>
    </div>
  </div>
</aside>

<div class="main-content">
  <header class="top-header">
    <div class="header-left">
      <h1 class="header-title">Maintenance Management</h1>
    </div>
    <div class="header-right">
      <span class="dept-pill">Asset Manager Portal</span>
      <a href="{% url 'logout' %}" class="logout-btn" style="text-decoration:none; display:inline-block; line-height:30px; text-align:center;">
        <i class="ri-logout-box-line"></i> Sign Out
      </a>
    </div>
  </header>

  <main class="page-body animate-slide-right">

    <!-- KPI summary bar -->
    <div class="kpi-grid" style="grid-template-columns:repeat(4,1fr);margin-bottom:24px;">
      <div class="card card-kpi active-kpi">
        <div class="kpi-header"><span class="kpi-title">Total Requests</span><div class="kpi-icon"><i class="ri-tools-line"></i></div></div>
        <span class="kpi-value" id="mnt-total">0</span>
      </div>
      <div class="card card-kpi">
        <div class="kpi-header"><span class="kpi-title">Pending Approval</span><div class="kpi-icon"><i class="ri-time-line"></i></div></div>
        <span class="kpi-value" id="mnt-pending">0</span>
      </div>
      <div class="card card-kpi">
        <div class="kpi-header"><span class="kpi-title">Approved / In Progress</span><div class="kpi-icon"><i class="ri-hammer-line"></i></div></div>
        <span class="kpi-value" id="mnt-approved">0</span>
      </div>
      <div class="card card-kpi">
        <div class="kpi-header"><span class="kpi-title">Critical Priority</span><div class="kpi-icon"><i class="ri-alarm-warning-line"></i></div></div>
        <span class="kpi-value" id="mnt-critical">0</span>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-bar" style="margin-bottom:24px;">
      <div class="search-wrapper">
        <i class="ri-search-line search-icon"></i>
        <input type="text" id="mnt-search" class="search-input" placeholder="Search asset, reporter, department…">
      </div>
      <div class="filter-group">
        <select id="mnt-priority-filter" class="filter-select">
          <option value="All">All Priorities</option>
          <option>Critical</option><option>High</option><option>Medium</option><option>Low</option>
        </select>
        <select id="mnt-status-filter" class="filter-select">
          <option value="All">All Statuses</option>
          <option>Pending</option><option>Approved</option><option>In Progress</option><option>Resolved</option><option>Rejected</option>
        </select>
      </div>
    </div>

    <!-- Maintenance Cards Grid -->
    <div class="cards-grid" id="maintenance-grid"></div>

  </main>
</div>

<!-- APPROVE MAINTENANCE MODAL -->
<div class="modal-overlay" id="modal-mnt-approve">
  <div class="modal-container" style="max-width:500px;">
    <div class="modal-header" style="background:var(--color-success-light);">
      <span class="modal-title" style="color:var(--color-success);"><i class="ri-checkbox-circle-line"></i> Approve Maintenance</span>
      <button class="modal-close-btn" onclick="App.closeModal('modal-mnt-approve')"><i class="ri-close-line"></i></button>
    </div>
    <div class="modal-body">
      <div class="detail-panel" style="margin-bottom:16px; border:1px solid var(--color-border); padding:10px; border-radius:var(--radius-sm);">
        <div class="detail-panel-title" style="font-weight:700; margin-bottom:8px;">Request Summary</div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Request ID</span><span class="detail-value" id="mnt-app-id" style="font-weight:600;color:var(--color-brand);"></span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Asset</span><span class="detail-value" id="mnt-app-asset"></span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Priority</span><span class="detail-value" id="mnt-app-priority"></span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Reported By</span><span class="detail-value" id="mnt-app-reporter"></span></div>
      </div>
      <div class="form-group">
        <label class="form-label">Assign Technician</label>
        <input id="mnt-technician" class="form-control" placeholder="e.g. Mark Technical, IT Support Team">
      </div>
      <div class="form-group">
        <label class="form-label">Estimated Days</label>
        <input id="mnt-est-days" type="number" min="0" class="form-control" placeholder="e.g. 3">
      </div>
      <div class="form-group">
        <label class="form-label">Approval Remarks</label>
        <textarea id="mnt-app-remarks" class="form-control" rows="3" placeholder="Add additional technician notes…"></textarea>
      </div>
      <input type="hidden" id="mnt-app-record-id">
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="App.closeModal('modal-mnt-approve')">Cancel</button>
      <button class="btn btn-success" onclick="confirmMntApprove()"><i class="ri-checkbox-circle-line"></i> Approve & Assign</button>
    </div>
  </div>
</div>

<!-- REJECT MAINTENANCE MODAL -->
<div class="modal-overlay" id="modal-mnt-reject">
  <div class="modal-container" style="max-width:440px;">
    <div class="modal-header" style="background:var(--color-danger-light);">
      <span class="modal-title" style="color:var(--color-danger);"><i class="ri-close-circle-line"></i> Reject Request</span>
      <button class="modal-close-btn" onclick="App.closeModal('modal-mnt-reject')"><i class="ri-close-line"></i></button>
    </div>
    <div class="modal-body">
      <p style="font-size:14px;margin-bottom:16px;">Reject request <strong id="mnt-rej-id"></strong>?</p>
      <div class="form-group">
        <label class="form-label">Rejection Reason *</label>
        <textarea id="mnt-rej-remarks" class="form-control" rows="3" placeholder="Explain why the maintenance is rejected…" required></textarea>
      </div>
      <input type="hidden" id="mnt-rej-record-id">
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="App.closeModal('modal-mnt-reject')">Cancel</button>
      <button class="btn btn-danger" onclick="confirmMntReject()"><i class="ri-close-circle-line"></i> Confirm Rejection</button>
    </div>
  </div>
</div>

<div class="toast-container" id="toastContainer"></div>

<script>
  const App = {
    showToast(message, type = 'success') {
      let c = document.getElementById('toastContainer');
      if (!c) { c = document.createElement('div'); c.id = 'toastContainer'; c.className = 'toast-container'; document.body.appendChild(c); }
      const t = document.createElement('div');
      t.className = `toast toast-${type === 'error' ? 'danger' : type}`;
      const icons = { success:'ri-checkbox-circle-fill', danger:'ri-error-warning-fill', warning:'ri-alert-fill', info:'ri-information-line' };
      t.innerHTML = `<i class="${icons[type]||icons.success}"></i><span>${message}</span>`;
      c.appendChild(t);
      setTimeout(() => { t.style.opacity = '0'; t.style.transform = 'translateY(10px)'; setTimeout(() => t.remove(), 300); }, 3500);
    },
    openModal(id) { const e = document.getElementById(id); if (e) { e.classList.add('open'); document.body.style.overflow = 'hidden'; } },
    closeModal(id) { const e = document.getElementById(id); if (e) { e.classList.remove('open'); document.body.style.overflow = ''; } }
  };

  let db = { maintenance: [] };
  
  function priorityClass(p) { return p === 'Critical' ? 'priority-critical' : p === 'High' ? 'priority-high' : p === 'Medium' ? 'priority-medium' : 'priority-low'; }
  function priorityBadge(p) { return `<span class="badge badge-${p.toLowerCase()}">${p}</span>`; }

  function updateKPIs() {
    document.getElementById('mnt-total').textContent = db.maintenance.length;
    document.getElementById('mnt-pending').textContent = db.maintenance.filter(m=>m.status==='Pending').length;
    document.getElementById('mnt-approved').textContent = db.maintenance.filter(m=>m.status==='Approved' || m.status === 'In Progress').length;
    document.getElementById('mnt-critical').textContent = db.maintenance.filter(m=>m.priority==='Critical').length;
  }

  function renderCards() {
    const q = document.getElementById('mnt-search').value.toLowerCase();
    const pf = document.getElementById('mnt-priority-filter').value;
    const sf = document.getElementById('mnt-status-filter').value;

    const filtered = db.maintenance.filter(m =>
      (!q || [m.id, m.assetName, m.reportedBy, m.department].some(f => f.toLowerCase().includes(q))) &&
      (pf === 'All' || m.priority === pf) &&
      (sf === 'All' || m.status === sf)
    );

    const grid = document.getElementById('maintenance-grid');
    if (!filtered.length) {
      grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1;"><i class="ri-tools-line empty-state-icon"></i><div class="empty-state-title">No maintenance requests</div><p class="empty-state-desc">No requests match your current filters.</p></div>`;
      return;
    }

    grid.innerHTML = filtered.map(m => `
      <div class="maintenance-card ${priorityClass(m.priority)}" style="border:1px solid var(--color-border); border-radius:var(--radius-md); padding:16px; margin-bottom:16px; background:var(--bg-card); display:flex; flex-direction:column; gap:10px;">
        <div class="maintenance-card-header" style="display:flex; justify-content:space-between; align-items:center;">
          <div>
            <div class="maintenance-asset-name" style="font-weight:700; font-size:14px; color:var(--color-text-primary);">${m.assetName}</div>
            <div style="font-size:11px;color:var(--color-brand);font-weight:600;margin-top:2px;">${m.id}</div>
          </div>
          <div style="display:flex;flex-direction:column;align-items:flex-end;gap:6px;">
            ${priorityBadge(m.priority)}
            <span class="badge badge-${m.status==='Approved'||m.status==='Resolved'?'approved':m.status==='Rejected'?'rejected':'pending'}">${m.status}</span>
          </div>
        </div>
        <div class="maintenance-meta" style="display:flex; flex-wrap:wrap; gap:12px; font-size:11px; color:var(--color-text-muted);">
          <span><i class="ri-user-line"></i> ${m.reportedBy}</span>
          <span><i class="ri-building-line"></i> ${m.department}</span>
          <span><i class="ri-calendar-line"></i> ${m.reportDate}</span>
          <span><i class="ri-time-line"></i> ~${m.estimatedDays} day${m.estimatedDays>1?'s':''}</span>
        </div>
        <div class="maintenance-issue" style="font-size:13px; color:var(--color-text-secondary); line-height:1.4;">${m.issue}</div>
        ${m.technician ? `<div style="font-size:12px;padding:8px 12px;background:var(--color-success-light);border-radius:var(--radius-sm);color:var(--color-success);font-weight:600;"><i class="ri-user-settings-line"></i> Assigned: ${m.technician}</div>` : ''}
        ${m.remarks ? `<div style="font-size:12px;color:var(--color-text-secondary);background:var(--bg-primary);padding:8px 12px;border-radius:var(--radius-sm);border:1px solid var(--color-border);">${m.remarks}</div>` : ''}
        <div class="maintenance-actions" style="display:flex; justify-content:flex-end; gap:8px;">
          ${m.status === 'Pending' ? `
            <button class="btn btn-success btn-sm" onclick="openMntApprove('${m.id}')"><i class="ri-checkbox-circle-line"></i> Approve</button>
            <button class="btn btn-danger btn-sm" onclick="openMntReject('${m.id}')"><i class="ri-close-circle-line"></i> Reject</button>
          ` : m.status === 'Approved' || m.status === 'In Progress' ? `
            <button class="btn btn-primary btn-sm" onclick="resolveMaint('${m.id}')"><i class="ri-check-double-line"></i> Resolve</button>
          ` : m.status === 'Resolved' ? `<span style="font-size:12px;color:var(--color-success);font-weight:600;"><i class="ri-checkbox-circle-fill"></i> Resolved</span>`
          : `<span style="font-size:12px;color:var(--color-danger);font-weight:600;"><i class="ri-close-circle-fill"></i> Request Rejected</span>`}
        </div>
      </div>
    `).join('');
  }

  function openMntApprove(id) {
    const m = db.maintenance.find(x => x.id === id);
    if (!m) return;
    document.getElementById('mnt-app-record-id').value = id;
    document.getElementById('mnt-app-id').textContent = id;
    document.getElementById('mnt-app-asset').textContent = m.assetName;
    document.getElementById('mnt-app-priority').innerHTML = `<span class="badge badge-${m.priority.toLowerCase()}">${m.priority}</span>`;
    document.getElementById('mnt-app-reporter').textContent = m.reportedBy;
    document.getElementById('mnt-technician').value = m.technician || '';
    document.getElementById('mnt-est-days').value = m.estimatedDays || '';
    document.getElementById('mnt-app-remarks').value = '';
    App.openModal('modal-mnt-approve');
  }

  async function confirmMntApprove() {
    const id = document.getElementById('mnt-app-record-id').value;
    const tech = document.getElementById('mnt-technician').value.trim() || 'IT Support';
    const est = document.getElementById('mnt-est-days').value.trim() || '3';
    const remarks = document.getElementById('mnt-app-remarks').value.trim() || 'Approved for repair.';

    const formData = new FormData();
    formData.append('id', id);
    formData.append('action', 'Approved');
    formData.append('technician', tech);
    formData.append('estimated_days', est);
    formData.append('remarks', remarks);
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

    try {
      const res = await fetch("{% url 'manager_handle_maintenance' %}", { method: 'POST', body: formData });
      const data = await res.json();
      if (data.success) {
        App.closeModal('modal-mnt-approve');
        App.showToast(`Maintenance request ${id} approved!`, 'success');
        loadData();
      }
    } catch(err) {
      console.error(err);
    }
  }

  function openMntReject(id) {
    document.getElementById('mnt-rej-record-id').value = id;
    document.getElementById('mnt-rej-id').textContent = id;
    document.getElementById('mnt-rej-remarks').value = '';
    App.openModal('modal-mnt-reject');
  }

  async function confirmMntReject() {
    const id = document.getElementById('mnt-rej-record-id').value;
    const remarks = document.getElementById('mnt-rej-remarks').value.trim();
    if (!remarks) { App.showToast('Please provide a rejection reason.', 'warning'); return; }

    const formData = new FormData();
    formData.append('id', id);
    formData.append('action', 'Rejected');
    formData.append('remarks', remarks);
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

    try {
      const res = await fetch("{% url 'manager_handle_maintenance' %}", { method: 'POST', body: formData });
      const data = await res.json();
      if (data.success) {
        App.closeModal('modal-mnt-reject');
        App.showToast(`Maintenance ${id} rejected.`, 'danger');
        loadData();
      }
    } catch(err) {
      console.error(err);
    }
  }

  async function resolveMaint(id) {
    const formData = new FormData();
    formData.append('id', id);
    formData.append('action', 'Resolved');
    formData.append('remarks', 'Issue fixed and resolved.');
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

    try {
      const res = await fetch("{% url 'manager_handle_maintenance' %}", { method: 'POST', body: formData });
      const data = await res.json();
      if (data.success) {
        App.showToast(`Maintenance request ${id} resolved!`, 'success');
        loadData();
      }
    } catch(err) {
      console.error(err);
    }
  }

  ['mnt-search','mnt-priority-filter','mnt-status-filter'].forEach(id => {
    const el = document.getElementById(id);
    el.addEventListener('input', renderCards);
    el.addEventListener('change', renderCards);
  });

  async function loadData() {
    try {
      const response = await fetch("{% url 'manager_dashboard_data' %}");
      db = await response.json();
      updateKPIs(); renderCards();
    } catch(err) {
      console.error(err);
    }
  }

  window.addEventListener('DOMContentLoaded', loadData);
</script>
</body>
</html>
