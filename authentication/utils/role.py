ROLE_CHOICES = [
    ("IA", "Institute Admin"),
    ("BA", "Branch Admin"),
    ("AU", "Authority"),
    ("TC", "Teacher"),
    ("SF", "Staff"),
    ("ST", "Student"),
]

ADMIN_ROLES = ["IA", "BA", "AU"]
EMPLOYEE_ROLES = ADMIN_ROLES+["TC", "SF"]
ALL_ROLES = [role for role, data in ROLE_CHOICES]
