{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard Overview — AssetFlow Department Head Portal</title>
  <link href="https://cdn.jsdelivr.net/npm/remixicon@4.2.0/fonts/remixicon.css" rel="stylesheet" />
  <link rel="stylesheet" href="{% static 'css/main.css' %}">
</head>
<body>

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
      <a href="{% url 'dept_head_index' %}" class="nav-link active"><i class="ri-dashboard-line"></i> Dashboard</a>
      <a href="{% url 'dept_head_assets' %}" class="nav-link"><i class="ri-box-3-line"></i> Department Assets</a>
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
        <h1 class="header-title">Dashboard Overview</h1>
      </div>
      <div class="header-right">
        <span class="dept-pill">{{ profile.department|default:"No Department" }}</span>
        <a href="{% url 'logout' %}" class="logout-btn"><i class="ri-logout-box-line"></i> Sign Out</a>
      </div>
    </header>
    
    <main class="page-body animate-slide-right">
      <!-- KPI Grid -->
      <div class="kpi-grid">
        <div class="card card-kpi">
          <div class="kpi-header">
            <span class="kpi-title">Total Dept Assets</span>
            <div class="kpi-icon"><i class="ri-box-3-line"></i></div>
          </div>
          <span class="kpi-value" id="kpi-total-assets">{{ total_assets }}</span>
        </div>
        <div class="card card-kpi active-kpi">
          <div class="kpi-header">
            <span class="kpi-title">Allocated Assets</span>
            <div class="kpi-icon"><i class="ri-checkbox-circle-line"></i></div>
          </div>
          <span class="kpi-value" id="kpi-allocated">{{ allocated_assets }}</span>
        </div>
        <div class="card card-kpi active-kpi">
          <div class="kpi-header">
            <span class="kpi-title">Pending Allocations</span>
            <div class="kpi-icon"><i class="ri-send-plane-line"></i></div>
          </div>
          <span class="kpi-value" id="kpi-pending-allocations">{{ pending_allocations }}</span>
        </div>
        <div class="card card-kpi active-kpi">
          <div class="kpi-header">
            <span class="kpi-title">Pending Transfers</span>
            <div class="kpi-icon"><i class="ri-shuffle-line"></i></div>
          </div>
          <span class="kpi-value" id="kpi-pending-transfers">{{ pending_transfers }}</span>
        </div>
        <div class="card card-kpi">
          <div class="kpi-header">
            <span class="kpi-title">Active Bookings</span>
            <div class="kpi-icon"><i class="ri-calendar-event-line"></i></div>
          </div>
          <span class="kpi-value" id="kpi-active-bookings">{{ active_bookings }}</span>
        </div>
      </div>

      <!-- Dashboard Layout Section -->
      <div class="dashboard-layout">
        <!-- Left Column: Tables -->
        <div class="column-gap-32">
          <!-- Recent Allocation Requests -->
          <div class="card">
            <div class="card-header">
              <span class="card-title">Recent Allocation Requests</span>
              <a href="{% url 'dept_head_allocations' %}" class="btn btn-secondary btn-sm">View All</a>
            </div>
            <div class="table-responsive">
              <table class="table-custom">
                <thead>
                  <tr>
                    <th>Request ID</th>
                    <th>Employee</th>
                    <th>Requested Asset</th>
                    <th>Request Date</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {% for alloc in recent_allocations %}
                  <tr>
                    <td><span class="font-semi">{{ alloc.allocation_id }}</span></td>
                    <td>{{ alloc.requested_by.username }}</td>
                    <td>{{ alloc.asset_name|default:alloc.asset.name|default:"—" }}</td>
                    <td>{{ alloc.request_date }}</td>
                    <td><span class="badge badge-{{ alloc.status|lower }}">{{ alloc.status }}</span></td>
                  </tr>
                  {% empty %}
                  <tr><td colspan="5" style="text-align:center; color:var(--color-text-secondary); padding:24px;">No allocation requests found.</td></tr>
                  {% endfor %}
                </tbody>
              </table>
            </div>
          </div>

          <!-- Recent Transfer Requests -->
          <div class="card">
            <div class="card-header">
              <span class="card-title">Recent Transfer Requests</span>
              <a href="{% url 'dept_head_transfers' %}" class="btn btn-secondary btn-sm">View All</a>
            </div>
            <div class="table-responsive">
              <table class="table-custom">
                <thead>
                  <tr>
                    <th>Transfer ID</th>
                    <th>Asset</th>
                    <th>Handover (From &rarr; To)</th>
                    <th>Request Date</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {% for t in recent_transfers %}
                  <tr>
                    <td><span class="font-semi">{{ t.transfer_id }}</span></td>
                    <td>{{ t.asset.tag }}</td>
                    <td>{{ t.from_employee.username }} &rarr; {{ t.to_employee.username }}</td>
                    <td>{{ t.request_date }}</td>
                    <td><span class="badge badge-{{ t.status|lower }}">{{ t.status }}</span></td>
                  </tr>
                  {% empty %}
                  <tr><td colspan="5" style="text-align:center; color:var(--color-text-secondary); padding:24px;">No transfer requests found.</td></tr>
                  {% endfor %}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Right Column: Sidebar Widgets -->
        <div class="column-gap-32">
          <!-- Upcoming Resource Bookings -->
          <div class="card">
            <div class="card-header">
              <span class="card-title">Upcoming Bookings</span>
              <a href="{% url 'dept_head_bookings' %}" class="btn btn-secondary btn-sm">Book</a>
            </div>
            <div style="display: flex; flex-direction: column; gap: 8px;">
              {% for b in active_bookings_list %}
              <div style="display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--color-border);">
                <div style="display: flex; gap: 12px; align-items: center; min-width: 0;">
                  <div style="width: 32px; height: 32px; border-radius: var(--radius-sm); background-color: var(--color-brand-light); color: var(--color-brand); display: flex; align-items: center; justify-content: center; font-size: 14px; flex-shrink: 0;">
                    <i class="ri-calendar-event-line"></i>
                  </div>
                  <div style="display:flex; flex-direction:column; min-width: 0;">
                    <span style="font-size:13px; font-weight:600; color:var(--color-text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{{ b.resource.name }}</span>
                    <span style="font-size:11px; color:var(--color-text-muted);">{{ b.date }} &bull; {{ b.start_time }} - {{ b.end_time }}</span>
                  </div>
                </div>
                <span class="badge badge-approved" style="font-size: 9px; flex-shrink: 0; padding: 2px 6px;">Active</span>
              </div>
              {% empty %}
              <div style="color: var(--color-text-secondary); font-size:13px; text-align:center; padding: 20px;">No active bookings found.</div>
              {% endfor %}
            </div>
          </div>

          <!-- Recent Activity Log -->
          <div class="card">
            <div class="card-header">
              <span class="card-title">Activity Timeline</span>
            </div>
            <div class="timeline">
              {% for act in activities %}
              <div class="timeline-item {% if forloop.counter <= 2 %}active-timeline{% endif %}">
                <div class="timeline-icon-wrap">
                  <i class="{% if act.type == 'approval' %}ri-checkbox-circle-line{% elif act.type == 'rejection' %}ri-close-circle-line{% elif act.type == 'booking' %}ri-calendar-event-line{% else %}ri-file-info-line{% endif %}"></i>
                </div>
                <div class="timeline-content">
                  <div class="timeline-header">
                    <span class="timeline-title">{{ act.text }}</span>
                    <span class="timeline-time">{{ act.time }}</span>
                  </div>
                  <p class="timeline-desc">Status log updated</p>
                </div>
              </div>
              {% empty %}
              <div style="color: var(--color-text-secondary); font-size:13px; text-align:center; padding: 20px;">No recent activity.</div>
              {% endfor %}
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>

  <script>
    function showToast(message, type = 'success') {
      let container = document.getElementById('toastContainer');
      if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container';
        document.body.appendChild(container);
      }
      const toast = document.createElement('div');
      toast.className = `toast toast-${type === 'error' ? 'danger' : type}`;
      const icons = { success: 'ri-checkbox-circle-fill', danger: 'ri-error-warning-fill', warning: 'ri-alert-fill', info: 'ri-information-line' };
      toast.innerHTML = `<i class="${icons[type] || icons.success}"></i><span>${message}</span>`;
      container.appendChild(toast);
      setTimeout(() => { toast.style.opacity = '0'; toast.style.transform = 'translateY(10px)'; setTimeout(() => toast.remove(), 300); }, 3500);
    }
  </script>
</body>
</html>
