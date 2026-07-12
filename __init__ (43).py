{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Audit Discrepancy Resolution — AssetFlow Asset Manager</title>
  <meta name="description" content="Review and resolve audit discrepancies identified during asset audits in AssetFlow ERP.">
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
    <a href="{% url 'manager_maintenance' %}" class="nav-link"><i class="ri-tools-line"></i> Maintenance</a>
    <a href="{% url 'manager_discrepancies' %}" class="nav-link active"><i class="ri-error-warning-line"></i> Discrepancies</a>
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
      <h1 class="header-title">Audit Discrepancy Resolution</h1>
    </div>
    <div class="header-right">
      <span class="dept-pill">Asset Manager Portal</span>
      <a href="{% url 'logout' %}" class="logout-btn" style="text-decoration:none; display:inline-block; line-height:30px; text-align:center;">
        <i class="ri-logout-box-line"></i> Sign Out
      </a>
    </div>
  </header>

  <main class="page-body animate-slide-right">

    <!-- KPIs -->
    <div class="kpi-grid" style="grid-template-columns:repeat(4,1fr);margin-bottom:24px;">
      <div class="card card-kpi active-kpi">
        <div class="kpi-header"><span class="kpi-title">Total Discrepancies</span><div class="kpi-icon"><i class="ri-error-warning-line"></i></div></div>
        <span class="kpi-value" id="disc-total">0</span>
      </div>
      <div class="card card-kpi">
        <div class="kpi-header"><span class="kpi-title">Pending Review</span><div class="kpi-icon"><i class="ri-time-line"></i></div></div>
        <span class="kpi-value" id="disc-pending">0</span>
      </div>
      <div class="card card-kpi">
        <div class="kpi-header"><span class="kpi-title">Resolved</span><div class="kpi-icon"><i class="ri-checkbox-circle-line"></i></div></div>
        <span class="kpi-value" id="disc-resolved">0</span>
      </div>
      <div class="card card-kpi">
        <div class="kpi-header"><span class="kpi-title">Missing Assets</span><div class="kpi-icon"><i class="ri-question-mark"></i></div></div>
        <span class="kpi-value" id="disc-missing">0</span>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="card-title">Discrepancy Register</span>
        <span class="badge badge-brand" id="disc-audit-label">AUD-2026-Q3</span>
      </div>

      <!-- Filters -->
      <div class="filters-bar">
        <div class="search-wrapper">
          <i class="ri-search-line search-icon"></i>
          <input type="text" id="disc-search" class="search-input" placeholder="Search asset, discrepancy type…">
        </div>
        <div class="filter-group">
          <select id="disc-type-filter" class="filter-select">
            <option value="All">All Types</option>
            <option>Missing Asset</option>
            <option>Condition Mismatch</option>
            <option>Location Mismatch</option>
            <option>Quantity Mismatch</option>
          </select>
          <select id="disc-severity-filter" class="filter-select">
            <option value="All">All Severities</option>
            <option>Critical</option><option>High</option><option>Medium</option><option>Low</option>
          </select>
          <select id="disc-status-filter" class="filter-select">
            <option value="All">All Statuses</option>
            <option>Pending</option><option>Resolved</option>
          </select>
        </div>
      </div>

      <!-- Table -->
      <div class="table-responsive">
        <table class="table-custom">
          <thead>
            <tr>
              <th>Disc. ID</th>
              <th>Audit Ref</th>
              <th>Asset</th>
              <th>Type</th>
              <th>Severity</th>
              <th>Detected</th>
              <th>Status</th>
              <th style="width:160px;text-align:right;">Actions</th>
            </tr>
          </thead>
          <tbody id="disc-tbody"></tbody>
        </table>
      </div>
    </div>

  </main>
</div>

<!-- RESOLVE DISCREPANCY MODAL -->
<div class="modal-overlay" id="modal-disc-resolve">
  <div class="modal-container" style="max-width:560px;">
    <div class="modal-header">
      <span class="modal-title"><i class="ri-checkbox-circle-line"></i> Resolve Discrepancy</span>
      <button class="modal-close-btn" onclick="App.closeModal('modal-disc-resolve')"><i class="ri-close-line"></i></button>
    </div>
    <div class="modal-body">
      <div class="detail-panel" style="margin-bottom:16px; border:1px solid var(--color-border); padding:10px; border-radius:var(--radius-sm);">
        <div class="detail-panel-title" style="font-weight:700; margin-bottom:8px;">Discrepancy Details</div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Discrepancy ID</span><span class="detail-value" id="dr-id" style="font-weight:600;color:var(--color-brand);"></span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Asset</span><span class="detail-value" id="dr-asset"></span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Type</span><span class="detail-value" id="dr-type"></span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Severity</span><span class="detail-value" id="dr-severity"></span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Detected On</span><span class="detail-value" id="dr-date"></span></div>
        <div style="margin-top:12px;padding:10px 12px;background:var(--bg-surface);border:1px solid var(--color-border);border-radius:var(--radius-sm);">
          <span style="font-size:11px;font-weight:600;color:var(--color-text-muted);display:block;margin-bottom:4px;">Issue Description</span>
          <p style="font-size:13px;color:var(--color-text-secondary);" id="dr-description"></p>
        </div>
      </div>
      <div class="form-group">
        <label class="form-label">Resolution Action *</label>
        <select id="dr-action" class="form-control">
          <option>Update asset record in system</option>
          <option>Physical location corrected</option>
          <option>Condition downgraded in record</option>
          <option>Asset written off — insurance filed</option>
          <option>Asset found — record corrected</option>
          <option>Quantity discrepancy acknowledged</option>
          <option>Other corrective action taken</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Resolution Notes *</label>
        <textarea id="dr-notes" class="form-control" rows="3" placeholder="Provide correction notes, transaction refs or audit remarks…" required></textarea>
      </div>
      <input type="hidden" id="dr-record-id">
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="App.closeModal('modal-disc-resolve')">Cancel</button>
      <button class="btn btn-primary" onclick="confirmResolve()"><i class="ri-checkbox-circle-line"></i> Resolve Discrepancy</button>
    </div>
  </div>
</div>

<!-- VIEW DETAILS MODAL -->
<div class="modal-overlay" id="modal-disc-view">
  <div class="modal-container" style="max-width:540px;">
    <div class="modal-header">
      <span class="modal-title">Discrepancy Details</span>
      <button class="modal-close-btn" onclick="App.closeModal('modal-disc-view')"><i class="ri-close-line"></i></button>
    </div>
    <div class="modal-body" id="disc-view-body"></div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="App.closeModal('modal-disc-view')">Close</button>
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

  let db = { discrepancies: [] };

  function typeBadge(t) {
    const m = { 'Missing Asset':'badge-rejected', 'Condition Mismatch':'badge-pending', 'Location Mismatch':'badge-brand', 'Quantity Mismatch':'badge-info' };
    return `<span class="badge ${m[t]||'badge-brand'}">${t}</span>`;
  }
  function severityDot(s) {
    const m = { Critical:'severity-critical', High:'severity-high', Medium:'severity-medium', Low:'severity-low' };
    return `<span class="severity-indicator ${m[s]||'severity-low'}" style="display:inline-block; width:8px; height:8px; border-radius:50%; margin-right:6px; background:var(--color-${s==='Critical'||s==='High'?'danger':s==='Medium'?'warning':'success'});"></span>${s}`;
  }

  function updateKPIs() {
    document.getElementById('disc-total').textContent = db.discrepancies.length;
    document.getElementById('disc-pending').textContent = db.discrepancies.filter(d=>d.status==='Pending').length;
    document.getElementById('disc-resolved').textContent = db.discrepancies.filter(d=>d.status==='Resolved').length;
    document.getElementById('disc-missing').textContent = db.discrepancies.filter(d=>d.type==='Missing Asset').length;
  }

  function renderTable() {
    const q = document.getElementById('disc-search').value.toLowerCase();
    const tf = document.getElementById('disc-type-filter').value;
    const svf = document.getElementById('disc-severity-filter').value;
    const sf = document.getElementById('disc-status-filter').value;

    const filtered = db.discrepancies.filter(d =>
      (!q || [d.id, d.assetName, d.type].some(f => f.toLowerCase().includes(q))) &&
      (tf === 'All' || d.type === tf) &&
      (svf === 'All' || d.severity === svf) &&
      (sf === 'All' || d.status === sf)
    );

    const tbody = document.getElementById('disc-tbody');
    tbody.innerHTML = filtered.length ? filtered.map(d => `
      <tr>
        <td><span style="font-weight:600;color:var(--color-brand);">${d.id}</span></td>
        <td><span class="badge badge-info">${d.auditId}</span></td>
        <td style="font-weight:500;">${d.assetName}</td>
        <td>${typeBadge(d.type)}</td>
        <td><span style="font-size:13px;">${severityDot(d.severity)}</span></td>
        <td>${d.detectedDate}</td>
        <td><span class="badge badge-${d.status==='Resolved'?'approved':'pending'}">${d.status}</span></td>
        <td style="text-align:right;">
          <div style="display:inline-flex;gap:4px;">
            <button class="btn btn-secondary btn-sm btn-icon" onclick="viewDisc('${d.id}')" title="View Details"><i class="ri-eye-line"></i></button>
            ${d.status==='Pending'?`<button class="btn btn-primary btn-sm" onclick="openResolve('${d.id}')"><i class="ri-checkbox-circle-line"></i> Resolve</button>`
            :`<span style="font-size:12px;color:var(--color-success);font-weight:600;"><i class="ri-checkbox-circle-fill"></i> Resolved</span>`}
          </div>
        </td>
      </tr>
    `).join('') : `<tr><td colspan="8"><div class="empty-state"><i class="ri-error-warning-line empty-state-icon"></i><div class="empty-state-title">No discrepancies found</div><p class="empty-state-desc">Adjust filters or all discrepancies are resolved.</p></div></td></tr>`;
  }

  function openResolve(id) {
    const d = db.discrepancies.find(x => x.id === id);
    if (!d) return;
    document.getElementById('dr-record-id').value = id;
    document.getElementById('dr-id').textContent = id;
    document.getElementById('dr-asset').textContent = d.assetName;
    document.getElementById('dr-type').innerHTML = typeBadge(d.type);
    document.getElementById('dr-severity').innerHTML = severityDot(d.severity);
    document.getElementById('dr-date').textContent = d.detectedDate;
    document.getElementById('dr-description').textContent = d.description;
    document.getElementById('dr-notes').value = '';
    App.openModal('modal-disc-resolve');
  }

  async function confirmResolve() {
    const id = document.getElementById('dr-record-id').value;
    const notes = document.getElementById('dr-notes').value.trim();
    const action = document.getElementById('dr-action').value;
    if (!notes) { App.showToast('Please provide resolution notes.', 'warning'); return; }

    const formData = new FormData();
    formData.append('id', id);
    formData.append('resolution', `${action}. ${notes}`);
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

    try {
      const res = await fetch("{% url 'manager_resolve_discrepancy' %}", { method: 'POST', body: formData });
      const data = await res.json();
      if (data.success) {
        App.closeModal('modal-disc-resolve');
        App.showToast(`Discrepancy ${id} marked as resolved!`, 'success');
        loadData();
      }
    } catch(err) {
      console.error(err);
    }
  }

  function viewDisc(id) {
    const d = db.discrepancies.find(x => x.id === id);
    if (!d) return;
    document.getElementById('disc-view-body').innerHTML = `
      <div class="detail-panel" style="margin-bottom:12px; border:1px solid var(--color-border); padding:10px; border-radius:var(--radius-sm);">
        <div class="detail-panel-title" style="font-weight:700; margin-bottom:8px;">Discrepancy Information</div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Discrepancy ID</span><span class="detail-value" style="font-weight:600;color:var(--color-brand);">${d.id}</span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Audit Cycle</span><span class="detail-value">${d.auditId}</span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Asset Name</span><span class="detail-value">${d.assetName}</span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Asset Tag</span><span class="detail-value">${d.assetId}</span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Type</span><span class="detail-value">${typeBadge(d.type)}</span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Severity</span><span class="detail-value">${severityDot(d.severity)}</span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Detected On</span><span class="detail-value">${d.detectedDate}</span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Current Status</span><span class="detail-value"><span class="badge badge-${d.status==='Resolved'?'approved':'pending'}">${d.status}</span></span></div>
      </div>
      <div class="detail-panel" style="margin-bottom:12px; border:1px solid var(--color-border); padding:10px; border-radius:var(--radius-sm);">
        <div class="detail-panel-title" style="font-weight:700; margin-bottom:8px;">Issue Description</div>
        <p style="font-size:13px;color:var(--color-text-secondary);line-height:1.6;">${d.description}</p>
      </div>
      ${d.resolution ? `
        <div class="detail-panel" style="border:1px solid var(--color-success); padding:10px; border-radius:var(--radius-sm);">
          <div class="detail-panel-title" style="color:var(--color-success); font-weight:700; margin-bottom:8px;">Resolution Details</div>
          <p style="font-size:13px;color:var(--color-text-secondary);line-height:1.6;">${d.resolution}</p>
        </div>
      ` : ''}
    `;
    App.openModal('modal-disc-view');
  }

  ['disc-search','disc-type-filter','disc-severity-filter','disc-status-filter'].forEach(id => {
    const el = document.getElementById(id);
    el.addEventListener('input', renderTable);
    el.addEventListener('change', renderTable);
  });

  async function loadData() {
    try {
      const response = await fetch("{% url 'manager_dashboard_data' %}");
      db = await response.json();
      updateKPIs(); renderTable();
    } catch(err) {
      console.error(err);
    }
  }

  window.addEventListener('DOMContentLoaded', loadData);
</script>
</body>
</html>
