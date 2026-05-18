from django.contrib import admin
from .models import Assignment, Question, Option, Submission, Answer, Trainer, Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name",)


class OptionInline(admin.TabularInline):
    model = Option
    extra = 4


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):

    list_display = ("title", "test_type", "status")
    list_filter = ("test_type", "status")
    search_fields = ("title",)

    inlines = []   # IMPORTANT: remove default inline

    def get_inlines(self, request, obj=None):
        """
        Show MCQ questions ONLY if test_type = mcq
        """
        if obj and obj.test_type == "mcq":
            return [QuestionInline]
        return []

    def get_readonly_fields(self, request, obj=None):
        return ("created_by",)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]


admin.site.register(Option)
admin.site.register(Submission)
admin.site.register(Answer)
admin.site.register(Trainer)