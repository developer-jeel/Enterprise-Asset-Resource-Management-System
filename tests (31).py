/* ── ASSET MANAGER SPECIFIC STYLES ──────────────────── */

/* ── DASHBOARD QUICK ACTIONS ─────────────────────── */
.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

@media (max-width: 1200px) {
  .quick-actions-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 640px) {
  .quick-actions-grid { grid-template-columns: 1fr; }
}

.quick-action-card {
  background: var(--bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  text-decoration: none;
  box-shadow: var(--shadow-sm);
}

.quick-action-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
  border-color: var(--color-brand);
}

.quick-action-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  flex-shrink: 0;
}

.quick-action-icon.orange { background-color: var(--color-brand-light); color: var(--color-brand); }
.quick-action-icon.green { background-color: var(--color-success-light); color: var(--color-success); }
.quick-action-icon.yellow { background-color: var(--color-warning-light); color: var(--color-warning); }
.quick-action-icon.red { background-color: var(--color-danger-light); color: var(--color-danger); }
.quick-action-icon.blue { background-color: #EFF6FF; color: #3B82F6; }
.quick-action-icon.purple { background-color: #F5F3FF; color: #7C3AED; }

.quick-action-info { flex: 1; min-width: 0; }
.quick-action-title { font-size: 13px; font-weight: 600; color: var(--color-text-primary); }
.quick-action-count { font-size: 22px; font-weight: 700; color: var(--color-text-primary); line-height: 1.2; }
.quick-action-sub { font-size: 11px; color: var(--color-text-muted); }

/* ── STATUS PIPELINE ──────────────────────────────── */
.status-pipeline {
  display: flex;
  gap: 0;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  margin-bottom: 24px;
}

.pipeline-step {
  flex: 1;
  padding: 14px 16px;
  text-align: center;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-secondary);
  background: var(--bg-primary);
  border-right: 1px solid var(--color-border);
  transition: all 0.2s ease;
  position: relative;
}

.pipeline-step:last-child { border-right: none; }

.pipeline-step.active {
  background: var(--color-brand-light);
  color: var(--color-brand);
}

.pipeline-step .step-count {
  display: block;
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.pipeline-step.active .step-count { color: var(--color-brand); }

/* ── ASSET STATUS BARS ────────────────────────────── */
.asset-status-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.asset-status-label {
  width: 120px;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-secondary);
  flex-shrink: 0;
}

.asset-status-track {
  flex: 1;
  height: 8px;
  background: var(--color-border);
  border-radius: 4px;
  overflow: hidden;
}

.asset-status-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.fill-brand { background: var(--color-brand); }
.fill-success { background: var(--color-success); }
.fill-warning { background: var(--color-warning); }
.fill-danger { background: var(--color-danger); }
.fill-blue { background: #3B82F6; }

.asset-status-value {
  width: 40px;
  font-size: 12px;
  font-weight: 700;
  color: var(--color-text-primary);
  text-align: right;
  flex-shrink: 0;
}

/* ── PRIORITY BADGES ──────────────────────────────── */
.badge-high {
  background-color: var(--color-danger-light);
  color: var(--color-danger);
}
.badge-medium {
  background-color: var(--color-warning-light);
  color: var(--color-warning);
}
.badge-low {
  background-color: var(--color-success-light);
  color: var(--color-success);
}
.badge-critical {
  background-color: #FDF2F8;
  color: #9D174D;
}
.badge-info {
  background-color: #EFF6FF;
  color: #1D4ED8;
}
.badge-in-use {
  background-color: var(--color-success-light);
  color: var(--color-success);
}
.badge-storage {
  background-color: #EFF6FF;
  color: #1D4ED8;
}
.badge-repair {
  background-color: var(--color-warning-light);
  color: var(--color-warning);
}
.badge-retired {
  background-color: var(--color-border);
  color: var(--color-text-muted);
}

/* ── MAINTENANCE CARDS ────────────────────────────── */
.maintenance-card {
  background: var(--bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 20px;
  box-shadow: var(--shadow-sm);
  transition: all 0.25s ease;
  border-left: 4px solid var(--color-border);
}

.maintenance-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.maintenance-card.priority-high { border-left-color: var(--color-danger); }
.maintenance-card.priority-medium { border-left-color: var(--color-warning); }
.maintenance-card.priority-low { border-left-color: var(--color-success); }
.maintenance-card.priority-critical { border-left-color: #9D174D; }

.maintenance-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  gap: 12px;
}

.maintenance-asset-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.maintenance-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 12px;
  font-size: 12px;
  color: var(--color-text-secondary);
}

.maintenance-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.maintenance-issue {
  font-size: 13px;
  color: var(--color-text-secondary);
  background: var(--bg-primary);
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border);
  margin-bottom: 16px;
  line-height: 1.5;
}

.maintenance-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

/* ── RETURN INSPECTION CARD ───────────────────────── */
.return-card {
  background: var(--bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: all 0.25s ease;
}

.return-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.return-card-header {
  background: var(--bg-primary);
  padding: 16px 20px;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.return-card-body { padding: 20px; }

.condition-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}

.condition-item {
  background: var(--bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
}

.condition-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.condition-value {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-primary);
}

/* ── DISCREPANCY CARDS ────────────────────────────── */
.discrepancy-type-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
}

.disc-missing { background: var(--color-danger-light); color: var(--color-danger); }
.disc-condition { background: var(--color-warning-light); color: var(--color-warning); }
.disc-location { background: #EFF6FF; color: #1D4ED8; }
.disc-quantity { background: #F5F3FF; color: #7C3AED; }

.severity-indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 6px;
}

.severity-critical { background: #9D174D; }
.severity-high { background: var(--color-danger); }
.severity-medium { background: var(--color-warning); }
.severity-low { background: var(--color-success); }

/* ── WORKFLOW STEPPER ─────────────────────────────── */
.workflow-stepper {
  display: flex;
  align-items: center;
  gap: 0;
  margin-bottom: 20px;
}

.workflow-step {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  position: relative;
}

.workflow-step-dot {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: var(--color-text-muted);
  flex-shrink: 0;
  z-index: 1;
}

.workflow-step.done .workflow-step-dot {
  background: var(--color-success);
  color: white;
}

.workflow-step.active .workflow-step-dot {
  background: var(--color-brand);
  color: white;
}

.workflow-step-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-muted);
}

.workflow-step.done .workflow-step-label,
.workflow-step.active .workflow-step-label {
  color: var(--color-text-primary);
}

.workflow-connector {
  flex: 1;
  height: 2px;
  background: var(--color-border);
  margin: 0 4px;
}

.workflow-connector.done { background: var(--color-success); }

/* ── DETAIL PANEL ─────────────────────────────────── */
.detail-panel {
  background: var(--bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 16px;
  margin-bottom: 16px;
}

.detail-panel-title {
  font-size: 12px;
  font-weight: 700;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--color-border);
}

/* ── CARDS GRID FOR MAINTENANCE / RETURNS ─────────── */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
}

@media (max-width: 768px) {
  .cards-grid { grid-template-columns: 1fr; }
}

/* ── ALLOCATION HISTORY TIMELINE ──────────────────── */
.alloc-timeline {
  display: flex;
  flex-direction: column;
  gap: 12px;
  position: relative;
  padding-left: 24px;
}

.alloc-timeline::before {
  content: '';
  position: absolute;
  left: 7px;
  top: 8px;
  bottom: 8px;
  width: 2px;
  background: var(--color-border);
}

.alloc-event {
  position: relative;
  font-size: 12px;
  color: var(--color-text-secondary);
  line-height: 1.5;
}

.alloc-event::before {
  content: '';
  position: absolute;
  left: -20px;
  top: 5px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-brand);
  border: 2px solid var(--bg-surface);
}

.alloc-event-title {
  font-weight: 600;
  color: var(--color-text-primary);
  font-size: 13px;
}

.alloc-event-time {
  font-size: 11px;
  color: var(--color-text-muted);
}

/* ── ASSET IMAGE PLACEHOLDER ──────────────────────── */
.asset-image-box {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-md);
  background: var(--bg-primary);
  border: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  color: var(--color-text-muted);
  flex-shrink: 0;
}

/* ── RESPONSIVE OVERRIDES ─────────────────────────── */
@media (max-width: 768px) {
  .filters-bar { flex-direction: column; align-items: stretch; }
  .filter-group { flex-wrap: wrap; }
  .maintenance-card-header { flex-direction: column; }
  .condition-grid { grid-template-columns: 1fr; }
}
