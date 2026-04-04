from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class StudySession(models.Model):
    """Track individual study sessions with focus metrics."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    subject = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    focus_score = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        help_text="Self-rated focus score from 1 (distracted) to 10 (deep focus)"
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def duration_minutes(self):
        delta = self.end_time - self.start_time
        return round(delta.total_seconds() / 60, 1)

    @property
    def duration_hours(self):
        return round(self.duration_minutes / 60, 2)

    def __str__(self):
        return f"{self.subject} - {self.start_time.strftime('%b %d, %Y %H:%M')}"

    class Meta:
        ordering = ['-start_time']


class DistractionLog(models.Model):
    """Record distractions during study sessions."""
    DISTRACTION_TYPES = [
        ('social_media', 'Social Media'),
        ('phone', 'Phone Notifications'),
        ('people', 'People / Conversations'),
        ('food', 'Food / Snacks'),
        ('daydreaming', 'Daydreaming'),
        ('entertainment', 'Entertainment (TV, Games)'),
        ('internet', 'Internet Browsing'),
        ('noise', 'Noise / Environment'),
        ('fatigue', 'Fatigue / Sleepiness'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='distractions')
    session = models.ForeignKey(
        StudySession, on_delete=models.CASCADE, related_name='distractions',
        blank=True, null=True
    )
    distraction_type = models.CharField(max_length=50, choices=DISTRACTION_TYPES)
    duration_minutes = models.PositiveIntegerField(help_text="Distraction duration in minutes")
    context = models.TextField(
        blank=True, null=True,
        help_text="What were you doing when you got distracted?"
    )
    timestamp = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_distraction_type_display()} - {self.duration_minutes} min"

    class Meta:
        ordering = ['-timestamp']


class Habit(models.Model):
    """Track recurring habits with streaks and consistency."""
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('custom', 'Custom'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    target_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='daily')
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    total_completions = models.PositiveIntegerField(default=0)
    last_completed = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def stability_score(self):
        """Calculate habit stability (0-100) based on streak and consistency."""
        if self.total_completions == 0:
            return 0
        days_since_creation = max((timezone.now().date() - self.created_at.date()).days, 1)
        if self.target_frequency == 'daily':
            expected = days_since_creation
        elif self.target_frequency == 'weekly':
            expected = max(days_since_creation // 7, 1)
        else:
            expected = max(days_since_creation // 3, 1)
        consistency = min(self.total_completions / expected, 1.0)
        streak_bonus = min(self.current_streak / 30, 0.3)  # Max 30% bonus for 30-day streak
        return min(round((consistency + streak_bonus) * 100), 100)

    def __str__(self):
        return f"{self.name} (streak: {self.current_streak})"

    class Meta:
        ordering = ['-current_streak']


class Task(models.Model):
    """Task management with priority and deadline tracking."""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    deadline = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_overdue(self):
        if self.deadline and self.status != 'completed':
            return timezone.now() > self.deadline
        return False

    def __str__(self):
        return f"{self.title} [{self.get_priority_display()}]"

    class Meta:
        ordering = ['-priority', 'deadline']


class ProductivityMetrics(models.Model):
    """Derived daily productivity metrics for trend analysis."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productivity_metrics')
    date = models.DateField()
    total_study_minutes = models.FloatField(default=0)
    avg_focus_score = models.FloatField(default=0)
    total_distraction_minutes = models.FloatField(default=0)
    distraction_ratio = models.FloatField(
        default=0,
        help_text="Ratio of distraction time to study time"
    )
    sessions_count = models.PositiveIntegerField(default=0)
    tasks_completed = models.PositiveIntegerField(default=0)
    habits_completed = models.PositiveIntegerField(default=0)
    productivity_score = models.FloatField(
        default=0,
        help_text="Overall productivity score (0-100)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Metrics for {self.date} - Score: {self.productivity_score}"

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']
        verbose_name_plural = "Productivity metrics"


class SuggestionHistory(models.Model):
    """Store generated suggestions and track effectiveness."""
    CATEGORY_CHOICES = [
        ('focus', 'Focus Improvement'),
        ('distraction', 'Distraction Management'),
        ('habit', 'Habit Building'),
        ('task', 'Task Management'),
        ('schedule', 'Schedule Optimization'),
        ('wellness', 'Wellness & Breaks'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='suggestions')
    suggestion_text = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    is_helpful = models.BooleanField(null=True, blank=True, help_text="User feedback on suggestion")
    is_read = models.BooleanField(default=False)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_category_display()}: {self.suggestion_text[:50]}..."

    class Meta:
        ordering = ['-generated_at']
        verbose_name_plural = "Suggestion histories"


class BehaviorPattern(models.Model):
    """Detected behavioral patterns from analytics."""
    PATTERN_TYPES = [
        ('peak_focus', 'Peak Focus Time'),
        ('low_focus', 'Low Focus Time'),
        ('distraction_trigger', 'Distraction Trigger'),
        ('productive_habit', 'Productive Habit'),
        ('procrastination', 'Procrastination Pattern'),
        ('improvement', 'Improvement Trend'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='behavior_patterns')
    pattern_type = models.CharField(max_length=30, choices=PATTERN_TYPES)
    description = models.TextField()
    confidence = models.FloatField(
        default=0.5,
        help_text="Confidence score 0.0 to 1.0"
    )
    data_points = models.PositiveIntegerField(default=0, help_text="Number of data points supporting this pattern")
    first_detected = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_pattern_type_display()}: {self.description[:50]}"

    class Meta:
        ordering = ['-confidence']


class Alert(models.Model):
    """Notifications and alerts for the user."""
    ALERT_TYPES = [
        ('streak_broken', 'Streak Broken'),
        ('streak_milestone', 'Streak Milestone'),
        ('low_focus', 'Low Focus Warning'),
        ('high_distraction', 'High Distraction Warning'),
        ('task_overdue', 'Task Overdue'),
        ('goal_achieved', 'Goal Achieved'),
        ('improvement', 'Improvement Detected'),
        ('reminder', 'Study Reminder'),
    ]
    SEVERITY_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('danger', 'Danger'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='info')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_dismissed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_severity_display()}] {self.title}"

    class Meta:
        ordering = ['-created_at']
