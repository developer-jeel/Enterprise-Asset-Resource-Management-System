from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
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


def _ctx(request, extra=None):
    ctx = {
        'user_name': request.session.get('user_name', 'Admin'),
        'user_role': request.session.get('user_role', 'admin'),
    }
    if extra:
        ctx.update(extra)
    return ctx


# --------------------------------------------------------------------------
# Authentication
# --------------------------------------------------------------------------

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            login_user = user.objects.get(email=email)
        except user.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'custom_admin/login.html')

        if password == login_user.password or check_password(password, login_user.password):
            request.session['user_id'] = login_user.id
            request.session['user_name'] = login_user.name
            request.session['user_role'] = login_user.role
            login_user.is_active = True
            login_user.save()
            role = login_user.role
            if role == 'dept_head':
                return redirect('dh_index')
            elif role == 'manager':
                return redirect('mgr_index')
            elif role == 'employee':
                return redirect('emp_index')
            else:
                return redirect('admin_index')
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'custom_admin/login.html')

    return render(request, 'custom_admin/login.html')


def logout(request):
    request.session.flush()
    return redirect('login')


# --------------------------------------------------------------------------
# Session guard decorator
# --------------------------------------------------------------------------

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request, 'Please log in to access this page.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


# --------------------------------------------------------------------------
# Dashboard / Index
# --------------------------------------------------------------------------

@login_required
def index(request):
    total_assets = Asset.objects.count()
    allocated_assets = Asset.objects.filter(status='Allocated').count()
    pending_allocations = AllocationRequest.objects.filter(status='Pending').count()
    pending_transfers = TransferRequest.objects.filter(status='Pending').count()
    active_bookings = ResourceBooking.objects.filter(status='Active').count()

    recent_allocations = AllocationRequest.objects.select_related('employee').order_by('-request_date')[:5]
    recent_transfers = TransferRequest.objects.select_related('asset', 'from_employee', 'to_employee').order_by('-request_date')[:5]
    upcoming_bookings = ResourceBooking.objects.filter(status='Active').order_by('booking_date')[:5]

    return render(request, 'custom_admin/index.html', _ctx(request, {
        'total_assets': total_assets,
        'allocated_assets': allocated_assets,
        'pending_allocations': pending_allocations,
        'pending_transfers': pending_transfers,
        'active_bookings': active_bookings,
        'recent_allocations': recent_allocations,
        'recent_transfers': recent_transfers,
        'upcoming_bookings': upcoming_bookings,
    }))


# --------------------------------------------------------------------------
# Assets
# --------------------------------------------------------------------------

@login_required
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
        
        return redirect('admin_assets')

    all_assets = Asset.objects.select_related('assigned_to').order_by('-id')
    all_users = user.objects.all()
    return render(request, 'custom_admin/assets.html', _ctx(request, {
        'assets': all_assets,
        'all_users': all_users
    }))


# --------------------------------------------------------------------------
# Allocations — Admin can create new requests AND approve/reject existing ones
# --------------------------------------------------------------------------

@login_required
def allocations(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        # ── Create a new allocation request ──
        if action == 'create':
            try:
                employee_id = request.POST.get('employee_id')
                requester = user.objects.get(id=employee_id)
                AllocationRequest.objects.create(
                    request_id=_next_id(AllocationRequest, 'request_id', 'AR', 3001),
                    employee=requester,
                    asset_name=request.POST.get('asset_name', '').strip(),
                    category=request.POST.get('category', ''),
                    remarks=request.POST.get('remarks', ''),
                    status='Pending',
                )
                messages.success(request, f'Allocation request created for {requester.name}.')
            except user.DoesNotExist:
                messages.error(request, 'Employee not found.')
            except Exception as e:
                messages.error(request, f'Failed to create request: {e}')

        # ── Approve or Reject ──
        elif action in ('Approved', 'Rejected'):
            req_id = request.POST.get('request_id')
            remarks = request.POST.get('remarks', '')
            try:
                alloc = AllocationRequest.objects.get(id=req_id)
                alloc.status = action
                alloc.remarks = remarks
                alloc.save()
                messages.success(request, f'Request {alloc.request_id} has been {action.lower()}.')
            except AllocationRequest.DoesNotExist:
                messages.error(request, 'Allocation request not found.')

        return redirect('admin_allocations')

    all_allocations = AllocationRequest.objects.select_related('employee').order_by('-request_date')
    all_users = user.objects.all()
    return render(request, 'custom_admin/allocations.html', _ctx(request, {
        'allocations': all_allocations,
        'all_users': all_users,
    }))


# --------------------------------------------------------------------------
# Transfers — Admin can approve/reject
# --------------------------------------------------------------------------

@login_required
def transfers(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks', '')

        if action == 'create':
            try:
                from_emp = user.objects.get(id=request.POST.get('from_employee'))
                to_emp = user.objects.get(id=request.POST.get('to_employee'))
                asset_obj = Asset.objects.get(id=request.POST.get('asset_id'))
                TransferRequest.objects.create(
                    transfer_id=_next_id(TransferRequest, 'transfer_id', 'TR', 8801),
                    asset=asset_obj,
                    from_employee=from_emp,
                    to_employee=to_emp,
                    reason=request.POST.get('reason', ''),
                    status='Pending',
                )
                messages.success(request, 'Transfer request created successfully.')
            except Exception as e:
                messages.error(request, f'Failed to create transfer: {e}')

        elif action in ('Approved', 'Rejected'):
            req_id = request.POST.get('transfer_id')
            try:
                transfer = TransferRequest.objects.get(id=req_id)
                transfer.status = action
                transfer.remarks = remarks
                transfer.save()
                if action == 'Approved':
                    transfer.asset.assigned_to = transfer.to_employee
                    transfer.asset.status = 'Allocated'
                    transfer.asset.save()
                messages.success(request, f'Transfer {transfer.transfer_id} has been {action.lower()}.')
            except TransferRequest.DoesNotExist:
                messages.error(request, 'Transfer request not found.')

        return redirect('admin_transfers')

    all_transfers = TransferRequest.objects.select_related('asset', 'from_employee', 'to_employee').order_by('-request_date')
    all_users = user.objects.all()
    all_assets = Asset.objects.filter(status='Allocated')
    return render(request, 'custom_admin/transfers.html', _ctx(request, {
        'transfers': all_transfers,
        'all_users': all_users,
        'all_assets': all_assets,
    }))


# --------------------------------------------------------------------------
# Bookings
# --------------------------------------------------------------------------

@login_required
def bookings(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create':
            try:
                booked_user = user.objects.get(id=request.session['user_id'])
                ResourceBooking.objects.create(
                    booking_id=_next_id(ResourceBooking, 'booking_id', 'BK', 5001),
                    resource_name=request.POST.get('resource', '').strip(),
                    booked_by=booked_user,
                    booking_date=request.POST.get('date'),
                    start_time=request.POST.get('start_time'),
                    end_time=request.POST.get('end_time'),
                    purpose=request.POST.get('purpose', '').strip(),
                    department=request.POST.get('department', 'Admin'),
                    notes=request.POST.get('notes', ''),
                    status='Active',
                )
                messages.success(request, f'Resource "{request.POST.get("resource")}" booked successfully!')
            except Exception as e:
                messages.error(request, f'Booking failed: {e}')

        elif action == 'cancel':
            booking_id = request.POST.get('booking_id')
            try:
                booking = ResourceBooking.objects.get(id=booking_id)
                booking.status = 'Cancelled'
                booking.save()
                messages.success(request, f'Booking {booking.booking_id} cancelled.')
            except ResourceBooking.DoesNotExist:
                messages.error(request, 'Booking not found.')

        return redirect('admin_bookings')

    all_bookings = ResourceBooking.objects.select_related('booked_by').order_by('-booking_date')
    return render(request, 'custom_admin/bookings.html', _ctx(request, {'bookings': all_bookings}))
