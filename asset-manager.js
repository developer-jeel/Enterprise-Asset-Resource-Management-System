# This app owns no models of its own. All shared domain models
# (Asset, AssetAllocation, AssetTransfer, MaintenanceRequest, AssetReturn,
# ResourceBooking, ActivityLog, etc.) live in `core.models` and are
# imported explicitly wherever they're needed, e.g.:
#
#     from core.models import Asset, ResourceBooking
#
# No `from core.models import *` here -- that pattern is exactly what
# caused the original circular-import / unreadable-namespace problem
# (see BACKEND_FIXES.md). Keeping this file intentionally empty (instead
# of deleting it) documents that decision for anyone who goes looking for
# an Employee-specific model and doesn't find one.
