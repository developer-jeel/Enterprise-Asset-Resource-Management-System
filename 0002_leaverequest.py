{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Asset Returns — AssetFlow Asset Manager</title>
  <meta name="description" content="Review and approve asset return requests with condition check-in in AssetFlow ERP.">
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
    <a href="{% url 'manager_discrepancies' %}" class="nav-link"><i class="ri-error-warning-line"></i> Discrepancies</a>
    <a href="{% url 'manager_returns' %}" class="nav-link active"><i class="ri-arrow-go-back-line"></i> Returns</a>
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
      <h1 class="header-title">Asset Return & Condition Check-In</h1>
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
      <div class="card card-kpi">
        <div class="kpi-header"><span class="kpi-title">Total Return Requests</span><div class="kpi-icon"><i class="ri-arrow-go-back-line"></i></div></div>
        <span class="kpi-value" id="ret-total">0</span>
      </div>
      <div class="card card-kpi active-kpi">
        <div class="kpi-header"><span class="kpi-title">Pending Review</span><div class="kpi-icon"><i class="ri-time-line"></i></div></div>
        <span class="kpi-value" id="ret-pending">0</span>
      </div>
      <div class="card card-kpi">
        <div class="kpi-header"><span class="kpi-title">Approved Returns</span><div class="kpi-icon"><i class="ri-checkbox-circle-line"></i></div></div>
        <span class="kpi-value" id="ret-approved">0</span>
      </div>
      <div class="card card-kpi">
        <div class="kpi-header"><span class="kpi-title">Condition Downgraded</span><div class="kpi-icon"><i class="ri-arrow-down-circle-line"></i></div></div>
        <span class="kpi-value" id="ret-degraded">0</span>
      </div>
    </div>

    <!-- Filter Bar -->
    <div class="filters-bar" style="margin-bottom:24px;">
      <div class="search-wrapper">
        <i class="ri-search-line search-icon"></i>
        <input type="text" id="ret-search" class="search-input" placeholder="Search asset, employee, department…">
      </div>
      <div class="filter-group">
        <select id="ret-status-filter" class="filter-select">
          <option value="All">All Statuses</option>
          <option>Pending</option><option>Approved</option><option>Rejected</option>
        </select>
      </div>
    </div>

    <!-- Return Request Cards -->
    <div class="cards-grid" id="returns-grid" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(320px, 1fr)); gap:16px;"></div>

  </main>
</div>

<!-- CONDITION CHECK-IN MODAL (Approve Return) -->
<div class="modal-overlay" id="modal-ret-checkin">
  <div class="modal-container" style="max-width:580px;">
    <div class="modal-header">
      <span class="modal-title"><i class="ri-survey-line"></i> Asset Condition Check-In</span>
      <button class="modal-close-btn" onclick="App.closeModal('modal-ret-checkin')"><i class="ri-close-line"></i></button>
    </div>
    <div class="modal-body" style="max-height:70vh;overflow-y:auto;">
      <div class="detail-panel" style="margin-bottom:16px; border:1px solid var(--color-border); padding:10px; border-radius:var(--radius-sm);">
        <div class="detail-panel-title" style="font-weight:700; margin-bottom:8px;">Return Request Summary</div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Return ID</span><span class="detail-value" id="ci-id" style="font-weight:600;color:var(--color-brand);"></span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Asset Name</span><span class="detail-value" id="ci-asset"></span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Returned By</span><span class="detail-value" id="ci-employee"></span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Department</span><span class="detail-value" id="ci-dept"></span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Expected Return</span><span class="detail-value" id="ci-expected"></span></div>
        <div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label">Actual Return Date</span><span class="detail-value" id="ci-actual"></span></div>
      </div>

      <div class="detail-panel" style="margin-bottom:16px; border:1px solid var(--color-border); padding:10px; border-radius:var(--radius-sm);">
        <div class="detail-panel-title" style="font-weight:700; margin-bottom:8px;">Condition Assessment</div>
        <div class="condition-grid" id="ci-condition-grid" style="display:flex; justify-content:space-between; margin-bottom:8px;">
          <div class="condition-item">
            <div class="condition-label" style="font-size:11px; color:var(--color-text-muted);">Original Condition</div>
            <div class="condition-value" id="ci-cond-original">—</div>
          </div>
          <div class="condition-item">
            <div class="condition-label" style="font-size:11px; color:var(--color-text-muted);">Returned Condition</div>
            <div class="condition-value" id="ci-cond-returned">—</div>
          </div>
        </div>
        <div style="background:var(--bg-primary);border:1px solid var(--color-border);border-radius:var(--radius-sm);padding:10px 12px;">
          <span style="font-size:11px;font-weight:600;color:var(--color-text-muted);display:block;margin-bottom:4px;">Employee's Handover Notes</span>
          <p style="font-size:13px;color:var(--color-text-secondary);" id="ci-employee-notes">—</p>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">Inspector's Verified Condition</label>
        <select id="ci-verified-cond" class="form-control">
          <option>Excellent</option><option>Good</option><option>Fair</option><option>Poor</option>
        </select>
      </div>
      <div class="form-group">
        <label class="form-label">Inspection Notes *</label>
        <textarea id="ci-inspection-notes" class="form-control" rows="3" placeholder="Describe the physical inspection findings…"></textarea>
      </div>
      <input type="hidden" id="ci-record-id">
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="App.closeModal('modal-ret-checkin')">Cancel</button>
      <button class="btn btn-success" onclick="confirmCheckin()"><i class="ri-checkbox-circle-line"></i> Approve & Check In</button>
    </div>
  </div>
</div>

<!-- REJECT RETURN MODAL -->
<div class="modal-overlay" id="modal-ret-reject">
  <div class="modal-container" style="max-width:440px;">
    <div class="modal-header" style="background:var(--color-danger-light);">
      <span class="modal-title" style="color:var(--color-danger);"><i class="ri-close-circle-line"></i> Reject Return Request</span>
      <button class="modal-close-btn" onclick="App.closeModal('modal-ret-reject')"><i class="ri-close-line"></i></button>
    </div>
    <div class="modal-body">
      <p style="font-size:14px;margin-bottom:16px;">Reject return for <strong id="rr-asset"></strong>?</p>
      <div class="form-group">
        <label class="form-label">Rejection Reason *</label>
        <textarea id="rr-reason" class="form-control" rows="3" placeholder="State reason — e.g., asset not found, damaged beyond threshold…"></textarea>
      </div>
      <input type="hidden" id="rr-record-id">
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="App.closeModal('modal-ret-reject')">Cancel</button>
      <button class="btn btn-danger" onclick="confirmRetReject()">Reject Return</button>
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

  let db = { returns: [] };

  function condBadge(c) {
    const m = { Excellent:'approved', Good:'approved', Fair:'pending', Poor:'rejected' };
    return `<span class="badge badge-${m[c]||'brand'}">${c}</span>`;
  }

  function isLate(expected, actual) {
    if (!actual) return false;
    return new Date(actual) > new Date(expected);
  }

  function updateKPIs() {
    document.getElementById('ret-total').textContent = db.returns.length;
    document.getElementById('ret-pending').textContent = db.returns.filter(r=>r.status==='Pending').length;
    document.getElementById('ret-approved').textContent = db.returns.filter(r=>r.status==='Approved').length;
    document.getElementById('ret-degraded').textContent = db.returns.filter(r => {
      const condOrder = { Excellent:4, Good:3, Fair:2, Poor:1 };
      return (condOrder[r.conditionAtReturn] || 0) < (condOrder[r.conditionOriginal] || 0);
    }).length;
  }

  function renderCards() {
    const q = document.getElementById('ret-search').value.toLowerCase();
    const sf = document.getElementById('ret-status-filter').value;

    const filtered = db.returns.filter(r =>
      (!q || [r.id, r.assetName, r.employee, r.department].some(f => f.toLowerCase().includes(q))) &&
      (sf === 'All' || r.status === sf)
    );

    const grid = document.getElementById('returns-grid');
    if (!filtered.length) {
      grid.innerHTML = `<div class="empty-state" style="grid-column:1/-1;"><i class="ri-arrow-go-back-line empty-state-icon"></i><div class="empty-state-title">No return requests</div><p class="empty-state-desc">No asset returns match your current filters.</p></div>`;
      return;
    }

    const condOrder = { Excellent:4, Good:3, Fair:2, Poor:1 };
    grid.innerHTML = filtered.map(r => {
      const degraded = (condOrder[r.conditionAtReturn]||0) < (condOrder[r.conditionOriginal]||0);
      const late = isLate(r.expectedReturn, r.actualReturn);
      return `
        <div class="return-card" style="border:1px solid var(--color-border); border-radius:var(--radius-md); padding:16px; background:var(--bg-card); display:flex; flex-direction:column; gap:10px;">
          <div class="return-card-header" style="display:flex; justify-content:space-between; align-items:center;">
            <div>
              <div style="font-weight:700;font-size:14px;color:var(--color-text-primary);">${r.assetName}</div>
              <div style="font-size:11px;color:var(--color-brand);font-weight:600;margin-top:2px;">${r.id}</div>
            </div>
            <span class="badge badge-${r.status==='Approved'?'approved':r.status==='Rejected'?'rejected':'pending'}">${r.status}</span>
          </div>
          <div class="return-card-body" style="display:flex; flex-direction:column; gap:10px;">
            <div class="condition-grid" style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:12px;">
              <div class="condition-item">
                <div class="condition-label" style="font-size:10px; color:var(--color-text-muted);">Employee</div>
                <div class="condition-value">${r.employee}</div>
              </div>
              <div class="condition-item">
                <div class="condition-label" style="font-size:10px; color:var(--color-text-muted);">Department</div>
                <div class="condition-value">${r.department}</div>
              </div>
              <div class="condition-item">
                <div class="condition-label" style="font-size:10px; color:var(--color-text-muted);">Expected Return</div>
                <div class="condition-value">${r.expectedReturn}</div>
              </div>
              <div class="condition-item">
                <div class="condition-label" style="font-size:10px; color:var(--color-text-muted);">Actual Return</div>
                <div class="condition-value" style="${late?'color:var(--color-danger);':''}">${r.actualReturn || '—'} ${late?'<span style="font-size:10px;">(LATE)</span>':''}</div>
              </div>
            </div>

            <!-- Condition comparison -->
            <div style="display:flex;align-items:center;justify-content:space-around;gap:12px;margin-bottom:14px;padding:10px 12px;background:var(--bg-primary);border-radius:var(--radius-sm);border:1px solid var(--color-border);">
              <div style="text-align:center;">
                <div style="font-size:10px;font-weight:600;color:var(--color-text-muted);margin-bottom:4px;">ORIGINAL</div>
                ${condBadge(r.conditionOriginal || 'Good')}
              </div>
              <i class="ri-arrow-right-line" style="color:var(--color-text-muted);"></i>
              <div style="text-align:center;">
                <div style="font-size:10px;font-weight:600;color:var(--color-text-muted);margin-bottom:4px;">RETURNED</div>
                ${condBadge(r.conditionAtReturn || 'Good')}
              </div>
              ${degraded?`<span class="badge badge-high" style="margin-left:4px;">Degraded</span>`:''}
            </div>

            ${r.notes?`<div style="font-size:12px;color:var(--color-text-secondary);padding:8px 12px;background:var(--bg-surface);border:1px solid var(--color-border);border-radius:var(--radius-sm);margin-bottom:14px;">${r.notes}</div>`:''}

            <div style="display:flex;gap:8px;justify-content:flex-end;">
              ${r.status==='Pending'?`
                <button class="btn btn-primary btn-sm" onclick="openCheckin('${r.id}')"><i class="ri-survey-line"></i> Inspect & Approve</button>
                <button class="btn btn-danger btn-sm" onclick="openRetReject('${r.id}')"><i class="ri-close-line"></i> Reject</button>
              `:r.status==='Approved'?`<span style="font-size:12px;color:var(--color-success);font-weight:600;"><i class="ri-checkbox-circle-fill"></i> Return Approved & Checked In</span>`
              :`<span style="font-size:12px;color:var(--color-danger);font-weight:600;"><i class="ri-close-circle-fill"></i> Return Rejected</span>`}
            </div>
          </div>
        </div>
      `;
    }).join('');
  }

  function openCheckin(id) {
    const r = db.returns.find(x => x.id === id);
    if (!r) return;
    document.getElementById('ci-record-id').value = id;
    document.getElementById('ci-id').textContent = id;
    document.getElementById('ci-asset').textContent = r.assetName;
    document.getElementById('ci-employee').textContent = r.employee;
    document.getElementById('ci-dept').textContent = r.department;
    document.getElementById('ci-expected').textContent = r.expectedReturn;
    document.getElementById('ci-actual').textContent = r.actualReturn || 'Just Now';
    document.getElementById('ci-cond-original').innerHTML = condBadge(r.conditionOriginal || 'Good');
    document.getElementById('ci-cond-returned').innerHTML = condBadge(r.conditionAtReturn || 'Good');
    document.getElementById('ci-employee-notes').textContent = r.notes || 'No notes provided.';
    document.getElementById('ci-verified-cond').value = r.conditionAtReturn || 'Good';
    document.getElementById('ci-inspection-notes').value = '';
    App.openModal('modal-ret-checkin');
  }

  async function confirmCheckin() {
    const id = document.getElementById('ci-record-id').value;
    const notes = document.getElementById('ci-inspection-notes').value.trim();
    if (!notes) { App.showToast('Please add inspection notes before approving.', 'warning'); return; }

    const formData = new FormData();
    formData.append('id', id);
    formData.append('action', 'Approved');
    formData.append('notes', notes);
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

    try {
      const res = await fetch("{% url 'manager_handle_return' %}", { method: 'POST', body: formData });
      const data = await res.json();
      if (data.success) {
        App.closeModal('modal-ret-checkin');
        App.showToast(`Asset return ${id} approved and checked in!`, 'success');
        loadData();
      }
    } catch(err) {
      console.error(err);
    }
  }

  function openRetReject(id) {
    const r = db.returns.find(x => x.id === id);
    document.getElementById('rr-record-id').value = id;
    document.getElementById('rr-asset').textContent = r ? r.assetName : id;
    document.getElementById('rr-reason').value = '';
    App.openModal('modal-ret-reject');
  }

  async function confirmRetReject() {
    const id = document.getElementById('rr-record-id').value;
    const reason = document.getElementById('rr-reason').value.trim();
    if (!reason) { App.showToast('Please provide a rejection reason.', 'warning'); return; }

    const formData = new FormData();
    formData.append('id', id);
    formData.append('action', 'Rejected');
    formData.append('notes', reason);
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

    try {
      const res = await fetch("{% url 'manager_handle_return' %}", { method: 'POST', body: formData });
      const data = await res.json();
      if (data.success) {
        App.closeModal('modal-ret-reject');
        App.showToast(`Return ${id} rejected.`, 'danger');
        loadData();
      }
    } catch(err) {
      console.error(err);
    }
  }

  ['ret-search','ret-status-filter'].forEach(id => {
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
