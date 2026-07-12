@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  --bg-primary: #F8F9FA;
  --bg-surface: #FFFFFF;
  --bg-sidebar: #FFFFFF;
  --color-brand: #FE6E04;
  --color-brand-hover: #E05E00;
  --color-brand-light: #FFF7ED;
  --color-text-primary: #0F172A;
  --color-text-secondary: #475569;
  --color-text-muted: #94A3B8;
  --color-border: #E2E8F0;
  --color-border-hover: #CBD5E1;
  --color-success: #10B981;
  --color-success-light: #D1FAE5;
  --color-danger: #EF4444;
  --color-danger-light: #FEE2E2;
  --color-warning: #F59E0B;
  --color-warning-light: #FEF3C7;

  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
  --shadow-lg: 0 10px 15px -3px rgba(15, 23, 42, 0.04), 0 4px 6px -4px rgba(15, 23, 42, 0.03);

  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Inter', sans-serif;
  background-color: var(--bg-primary);
  color: var(--color-text-primary);
  line-height: 1.5;
  min-height: 100vh;
  display: flex;
  overflow-x: hidden;

}

button,
a {
  text-decoration: none !important;
}

/* ── LAYOUT ──────────────────────────────────────── */
.sidebar {
  width: 260px;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  background-color: var(--bg-sidebar);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  z-index: 100;
}

.main-content {
  margin-left: 260px;
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.top-header {
  height: 70px;
  background-color: var(--bg-surface);
  border-bottom: 1px solid var(--color-border);
  padding: 0 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 90;
}

.page-body {
  padding: 32px;
  flex: 1;
}

/* ── SIDEBAR ─────────────────────────────────────── */
.sidebar-brand {
  padding: 24px 24px 20px 24px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.sidebar-logo {
  background-color: var(--color-brand);
  color: white;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
}

.sidebar-brand-text {
  display: flex;
  flex-direction: column;
}

.sidebar-app-name {
  font-weight: 700;
  font-size: 16px;
  color: var(--color-text-primary);
}

.sidebar-app-sub {
  font-size: 11px;
  color: var(--color-brand);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.sidebar-nav {
  flex: 1;
  padding: 12px 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: var(--color-text-secondary);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
}

.nav-link i {
  font-size: 18px;
  color: var(--color-text-secondary);
  transition: all 0.2s ease;
}

.nav-link:hover {
  background-color: var(--bg-primary);
  color: var(--color-text-primary);
}

.nav-link:hover i {
  color: var(--color-text-primary);
}

.nav-link.active {
  background-color: var(--color-brand-light);
  color: var(--color-brand);
  font-weight: 600;
}

.nav-link.active i {
  color: var(--color-brand);
}

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid var(--color-border);
  background-color: var(--bg-primary);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--color-brand);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
}

.user-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.user-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 11px;
  color: var(--color-text-secondary);
}

/* ── HEADER ──────────────────────────────────────── */
.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.dept-pill {
  background-color: var(--color-brand-light);
  color: var(--color-brand);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid rgba(254, 110, 4, 0.15);
}

.logout-btn {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 6px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background-color: var(--bg-primary);
  color: var(--color-danger);
}

/* ── GRIDS ───────────────────────────────────────── */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

@media (max-width: 1200px) {
  .kpi-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .kpi-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.dashboard-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 32px;
  align-items: start;
}

@media (max-width: 1024px) {
  .dashboard-layout {
    grid-template-columns: 1fr;
  }
}

.column-gap-32 {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

/* ── CARDS ───────────────────────────────────────── */
.card {
  background-color: var(--bg-surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
  padding: 24px;
  position: relative;
}

.card-kpi {
  display: flex;
  flex-direction: column;
  padding: 20px 24px;
}

.kpi-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.kpi-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.kpi-icon {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  background-color: var(--bg-primary);
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.card-kpi.active-kpi .kpi-icon {
  background-color: var(--color-brand-light);
  color: var(--color-brand);
}

.kpi-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--color-border);
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary);
}

/* ── BUTTONS ─────────────────────────────────────── */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  line-height: 1.2;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

.btn-primary {
  background-color: var(--color-brand);
  color: white;
  border-color: var(--color-brand);
}

.btn-primary:hover {
  background-color: var(--color-brand-hover);
  border-color: var(--color-brand-hover);
}

.btn-secondary {
  background-color: var(--bg-surface);
  color: var(--color-text-secondary);
  border-color: var(--color-border);
}

.btn-secondary:hover {
  background-color: var(--bg-primary);
  border-color: var(--color-border-hover);
  color: var(--color-text-primary);
}

.btn-danger {
  background-color: var(--color-danger);
  color: white;
  border-color: var(--color-danger);
}

.btn-danger:hover {
  background-color: #DC2626;
  border-color: #DC2626;
}

.btn-success {
  background-color: var(--color-success);
  color: white;
  border-color: var(--color-success);
}

.btn-success:hover {
  background-color: #059669;
  border-color: #059669;
}

.btn-icon {
  padding: 8px;
  border-radius: var(--radius-sm);
}

/* ── TABLES ──────────────────────────────────────── */
.table-responsive {
  width: 100%;
  overflow-x: auto;
}

.table-custom {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 13px;
}

.table-custom th {
  padding: 12px 16px;
  background-color: var(--bg-primary);
  color: var(--color-text-secondary);
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid var(--color-border);
}

.table-custom td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text-primary);
  vertical-align: middle;
}

.table-custom tbody tr:last-child td {
  border-bottom: none;
}

.table-custom tbody tr:hover {
  background-color: rgba(248, 249, 250, 0.7);
}

/* ── BADGES ──────────────────────────────────────── */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-pending {
  background-color: var(--color-warning-light);
  color: var(--color-warning);
}

.badge-approved {
  background-color: var(--color-success-light);
  color: var(--color-success);
}

.badge-rejected {
  background-color: var(--color-danger-light);
  color: var(--color-danger);
}

.badge-active {
  background-color: var(--color-success-light);
  color: var(--color-success);
}

.badge-brand {
  background-color: var(--color-brand-light);
  color: var(--color-brand);
}

/* ── FILTERS & SEARCH ────────────────────────────── */
.filters-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.search-wrapper {
  position: relative;
  flex: 1;
  max-width: 320px;
}

.search-input {
  width: 100%;
  padding: 8px 12px 8px 36px;
  font-size: 13px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background-color: var(--bg-surface);
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--color-brand);
  box-shadow: 0 0 0 3px rgba(254, 110, 4, 0.1);
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-muted);
  font-size: 16px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-select {
  padding: 8px 12px;
  font-size: 13px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background-color: var(--bg-surface);
  color: var(--color-text-secondary);
  cursor: pointer;
  outline: none;
  transition: all 0.2s ease;
}

.filter-select:focus {
  border-color: var(--color-brand);
}

/* ── TIMELINE ────────────────────────────────────── */
.timeline {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: relative;
}

.timeline::before {
  content: '';
  position: absolute;
  top: 8px;
  bottom: 8px;
  left: 19px;
  width: 2px;
  background-color: var(--color-border);
}

.timeline-item {
  display: flex;
  gap: 16px;
  position: relative;
}

.timeline-icon-wrap {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--bg-primary);
  border: 2px solid var(--bg-surface);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
  color: var(--color-text-secondary);
  font-size: 16px;
}

.timeline-item.active-timeline .timeline-icon-wrap {
  background-color: var(--color-brand-light);
  color: var(--color-brand);
  border-color: var(--color-brand-light);
}

.timeline-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.timeline-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.timeline-time {
  font-size: 11px;
  color: var(--color-text-muted);
}

.timeline-desc {
  font-size: 12px;
  color: var(--color-text-secondary);
  margin-top: 4px;
}

/* ── FORMS ───────────────────────────────────────── */
.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-secondary);
  margin-bottom: 6px;
}

.form-control {
  width: 100%;
  padding: 10px 12px;
  font-size: 13px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background-color: var(--bg-surface);
  color: var(--color-text-primary);
  transition: all 0.2s ease;
}

.form-control:focus {
  outline: none;
  border-color: var(--color-brand);
  box-shadow: 0 0 0 3px rgba(254, 110, 4, 0.1);
}

.form-control:disabled {
  background-color: var(--bg-primary);
  color: var(--color-text-secondary);
  cursor: not-allowed;
}

textarea.form-control {
  resize: vertical;
  min-height: 80px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

/* ── MODALS ──────────────────────────────────────── */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.2s ease, visibility 0.2s ease;
}

.modal-overlay.open {
  opacity: 1;
  visibility: visible;
}

.modal-container {
  background-color: var(--bg-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  width: 100%;
  max-width: 550px;
  overflow: hidden;
  transform: scale(0.97) translateY(10px);
  opacity: 0;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease;
}

.modal-overlay.open .modal-container {
  transform: scale(1) translateY(0);
  opacity: 1;
}

.modal-header {
  padding: 16px 24px;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--bg-primary);
}

.modal-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.modal-close-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.modal-close-btn:hover {
  background-color: var(--color-border);
  color: var(--color-text-primary);
}

.modal-body {
  padding: 24px;
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid var(--color-border);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  background-color: var(--bg-primary);
}

.detail-row {
  display: flex;
  padding: 8px 0;
  border-bottom: 1px solid var(--bg-primary);
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  width: 160px;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-secondary);
}

.detail-value {
  flex: 1;
  font-size: 13px;
  color: var(--color-text-primary);
}

/* ── TOAST NOTIFICATIONS ─────────────────────────── */
.toast-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 1100;
}

.toast {
  background-color: var(--bg-surface);
  border-left: 4px solid var(--color-brand);
  box-shadow: var(--shadow-lg);
  border-radius: var(--radius-sm);
  padding: 12px 18px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 13px;
  font-weight: 500;
  min-width: 280px;
  animation: slideInFromRight 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.toast-success {
  border-left-color: var(--color-success);
}

.toast-success i {
  color: var(--color-success);
}

.toast-danger {
  border-left-color: var(--color-danger);
}

.toast-danger i {
  color: var(--color-danger);
}

/* ── ANIMATIONS ──────────────────────────────────── */
@keyframes slideInFromRight {
  from {
    opacity: 0;
    transform: translateX(30px) scale(0.97);
  }

  to {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

@keyframes slideInFromLeft {
  from {
    opacity: 0;
    transform: translateX(-30px) scale(0.97);
  }

  to {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

.animate-slide-right {
  animation: slideInFromRight 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.animate-slide-left {
  animation: slideInFromLeft 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Resource Card grid */
.resource-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.resource-card {
  background-color: var(--bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 20px;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: all 0.2s ease;
}

.resource-card:hover {
  border-color: var(--color-brand);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.resource-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.resource-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  background-color: var(--color-brand-light);
  color: var(--color-brand);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.resource-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.resource-desc {
  font-size: 12px;
  color: var(--color-text-secondary);
}

.resource-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 4px;
  font-size: 11px;
  color: var(--color-text-muted);
}