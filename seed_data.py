{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Asset Directory — AssetFlow Asset Manager</title>
  <meta name="description" content="Register and manage all organizational assets in the AssetFlow ERP asset directory.">
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
    <a href="{% url 'manager_assets' %}" class="nav-link active"><i class="ri-box-3-line"></i> Asset Directory</a>
    <a href="{% url 'manager_transfers' %}" class="nav-link"><i class="ri-shuffle-line"></i> Allocation & Transfer</a>
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
      <h1 class="header-title">Asset Registration & Directory</h1>
    </div>
    <div class="header-right">
      <span class="dept-pill">Asset Manager Portal</span>
      <a href="{% url 'logout' %}" class="logout-btn" style="text-decoration:none; display:inline-block; line-height:30px; text-align:center;">
        <i class="ri-logout-box-line"></i> Sign Out
      </a>
    </div>
  </header>

  <main class="page-body animate-slide-right">
    <div class="card">
      <div class="card-header">
        <span class="card-title">Organizational Asset Register</span>
        <button class="btn btn-primary" id="btn-add-asset"><i class="ri-add-line"></i> Register Asset</button>
      </div>

      <!-- Filters -->
      <div class="filters-bar">
        <div class="search-wrapper">
          <i class="ri-search-line search-icon"></i>
          <input type="text" id="asset-search" class="search-input" placeholder="Search tag, name, serial, employee…">
        </div>
        <div class="filter-group">
          <select id="cat-filter" class="filter-select">
            <option value="All">All Categories</option>
            <option>Laptops</option><option>Phones</option><option>Monitors</option>
            <option>Tablets</option><option>Furniture</option><option>Accessories</option>
          </select>
          <select id="life-filter" class="filter-select">
            <option value="All">All Statuses</option>
            <option>In Use</option><option>Storage</option><option>Repair</option><option>Retired</option>
          </select>
        </div>
      </div>

      <!-- Table -->
      <div class="table-responsive">
        <table class="table-custom">
          <thead>
            <tr>
              <th>Asset Tag</th>
              <th>Asset Name</th>
              <th>Category</th>
              <th>Serial No.</th>
              <th>Condition</th>
              <th>Status</th>
              <th>Dept</th>
              <th>Employee</th>
              <th style="width:160px;text-align:right;">Actions</th>
            </tr>
          </thead>
          <tbody id="assets-tbody"></tbody>
        </table>
      </div>
      <div style="margin-top:16px;display:flex;justify-content:space-between;align-items:center;font-size:13px;color:var(--color-text-secondary);">
        <span id="table-info">—</span>
        <div id="table-pagination" style="display:flex;gap:6px;"></div>
      </div>
    </div>
  </main>
</div>

<!-- ═══ REGISTER / EDIT ASSET MODAL ═══ -->
<div class="modal-overlay" id="modal-asset-form">
  <div class="modal-container" style="max-width:640px;">
    <div class="modal-header">
      <span class="modal-title" id="asset-form-title">Register New Asset</span>
      <button class="modal-close-btn" onclick="App.closeModal('modal-asset-form')"><i class="ri-close-line"></i></button>
    </div>
    <form id="asset-form" onsubmit="handleSaveAsset(event)">
      <input type="hidden" id="edit-asset-id">
      <div class="modal-body" style="max-height:70vh;overflow-y:auto;">
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Asset Tag / ID *</label>
            <input id="f-id" class="form-control" placeholder="e.g. AST-0109" required>
          </div>
          <div class="form-group">
            <label class="form-label">Asset Name *</label>
            <input id="f-name" class="form-control" placeholder="e.g. Dell Latitude 5540" required>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Category *</label>
            <select id="f-cat" class="form-control">
              <option>Laptops</option><option>Phones</option><option>Monitors</option>
              <option>Tablets</option><option>Furniture</option><option>Accessories</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Serial Number *</label>
            <input id="f-serial" class="form-control" placeholder="e.g. SN20240101X" required>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Condition</label>
            <select id="f-cond" class="form-control">
              <option>Excellent</option><option>Good</option><option>Fair</option><option>Poor</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Lifecycle Status</label>
            <select id="f-life" class="form-control">
              <option>In Use</option><option>Storage</option><option>Repair</option><option>Retired</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Assigned Department</label>
            <input id="f-dept" class="form-control" placeholder="e.g. Engineering">
          </div>
          <div class="form-group">
            <label class="form-label">Assigned Employee</label>
            <input id="f-emp" class="form-control" placeholder="e.g. John Doe or —">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Location</label>
            <input id="f-loc" class="form-control" placeholder="e.g. HQ-402">
          </div>
          <div class="form-group">
            <label class="form-label">Acquisition Date *</label>
            <input id="f-date" type="date" class="form-control" required>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Purchase Cost ($)</label>
            <input id="f-cost" type="number" min="0" class="form-control" placeholder="e.g. 1299">
          </div>
          <div class="form-group">
            <label class="form-label">Warranty Expiry</label>
            <input id="f-warranty" type="date" class="form-control">
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">Vendor / Supplier</label>
          <input id="f-vendor" class="form-control" placeholder="e.g. Dell Inc.">
        </div>
        <div class="form-group">
          <label class="form-label">Notes</label>
          <textarea id="f-notes" class="form-control" rows="2" placeholder="Any additional remarks…"></textarea>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" onclick="App.closeModal('modal-asset-form')">Cancel</button>
        <button type="submit" class="btn btn-primary" id="asset-form-submit-btn">Register Asset</button>
      </div>
    </form>
  </div>
</div>

<!-- ═══ VIEW ASSET DETAILS MODAL ═══ -->
<div class="modal-overlay" id="modal-asset-view">
  <div class="modal-container" style="max-width:620px;">
    <div class="modal-header">
      <span class="modal-title" id="view-modal-title">Asset Details</span>
      <button class="modal-close-btn" onclick="App.closeModal('modal-asset-view')"><i class="ri-close-line"></i></button>
    </div>
    <div class="modal-body" style="max-height:75vh;overflow-y:auto;" id="view-modal-body"></div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="App.closeModal('modal-asset-view')">Close</button>
    </div>
  </div>
</div>

<!-- ═══ DELETE CONFIRM MODAL ═══ -->
<div class="modal-overlay" id="modal-del-asset">
  <div class="modal-container" style="max-width:400px;">
    <div class="modal-header" style="background:var(--color-danger-light);">
      <span class="modal-title" style="color:var(--color-danger);"><i class="ri-delete-bin-line"></i> Retire Asset</span>
      <button class="modal-close-btn" onclick="App.closeModal('modal-del-asset')"><i class="ri-close-line"></i></button>
    </div>
    <div class="modal-body">
      <p style="font-size:14px;margin-bottom:10px;">Are you sure you want to mark <strong id="del-asset-name"></strong> as <em>Retired</em>?</p>
      <p style="font-size:12px;color:var(--color-text-secondary);">This changes the lifecycle status to Retired. The asset record is preserved.</p>
      <input type="hidden" id="del-asset-id">
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="App.closeModal('modal-del-asset')">Cancel</button>
      <button class="btn btn-danger" onclick="confirmRetire()">Retire Asset</button>
    </div>
  </div>
</div>

<div class="toast-container" id="toastContainer"></div>

<script>
  // Shared Toast & Modal shims
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

  let allAssets = [], currentPage = 1, perPage = 7;

  function condBadge(c) {
    const m = { Excellent:'approved', Good:'approved', Fair:'pending', Poor:'rejected' };
    return `<span class="badge badge-${m[c]||'brand'}">${c}</span>`;
  }
  function lifeBadge(l) {
    const m = { 'In Use':'in-use', Storage:'storage', Repair:'repair', Retired:'retired' };
    return `<span class="badge badge-${m[l]||'brand'}">${l}</span>`;
  }

  function getFiltered() {
    const q = document.getElementById('asset-search').value.toLowerCase();
    const cat = document.getElementById('cat-filter').value;
    const life = document.getElementById('life-filter').value;
    return allAssets.filter(a =>
      (!q || [a.id, a.name, a.serial, a.employee, a.department].some(f => f.toLowerCase().includes(q))) &&
      (cat === 'All' || a.category === cat) &&
      (life === 'All' || a.lifecycle === life)
    );
  }

  function renderTable() {
    const filtered = getFiltered();
    const total = filtered.length;
    const pages = Math.ceil(total / perPage) || 1;
    if (currentPage > pages) currentPage = pages;
    const start = (currentPage - 1) * perPage;
    const slice = filtered.slice(start, start + perPage);

    const tbody = document.getElementById('assets-tbody');
    if (!slice.length) {
      tbody.innerHTML = `<tr><td colspan="9"><div class="empty-state"><i class="ri-box-3-line empty-state-icon"></i><div class="empty-state-title">No assets found</div><p class="empty-state-desc">Adjust filters or register a new asset.</p></div></td></tr>`;
    } else {
      tbody.innerHTML = slice.map(a => `
        <tr>
          <td><span style="font-weight:600;color:var(--color-brand);">${a.id}</span></td>
          <td style="font-weight:500;">${a.name}</td>
          <td>${a.category}</td>
          <td style="font-family:monospace;font-size:12px;">${a.serial}</td>
          <td>${condBadge(a.condition)}</td>
          <td>${lifeBadge(a.lifecycle)}</td>
          <td>${a.department}</td>
          <td>${a.employee}</td>
          <td style="text-align:right;">
            <div style="display:inline-flex;gap:4px;">
              <button class="btn btn-secondary btn-sm btn-icon" onclick="viewAsset('${a.id}')" title="View Details"><i class="ri-eye-line"></i></button>
              <button class="btn btn-secondary btn-sm btn-icon" onclick="editAsset('${a.id}')" title="Edit Asset"><i class="ri-pencil-line"></i></button>
              <button class="btn btn-secondary btn-sm btn-icon" onclick="openRetire('${a.id}')" style="color:var(--color-danger);" title="Retire Asset"><i class="ri-delete-bin-line"></i></button>
            </div>
          </td>
        </tr>
      `).join('');
    }

    document.getElementById('table-info').textContent = total ? `Showing ${start+1}–${Math.min(start+perPage,total)} of ${total} assets` : 'No matching assets';
    let pg = '';
    for (let i = 1; i <= pages; i++) pg += `<button class="btn btn-sm ${i===currentPage?'btn-primary':'btn-secondary'}" onclick="changePg(${i})">${i}</button>`;
    document.getElementById('table-pagination').innerHTML = pg;
  }

  function changePg(p) { currentPage = p; renderTable(); }

  function viewAsset(id) {
    const a = allAssets.find(x => x.id === id);
    if (!a) return;
    document.getElementById('view-modal-title').textContent = `${a.name} — ${a.id}`;
    document.getElementById('view-modal-body').innerHTML = `
      <div style="display:flex;gap:16px;align-items:flex-start;margin-bottom:20px;">
        <div class="asset-image-box" style="width:64px; height:64px; background:var(--color-brand-light); color:var(--color-brand); display:flex; align-items:center; justify-content:center; font-size:28px; border-radius:var(--radius-md);"><i class="ri-box-3-line"></i></div>
        <div>
          <h3 style="font-size:16px;font-weight:700;margin-bottom:4px;">${a.name}</h3>
          <p style="font-size:12px;color:var(--color-text-secondary);">${a.category} · ${a.vendor}</p>
          <div style="display:flex;gap:8px;margin-top:8px;">${condBadge(a.condition)} ${lifeBadge(a.lifecycle)}</div>
        </div>
      </div>
      <div class="detail-panel" style="margin-bottom:12px; border:1px solid var(--color-border); padding:12px; border-radius:var(--radius-md);">
        <div class="detail-panel-title" style="font-weight:700; margin-bottom:8px;">Technical Specifications</div>
        ${[['Asset Tag',a.id],['Serial Number',a.serial],['Category',a.category],['Condition',a.condition],['Lifecycle Status',a.lifecycle]].map(([l,v])=>`<div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label" style="color:var(--color-text-muted);">${l}</span><span class="detail-value">${v}</span></div>`).join('')}
      </div>
      <div class="detail-panel" style="margin-bottom:12px; border:1px solid var(--color-border); padding:12px; border-radius:var(--radius-md);">
        <div class="detail-panel-title" style="font-weight:700; margin-bottom:8px;">Assignment & Location</div>
        ${[['Department',a.department],['Assigned Employee',a.employee],['Location',a.location]].map(([l,v])=>`<div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label" style="color:var(--color-text-muted);">${l}</span><span class="detail-value">${v}</span></div>`).join('')}
      </div>
      <div class="detail-panel" style="margin-bottom:12px; border:1px solid var(--color-border); padding:12px; border-radius:var(--radius-md);">
        <div class="detail-panel-title" style="font-weight:700; margin-bottom:8px;">Acquisition Details</div>
        ${[['Acquisition Date',a.acquired],['Purchase Cost','$'+a.cost.toLocaleString()],['Warranty Expiry',a.warranty],['Vendor',a.vendor]].map(([l,v])=>`<div class="detail-row" style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:4px;"><span class="detail-label" style="color:var(--color-text-muted);">${l}</span><span class="detail-value">${v}</span></div>`).join('')}
      </div>
      ${a.notes ? `<div class="detail-panel" style="border:1px solid var(--color-border); padding:12px; border-radius:var(--radius-md);"><div class="detail-panel-title" style="font-weight:700; margin-bottom:6px;">Notes</div><p style="font-size:13px;color:var(--color-text-secondary);">${a.notes}</p></div>` : ''}
    `;
    App.openModal('modal-asset-view');
  }

  function editAsset(id) {
    const a = allAssets.find(x => x.id === id);
    if (!a) return;
    document.getElementById('asset-form-title').textContent = 'Edit Asset Details';
    document.getElementById('asset-form-submit-btn').textContent = 'Save Changes';
    document.getElementById('edit-asset-id').value = a.id;
    document.getElementById('f-id').value = a.id;
    document.getElementById('f-id').disabled = true;
    document.getElementById('f-name').value = a.name;
    document.getElementById('f-cat').value = a.category;
    document.getElementById('f-serial').value = a.serial;
    document.getElementById('f-cond').value = a.condition;
    document.getElementById('f-life').value = a.lifecycle;
    document.getElementById('f-dept').value = a.department;
    document.getElementById('f-emp').value = a.employee;
    document.getElementById('f-loc').value = a.location;
    document.getElementById('f-date').value = a.acquired;
    document.getElementById('f-cost').value = a.cost;
    document.getElementById('f-warranty').value = a.warranty;
    document.getElementById('f-vendor').value = a.vendor;
    document.getElementById('f-notes').value = a.notes;
    App.openModal('modal-asset-form');
  }

  function openRetire(id) {
    const a = allAssets.find(x => x.id === id);
    if (!a) return;
    document.getElementById('del-asset-id').value = a.id;
    document.getElementById('del-asset-name').textContent = a.name;
    App.openModal('modal-del-asset');
  }

  async function confirmRetire() {
    const id = document.getElementById('del-asset-id').value;
    const formData = new FormData();
    formData.append('tag', id);
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

    try {
      const res = await fetch("{% url 'manager_retire_asset' %}", { method: 'POST', body: formData });
      const data = await res.json();
      if (data.success) {
        App.closeModal('modal-del-asset');
        App.showToast(`Asset retired successfully!`, 'warning');
        loadData();
      }
    } catch(err) {
      console.error(err);
    }
  }

  document.getElementById('btn-add-asset').onclick = () => {
    document.getElementById('asset-form').reset();
    document.getElementById('edit-asset-id').value = '';
    document.getElementById('f-id').disabled = false;
    document.getElementById('asset-form-title').textContent = 'Register New Asset';
    document.getElementById('asset-form-submit-btn').textContent = 'Register Asset';
    App.openModal('modal-asset-form');
  };

  async function handleSaveAsset(e) {
    e.preventDefault();
    const editId = document.getElementById('edit-asset-id').value;
    const formData = new FormData();
    formData.append('edit_id', editId);
    formData.append('tag', document.getElementById('f-id').value);
    formData.append('name', document.getElementById('f-name').value);
    formData.append('category', document.getElementById('f-cat').value);
    formData.append('serial', document.getElementById('f-serial').value);
    formData.append('condition', document.getElementById('f-cond').value);
    formData.append('lifecycle', document.getElementById('f-life').value);
    formData.append('department', document.getElementById('f-dept').value);
    formData.append('employee', document.getElementById('f-emp').value);
    formData.append('location', document.getElementById('f-loc').value);
    formData.append('acquired', document.getElementById('f-date').value);
    formData.append('cost', document.getElementById('f-cost').value);
    formData.append('warranty', document.getElementById('f-warranty').value);
    formData.append('vendor', document.getElementById('f-vendor').value);
    formData.append('notes', document.getElementById('f-notes').value);
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

    try {
      const res = await fetch("{% url 'manager_save_asset' %}", { method: 'POST', body: formData });
      const data = await res.json();
      if (data.success) {
        App.closeModal('modal-asset-form');
        App.showToast(data.message, 'success');
        loadData();
      } else {
        App.showToast(data.message, 'danger');
      }
    } catch(err) {
      console.error(err);
    }
  }

  ['asset-search','cat-filter','life-filter'].forEach(id => {
    document.getElementById(id).addEventListener('input', () => { currentPage = 1; renderTable(); });
    document.getElementById(id).addEventListener('change', () => { currentPage = 1; renderTable(); });
  });

  async function loadData() {
    try {
      const response = await fetch("{% url 'manager_dashboard_data' %}");
      const db = await response.json();
      allAssets = db.assets;
      renderTable();
    } catch(err) {
      console.error(err);
    }
  }

  window.addEventListener('DOMContentLoaded', loadData);
</script>
</body>
</html>
