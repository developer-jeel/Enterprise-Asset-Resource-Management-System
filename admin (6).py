{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Department Assets — AssetFlow Department Head Portal</title>
  <link href="https://cdn.jsdelivr.net/npm/remixicon@4.2.0/fonts/remixicon.css" rel="stylesheet" />
  <link rel="stylesheet" href="{% static 'css/main.css' %}">
</head>
<body>

  <!-- Toast Container -->
  <div class="toast-container" id="toastContainer"></div>

  <!-- Sidebar -->
  <aside class="sidebar">
    <div class="sidebar-brand">
      <div class="sidebar-logo">AF</div>
      <div class="sidebar-brand-text">
        <span class="sidebar-app-name">AssetFlow</span>
        <span class="sidebar-app-sub">Dept Head</span>
      </div>
    </div>
    <nav class="sidebar-nav">
      <a href="{% url 'dept_head_index' %}" class="nav-link"><i class="ri-dashboard-line"></i> Dashboard</a>
      <a href="{% url 'dept_head_assets' %}" class="nav-link active"><i class="ri-box-3-line"></i> Department Assets</a>
      <a href="{% url 'dept_head_allocations' %}" class="nav-link"><i class="ri-send-plane-line"></i> Allocation Requests</a>
      <a href="{% url 'dept_head_transfers' %}" class="nav-link"><i class="ri-shuffle-line"></i> Transfer Requests</a>
      <a href="{% url 'dept_head_bookings' %}" class="nav-link"><i class="ri-calendar-event-line"></i> Resource Booking</a>
    </nav>
    <div class="sidebar-footer">
      <div class="user-profile">
        <div class="user-avatar">{{ profile.user.username|slice:":2"|upper }}</div>
        <div class="user-info">
          <span class="user-name">{{ profile.user.get_full_name|default:profile.user.username }}</span>
          <span class="user-role">Department Head</span>
        </div>
      </div>
    </div>
  </aside>

  <!-- Main Content -->
  <div class="main-content">
    <header class="top-header">
      <div class="header-left">
        <h1 class="header-title">Department Assets</h1>
      </div>
      <div class="header-right">
        <span class="dept-pill">{{ profile.department|default:"No Department" }}</span>
        <a href="{% url 'logout' %}" class="logout-btn"><i class="ri-logout-box-line"></i> Sign Out</a>
      </div>
    </header>
    
    <main class="page-body animate-slide-right">
      <div class="card">
        <div class="card-header">
          <span class="card-title">Allocated Assets</span>
        </div>
        
        <!-- Filters Bar -->
        <div class="filters-bar">
          <div class="search-wrapper">
            <i class="ri-search-line search-icon"></i>
            <input type="text" id="asset-search" class="search-input" placeholder="Search ID, name, employee...">
          </div>
          <div class="filter-group">
            <label for="category-filter" class="form-label" style="margin-bottom:0; font-weight:500;">Category:</label>
            <select id="category-filter" class="filter-select">
              <option value="All">All Categories</option>
              {% for cat in categories %}
              <option value="{{ cat }}">{{ cat }}</option>
              {% endfor %}
            </select>
          </div>
        </div>

        <!-- Table Container -->
        <div class="table-responsive">
          <table class="table-custom">
            <thead>
              <tr>
                <th>Asset ID</th>
                <th>Asset Name</th>
                <th>Category</th>
                <th>Assigned Employee</th>
                <th>Status</th>
                <th>Location</th>
                <th>Acquired Date</th>
                <th>Warranty</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody id="assets-table-body">
              {% for asset in assets %}
              <tr data-name="{{ asset.name|lower }}" data-id="{{ asset.tag|lower }}" data-employee="{{ asset.assigned_to.username|default:'—'|lower }}" data-category="{{ asset.category }}" data-location="{{ asset.location|lower }}">
                <td><span style="font-weight: 600; color: var(--color-brand);">{{ asset.tag }}</span></td>
                <td style="font-weight: 500;">{{ asset.name }}</td>
                <td>{{ asset.category }}</td>
                <td>{{ asset.assigned_to.username|default:"—" }}</td>
                <td><span class="badge badge-{% if asset.lifecycle == 'In Use' %}approved{% elif asset.lifecycle == 'Repair' %}pending{% else %}rejected{% endif %}">{{ asset.lifecycle }}</span></td>
                <td>{{ asset.location }}</td>
                <td>{{ asset.acquired }}</td>
                <td>{{ asset.warranty|default:"—" }}</td>
                <td>
                  <button class="btn btn-secondary btn-sm"
                    onclick="viewAssetDetails('{{ asset.tag }}', '{{ asset.name }}', '{{ asset.category }}', '{{ asset.serial }}', '{{ asset.cost }}', '{{ asset.condition }}', '{{ asset.assigned_to.username|default:'—' }}', '{{ asset.lifecycle }}', '{{ asset.location }}', '{{ asset.acquired }}', '{{ asset.warranty|default:'—' }}', '{{ asset.notes|default:'' }}')"
                  >
                    <i class="ri-eye-line"></i> View Details
                  </button>
                </td>
              </tr>
              {% empty %}
              <tr><td colspan="9" style="text-align:center; color:var(--color-text-secondary); padding:24px;">No assets found for your department.</td></tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>

  <!-- Detail Modal Popup -->
  <div class="modal-overlay" id="details-modal">
    <div class="modal-container">
      <div class="modal-header">
        <span class="modal-title" id="modal-asset-title">Asset Technical Details</span>
        <button class="modal-close-btn" onclick="closeModal('details-modal')"><i class="ri-close-line"></i></button>
      </div>
      <div class="modal-body">
        <div class="detail-row">
          <span class="detail-label">Asset ID</span>
          <span class="detail-value" id="modal-asset-id" style="font-weight:600; color:var(--color-brand);">—</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Asset Name</span>
          <span class="detail-value" id="modal-asset-name">—</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Category</span>
          <span class="detail-value" id="modal-asset-category">—</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Serial Number</span>
          <span class="detail-value" id="modal-asset-sn">—</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Purchase Value</span>
          <span class="detail-value" id="modal-asset-value">—</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Condition</span>
          <span class="detail-value" id="modal-asset-condition">—</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Assigned Employee</span>
          <span class="detail-value" id="modal-asset-employee">—</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Current Status</span>
          <span class="detail-value"><span class="badge badge-approved" id="modal-asset-status">—</span></span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Location</span>
          <span class="detail-value" id="modal-asset-location">—</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Acquired Date</span>
          <span class="detail-value" id="modal-asset-date">—</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Warranty Expiry</span>
          <span class="detail-value" id="modal-asset-returnDate">—</span>
        </div>
        <div style="margin-top: 16px;">
          <span class="form-label">Administrative Notes</span>
          <p id="modal-asset-notes" style="font-size:13px; color:var(--color-text-secondary); background:var(--bg-primary); padding:10px; border-radius:var(--radius-sm); border:1px solid var(--color-border);"></p>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="closeModal('details-modal')">Close Details</button>
      </div>
    </div>
  </div>

  <script>
    function openModal(id) { document.getElementById(id).classList.add('open'); }
    function closeModal(id) { document.getElementById(id).classList.remove('open'); }

    function showToast(message, type = 'success') {
      let container = document.getElementById('toastContainer');
      const toast = document.createElement('div');
      toast.className = `toast toast-${type === 'error' ? 'danger' : type}`;
      const icons = { success: 'ri-checkbox-circle-fill', danger: 'ri-error-warning-fill', warning: 'ri-alert-fill' };
      toast.innerHTML = `<i class="${icons[type] || icons.success}"></i><span>${message}</span>`;
      container.appendChild(toast);
      setTimeout(() => { toast.style.opacity = '0'; setTimeout(() => toast.remove(), 300); }, 3500);
    }

    function viewAssetDetails(id, name, category, sn, value, condition, employee, status, location, date, warranty, notes) {
      document.getElementById('modal-asset-title').textContent = `Technical Specifications: ${name}`;
      document.getElementById('modal-asset-id').textContent = id;
      document.getElementById('modal-asset-name').textContent = name;
      document.getElementById('modal-asset-category').textContent = category;
      document.getElementById('modal-asset-sn').textContent = sn;
      document.getElementById('modal-asset-value').textContent = '$' + parseFloat(value).toFixed(2);
      document.getElementById('modal-asset-condition').textContent = condition;
      document.getElementById('modal-asset-employee').textContent = employee;
      document.getElementById('modal-asset-status').textContent = status;
      document.getElementById('modal-asset-location').textContent = location;
      document.getElementById('modal-asset-date').textContent = date;
      document.getElementById('modal-asset-returnDate').textContent = warranty;
      document.getElementById('modal-asset-notes').textContent = notes || 'No notes available.';
      openModal('details-modal');
    }

    // Client-side search & filter
    function applySearchAndFilters() {
      const q = document.getElementById('asset-search').value.toLowerCase().trim();
      const cat = document.getElementById('category-filter').value;
      const rows = document.querySelectorAll('#assets-table-body tr[data-name]');

      rows.forEach(row => {
        const matchSearch = !q || row.dataset.name.includes(q) || row.dataset.id.includes(q) || row.dataset.employee.includes(q) || row.dataset.location.includes(q);
        const matchCat = cat === 'All' || row.dataset.category === cat;
        row.style.display = (matchSearch && matchCat) ? '' : 'none';
      });
    }

    document.getElementById('asset-search').addEventListener('input', applySearchAndFilters);
    document.getElementById('category-filter').addEventListener('change', applySearchAndFilters);
  </script>
</body>
</html>
