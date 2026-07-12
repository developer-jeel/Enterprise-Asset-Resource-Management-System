{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Resource Booking — AssetFlow Department Head Portal</title>
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
      <a href="{% url 'dept_head_allocations' %}" class="nav-link"><i class="ri-send-plane-line"></i> Allocation Requests</a>
      <a href="{% url 'dept_head_transfers' %}" class="nav-link"><i class="ri-shuffle-line"></i> Transfer Requests</a>
      <a href="{% url 'dept_head_bookings' %}" class="nav-link active"><i class="ri-calendar-event-line"></i> Resource Booking</a>
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
        <h1 class="header-title">Resource Booking</h1>
      </div>
      <div class="header-right">
        <span class="dept-pill">{{ profile.department|default:"No Department" }}</span>
        <a href="{% url 'logout' %}" class="logout-btn"><i class="ri-logout-box-line"></i> Sign Out</a>
      </div>
    </header>
    
    <main class="page-body animate-slide-right">
      <!-- Top Actions -->
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:24px;">
        <span style="font-size:14px; color:var(--color-text-secondary);">Book shared organization tools, conference halls, rooms, and vehicles on behalf of your department.</span>
        <button class="btn btn-primary" onclick="openModal('booking-modal')">
          <i class="ri-calendar-todo-line"></i> New Booking
        </button>
      </div>

      <!-- Resource Cards -->
      <div class="resource-grid">
        {% for resource in resources %}
        <div class="resource-card">
          <div class="resource-header">
            <div class="resource-icon"><i class="{{ resource.icon|default:'ri-box-3-line' }}"></i></div>
            <span class="resource-name">{{ resource.name }}</span>
          </div>
          <p class="resource-desc">{{ resource.type }} &bull; Floor {{ resource.floor }}</p>
          <div class="resource-meta">
            <span>Capacity: {{ resource.capacity }}</span>
            <span class="badge badge-brand" style="font-size: 8px;">{{ resource.availability }}</span>
          </div>
        </div>
        {% empty %}
        <div class="resource-card">
          <div class="resource-header">
            <div class="resource-icon"><i class="ri-community-line"></i></div>
            <span class="resource-name">Meeting Room 204</span>
          </div>
          <p class="resource-desc">Medium-sized workspace with smart whiteboards and 4K TV.</p>
          <div class="resource-meta">
            <span>Capacity: 10 Seats</span>
            <span class="badge badge-brand" style="font-size: 8px;">Available</span>
          </div>
        </div>
        {% endfor %}
      </div>

      <!-- Booking History -->
      <div class="card animate-slide-left">
        <div class="card-header">
          <span class="card-title">Departmental Booking History</span>
        </div>

        <div class="table-responsive">
          <table class="table-custom">
            <thead>
              <tr>
                <th>Booking ID</th>
                <th>Resource Name</th>
                <th>Booking Date</th>
                <th>Time Window</th>
                <th>Purpose</th>
                <th>Reserved By</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody id="bookings-table-body">
              {% for b in bookings %}
              <tr id="brow-{{ b.booking_id }}">
                <td><span style="font-weight:600; color:var(--color-brand);">{{ b.booking_id }}</span></td>
                <td style="font-weight: 500;">{{ b.resource.name }}</td>
                <td>{{ b.date }}</td>
                <td>{{ b.start_time }} - {{ b.end_time }}</td>
                <td>{{ b.purpose }}</td>
                <td>{{ b.booked_by.username }}</td>
                <td>
                  {% if b.status == 'Active' %}
                  <span class="badge badge-approved" id="bbadge-{{ b.booking_id }}">Active</span>
                  {% elif b.status == 'Cancelled' %}
                  <span class="badge badge-rejected" id="bbadge-{{ b.booking_id }}">Cancelled</span>
                  {% else %}
                  <span class="badge badge-pending" id="bbadge-{{ b.booking_id }}">{{ b.status }}</span>
                  {% endif %}
                </td>
                <td>
                  {% if b.status == 'Active' %}
                  <button class="btn btn-danger btn-sm" onclick="cancelBooking('{{ b.booking_id }}')">
                    <i class="ri-delete-bin-line"></i> Cancel
                  </button>
                  {% else %}
                  <span style="font-size:12px; color:var(--color-text-muted); font-style:italic;">N/A</span>
                  {% endif %}
                </td>
              </tr>
              {% empty %}
              <tr><td colspan="8" style="text-align:center; color:var(--color-text-secondary); padding:24px;">No booking records found.</td></tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>

  <!-- New Booking Modal -->
  <div class="modal-overlay" id="booking-modal">
    <div class="modal-container">
      <div class="modal-header">
        <span class="modal-title">Book Shared Resource</span>
        <button class="modal-close-btn" onclick="closeModal('booking-modal')"><i class="ri-close-line"></i></button>
      </div>
      <form id="booking-form" onsubmit="handleNewBooking(event)">
        <div class="modal-body">
          <div class="form-group">
            <label for="booking-resource" class="form-label">Select Shared Resource <span style="color:var(--color-danger)">*</span></label>
            <select id="booking-resource" class="form-control" required>
              <option value="" disabled selected>-- Select a Resource --</option>
              {% for resource in resources %}
              <option value="{{ resource.resource_id }}">{{ resource.name }} ({{ resource.type }})</option>
              {% empty %}
              <option value="1">Meeting Room 204</option>
              {% endfor %}
            </select>
          </div>

          <div class="form-group">
            <label for="booking-date" class="form-label">Booking Date <span style="color:var(--color-danger)">*</span></label>
            <input type="date" id="booking-date" class="form-control" required>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="booking-start" class="form-label">Start Time <span style="color:var(--color-danger)">*</span></label>
              <input type="time" id="booking-start" class="form-control" required>
            </div>
            <div class="form-group">
              <label for="booking-end" class="form-label">End Time <span style="color:var(--color-danger)">*</span></label>
              <input type="time" id="booking-end" class="form-control" required>
            </div>
          </div>

          <div class="form-group">
            <label for="booking-purpose" class="form-label">Purpose of Booking <span style="color:var(--color-danger)">*</span></label>
            <input type="text" id="booking-purpose" class="form-control" placeholder="e.g. Design review, client meetings..." required>
          </div>

          <div class="form-group">
            <label class="form-label">Booking Department</label>
            <input type="text" class="form-control" value="{{ profile.department|default:'General' }}" disabled readonly>
          </div>

          <div class="form-group" style="margin-bottom:0;">
            <label for="booking-notes" class="form-label">Special Notes / Requirements</label>
            <textarea id="booking-notes" class="form-control" placeholder="e.g. Setup adapter, room layout request..."></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" onclick="closeModal('booking-modal')">Cancel</button>
          <button type="submit" class="btn btn-primary" id="booking-submit-btn">Confirm Booking</button>
        </div>
      </form>
    </div>
  </div>

  <script>
    const CSRF_TOKEN = '{{ csrf_token }}';

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

    // Set min date on datepicker to today
    window.addEventListener('DOMContentLoaded', () => {
      const dateInput = document.getElementById('booking-date');
      if (dateInput) dateInput.min = new Date().toISOString().split('T')[0];
    });

    function handleNewBooking(e) {
      e.preventDefault();
      const btn = document.getElementById('booking-submit-btn');
      btn.disabled = true;

      const payload = {
        resource_id: document.getElementById('booking-resource').value,
        date: document.getElementById('booking-date').value,
        start_time: document.getElementById('booking-start').value,
        end_time: document.getElementById('booking-end').value,
        purpose: document.getElementById('booking-purpose').value.trim(),
        notes: document.getElementById('booking-notes').value.trim(),
      };

      fetch('{% url "dept_head_create_booking" %}', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
        body: JSON.stringify(payload)
      })
      .then(r => r.json())
      .then(data => {
        btn.disabled = false;
        if (data.success) {
          // Append new row to table
          const tbody = document.getElementById('bookings-table-body');
          const b = data.booking;
          const emptyRow = tbody.querySelector('td[colspan]');
          if (emptyRow) emptyRow.closest('tr').remove();

          tbody.insertAdjacentHTML('afterbegin', `
            <tr id="brow-${b.id}">
              <td><span style="font-weight:600; color:var(--color-brand);">${b.id}</span></td>
              <td style="font-weight: 500;">${b.resource}</td>
              <td>${b.date}</td>
              <td>${b.start} - ${b.end}</td>
              <td>${b.purpose}</td>
              <td>{{ profile.user.username }}</td>
              <td><span class="badge badge-approved" id="bbadge-${b.id}">Active</span></td>
              <td><button class="btn btn-danger btn-sm" onclick="cancelBooking('${b.id}')"><i class="ri-delete-bin-line"></i> Cancel</button></td>
            </tr>
          `);

          document.getElementById('booking-form').reset();
          closeModal('booking-modal');
          showToast(`${b.resource} has been booked successfully!`, 'success');
        } else {
          showToast(data.message || 'Error creating booking.', 'danger');
        }
      })
      .catch(() => { btn.disabled = false; showToast('Network error. Please try again.', 'danger'); });
    }

    function cancelBooking(bookingId) {
      if (!confirm(`Are you sure you want to cancel booking ${bookingId}?`)) return;

      fetch('{% url "dept_head_cancel_booking" %}', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
        body: JSON.stringify({ booking_id: bookingId })
      })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          const badge = document.getElementById(`bbadge-${bookingId}`);
          if (badge) { badge.textContent = 'Cancelled'; badge.className = 'badge badge-rejected'; }
          const row = document.getElementById(`brow-${bookingId}`);
          if (row) {
            const actionCell = row.querySelector('td:last-child');
            if (actionCell) actionCell.innerHTML = `<span style="font-size:12px; color:var(--color-text-muted); font-style:italic;">N/A</span>`;
          }
          showToast(data.message, 'warning');
        } else {
          showToast(data.message || 'Error cancelling booking.', 'danger');
        }
      })
      .catch(() => showToast('Network error. Please try again.', 'danger'));
    }
  </script>
</body>
</html>
