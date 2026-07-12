{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Profile — AssetFlow Employee Portal</title>
  <meta name="description" content="View and edit your profile, and change your password, in the AssetFlow ERP employee portal.">
  <link href="https://cdn.jsdelivr.net/npm/remixicon@4.2.0/fonts/remixicon.css" rel="stylesheet"/>
  <link rel="stylesheet" href="{% static 'css/main.css' %}">
  <link rel="stylesheet" href="{% static 'css/employee.css' %}">
</head>
<body>

<aside class="sidebar">
  <div class="sidebar-brand">
    <div class="sidebar-logo">AF</div>
    <div class="sidebar-brand-text">
      <span class="sidebar-app-name">AssetFlow</span>
      <span class="sidebar-app-sub">Employee</span>
    </div>
  </div>
  <nav class="sidebar-nav">
    <a href="{% url 'employee_index' %}" class="nav-link"><i class="ri-dashboard-line"></i> Dashboard</a>
    <a href="{% url 'employee_assets' %}" class="nav-link"><i class="ri-box-3-line"></i> My Assets</a>
    <a href="{% url 'employee_bookings' %}" class="nav-link"><i class="ri-calendar-event-line"></i> Resource Booking</a>
    <a href="{% url 'employee_maintenance' %}" class="nav-link"><i class="ri-tools-line"></i> Maintenance</a>
    <a href="{% url 'employee_requests' %}" class="nav-link"><i class="ri-arrow-go-back-line"></i> Return & Transfer</a>
    <a href="{% url 'employee_leave' %}" class="nav-link"><i class="ri-calendar-todo-line"></i> Leave Requests</a>
    <a href="{% url 'employee_notifications' %}" class="nav-link"><i class="ri-notification-3-line"></i> Notifications</a>
    <a href="{% url 'employee_profile' %}" class="nav-link active"><i class="ri-user-settings-line"></i> My Profile</a>
  </nav>
  <div class="sidebar-footer">
    <div class="user-profile">
      <div class="user-avatar">EM</div>
      <div class="user-info">
        <span class="user-name">{{ request.user.username }}</span>
        <span class="user-role">{{ request.user.profile.department }}</span>
      </div>
    </div>
  </div>
</aside>

<div class="main-content">
  <header class="top-header">
    <div class="header-left">
      <h1 class="header-title">My Profile</h1>
    </div>
    <div class="header-right">
      <span class="dept-pill">{{ request.user.profile.department }}</span>
      <a href="{% url 'logout' %}" class="logout-btn" style="text-decoration:none; display:inline-block; line-height:30px; text-align:center;">
        <i class="ri-logout-box-line"></i> Sign Out
      </a>
    </div>
  </header>

  <main class="page-body animate-slide-right">

    <div class="dashboard-layout">

      <!-- LEFT: Summary card -->
      <div>
        <div class="card" style="text-align:center;padding:28px 20px;">
          <div class="user-avatar" id="profile-avatar" style="width:72px;height:72px;font-size:26px;margin:0 auto 14px auto;">EM</div>
          <div style="font-size:16px;font-weight:700;color:var(--color-text-primary);" id="profile-fullname">—</div>
          <div style="font-size:13px;color:var(--color-text-muted);margin-bottom:12px;" id="profile-role">—</div>
          <div style="text-align:left;border-top:1px solid var(--color-border);padding-top:14px;margin-top:6px;">
            <div style="display:flex;justify-content:space-between;font-size:13px;padding:6px 0;">
              <span style="color:var(--color-text-muted);">Employee ID</span>
              <span style="font-weight:600;" id="profile-empid">—</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:13px;padding:6px 0;">
              <span style="color:var(--color-text-muted);">Department</span>
              <span style="font-weight:600;" id="profile-dept">—</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:13px;padding:6px 0;">
              <span style="color:var(--color-text-muted);">Joined</span>
              <span style="font-weight:600;" id="profile-joined">—</span>
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT: Edit profile & change password -->
      <div>
        <div class="card" style="margin-bottom:24px;">
          <div class="card-header"><span class="card-title">Edit Profile</span></div>
          <form id="edit-profile-form" onsubmit="handleProfileSubmit(event)" enctype="multipart/form-data">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
              <div class="form-group">
                <label class="form-label">First Name</label>
                <input type="text" id="edit-first-name" class="form-control" placeholder="First name">
              </div>
              <div class="form-group">
                <label class="form-label">Last Name</label>
                <input type="text" id="edit-last-name" class="form-control" placeholder="Last name">
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">Email Address</label>
              <input type="email" id="edit-email" class="form-control" placeholder="you@company.com" required>
            </div>
            <div class="form-group">
              <label class="form-label">Phone Number</label>
              <input type="text" id="edit-phone" class="form-control" placeholder="+1 555 000 0000">
            </div>
            <div class="form-group">
              <label class="form-label">Profile Picture</label>
              <div class="upload-zone" onclick="document.getElementById('edit-profile-pic').click()">
                <i class="ri-upload-cloud-2-line"></i>
                <p id="upload-zone-text">Click to upload a new profile picture</p>
              </div>
              <input type="file" id="edit-profile-pic" accept="image/*" style="display:none;" onchange="document.getElementById('upload-zone-text').textContent = this.files[0] ? this.files[0].name : 'Click to upload a new profile picture';">
            </div>
            <button type="submit" class="btn btn-primary"><i class="ri-save-line"></i> Save Changes</button>
          </form>
        </div>

        <div class="card">
          <div class="card-header"><span class="card-title">Change Password</span></div>
          <form id="change-password-form" onsubmit="handlePasswordSubmit(event)">
            <div class="form-group">
              <label class="form-label">Current Password *</label>
              <input type="password" id="current-password" class="form-control" required>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
              <div class="form-group">
                <label class="form-label">New Password *</label>
                <input type="password" id="new-password" class="form-control" minlength="8" required>
              </div>
              <div class="form-group">
                <label class="form-label">Confirm New Password *</label>
                <input type="password" id="confirm-password" class="form-control" minlength="8" required>
              </div>
            </div>
            <button type="submit" class="btn btn-primary"><i class="ri-lock-2-line"></i> Update Password</button>
          </form>
        </div>
      </div>

    </div>
  </main>
</div>

<div class="toast-container" id="toastContainer"></div>

<script>
  const App = {
    showToast(message, type = 'success') {
      let c = document.getElementById('toastContainer');
      const t = document.createElement('div');
      t.className = `toast toast-${type === 'error' ? 'danger' : type}`;
      t.textContent = message;
      c.appendChild(t);
      setTimeout(() => t.remove(), 3500);
    }
  };

  async function loadProfile() {
    try {
      const response = await fetch("{% url 'employee_profile_data' %}");
      const data = await response.json();
      if (!data.success) return;
      const p = data.profile;
      document.getElementById('profile-avatar').textContent = p.avatar;
      document.getElementById('profile-fullname').textContent = (p.firstName || p.lastName) ? `${p.firstName} ${p.lastName}`.trim() : p.username;
      document.getElementById('profile-role').textContent = p.role;
      document.getElementById('profile-empid').textContent = p.employeeId;
      document.getElementById('profile-dept').textContent = p.department;
      document.getElementById('profile-joined').textContent = p.dateJoined;

      document.getElementById('edit-first-name').value = p.firstName || '';
      document.getElementById('edit-last-name').value = p.lastName || '';
      document.getElementById('edit-email').value = p.email || '';
      document.getElementById('edit-phone').value = p.phone || '';
    } catch (err) { console.error(err); }
  }

  async function handleProfileSubmit(event) {
    event.preventDefault();
    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
    formData.append('first_name', document.getElementById('edit-first-name').value.trim());
    formData.append('last_name', document.getElementById('edit-last-name').value.trim());
    formData.append('email', document.getElementById('edit-email').value.trim());
    formData.append('phone', document.getElementById('edit-phone').value.trim());
    const picInput = document.getElementById('edit-profile-pic');
    if (picInput.files[0]) formData.append('profile_pic', picInput.files[0]);

    try {
      const res = await fetch("{% url 'employee_update_profile' %}", { method: 'POST', body: formData });
      const data = await res.json();
      App.showToast(data.message, data.success ? 'success' : 'error');
      if (data.success) loadProfile();
    } catch (err) { App.showToast('Something went wrong. Please try again.', 'error'); }
  }

  async function handlePasswordSubmit(event) {
    event.preventDefault();
    const newPass = document.getElementById('new-password').value;
    const confirmPass = document.getElementById('confirm-password').value;
    if (newPass !== confirmPass) { App.showToast('New password and confirmation do not match.', 'error'); return; }

    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');
    formData.append('current_password', document.getElementById('current-password').value);
    formData.append('new_password', newPass);
    formData.append('confirm_password', confirmPass);

    try {
      const res = await fetch("{% url 'employee_change_password' %}", { method: 'POST', body: formData });
      const data = await res.json();
      App.showToast(data.message, data.success ? 'success' : 'error');
      if (data.success) document.getElementById('change-password-form').reset();
    } catch (err) { App.showToast('Something went wrong. Please try again.', 'error'); }
  }

  window.addEventListener('DOMContentLoaded', loadProfile);
</script>
</body>
</html>
