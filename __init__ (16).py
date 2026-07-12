from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import JsonResponse

from core.decorators import check_login
from core.models import (
    Asset,
    AssetAllocation,
    AssetTransfer,
    AssetReturn,
    MaintenanceRequest,
    Resource,
    ResourceBooking,
    ActivityLog,
    Notification,
    LeaveRequest,
)
import datetime

@login_required
@check_login(['employee'])
def index(request):
    profile = request.user.profile
    my_assets = Asset.objects.filter(assigned_to=request.user)
    bookings = ResourceBooking.objects.filter(booked_by=request.user)
    maint = MaintenanceRequest.objects.filter(reported_by=request.user)
    reqs = AssetAllocation.objects.filter(requested_by=request.user) # Or merge Return/Transfer requests
    
    context = {
        'profile': profile,
        'my_assets_count': my_assets.count(),
        'bookings_count': bookings.filter(status='Active').count(),
        'maint_count': maint.count(),
        'requests_count': reqs.filter(status='Pending').count()
    }
    return render(request, 'employee/index.html', context)

@login_required
@check_login(['employee'])
def get_dashboard_data(request):
    profile = request.user.profile
    my_assets = Asset.objects.filter(assigned_to=request.user)
    bookings = ResourceBooking.objects.filter(booked_by=request.user)
    resources = Resource.objects.all()
    maint = MaintenanceRequest.objects.filter(reported_by=request.user)
    
    # Custom model combination for requests
    allocations = AssetAllocation.objects.filter(requested_by=request.user)
    transfers = AssetTransfer.objects.filter(from_employee=request.user)
    returns = AssetReturn.objects.filter(employee=request.user)
    
    activities = ActivityLog.objects.filter(user=request.user).order_by('-id')[:5]

    employee_info = {
        'id': profile.employee_id,
        'name': request.user.username,
        'email': request.user.email,
        'department': profile.department or '—',
        'role': profile.get_role_display(),
        'avatar': profile.profile_pic.url if profile.profile_pic else (request.user.username[:2].upper() if request.user.username else 'EM')
    }

    my_assets_list = []
    for a in my_assets:
        my_assets_list.append({
            'id': a.tag,
            'name': a.name,
            'tag': a.tag,
            'category': a.category,
            'serial': a.serial,
            'condition': a.condition,
            'status': a.lifecycle,
            'department': a.department or '—',
            'location': a.location,
            'allocDate': str(a.acquired),
            'returnDate': str(a.acquired + datetime.timedelta(days=365)), # Mock return date
            'vendor': a.vendor or '—',
            'cost': float(a.cost),
            'warranty': str(a.warranty) if a.warranty else '—',
            'notes': a.notes or ''
        })

    bookings_list = []
    for b in bookings:
        bookings_list.append({
            'id': b.booking_id,
            'resource': b.resource.name,
            'type': b.resource.type,
            'capacity': b.resource.capacity,
            'date': str(b.date),
            'start': b.start_time,
            'end': b.end_time,
            'purpose': b.purpose,
            'status': b.status,
            'notes': b.notes or ''
        })

    resources_list = []
    for r in resources:
        resources_list.append({
            'id': r.resource_id,
            'name': r.name,
            'type': r.type,
            'capacity': r.capacity,
            'floor': r.floor,
            'icon': r.icon,
            'availability': r.availability
        })

    maint_list = []
    for m in maint:
        maint_list.append({
            'id': m.maintenance_id,
            'assetId': m.asset.tag,
            'assetName': m.asset.name,
            'priority': m.priority,
            'issue': m.issue,
            'submittedDate': str(m.report_date),
            'status': m.status,
            'technician': m.technician or 'IT Support Team',
            'remarks': m.remarks or ''
        })

    requests_list = []
    for al in allocations:
        requests_list.append({
            'id': al.allocation_id,
            'type': 'Allocation',
            'assetName': al.asset_name or (al.asset.name if al.asset else ''),
            'submittedDate': str(al.request_date),
            'status': al.status,
            'remarks': al.remarks or ''
        })
    for t in transfers:
        requests_list.append({
            'id': t.transfer_id,
            'type': 'Transfer',
            'assetName': t.asset.name,
            'submittedDate': str(t.request_date),
            'status': t.status,
            'remarks': t.remarks or ''
        })
    for r in returns:
        requests_list.append({
            'id': r.return_id,
            'type': 'Return',
            'assetName': r.asset.name,
            'submittedDate': str(r.expected_return),
            'status': r.status,
            'remarks': r.notes or ''
        })

    activities_list = []
    for act in activities:
        activities_list.append({
            'text': act.text,
            'time': act.time,
            'type': act.type
        })

    return JsonResponse({
        'employee': employee_info,
        'myAssets': my_assets_list,
        'bookings': bookings_list,
        'resources': resources_list,
        'maintenance': maint_list,
        'requests': requests_list,
        'activities': activities_list
    })

@login_required
@check_login(['employee'])
def assets_view(request):
    return render(request, 'employee/assets.html')

@login_required
@check_login(['employee'])
def bookings_view(request):
    return render(request, 'employee/bookings.html')

@login_required
@check_login(['employee'])
def create_booking(request):
    if request.method == 'POST':
        resource_id = request.POST.get('resource_id')
        date_str = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        purpose = request.POST.get('purpose').strip()
        notes = request.POST.get('notes', '').strip()

        resource = get_object_or_404(Resource, resource_id=resource_id)
        booking_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

        # Simple verification of booking overlap (can be optimized but fits standard use case)
        if ResourceBooking.objects.filter(resource=resource, date=booking_date, start_time=start_time, status='Active').exists():
            return JsonResponse({'success': False, 'message': 'This resource is already booked for the selected time slot.'})

        booking_id = f"BK-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')[-4:]}"
        booking = ResourceBooking.objects.create(
            booking_id=booking_id,
            resource=resource,
            booked_by=request.user,
            date=booking_date,
            start_time=start_time,
            end_time=end_time,
            purpose=purpose,
            department=request.user.profile.department or 'Engineering',
            notes=notes
        )

        ActivityLog.objects.create(
            user=request.user,
            text=f"Booking {booking_id} confirmed — {resource.name} for {purpose}",
            time='Just now',
            type='booking'
        )

        return JsonResponse({'success': True, 'message': 'Resource booked successfully.'})

    return JsonResponse({'success': False, 'message': 'Invalid HTTP request.'})

@login_required
@check_login(['employee'])
def cancel_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(ResourceBooking, booking_id=booking_id, booked_by=request.user)
        booking.status = 'Cancelled'
        booking.save()

        ActivityLog.objects.create(
            user=request.user,
            text=f"Booking {booking_id} was cancelled.",
            time='Just now',
            type='booking'
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
@check_login(['employee'])
def maintenance_view(request):
    return render(request, 'employee/maintenance.html')

@login_required
@check_login(['employee'])
def report_issue(request):
    if request.method == 'POST':
        asset_tag = request.POST.get('asset_tag')
        priority = request.POST.get('priority')
        issue = request.POST.get('issue').strip()

        asset = get_object_or_404(Asset, tag=asset_tag, assigned_to=request.user)
        maint_id = f"MR-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')[-4:]}"

        MaintenanceRequest.objects.create(
            maintenance_id=maint_id,
            asset=asset,
            priority=priority,
            issue=issue,
            reported_by=request.user,
            department=request.user.profile.department or 'Engineering'
        )

        ActivityLog.objects.create(
            user=request.user,
            text=f"Submitted Maintenance Request {maint_id} for {asset.name}.",
            time='Just now',
            type='maintenance'
        )
        return JsonResponse({'success': True, 'message': 'Issue reported successfully.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required
@check_login(['employee'])
def requests_view(request):
    return render(request, 'employee/requests.html')

@login_required
@check_login(['employee'])
def submit_request(request):
    if request.method == 'POST':
        # The requests.html template sends the request type as a lowercase
        # string under the key 'request_type' (e.g. 'return' / 'transfer'),
        # and for transfers sends the target username under
        # 'to_employee_username' rather than 'target_employee'. Read the
        # actual keys/casing the frontend sends instead of the old
        # mismatched ones so requests are no longer silently dropped.
        req_type_raw = (request.POST.get('request_type') or '').strip().lower()
        req_type = 'Return' if req_type_raw == 'return' else 'Transfer' if req_type_raw == 'transfer' else None
        asset_tag = request.POST.get('asset_tag')
        reason = (request.POST.get('reason') or '').strip()

        if req_type is None:
            return JsonResponse({'success': False, 'message': 'Invalid request type.'})

        asset = get_object_or_404(Asset, tag=asset_tag, assigned_to=request.user)
        req_id = f"REQ-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')[-4:]}"

        if req_type == 'Return':
            AssetReturn.objects.create(
                return_id=req_id,
                asset=asset,
                employee=request.user,
                department=request.user.profile.department or 'Engineering',
                expected_return=datetime.date.today() + datetime.timedelta(days=1),
                notes=reason
            )
        elif req_type == 'Transfer':
            target_emp_username = (request.POST.get('to_employee_username') or '').strip()
            target_user = get_object_or_404(User, username=target_emp_username)
            AssetTransfer.objects.create(
                transfer_id=req_id,
                asset=asset,
                from_employee=request.user,
                to_employee=target_user,
                to_dept=request.POST.get('to_department') or target_user.profile.department or 'Engineering',
                reason=reason
            )

        ActivityLog.objects.create(
            user=request.user,
            text=f"Submitted {req_type} request {req_id} for {asset.name}.",
            time='Just now',
            type='transfer'
        )

        return JsonResponse({'success': True, 'message': f'{req_type} request submitted.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required
@check_login(['employee'])
def profile_view(request):
    return render(request, 'employee/profile.html')


@login_required
@check_login(['employee'])
def get_profile_data(request):
    profile = request.user.profile
    data = {
        'username': request.user.username,
        'firstName': request.user.first_name,
        'lastName': request.user.last_name,
        'email': request.user.email,
        'phone': profile.phone or '',
        'department': profile.department or '—',
        'role': profile.get_role_display(),
        'employeeId': profile.employee_id,
        'avatar': profile.profile_pic.url if profile.profile_pic else (request.user.username[:2].upper() if request.user.username else 'EM'),
        'dateJoined': request.user.date_joined.strftime('%Y-%m-%d'),
    }
    return JsonResponse({'success': True, 'profile': data})


@login_required
@check_login(['employee'])
def update_profile(request):
    if request.method == 'POST':
        profile = request.user.profile
        user = request.user

        first_name = (request.POST.get('first_name') or '').strip()
        last_name = (request.POST.get('last_name') or '').strip()
        email = (request.POST.get('email') or '').strip()
        phone = (request.POST.get('phone') or '').strip()

        if email:
            user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        profile.phone = phone
        if request.FILES.get('profile_pic'):
            profile.profile_pic = request.FILES['profile_pic']
        profile.save()

        ActivityLog.objects.create(
            user=request.user,
            text="Updated profile information.",
            time='Just now',
            type='profile'
        )
        return JsonResponse({'success': True, 'message': 'Profile updated successfully.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required
@check_login(['employee'])
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password') or ''
        new_password = request.POST.get('new_password') or ''
        confirm_password = request.POST.get('confirm_password') or ''

        if not request.user.check_password(current_password):
            return JsonResponse({'success': False, 'message': 'Current password is incorrect.'})

        if new_password != confirm_password:
            return JsonResponse({'success': False, 'message': 'New password and confirmation do not match.'})

        form = PasswordChangeForm(user=request.user, data={
            'old_password': current_password,
            'new_password1': new_password,
            'new_password2': confirm_password,
        })

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            ActivityLog.objects.create(
                user=request.user,
                text="Changed account password.",
                time='Just now',
                type='profile'
            )
            return JsonResponse({'success': True, 'message': 'Password changed successfully.'})
        else:
            errors = ' '.join([e for errs in form.errors.values() for e in errs])
            return JsonResponse({'success': False, 'message': errors or 'Unable to change password.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required
@check_login(['employee'])
def notifications_view(request):
    return render(request, 'employee/notifications.html')


@login_required
@check_login(['employee'])
def get_notifications_data(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    data = []
    for n in notifications:
        data.append({
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'isRead': n.is_read,
            'createdAt': n.created_at.strftime('%Y-%m-%d %H:%M'),
        })
    return JsonResponse({'notifications': data, 'unreadCount': notifications.filter(is_read=False).count()})


@login_required
@check_login(['employee'])
def mark_notification_read(request):
    if request.method == 'POST':
        notif_id = request.POST.get('notification_id')
        if notif_id == 'all':
            Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
            return JsonResponse({'success': True})
        notif = get_object_or_404(Notification, id=notif_id, recipient=request.user)
        notif.is_read = True
        notif.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required
@check_login(['employee'])
def leave_view(request):
    return render(request, 'employee/leave.html')


@login_required
@check_login(['employee'])
def get_leave_data(request):
    leaves = LeaveRequest.objects.filter(employee=request.user).order_by('-id')
    data = []
    for l in leaves:
        data.append({
            'id': l.leave_id,
            'type': l.leave_type,
            'startDate': str(l.start_date),
            'endDate': str(l.end_date),
            'days': (l.end_date - l.start_date).days + 1,
            'reason': l.reason,
            'appliedDate': str(l.applied_date),
            'status': l.status,
            'remarks': l.remarks or '',
        })
    return JsonResponse({'leaves': data})


@login_required
@check_login(['employee'])
def submit_leave(request):
    if request.method == 'POST':
        leave_type = request.POST.get('leave_type')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        reason = (request.POST.get('reason') or '').strip()

        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except (TypeError, ValueError):
            return JsonResponse({'success': False, 'message': 'Invalid dates supplied.'})

        if end_date < start_date:
            return JsonResponse({'success': False, 'message': 'End date cannot be before start date.'})

        leave_id = f"LV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')[-4:]}"
        LeaveRequest.objects.create(
            leave_id=leave_id,
            employee=request.user,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            department=request.user.profile.department or 'Engineering',
        )

        ActivityLog.objects.create(
            user=request.user,
            text=f"Submitted {leave_type} leave request {leave_id}.",
            time='Just now',
            type='leave'
        )
        return JsonResponse({'success': True, 'message': 'Leave request submitted successfully.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required
@check_login(['employee'])
def cancel_leave(request):
    if request.method == 'POST':
        leave_id = request.POST.get('leave_id')
        leave = get_object_or_404(LeaveRequest, leave_id=leave_id, employee=request.user)
        if leave.status != 'Pending':
            return JsonResponse({'success': False, 'message': 'Only pending leave requests can be cancelled.'})
        leave.delete()
        ActivityLog.objects.create(
            user=request.user,
            text=f"Cancelled leave request {leave_id}.",
            time='Just now',
            type='leave'
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
