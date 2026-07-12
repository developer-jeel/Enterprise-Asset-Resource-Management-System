from django.db import models


class user(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('dept_head', 'Department Head'),
        ('employee', 'Employee'),
    ]
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.role})"


class Asset(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Allocated', 'Allocated'),
        ('Under Maintenance', 'Under Maintenance'),
        ('Retired', 'Retired'),
    ]
    CATEGORY_CHOICES = [
        ('Laptops', 'Laptops'),
        ('Monitors', 'Monitors'),
        ('Phones', 'Phones'),
        ('Tablets', 'Tablets'),
        ('Chairs', 'Chairs'),
        ('Headsets', 'Headsets'),
        ('Other', 'Other'),
    ]
    asset_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    purchase_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    condition = models.CharField(max_length=50, default='Good')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Available')
    location = models.CharField(max_length=200, blank=True, null=True)
    assigned_to = models.ForeignKey(user, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    allocation_date = models.DateField(blank=True, null=True)
    expected_return = models.DateField(blank=True, null=True)
    last_audit_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset_id} — {self.name}"


class AllocationRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    request_id = models.CharField(max_length=20, unique=True)
    employee = models.ForeignKey(user, on_delete=models.CASCADE, related_name='allocation_requests')
    asset_name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    remarks = models.TextField(blank=True, null=True)
    request_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.request_id} — {self.asset_name} ({self.status})"


class TransferRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    transfer_id = models.CharField(max_length=20, unique=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='transfers')
    from_employee = models.ForeignKey(user, on_delete=models.CASCADE, related_name='transfers_from')
    to_employee = models.ForeignKey(user, on_delete=models.CASCADE, related_name='transfers_to')
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    remarks = models.TextField(blank=True, null=True)
    request_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.transfer_id} — {self.asset.name} ({self.status})"


class ResourceBooking(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]
    booking_id = models.CharField(max_length=20, unique=True)
    resource_name = models.CharField(max_length=200)
    booked_by = models.ForeignKey(user, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    purpose = models.CharField(max_length=300)
    department = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking_id} — {self.resource_name} on {self.booking_date}"
