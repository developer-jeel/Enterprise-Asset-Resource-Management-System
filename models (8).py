{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Allocation Requests — AssetFlow Department Head Portal</title>
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
      <a href="{% url 'dept_head_assets' %}" class="nav-link"><i class="ri-box-3-line"></i> Department Assets</a>
      <a href="{% url 'dept_head_allocations' %}" class="nav-link active"><i class="ri-send-plane-line"></i> Allocation Requests</a>
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
        <h1 class="header-title">Allocation Requests</h1>
      </div>
      <div class="header-right">
        <span class="dept-pill">{{ profile.department|default:"No Department" }}</span>
        <a href="{% url 'logout' %}" class="logout-btn"><i class="ri-logout-box-line"></i> Sign Out</a>
      </div>
    </header>
    
    <main class="page-body animate-slide-right">
      <div class="card">
        <div class="card-header">
          <span class="card-title">Employee Asset Requests</span>
        </div>

        <div class="table-responsive">
          <table class="table-custom">
            <thead>
              <tr>
                <th>Request ID</th>
                <th>Employee</th>
                <th>Requested Asset</th>
                <th>Category</th>
                <th>Request Date</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody id="allocations-table-body">
              {% for alloc in allocations %}
              <tr id="row-{{ alloc.allocation_id }}">
                <td><span style="font-weight: 600; color: var(--color-brand);">{{ alloc.allocation_id }}</span></td>
                <td style="font-weight: 500;">{{ alloc.requested_by.username }}</td>
                <td>{{ alloc.asset_name|default:alloc.asset.name|default:"—" }}</td>
                <td>{{ alloc.category|default:alloc.asset.category|default:"—" }}</td>
                <td>{{ alloc.request_date }}</td>
                <td><span class="badge badge-{{ alloc.status|lower }}" id="badge-{{ alloc.allocation_id }}">{{ alloc.status }}</span></td>
                <td>
                  {% if alloc.status == 'Pending' %}
                  <div style="display:flex; gap: 8px;">
                    <button class="btn btn-success btn-sm" onclick="promptAction('{{ alloc.allocation_id }}', 'Approved', '{{ alloc.requested_by.username }}', '{{ alloc.asset_name|default:alloc.asset.name|default:"Asset" }}')">
                      <i class="ri-check-line"></i> Approve
                    </button>
                    <button class="btn btn-danger btn-sm" onclick="promptAction('{{ alloc.allocation_id }}', 'Rejected', '{{ alloc.requested_by.username }}', '{{ alloc.asset_name|default:alloc.asset.name|default:"Asset" }}')">
                      <i class="ri-close-line"></i> Reject
                    </button>
                  </div>
                  {% else %}
                  <span style="font-size:12px; color:var(--color-text-muted); font-style:italic;">No actions pending</span>
                  {% endif %}
                </td>
              </tr>
              {% empty %}
              <tr><td colspan="7" style="text-align:center; color:var(--color-text-secondary); padding:24px;">No requests found.</td></tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>

  <!-- Confirmation Modal -->
  <div class="modal-overlay" id="confirm-modal">
    <div class="modal-container">
      <div class="modal-header">
        <span class="modal-title" id="confirm-modal-title">Confirm Allocation Action</span>
        <button class="modal-close-btn" onclick="closeModal('confirm-modal')"><i class="ri-close-line"></i></button>
      </div>
      <div class="modal-body">
        <div style="background-color: var(--bg-primary); padding:16px; border-radius:var(--radius-md); border:1px solid var(--color-border); margin-bottom: 20px;">
          <div style="display:grid; grid-template-columns: 120px 1fr; row-gap: 8px; font-size:13px;">
            <span style="font-weight:600; color:var(--color-text-secondary);">Request ID:</span>
            <span id="summary-request-id" style="font-weight:600; color:var(--color-brand);">—</span>
            <span style="font-weight:600; color:var(--color-text-secondary);">Employee:</span>
            <span id="summary-employee">—</span>
            <span style="font-weight:600; color:var(--color-text-secondary);">Requested Asset:</span>
            <span id="summary-asset">—</span>
            <span style="font-weight:600; color:var(--color-text-secondary);">Action:</span>
            <span id="summary-action" style="font-weight:700;">—</span>
          </div>
        </div>
        <div class="form-group">
          <label for="manager-remarks" class="form-label">Review Remarks / Notes (Optional)</label>
          <textarea id="manager-remarks" class="form-control" placeholder="Enter reason or guidelines..."></textarea>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" onclick="closeModal('confirm-modal')">Cancel</button>
        <button class="btn" id="confirm-submit-btn" onclick="submitDecision()">Confirm Action</button>
      </div>
    </div>
  </div>

  <script>
    const CSRF_TOKEN = '{{ csrf_token }}';
    let currentTargetId = null;
    let currentActionType = null;

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

    function promptAction(requestId, action, employee, asset) {
      currentTargetId = requestId;
      currentActionType = action;

      document.getElementById('confirm-modal-title').textContent = `${action} Allocation Request`;
      document.getElementById('summary-request-id').textContent = requestId;
      document.getElementById('summary-employee').textContent = employee;
      document.getElementById('summary-asset').textContent = asset;
      document.getElementById('manager-remarks').value = '';

      const actionSpan = document.getElementById('summary-action');
      actionSpan.textContent = action.toUpperCase();
      const btn = document.getElementById('confirm-submit-btn');
      if (action === 'Approved') {
        actionSpan.style.color = 'var(--color-success)';
        btn.className = 'btn btn-success';
        btn.textContent = 'Approve Request';
      } else {
        actionSpan.style.color = 'var(--color-danger)';
        btn.className = 'btn btn-danger';
        btn.textContent = 'Reject Request';
      }
      openModal('confirm-modal');
    }

    function submitDecision() {
      if (!currentTargetId || !currentActionType) return;
      const remarks = document.getElementById('manager-remarks').value.trim();
      const btn = document.getElementById('confirm-submit-btn');
      btn.disabled = true;

      fetch('{% url "dept_head_handle_allocation" %}', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
        body: JSON.stringify({ allocation_id: currentTargetId, action: currentActionType, remarks })
      })
      .then(r => r.json())
      .then(data => {
        btn.disabled = false;
        if (data.success) {
          // Update badge in-place
          const badge = document.getElementById(`badge-${currentTargetId}`);
          if (badge) {
            badge.textContent = currentActionType;
            badge.className = `badge badge-${currentActionType.toLowerCase()}`;
          }
          // Hide action buttons
          const row = document.getElementById(`row-${currentTargetId}`);
          if (row) {
            const actionCell = row.querySelector('td:last-child');
            if (actionCell) actionCell.innerHTML = `<span style="font-size:12px; color:var(--color-text-muted); font-style:italic;">No actions pending</span>`;
          }
          showToast(data.message, 'success');
        } else {
          showToast(data.message || 'Error processing request.', 'danger');
        }
        closeModal('confirm-modal');
      })
      .catch(() => { btn.disabled = false; showToast('Network error. Please try again.', 'danger'); });
    }
  </script>
</body>
</html>
