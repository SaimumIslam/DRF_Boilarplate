ROLE_CHOICES = [
    ("IA", "Institute Admin"),
    ("BA", "Branch Admin"),
    ("SA", "Staff Admin"),
    ("TC", "Teacher"),
    ("SF", "Staff"),
    ("AG", "Agent"),
    ("ST", "Student"),
]

ADMIN_ROLES = ["IA", "BA", "SA"]
EMPLOYEE_ROLES = ["TC", "SF"]+ADMIN_ROLES
ALL_ROLES = [role for role, data in ROLE_CHOICES]
