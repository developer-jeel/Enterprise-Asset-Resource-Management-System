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

def dh_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request, 'Please log in to access this page.')
            return redirect('login')
        if request.session.get('user_role') != 'dept_head':
            messages.error(request, 'Access denied. Department Head only.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def _ctx(request, extra=None):
    ctx = {
        'user_name': request.session.get('user_name', 'Dept Head'),
        'user_role': request.session.get('user_role', 'dept_head'),
    }
    if extra:
        ctx.update(extra)
    return ctx


# --------------------------------------------------------------------------
# Dashboard / Index
# --------------------------------------------------------------------------

@dh_login_required
def index(request):
    total_assets = Asset.objects.count()
    allocated_assets = Asset.objects.filter(status='Allocated').count()
    pending_allocations = AllocationRequest.objects.filter(status='Pending').count()
    pending_transfers = TransferRequest.objects.filter(status='Pending').count()
    active_bookings = ResourceBooking.objects.filter(status='Active').count()

    recent_allocations = AllocationRequest.objects.select_related('employee').order_by('-request_date')[:5]
    recent_transfers = TransferRequest.objects.select_related('asset', 'from_employee', 'to_employee').order_by('-request_date')[:5]
    upcoming_bookings = ResourceBooking.objects.filter(status='Active').order_by('booking_date')[:5]

    return render(request, 'dept_head/index.html', _ctx(request, {
        'total_assets': total_assets,
        'allocated_assets': allocated_assets,
        'pending_allocations': pending_allocations,
        'pending_transfers': pending_transfers,
        'active_bookings': active_bookings,
        'recent_allocations': recent_allocations,
        'recent_transfers': recent_transfers,
        'upcoming_bookings': upcoming_bookings,
    }))


def home(request):
    return index(request)


# --------------------------------------------------------------------------
# Assets
# --------------------------------------------------------------------------

@dh_login_required
def assets(request):
    all_assets = Asset.objects.select_related('assigned_to').all()
    return render(request, 'dept_head/assets.html', _ctx(request, {'assets': all_assets}))


# --------------------------------------------------------------------------
# Allocation Requests — Dept Head can submit NEW requests on behalf of team
# --------------------------------------------------------------------------

@dh_login_required
def allocations(request):
    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'create':
            try:
                employee_id = request.POST.get('employee_id') or request.session['user_id']
                requester = user.objects.get(id=employee_id)
                AllocationRequest.objects.create(
                    request_id=_next_id(AllocationRequest, 'request_id', 'AR', 3001),
                    employee=requester,
                    asset_name=request.POST.get('asset_name', '').strip(),
                    category=request.POST.get('category', ''),
                    remarks=request.POST.get('remarks', ''),
                    status='Pending',
                )
                messages.success(request, f'Allocation request submitted for {requester.name}.')
            except user.DoesNotExist:
                messages.error(request, 'Employee not found.')
            except Exception as e:
                messages.error(request, f'Failed to create request: {e}')

        return redirect('dh_allocations')

    all_allocations = AllocationRequest.objects.select_related('employee').order_by('-request_date')
    all_users = user.objects.all()
    return render(request, 'dept_head/allocations.html', _ctx(request, {
        'allocations': all_allocations,
        'all_users': all_users,
    }))


# --------------------------------------------------------------------------
# Transfer Requests — Dept Head can submit new transfers
# --------------------------------------------------------------------------

@dh_login_required
def transfers(request):
    if request.method == 'POST':
        action = request.POST.get('action', '')

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
                messages.success(request, 'Transfer request submitted successfully!')
            except user.DoesNotExist:
                messages.error(request, 'Selected employee not found.')
            except Asset.DoesNotExist:
                messages.error(request, 'Selected asset not found.')
            except Exception as e:
                messages.error(request, f'Failed to create transfer: {e}')

        return redirect('dh_transfers')

    all_transfers = TransferRequest.objects.select_related('asset', 'from_employee', 'to_employee').order_by('-request_date')
    all_users = user.objects.all()
    all_assets = Asset.objects.filter(status='Allocated')
    return render(request, 'dept_head/transfers.html', _ctx(request, {
        'transfers': all_transfers,
        'all_users': all_users,
        'all_assets': all_assets,
    }))


# --------------------------------------------------------------------------
# Resource Bookings — Dept Head can create / cancel bookings
# --------------------------------------------------------------------------

@dh_login_required
def bookings(request):
    if request.method == 'POST':
        action = request.POST.get('action', '')

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
                    department=request.POST.get('department', 'Engineering'),
                    notes=request.POST.get('notes', ''),
                    status='Active',
                )
                messages.success(request, f'Resource "{request.POST.get("resource")}" booked successfully!')
            except user.DoesNotExist:
                messages.error(request, 'Session user not found. Please log in again.')
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

        return redirect('dh_bookings')

    all_bookings = ResourceBooking.objects.select_related('booked_by').order_by('-booking_date')
    return render(request, 'dept_head/bookings.html', _ctx(request, {'bookings': all_bookings}))
