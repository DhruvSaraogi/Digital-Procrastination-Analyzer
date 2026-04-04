from django.contrib import admin
from .models import (
    StudySession, DistractionLog, Habit, Task,
    ProductivityMetrics, SuggestionHistory, BehaviorPattern, Alert
)


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'start_time', 'end_time', 'focus_score', 'duration_minutes')
    list_filter = ('user', 'focus_score')
    search_fields = ('subject', 'notes')


@admin.register(DistractionLog)
class DistractionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'distraction_type', 'duration_minutes', 'timestamp')
    list_filter = ('distraction_type', 'user')


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'target_frequency', 'current_streak', 'longest_streak', 'stability_score')
    list_filter = ('target_frequency', 'is_active')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'priority', 'status', 'deadline')
    list_filter = ('priority', 'status')


@admin.register(ProductivityMetrics)
class ProductivityMetricsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'avg_focus_score', 'total_study_minutes', 'productivity_score')
    list_filter = ('user',)


@admin.register(SuggestionHistory)
class SuggestionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'is_helpful', 'generated_at')
    list_filter = ('category', 'is_helpful')


@admin.register(BehaviorPattern)
class BehaviorPatternAdmin(admin.ModelAdmin):
    list_display = ('user', 'pattern_type', 'confidence', 'data_points', 'is_active')
    list_filter = ('pattern_type',)


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'alert_type', 'severity', 'title', 'is_read', 'created_at')
    list_filter = ('alert_type', 'severity', 'is_read')
