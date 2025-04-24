from django.db import models
from django.utils.text import slugify


class Department(models.Model):
    """
    Model representing lean manufacturing departments
    """

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    manager = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        related_name="managed_departments",
        null=True,
        blank=True,
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sub_departments",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class LeanDepartment(models.Model):
    """
    Predefined lean manufacturing departments with standard descriptions
    """

    DEPARTMENT_TYPES = [
        ("PROD", "Production"),
        ("ASSY", "Assembly"),
        ("QUAL", "Quality Assurance"),
        ("SUPP", "Supply Chain"),
        ("ENGR", "Engineering"),
        ("MAINT", "Maintenance"),
        ("PLAN", "Planning"),
        ("OPER", "Operations"),
        ("WRHSE", "Warehouse"),
        ("LOGIS", "Logistics"),
        ("MATLS", "Materials Management"),
        ("RD", "Research & Development"),
        ("TOOL", "Tooling"),
        ("KAIZEN", "Continuous Improvement"),
        ("VSM", "Value Stream"),
        ("KANBAN", "Kanban Management"),
        ("QCONT", "Quality Control"),
        ("LEAN", "Lean Office"),
        ("TPM", "Total Productive Maintenance"),
        ("INNOV", "Innovation"),
    ]

    department = models.OneToOneField(
        Department, on_delete=models.CASCADE, related_name="lean_details"
    )
    department_type = models.CharField(max_length=10, choices=DEPARTMENT_TYPES)
    lean_principles = models.TextField(
        blank=True, help_text="Key lean principles implemented in this department"
    )
    kpis = models.TextField(
        blank=True, help_text="Key Performance Indicators tracked by this department"
    )
    improvement_initiatives = models.TextField(
        blank=True, help_text="Current improvement initiatives"
    )
    takt_time = models.FloatField(
        null=True, blank=True, help_text="Target takt time in minutes"
    )
    lead_time = models.FloatField(
        null=True, blank=True, help_text="Current lead time in days"
    )
    cycle_time = models.FloatField(
        null=True, blank=True, help_text="Average cycle time in minutes"
    )
    oee = models.FloatField(
        null=True, blank=True, help_text="Overall Equipment Effectiveness percentage"
    )

    def __str__(self):
        return f"{self.get_department_type_display()} Lean Details"


class Position(models.Model):
    """
    Model representing common positions/roles in lean manufacturing
    """

    POSITION_LEVELS = [
        ("LEAD", "Leadership"),
        ("SPEC", "Specialist"),
        ("ENG", "Engineering"),
        ("TECH", "Technical"),
        ("OPER", "Operational"),
        ("SUPP", "Support"),
    ]

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    level = models.CharField(max_length=10, choices=POSITION_LEVELS, default="OPER")
    description = models.TextField(blank=True)
    responsibilities = models.TextField(
        blank=True, help_text="Key responsibilities for this position"
    )
    required_skills = models.TextField(
        blank=True, help_text="Skills required for this position"
    )
    departments = models.ManyToManyField(
        Department, through="PositionDepartment", related_name="positions"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["level", "name"]
        verbose_name = "Position"
        verbose_name_plural = "Positions"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PositionDepartment(models.Model):
    """
    Intermediary model linking positions to departments with additional relationship data
    """

    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_primary = models.BooleanField(
        default=False,
        help_text="Whether this is the primary department for this position",
    )
    additional_requirements = models.TextField(
        blank=True,
        help_text="Additional requirements specific to this position in this department",
    )
    headcount = models.PositiveIntegerField(
        default=0, help_text="Number of people with this position in this department"
    )

    class Meta:
        unique_together = ("position", "department")
        verbose_name = "Position-Department Relationship"
        verbose_name_plural = "Position-Department Relationships"

    def __str__(self):
        return f"{self.position} in {self.department}"
