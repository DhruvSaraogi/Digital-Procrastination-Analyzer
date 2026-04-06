

from django.utils import timezone
from django.db.models import Avg, Sum, Count
from datetime import timedelta


def analyze_and_suggest(user):
    from .models import (
        StudySession, DistractionLog, Habit, Task,
        ProductivityMetrics, SuggestionHistory, BehaviorPattern, Alert
    )

    suggestions = []
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)


    recent_sessions = StudySession.objects.filter(user=user, start_time__gte=week_ago)
    recent_distractions = DistractionLog.objects.filter(user=user, timestamp__gte=week_ago)
    active_habits = Habit.objects.filter(user=user, is_active=True)
    pending_tasks = Task.objects.filter(user=user).exclude(status='completed')
    month_sessions = StudySession.objects.filter(user=user, start_time__gte=month_ago)

    if not recent_sessions.exists():
        suggestions.append({
            'text': "You haven't logged any study sessions this week. Start with just 25 minutes today using the Pomodoro technique — small wins build momentum!",
            'category': 'focus'
        })

    if recent_sessions.exists():
        avg_focus = recent_sessions.aggregate(avg=Avg('focus_score'))['avg'] or 0
        if avg_focus < 4:
            suggestions.append({
                'text': f"Your average focus score this week is {avg_focus:.1f}/10. Try eliminating your top distraction source before starting your next session. Consider the 2-minute rule: if a distraction takes less than 2 minutes, note it down and address it after your study block.",
                'category': 'focus'
            })
        elif avg_focus < 6:
            suggestions.append({
                'text': f"Your focus score averages {avg_focus:.1f}/10. You're doing okay but there's room for improvement. Try studying in a different environment or using noise-cancelling headphones.",
                'category': 'focus'
            })
        elif avg_focus >= 8:
            suggestions.append({
                'text': f"Excellent focus! Your average score is {avg_focus:.1f}/10. Keep this momentum going. Consider gradually extending your study sessions by 10 minutes.",
                'category': 'focus'
            })
    if recent_distractions.exists():
        distraction_count = recent_distractions.count()
        if distraction_count > 15:
            suggestions.append({
                'text': f"You logged {distraction_count} distractions this week. That's quite high. Try the 'distraction notepad' technique: write down urges instead of acting on them, and review them after your study session.",
                'category': 'distraction'
            })

    if recent_distractions.exists():
        top_distraction = (
            recent_distractions
            .values('distraction_type')
            .annotate(total=Sum('duration_minutes'))
            .order_by('-total')
            .first()
        )
        if top_distraction:
            dtype = top_distraction['distraction_type']
            total_mins = top_distraction['total']
            type_labels = dict(DistractionLog.DISTRACTION_TYPES)
            label = type_labels.get(dtype, dtype)

            distraction_tips = {
                'social_media': "Use app blockers like Forest or Cold Turkey during study sessions. Set specific social media check-in times.",
                'phone': "Put your phone in another room or use Do Not Disturb mode. The physical distance creates a friction barrier.",
                'daydreaming': "Try active recall study methods instead of passive reading. Engage your mind with practice problems or teaching the material.",
                'entertainment': "Remove entertainment shortcuts from your study device. Create a separate 'study-only' browser profile.",
                'fatigue': "You might be studying at suboptimal times. Track your energy levels and study during peak alertness hours.",
                'internet': "Use website blockers and consider downloading study materials for offline access.",
                'noise': "Try noise-cancelling headphones, white noise apps, or find a quieter study location.",
                'food': "Prepare snacks before your study session so you don't need to break your flow.",
                'people': "Communicate your study schedule to people around you. Use a 'do not disturb' sign.",
            }
            tip = distraction_tips.get(dtype, "Identify the trigger and create a plan to minimize it.")
            suggestions.append({
                'text': f"Your biggest time drain is '{label}' ({total_mins} minutes lost this week). {tip}",
                'category': 'distraction'
            })


    if recent_sessions.exists() and recent_distractions.exists():
        total_study = sum(s.duration_minutes for s in recent_sessions)
        total_distraction = recent_distractions.aggregate(total=Sum('duration_minutes'))['total'] or 0
        if total_study > 0:
            ratio = total_distraction / total_study
            if ratio > 0.3:
                suggestions.append({
                    'text': f"Your distraction-to-study ratio is {ratio:.0%} — nearly a third of your study time is lost. Try shorter, more intense study blocks (25 min) with 5-min breaks.",
                    'category': 'distraction'
                })

    broken_habits = active_habits.filter(current_streak=0, total_completions__gt=0)
    if broken_habits.exists():
        names = ', '.join(h.name for h in broken_habits[:3])
        suggestions.append({
            'text': f"You've broken your streak on: {names}. Don't let the 'what-the-hell' effect kick in — restart today with a minimal version of each habit.",
            'category': 'habit'
        })

    low_stability = [h for h in active_habits if h.stability_score < 30 and h.total_completions > 0]
    if low_stability:
        suggestions.append({
            'text': "Some of your habits have low consistency. Try habit stacking — attach new habits to existing routines (e.g., 'After my morning coffee, I will study for 20 minutes').",
            'category': 'habit'
        })

    if not active_habits.exists():
        suggestions.append({
            'text': "You don't have any active habits tracked. Start with one small daily habit related to your studies — consistency beats intensity.",
            'category': 'habit'
        })

    # --- Rule 9: Overdue tasks ---
    overdue = [t for t in pending_tasks if t.is_overdue]
    if len(overdue) > 0:
        suggestions.append({
            'text': f"You have {len(overdue)} overdue task(s). Prioritize the most important one and break it into smaller, actionable steps. Completing even a small part reduces procrastination anxiety.",
            'category': 'task'
        })

    if pending_tasks.count() > 10:
        suggestions.append({
            'text': f"You have {pending_tasks.count()} pending tasks — that's a lot! Use the Eisenhower Matrix: categorize by urgency and importance. Eliminate or delegate non-essential tasks.",
            'category': 'task'
        })

    if not Task.objects.filter(user=user).exists():
        suggestions.append({
            'text': "You haven't created any tasks yet. Planning your work reduces decision fatigue and procrastination. Add your top 3 priorities for this week.",
            'category': 'task'
        })

    if recent_sessions.exists():
        avg_duration = sum(s.duration_minutes for s in recent_sessions) / recent_sessions.count()
        if avg_duration < 20:
            suggestions.append({
                'text': f"Your average session is only {avg_duration:.0f} minutes. Short sessions can indicate difficulty maintaining focus. Try the Pomodoro technique: 25 min study, 5 min break.",
                'category': 'schedule'
            })

    if month_sessions.count() >= 5:
        morning = month_sessions.filter(start_time__hour__lt=12).aggregate(avg=Avg('focus_score'))['avg'] or 0
        afternoon = month_sessions.filter(start_time__hour__gte=12, start_time__hour__lt=17).aggregate(avg=Avg('focus_score'))['avg'] or 0
        evening = month_sessions.filter(start_time__hour__gte=17).aggregate(avg=Avg('focus_score'))['avg'] or 0

        best_time = max(
            [('morning (before noon)', morning), ('afternoon (12-5 PM)', afternoon), ('evening (after 5 PM)', evening)],
            key=lambda x: x[1]
        )
        if best_time[1] > 0:
            suggestions.append({
                'text': f"Your highest focus scores tend to be in the {best_time[0]} with an average of {best_time[1]:.1f}/10. Schedule your most challenging tasks during this time.",
                'category': 'schedule'
            })

    if recent_sessions.exists():
        total_hours = sum(s.duration_hours for s in recent_sessions)
        if total_hours > 35:
            suggestions.append({
                'text': f"You've studied {total_hours:.1f} hours this week — impressive but don't burn out! Take regular breaks, exercise, and get 7-8 hours of sleep for optimal cognitive performance.",
                'category': 'wellness'
            })

    metrics = ProductivityMetrics.objects.filter(user=user).order_by('-date')[:14]
    if metrics.count() >= 7:
        recent_avg = sum(m.productivity_score for m in metrics[:7]) / 7
        older_avg = sum(m.productivity_score for m in metrics[7:14]) / min(metrics.count() - 7, 7)
        if recent_avg > older_avg * 1.15:
            suggestions.append({
                'text': f"Great progress! Your productivity score improved by {((recent_avg/older_avg)-1)*100:.0f}% compared to last week. Keep up the great work!",
                'category': 'focus'
            })

    if not suggestions:
        suggestions.append({
            'text': "Keep logging your study sessions and habits to get personalized insights. The more data you provide, the smarter your suggestions become!",
            'category': 'focus'
        })

    return suggestions


def compute_daily_metrics(user, date=None):
    """Compute and store productivity metrics for a given date."""
    from .models import StudySession, DistractionLog, Habit, Task, ProductivityMetrics

    if date is None:
        date = timezone.now().date()

    sessions = StudySession.objects.filter(
        user=user,
        start_time__date=date
    )
    distractions = DistractionLog.objects.filter(
        user=user,
        timestamp__date=date
    )

    total_study = sum(s.duration_minutes for s in sessions)
    avg_focus = sessions.aggregate(avg=Avg('focus_score'))['avg'] or 0
    total_distraction = distractions.aggregate(total=Sum('duration_minutes'))['total'] or 0
    distraction_ratio = (total_distraction / total_study) if total_study > 0 else 0
    tasks_done = Task.objects.filter(user=user, completed_at__date=date).count()
    habits_done = Habit.objects.filter(user=user, last_completed=date).count()

    # Productivity formula: weighted combination
    focus_component = (avg_focus / 10) * 40  # 40% weight
    study_component = min(total_study / 240, 1.0) * 30  # 30% weight (4h = 100%)
    distraction_penalty = min(distraction_ratio, 1.0) * 20  # -20% max
    task_bonus = min(tasks_done / 3, 1.0) * 10  # 10% weight
    habit_bonus = min(habits_done / 3, 1.0) * 10  # not used but calculated

    productivity_score = max(0, focus_component + study_component - distraction_penalty + task_bonus)

    metrics, _ = ProductivityMetrics.objects.update_or_create(
        user=user,
        date=date,
        defaults={
            'total_study_minutes': total_study,
            'avg_focus_score': round(avg_focus, 2),
            'total_distraction_minutes': total_distraction,
            'distraction_ratio': round(distraction_ratio, 4),
            'sessions_count': sessions.count(),
            'tasks_completed': tasks_done,
            'habits_completed': habits_done,
            'productivity_score': round(productivity_score, 2),
        }
    )
    return metrics


def detect_patterns(user):
    """Detect behavioral patterns from historical data."""
    from .models import StudySession, DistractionLog, BehaviorPattern

    now = timezone.now()
    month_ago = now - timedelta(days=30)
    sessions = StudySession.objects.filter(user=user, start_time__gte=month_ago)

    if sessions.count() < 5:
        return

    # Peak focus time detection
    morning = sessions.filter(start_time__hour__lt=12)
    afternoon = sessions.filter(start_time__hour__gte=12, start_time__hour__lt=17)
    evening = sessions.filter(start_time__hour__gte=17)

    time_blocks = {
        'Morning (6 AM - 12 PM)': morning,
        'Afternoon (12 PM - 5 PM)': afternoon,
        'Evening (5 PM onwards)': evening,
    }

    for label, qs in time_blocks.items():
        if qs.count() >= 3:
            avg = qs.aggregate(avg=Avg('focus_score'))['avg'] or 0
            if avg >= 7:
                BehaviorPattern.objects.update_or_create(
                    user=user,
                    pattern_type='peak_focus',
                    description__contains=label,
                    defaults={
                        'description': f"Peak focus detected during {label} with average score {avg:.1f}/10",
                        'confidence': min(avg / 10, 1.0),
                        'data_points': qs.count(),
                    }
                )
            elif avg <= 4:
                BehaviorPattern.objects.update_or_create(
                    user=user,
                    pattern_type='low_focus',
                    description__contains=label,
                    defaults={
                        'description': f"Low focus detected during {label} with average score {avg:.1f}/10",
                        'confidence': min((10 - avg) / 10, 1.0),
                        'data_points': qs.count(),
                    }
                )

    # Distraction trigger detection
    distractions = DistractionLog.objects.filter(user=user, timestamp__gte=month_ago)
    if distractions.count() >= 5:
        top = (
            distractions
            .values('distraction_type')
            .annotate(count=Count('id'), total_mins=Sum('duration_minutes'))
            .order_by('-total_mins')
            .first()
        )
        if top:
            type_labels = dict(DistractionLog.DISTRACTION_TYPES)
            label = type_labels.get(top['distraction_type'], top['distraction_type'])
            BehaviorPattern.objects.update_or_create(
                user=user,
                pattern_type='distraction_trigger',
                defaults={
                    'description': f"Primary distraction trigger: {label} ({top['total_mins']} minutes over {top['count']} occurrences)",
                    'confidence': min(top['count'] / 20, 1.0),
                    'data_points': top['count'],
                }
            )


def generate_alerts(user):
    """Generate alerts based on current user state."""
    from .models import Habit, Task, Alert, StudySession

    now = timezone.now()
    today = now.date()

    # Streak broken alerts
    for habit in Habit.objects.filter(user=user, is_active=True):
        if habit.last_completed and habit.target_frequency == 'daily':
            days_since = (today - habit.last_completed).days
            if days_since >= 2:
                if not Alert.objects.filter(
                    user=user, alert_type='streak_broken',
                    title__contains=habit.name, created_at__date=today
                ).exists():
                    Alert.objects.create(
                        user=user,
                        alert_type='streak_broken',
                        severity='warning',
                        title=f"Streak broken: {habit.name}",
                        message=f"You haven't completed '{habit.name}' in {days_since} days. Your streak was reset. Don't give up — restart today!"
                    )

    # Streak milestone alerts
    for habit in Habit.objects.filter(user=user, is_active=True):
        milestones = [7, 14, 21, 30, 60, 100]
        if habit.current_streak in milestones:
            if not Alert.objects.filter(
                user=user, alert_type='streak_milestone',
                title__contains=str(habit.current_streak), created_at__date=today
            ).exists():
                Alert.objects.create(
                    user=user,
                    alert_type='streak_milestone',
                    severity='success',
                    title=f"🎉 {habit.current_streak}-day streak: {habit.name}!",
                    message=f"Amazing! You've maintained '{habit.name}' for {habit.current_streak} consecutive days. Keep going!"
                )

    # Task overdue alerts
    overdue_tasks = Task.objects.filter(user=user, deadline__lt=now).exclude(status='completed')
    for task in overdue_tasks:
        if not Alert.objects.filter(
            user=user, alert_type='task_overdue',
            title__contains=task.title[:50], created_at__date=today
        ).exists():
            Alert.objects.create(
                user=user,
                alert_type='task_overdue',
                severity='danger',
                title=f"Overdue: {task.title}",
                message=f"'{task.title}' was due on {task.deadline.strftime('%b %d at %I:%M %p')}. Complete it ASAP or update the deadline."
            )

    # Low focus warning
    recent = StudySession.objects.filter(user=user, start_time__date=today)
    if recent.count() >= 2:
        avg = recent.aggregate(avg=Avg('focus_score'))['avg'] or 0
        if avg < 4:
            if not Alert.objects.filter(
                user=user, alert_type='low_focus', created_at__date=today
            ).exists():
                Alert.objects.create(
                    user=user,
                    alert_type='low_focus',
                    severity='warning',
                    title="Low focus detected today",
                    message=f"Your average focus score today is {avg:.1f}/10. Consider taking a break, going for a walk, or switching study methods."
                )
