ROLE_CHOICES = [
    ("SA", "Super Admin"),
    ("IA", "Institute Admin"),
    ("BA", "Branch Admin"),
    ("TC", "Teacher"),
    ("SF", "Staff"),
    ("AG", "Agent"),
    ("ST", "Student"),
]

ADMIN_ROLES = ["SA", "IA", "BA"]
EMPLOYEE_ROLES = ["IA", "BA", "TC", "SF"]
ALL_ROLES = [role for role, data in ROLE_CHOICES]
