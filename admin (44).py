{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Allocation & Transfer — AssetFlow Asset Manager</title>
  <meta name="description" content="Manage asset allocations and transfer requests in AssetFlow ERP.">
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
    <a href="{% url 'manager_transfers' %}" class="nav-link active"><i class="ri-shuffle-line"></i> Allocation & Transfer</a>
    <a href="{% url 'manager_maintenance' %}" class="nav-link"><i class="ri-tools-line"></i> Maintenance</a>
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
      <h1 class="header-title">Asset Allocation & Transfer</h1>
    </div>
    <div class="header-right">
      <span class="dept-pill">Asset Manager Portal</span>
      <a href="{% url 'logout' %}" class="logout-btn" style="text-decoration:none; display:inline-block; line-height:30px; text-align:center;">
        <i class="ri-logout-box-line"></i> Sign Out
      </a>
    </div>
  </header>

  <main class="page-body animate-slide-right">

    <!-- Status Pipeline -->
    <div class="status-pipeline" id="pipeline"></div>

    <!-- Tabs -->
    <div style="display:flex;gap:4px;margin-bottom:24px;border-bottom:1px solid var(--color-border);">
      <button class="btn btn-primary btn-sm tab-btn active-tab" id="tab-alloc" onclick="switchTab('alloc')">
        <i class="ri-send-plane-line"></i> Allocation Requests
      </button>
      <button class="btn btn-secondary btn-sm tab-btn" id="tab-trans" onclick="switchTab('trans')">
        <i class="ri-shuffle-line"></i> Transfer Requests
      </button>
    </div>

    <!-- ALLOCATION TABLE -->
    <div id="panel-alloc" class="card">
      <div class="card-header">
        <span class="card-title">Allocation Requests from Departments</span>
      </div>
      <div class="filters-bar">
        <div class="search-wrapper">
          <i class="ri-search-line search-icon"></i>
          <input type="text" id="alloc-search" class="search-input" placeholder="Search request, asset, employee…">
        </div>
        <div class="filter-group">
          <select id="alloc-status-filter" class="filter-select">
            <option value="All">All Statuses</option>
            <option>Pending</option><option>Approved</option><option>Rejected</option>
          </select>
        </div>
      </div>
      <div class="table-responsive">
        <table class="table-custom">
          <thead>
            <tr>
              <th>Request ID</th><th>Asset</th><th>Requested By</th><th>Department</th>
              <th>Request Date</th><th>Return Date</th><th>Status</th>
              <th style="width:150px;text-align:right;">Actions</th>
            </tr>
          </thead>
          <tbody id="alloc-tbody"></tbody>
        </table>
      </div>
    </div>

    <!-- TRANSFER TABLE -->
    <div id="panel-trans" class="card" style="display:none;">
      <div class="card-header">
        <span class="card-title">Asset Transfer Requests</span>
      </div>
      <div class="filters-bar">
        <div class="search-wrapper">
          <i class="ri-search-line search-icon"></i>
          <input type="text" id="trans-search" class="search-input" placeholder="Search transfer, asset…">
        </div>
        <div class="filter-group">
          <select id="trans-status-filter" class="filter-select">
            <option value="All">All Statuses</option>
            <option>Pending</option><option>Approved</option><option>Rejected</option>
          </select>
        </div>
      </div>
      <div class="table-responsive">
        <table class="table-custom">
          <thead>
            <tr>
              <th>Transfer ID</th><th>Asset</th><th>From</th><th>To</th>
              <th>Request Date</th><th>Reason</th><th>Status</th>
              <th style="width:150px;text-align:right;">Actions</th>
            </tr>
          </thead>
          <tbody id="trans-tbody"></tbody>
        </table>
      </div>
    </div>

  </main>
</div>

<!-- APPROVE MODAL -->
<div class="modal-overlay" id="modal-approve">
  <div class="modal-container" style="max-width:460px;">
    <div class="modal-header" style="background:var(--color-success-light);">
      <span class="modal-title" style="color:var(--color-success);"><i class="ri-checkbox-circle-line"></i> Approve Request</span>
      <button class="modal-close-btn" onclick="App.closeModal('modal-approve')"><i class="ri-close-line"></i></button>
    </div>
    <div class="modal-body">
      <p style="font-size:14px;margin-bottom:16px;">Approve request <strong id="approve-id-display"></strong> for asset <strong id="approve-asset-display"></strong>?</p>
      <div class="form-group">
        <label class="form-label">Approval Remarks (optional)</label>
        <textarea id="approve-remarks" class="form-control" rows="3" placeholder="Add any approval notes…"></textarea>
      </div>
      <input type="hidden" id="approve-record-id">
      <input type="hidden" id="approve-record-type">
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="App.closeModal('modal-approve')">Cancel</button>
      <button class="btn btn-success" onclick="confirmApprove()"><i class="ri-checkbox-circle-line"></i> Confirm Approval</button>
    </div>
  </div>
</div>

<!-- REJECT MODAL -->
<div class="modal-overlay" id="modal-reject">
  <div class="modal-container" style="max-width:460px;">
    <div class="modal-header" style="background:var(--color-danger-light);">
      <span class="modal-title" style="color:var(--color-danger);"><i class="ri-close-circle-line"></i> Reject Request</span>
      <button class="modal-close-btn" onclick="App.closeModal('modal-reject')"><i class="ri-close-line"></i></button>
    </div>
    <div class="modal-body">
      <p style="font-size:14px;margin-bottom:16px;">Reject request <strong id="reject-id-display"></strong>?</p>
      <div class="form-group">
        <label class="form-label">Rejection Reason *</label>
        <textarea id="reject-remarks" class="form-control" rows="3" placeholder="Provide a reason for rejection…" required></textarea>
      </div>
      <input type="hidden" id="reject-record-id">
      <input type="hidden" id="reject-record-type">
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="App.closeModal('modal-reject')">Cancel</button>
      <button class="btn btn-danger" onclick="confirmReject()"><i class="ri-close-circle-line"></i> Confirm Rejection</button>
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

  let db = { allocations: [], transfers: [] };

  function statusBadge(s) {
    const m = { Pending:'pending', Approved:'approved', Rejected:'rejected' };
    return `<span class="badge badge-${m[s]||'brand'}">${s}</span>`;
  }

  function renderPipeline() {
    const allItems = [...db.allocations, ...db.transfers];
    const counts = { Pending: allItems.filter(x=>x.status==='Pending').length, Approved: allItems.filter(x=>x.status==='Approved').length, Rejected: allItems.filter(x=>x.status==='Rejected').length };
    document.getElementById('pipeline').innerHTML = Object.entries(counts).map(([label, count]) => `
      <div class="pipeline-step ${label==='Pending'?'active':''}">
        <span class="step-count">${count}</span>${label}
      </div>
    `).join('');
  }

  function renderAllocations() {
    const q = document.getElementById('alloc-search').value.toLowerCase();
    const sf = document.getElementById('alloc-status-filter').value;
    const rows = db.allocations.filter(a =>
      (!q || [a.id,a.assetName,a.requestedBy,a.department].some(f=>f.toLowerCase().includes(q))) &&
      (sf==='All'||a.status===sf)
    );
    const tbody = document.getElementById('alloc-tbody');
    tbody.innerHTML = rows.length ? rows.map(a => `
      <tr>
        <td><span style="font-weight:600;color:var(--color-brand);">${a.id}</span></td>
        <td style="font-weight:500;">${a.assetName}</td>
        <td>${a.requestedBy}</td>
        <td>${a.department}</td>
        <td>${a.requestDate}</td>
        <td>${a.returnDate}</td>
        <td>${statusBadge(a.status)}</td>
        <td style="text-align:right;">
          ${a.status==='Pending'?`
            <div style="display:inline-flex;gap:4px;">
              <button class="btn btn-success btn-sm" onclick="openApprove('${a.id}','alloc','${a.assetName}')"><i class="ri-check-line"></i></button>
              <button class="btn btn-danger btn-sm" onclick="openReject('${a.id}','alloc')"><i class="ri-close-line"></i></button>
            </div>
          `:a.status==='Approved'?`<span style="font-size:12px;color:var(--color-success);font-weight:600;"><i class="ri-checkbox-circle-fill"></i> Approved</span>`:`<span style="font-size:12px;color:var(--color-danger);font-weight:600;"><i class="ri-close-circle-fill"></i> Rejected</span>`}
        </td>
      </tr>
    `).join('') : `<tr><td colspan="8"><div class="empty-state"><i class="ri-send-plane-line empty-state-icon"></i><div class="empty-state-title">No requests found</div></div></td></tr>`;
  }

  function renderTransfers() {
    const q = document.getElementById('trans-search').value.toLowerCase();
    const sf = document.getElementById('trans-status-filter').value;
    const rows = db.transfers.filter(t =>
      (!q || [t.id,t.assetName,t.from,t.to].some(f=>f.toLowerCase().includes(q))) &&
      (sf==='All'||t.status===sf)
    );
    const tbody = document.getElementById('trans-tbody');
    tbody.innerHTML = rows.length ? rows.map(t => `
      <tr>
        <td><span style="font-weight:600;color:var(--color-brand);">${t.id}</span></td>
        <td style="font-weight:500;">${t.assetName}</td>
        <td style="font-size:12px;">${t.from}</td>
        <td style="font-size:12px;">${t.to}</td>
        <td>${t.requestDate}</td>
        <td style="max-width:200px;font-size:12px;color:var(--color-text-secondary);">${t.reason}</td>
        <td>${statusBadge(t.status)}</td>
        <td style="text-align:right;">
          ${t.status==='Pending'?`
            <div style="display:inline-flex;gap:4px;">
              <button class="btn btn-success btn-sm" onclick="openApprove('${t.id}','trans','${t.assetName}')"><i class="ri-check-line"></i></button>
              <button class="btn btn-danger btn-sm" onclick="openReject('${t.id}','trans')"><i class="ri-close-line"></i></button>
            </div>
          `:t.status==='Approved'?`<span style="font-size:12px;color:var(--color-success);font-weight:600;"><i class="ri-checkbox-circle-fill"></i> Approved</span>`:`<span style="font-size:12px;color:var(--color-danger);font-weight:600;"><i class="ri-close-circle-fill"></i> Rejected</span>`}
        </td>
      </tr>
    `).join('') : `<tr><td colspan="8"><div class="empty-state"><i class="ri-shuffle-line empty-state-icon"></i><div class="empty-state-title">No transfers found</div></div></td></tr>`;
  }

  function openApprove(id, type, assetName) {
    document.getElementById('approve-record-id').value = id;
    document.getElementById('approve-record-type').value = type;
    document.getElementById('approve-id-display').textContent = id;
    document.getElementById('approve-asset-display').textContent = assetName;
    document.getElementById('approve-remarks').value = '';
    App.openModal('modal-approve');
  }

  async function confirmApprove() {
    const id = document.getElementById('approve-record-id').value;
    const type = document.getElementById('approve-record-type').value;
    const remarks = document.getElementById('approve-remarks').value.trim();

    const url = type === 'alloc' ? "{% url 'manager_handle_allocation' %}" : "{% url 'manager_handle_transfer' %}";
    const formData = new FormData();
    formData.append('id', id);
    formData.append('action', 'Approved');
    formData.append('remarks', remarks);
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

    try {
      const res = await fetch(url, { method: 'POST', body: formData });
      const data = await res.json();
      if (data.success) {
        App.closeModal('modal-approve');
        App.showToast(`${id} approved successfully!`, 'success');
        loadData();
      }
    } catch(err) {
      console.error(err);
    }
  }

  function openReject(id, type) {
    document.getElementById('reject-record-id').value = id;
    document.getElementById('reject-record-type').value = type;
    document.getElementById('reject-id-display').textContent = id;
    document.getElementById('reject-remarks').value = '';
    App.openModal('modal-reject');
  }

  async function confirmReject() {
    const id = document.getElementById('reject-record-id').value;
    const type = document.getElementById('reject-record-type').value;
    const remarks = document.getElementById('reject-remarks').value.trim();
    if (!remarks) { App.showToast('Please provide a rejection reason.', 'warning'); return; }

    const url = type === 'alloc' ? "{% url 'manager_handle_allocation' %}" : "{% url 'manager_handle_transfer' %}";
    const formData = new FormData();
    formData.append('id', id);
    formData.append('action', 'Rejected');
    formData.append('remarks', remarks);
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

    try {
      const res = await fetch(url, { method: 'POST', body: formData });
      const data = await res.json();
      if (data.success) {
        App.closeModal('modal-reject');
        App.showToast(`${id} rejected.`, 'danger');
        loadData();
      }
    } catch(err) {
      console.error(err);
    }
  }

  function switchTab(tab) {
    document.getElementById('panel-alloc').style.display = tab === 'alloc' ? '' : 'none';
    document.getElementById('panel-trans').style.display = tab === 'trans' ? '' : 'none';
    document.getElementById('tab-alloc').className = `btn btn-sm tab-btn ${tab==='alloc'?'btn-primary':'btn-secondary'}`;
    document.getElementById('tab-trans').className = `btn btn-sm tab-btn ${tab==='trans'?'btn-primary':'btn-secondary'}`;
  }

  ['alloc-search','alloc-status-filter'].forEach(id => document.getElementById(id).addEventListener('change', renderAllocations));
  document.getElementById('alloc-search').addEventListener('input', renderAllocations);
  ['trans-search','trans-status-filter'].forEach(id => document.getElementById(id).addEventListener('change', renderTransfers));
  document.getElementById('trans-search').addEventListener('input', renderTransfers);

  async function loadData() {
    try {
      const response = await fetch("{% url 'manager_dashboard_data' %}");
      db = await response.json();
      renderPipeline(); renderAllocations(); renderTransfers();
    } catch(err) {
      console.error(err);
    }
  }

  window.addEventListener('DOMContentLoaded', loadData);
</script>
</body>
</html>
