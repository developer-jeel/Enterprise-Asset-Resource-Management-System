from django.shortcuts import render, redirect
from django.contrib import messages
from admin.models import user, Asset, AllocationRequest, TransferRequest, ResourceBooking


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def _next_id(model, id_field, prefix, start=1001):
    """Generate a robust unique sequential ID like 'AR-1005'."""
    last = model.objects.order_by('-id').first()
    if last:
        try:
            num = int(getattr(last, id_field).split('-')[1]) + 1
        except (ValueError, IndexError):
            num = model.objects.count() + start
    else:
        num = start
    return f"{prefix}-{num}"


# --------------------------------------------------------------------------
# Session guard decorator
# --------------------------------------------------------------------------

def mgr_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request, 'Please log in to access this page.')
            return redirect('login')
        if request.session.get('user_role') != 'manager':
            messages.error(request, 'Access denied. Manager only.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def _ctx(request):
    """Common context injected into every manager page."""
    return {
        'user_name': request.session.get('user_name', 'Manager'),
        'user_role': request.session.get('user_role', 'manager'),
    }


# --------------------------------------------------------------------------
# Dashboard / Index
# --------------------------------------------------------------------------

@mgr_login_required
def index(request):
    total_assets = Asset.objects.count()
    allocated_assets = Asset.objects.filter(status='Allocated').count()
    pending_allocations = AllocationRequest.objects.filter(status='Pending').count()
    pending_transfers = TransferRequest.objects.filter(status='Pending').count()
    active_bookings = ResourceBooking.objects.filter(status='Active').count()

    recent_allocations = AllocationRequest.objects.select_related('employee').order_by('-request_date')[:5]
    recent_transfers = TransferRequest.objects.select_related('asset', 'from_employee', 'to_employee').order_by('-request_date')[:5]
    upcoming_bookings = ResourceBooking.objects.filter(status='Active').order_by('booking_date')[:5]

    ctx = _ctx(request)
    ctx.update({
        'total_assets': total_assets,
        'allocated_assets': allocated_assets,
        'pending_allocations': pending_allocations,
        'pending_transfers': pending_transfers,
        'active_bookings': active_bookings,
        'recent_allocations': recent_allocations,
        'recent_transfers': recent_transfers,
        'upcoming_bookings': upcoming_bookings,
    })
    return render(request, 'manager/index.html', ctx)


def home(request):
    return index(request)


# --------------------------------------------------------------------------
# All Assets
# --------------------------------------------------------------------------

@mgr_login_required
def assets(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            try:
                assigned_to_id = request.POST.get('assigned_to')
                assigned_user = user.objects.get(id=assigned_to_id) if assigned_to_id else None
                status = 'Allocated' if assigned_user else request.POST.get('status', 'Available')

                Asset.objects.create(
                    asset_id=_next_id(Asset, 'asset_id', 'AST', 1001),
                    name=request.POST.get('name', '').strip(),
                    category=request.POST.get('category', 'Other'),
                    status=status,
                    assigned_to=assigned_user,
                    location=request.POST.get('location', '').strip(),
                    allocation_date=request.POST.get('allocation_date') or None,
                    expected_return=request.POST.get('expected_return') or None,
                )
                messages.success(request, 'Asset created successfully.')
            except Exception as e:
                messages.error(request, f'Failed to create asset: {e}')
        
        return redirect('mgr_assets')

    all_assets = Asset.objects.select_related('assigned_to').order_by('-id')
    all_users = user.objects.all()
    ctx = _ctx(request)
    ctx.update({
        'assets': all_assets,
        'all_users': all_users
    })
    return render(request, 'manager/assets.html', ctx)


# --------------------------------------------------------------------------
# Allocation Requests (Manager can approve/reject AND create)
# --------------------------------------------------------------------------

@mgr_login_required
def allocations(request):
    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'create':
            try:
                requester = user.objects.get(id=request.POST.get('employee_id'))
                AllocationRequest.objects.create(
                    request_id=_next_id(AllocationRequest, 'request_id', 'AR', 3001),
                    employee=requester,
                    asset_name=request.POST.get('asset_name', ''),
                    category=request.POST.get('category', ''),
                    remarks=request.POST.get('remarks', ''),
                    status='Pending',
                )
                messages.success(request, 'Allocation request submitted successfully!')
            except Exception as e:
                messages.error(request, f'Failed to create request: {e}')

        elif action in ['Approved', 'Rejected']:
            req_id = request.POST.get('request_id')
            try:
                alloc = AllocationRequest.objects.get(id=req_id)
                alloc.status = action
                alloc.save()
                messages.success(request, f'Request {alloc.request_id} has been {action.lower()}.')
            except AllocationRequest.DoesNotExist:
                messages.error(request, 'Request not found.')

        return redirect('mgr_allocations')

    all_allocations = AllocationRequest.objects.select_related('employee').order_by('-request_date')
    all_users = user.objects.all()
    ctx = _ctx(request)
    ctx.update({
        'allocations': all_allocations,
        'all_users': all_users,
    })
    return render(request, 'manager/allocations.html', ctx)


# --------------------------------------------------------------------------
# Transfer Requests (Manager can approve/reject AND create)
# --------------------------------------------------------------------------

@mgr_login_required
def transfers(request):
    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'create':
            try:
                from_emp = user.objects.get(id=request.POST.get('from_employee'))
                to_emp = user.objects.get(id=request.POST.get('to_employee'))
                asset = Asset.objects.get(id=request.POST.get('asset_id'))
                TransferRequest.objects.create(
                    transfer_id=_next_id(TransferRequest, 'transfer_id', 'TR', 8801),
                    asset=asset,
                    from_employee=from_emp,
                    to_employee=to_emp,
                    reason=request.POST.get('reason', ''),
                    status='Pending',
                )
                messages.success(request, 'Transfer request submitted successfully!')
            except Exception as e:
                messages.error(request, f'Failed to create transfer: {e}')

        elif action in ['Approved', 'Rejected']:
            req_id = request.POST.get('request_id')
            try:
                transfer = TransferRequest.objects.get(id=req_id)
                transfer.status = action
                transfer.save()
                
                # Apply the transfer if approved
                if action == 'Approved':
                    a = transfer.asset
                    a.assigned_to = transfer.to_employee
                    a.save()
                
                messages.success(request, f'Transfer {transfer.transfer_id} has been {action.lower()}.')
            except TransferRequest.DoesNotExist:
                messages.error(request, 'Transfer not found.')

        return redirect('mgr_transfers')

    all_transfers = TransferRequest.objects.select_related('asset', 'from_employee', 'to_employee').order_by('-request_date')
    all_users = user.objects.all()
    all_assets = Asset.objects.filter(status='Allocated')
    ctx = _ctx(request)
    ctx.update({
        'transfers': all_transfers,
        'all_users': all_users,
        'all_assets': all_assets,
    })
    return render(request, 'manager/transfers.html', ctx)


# --------------------------------------------------------------------------
# Bookings
# --------------------------------------------------------------------------

@mgr_login_required
def bookings(request):
    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'create':
            try:
                booked_user = user.objects.get(id=request.session['user_id'])
                ResourceBooking.objects.create(
                    booking_id=_next_id(ResourceBooking, 'booking_id', 'BK', 5001),
                    resource_name=request.POST.get('resource'),
                    booked_by=booked_user,
                    booking_date=request.POST.get('date'),
                    start_time=request.POST.get('start_time'),
                    end_time=request.POST.get('end_time'),
                    purpose=request.POST.get('purpose'),
                    department=request.POST.get('department', 'General'),
                    notes=request.POST.get('notes', ''),
                    status='Active',
                )
                messages.success(request, f'Resource "{request.POST.get("resource")}" booked successfully!')
            except Exception as e:
                messages.error(request, f'Booking failed: {e}')

        elif action == 'cancel':
            try:
                b = ResourceBooking.objects.get(id=request.POST.get('booking_id'))
                b.status = 'Cancelled'
                b.save()
                messages.success(request, f'Booking {b.booking_id} cancelled.')
            except ResourceBooking.DoesNotExist:
                messages.error(request, 'Booking not found.')

        return redirect('mgr_bookings')

    all_bookings = ResourceBooking.objects.select_related('booked_by').order_by('-booking_date')
    ctx = _ctx(request)
    ctx['bookings'] = all_bookings
    return render(request, 'manager/bookings.html', ctx)
