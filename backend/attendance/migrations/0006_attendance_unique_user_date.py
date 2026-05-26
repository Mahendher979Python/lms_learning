import django.utils.timezone
from django.db import migrations, models
from django.db.models import Count, Max


def dedupe_attendance(apps, schema_editor):
    Attendance = apps.get_model("attendance", "Attendance")
    duplicates = (
        Attendance.objects.values("user_id", "date")
        .annotate(cnt=Count("id"), keep_id=Max("id"))
        .filter(cnt__gt=1)
    )
    for row in duplicates:
        Attendance.objects.filter(user_id=row["user_id"], date=row["date"]).exclude(id=row["keep_id"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0005_attendance_status"),
    ]

    operations = [
        migrations.RunPython(dedupe_attendance, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name="attendance",
            name="date",
            field=models.DateField(default=django.utils.timezone.localdate),
        ),
        migrations.AddConstraint(
            model_name="attendance",
            constraint=models.UniqueConstraint(fields=("user", "date"), name="unique_attendance_user_date"),
        ),
    ]
