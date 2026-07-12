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

def emp_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request, 'Please log in to access this page.')
            return redirect('login')
        if request.session.get('user_role') != 'employee':
            messages.error(request, 'Access denied. Employee only.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def _ctx(request):
    """Common context injected into every employee page."""
    return {
        'user_name': request.session.get('user_name', 'Employee'),
        'user_role': request.session.get('user_role', 'employee'),
    }


# --------------------------------------------------------------------------
# Dashboard / Index
# --------------------------------------------------------------------------

@emp_login_required
def index(request):
    user_id = request.session['user_id']
    
    my_assets = Asset.objects.filter(assigned_to_id=user_id)
    my_allocations = AllocationRequest.objects.filter(employee_id=user_id, status='Pending')
    my_bookings = ResourceBooking.objects.filter(booked_by_id=user_id, status='Active')

    recent_allocs = AllocationRequest.objects.filter(employee_id=user_id).order_by('-request_date')[:5]
    recent_transfers = TransferRequest.objects.filter(from_employee_id=user_id).select_related('asset', 'to_employee').order_by('-request_date')[:5]
    upcoming_bookings = ResourceBooking.objects.filter(booked_by_id=user_id, status='Active').order_by('booking_date')[:5]

    ctx = _ctx(request)
    ctx.update({
        'total_my_assets': my_assets.count(),
        'my_pending_allocations': my_allocations.count(),
        'my_active_bookings': my_bookings.count(),
        'recent_allocations': recent_allocs,
        'recent_transfers': recent_transfers,
        'upcoming_bookings': upcoming_bookings,
    })
    return render(request, 'employee/index.html', ctx)


def home(request):
    return index(request)


# --------------------------------------------------------------------------
# My Assets
# --------------------------------------------------------------------------

@emp_login_required
def assets(request):
    user_id = request.session['user_id']
    my_assets = Asset.objects.filter(assigned_to_id=user_id)
    ctx = _ctx(request)
    ctx['assets'] = my_assets
    return render(request, 'employee/assets.html', ctx)


# --------------------------------------------------------------------------
# Allocation Requests
# --------------------------------------------------------------------------

@emp_login_required
def allocations(request):
    user_id = request.session['user_id']
    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'create':
            try:
                requester = user.objects.get(id=user_id)
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
        return redirect('emp_allocations')

    my_allocs = AllocationRequest.objects.filter(employee_id=user_id).order_by('-request_date')
    ctx = _ctx(request)
    ctx['allocations'] = my_allocs
    return render(request, 'employee/allocations.html', ctx)


# --------------------------------------------------------------------------
# Transfer Requests
# --------------------------------------------------------------------------

@emp_login_required
def transfers(request):
    user_id = request.session['user_id']
    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'create':
            try:
                from_emp = user.objects.get(id=user_id)
                to_emp = user.objects.get(id=request.POST.get('to_employee'))
                asset = Asset.objects.get(id=request.POST.get('asset_id'), assigned_to_id=user_id)
                
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
        return redirect('emp_transfers')

    my_transfers = TransferRequest.objects.filter(from_employee_id=user_id).select_related('asset', 'to_employee').order_by('-request_date')
    all_users = user.objects.exclude(id=user_id)
    my_allocated_assets = Asset.objects.filter(assigned_to_id=user_id)
    
    ctx = _ctx(request)
    ctx.update({
        'transfers': my_transfers,
        'all_users': all_users,
        'my_assets': my_allocated_assets,
    })
    return render(request, 'employee/transfers.html', ctx)


# --------------------------------------------------------------------------
# Bookings
# --------------------------------------------------------------------------

@emp_login_required
def bookings(request):
    user_id = request.session['user_id']
    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'create':
            try:
                booked_user = user.objects.get(id=user_id)
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
                b = ResourceBooking.objects.get(id=request.POST.get('booking_id'), booked_by_id=user_id)
                b.status = 'Cancelled'
                b.save()
                messages.success(request, f'Booking {b.booking_id} cancelled.')
            except ResourceBooking.DoesNotExist:
                messages.error(request, 'Booking not found or not authorized.')

        return redirect('emp_bookings')

    my_bookings = ResourceBooking.objects.filter(booked_by_id=user_id).order_by('-booking_date')
    ctx = _ctx(request)
    ctx['bookings'] = my_bookings
    return render(request, 'employee/bookings.html', ctx)
