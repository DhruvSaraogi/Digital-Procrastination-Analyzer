from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Avg, Sum, Count
from datetime import timedelta
import json

from .models import (
    StudySession, DistractionLog, Habit, Task,
    ProductivityMetrics, SuggestionHistory, BehaviorPattern, Alert
)
from .forms import RegisterForm, StudySessionForm, DistractionForm, HabitForm, TaskForm
from .suggestion_engine import analyze_and_suggest, compute_daily_metrics, detect_patterns, generate_alerts




def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'analyzer/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'analyzer/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')



@login_required
def dashboard_view(request):
    user = request.user
    now = timezone.now()
    today = now.date()
    week_ago = now - timedelta(days=7)

    # Compute today's metrics
    compute_daily_metrics(user, today)
    generate_alerts(user)

    # Summary stats
    recent_sessions = StudySession.objects.filter(user=user, start_time__gte=week_ago)
    total_study_hours = sum(s.duration_hours for s in recent_sessions)
    avg_focus = recent_sessions.aggregate(avg=Avg('focus_score'))['avg'] or 0
    total_distractions = DistractionLog.objects.filter(user=user, timestamp__gte=week_ago).count()
    active_tasks = Task.objects.filter(user=user).exclude(status='completed').count()
    completed_tasks = Task.objects.filter(user=user, status='completed', completed_at__gte=week_ago).count()

    # Habit streaks
    habits = Habit.objects.filter(user=user, is_active=True)[:5]

    # Recent alerts (unread)
    unread_alerts = Alert.objects.filter(user=user, is_read=False, is_dismissed=False)[:5]

    # Chart data — last 7 days
    chart_dates = []
    chart_study = []
    chart_focus = []
    chart_distraction = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        chart_dates.append(day.strftime('%b %d'))
        metrics = ProductivityMetrics.objects.filter(user=user, date=day).first()
        if metrics:
            chart_study.append(round(metrics.total_study_minutes / 60, 1))
            chart_focus.append(round(metrics.avg_focus_score, 1))
            chart_distraction.append(round(metrics.total_distraction_minutes, 0))
        else:
            day_sessions = StudySession.objects.filter(user=user, start_time__date=day)
            day_distractions = DistractionLog.objects.filter(user=user, timestamp__date=day)
            chart_study.append(round(sum(s.duration_hours for s in day_sessions), 1))
            chart_focus.append(round(day_sessions.aggregate(avg=Avg('focus_score'))['avg'] or 0, 1))
            chart_distraction.append(day_distractions.aggregate(total=Sum('duration_minutes'))['total'] or 0)

    # Distraction type distribution
    distraction_data = (
        DistractionLog.objects.filter(user=user, timestamp__gte=week_ago)
        .values('distraction_type')
        .annotate(total=Sum('duration_minutes'))
        .order_by('-total')
    )
    distraction_labels = []
    distraction_values = []
    type_map = dict(DistractionLog.DISTRACTION_TYPES)
    for d in distraction_data:
        distraction_labels.append(type_map.get(d['distraction_type'], d['distraction_type']))
        distraction_values.append(d['total'] or 0)

    # Productivity score
    today_metrics = ProductivityMetrics.objects.filter(user=user, date=today).first()
    productivity_score = today_metrics.productivity_score if today_metrics else 0

    context = {
        'total_study_hours': round(total_study_hours, 1),
        'avg_focus': round(avg_focus, 1),
        'total_distractions': total_distractions,
        'active_tasks': active_tasks,
        'completed_tasks': completed_tasks,
        'productivity_score': round(productivity_score),
        'habits': habits,
        'unread_alerts': unread_alerts,
        'unread_alert_count': Alert.objects.filter(user=user, is_read=False, is_dismissed=False).count(),
        'chart_dates': json.dumps(chart_dates),
        'chart_study': json.dumps(chart_study),
        'chart_focus': json.dumps(chart_focus),
        'chart_distraction': json.dumps(chart_distraction),
        'distraction_labels': json.dumps(distraction_labels),
        'distraction_values': json.dumps(distraction_values),
    }
    return render(request, 'analyzer/dashboard.html', context)


@login_required
def study_sessions_view(request):
    if request.method == 'POST':
        form = StudySessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            compute_daily_metrics(request.user, session.start_time.date())
            messages.success(request, 'Study session logged successfully!')
            return redirect('study_sessions')
    else:
        form = StudySessionForm()

    sessions = StudySession.objects.filter(user=request.user)[:20]
    return render(request, 'analyzer/study_session.html', {
        'form': form,
        'sessions': sessions,
    })


@login_required
def delete_session(request, pk):
    session = get_object_or_404(StudySession, pk=pk, user=request.user)
    session.delete()
    messages.info(request, 'Session deleted.')
    return redirect('study_sessions')


# ─── DISTRACTIONS ──────────────────────────────────────────

@login_required
def distractions_view(request):
    if request.method == 'POST':
        form = DistractionForm(request.user, request.POST)
        if form.is_valid():
            distraction = form.save(commit=False)
            distraction.user = request.user
            distraction.save()
            messages.success(request, 'Distraction logged.')
            return redirect('distractions')
    else:
        form = DistractionForm(request.user)

    distractions = DistractionLog.objects.filter(user=request.user)[:20]
    return render(request, 'analyzer/distraction_log.html', {
        'form': form,
        'distractions': distractions,
    })


# ─── HABITS ────────────────────────────────────────────────

@login_required
def habits_view(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, f"Habit '{habit.name}' created!")
            return redirect('habits')
    else:
        form = HabitForm()

    habits = Habit.objects.filter(user=request.user, is_active=True)
    return render(request, 'analyzer/habits.html', {
        'form': form,
        'habits': habits,
    })


@login_required
def complete_habit(request, pk):
    """Mark a habit as completed for today (AJAX)."""
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    today = timezone.now().date()

    if habit.last_completed == today:
        return JsonResponse({'status': 'already_done', 'message': 'Already completed today!'})

    if habit.last_completed == today - timedelta(days=1):
        habit.current_streak += 1
    else:
        habit.current_streak = 1

    habit.longest_streak = max(habit.longest_streak, habit.current_streak)
    habit.total_completions += 1
    habit.last_completed = today
    habit.save()

    return JsonResponse({
        'status': 'success',
        'streak': habit.current_streak,
        'total': habit.total_completions,
        'stability': habit.stability_score,
    })


@login_required
def delete_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    habit.is_active = False
    habit.save()
    messages.info(request, f"Habit '{habit.name}' archived.")
    return redirect('habits')


@login_required
def tasks_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f"Task '{task.title}' created!")
            return redirect('tasks')
    else:
        form = TaskForm()

    pending = Task.objects.filter(user=request.user).exclude(status='completed')
    completed = Task.objects.filter(user=request.user, status='completed').order_by('-completed_at')[:10]
    return render(request, 'analyzer/tasks.html', {
        'form': form,
        'pending': pending,
        'completed': completed,
    })


@login_required
def complete_task(request, pk):
    """Mark a task as completed (AJAX)."""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.status = 'completed'
    task.completed_at = timezone.now()
    task.save()
    return JsonResponse({'status': 'success', 'message': f"'{task.title}' completed!"})


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    messages.info(request, 'Task deleted.')
    return redirect('tasks')


@login_required
def suggestions_view(request):
    # Generate fresh suggestions
    raw_suggestions = analyze_and_suggest(request.user)

    # Also detect patterns
    detect_patterns(request.user)

    # Save new suggestions to history
    for s in raw_suggestions:
        if not SuggestionHistory.objects.filter(
            user=request.user,
            suggestion_text=s['text'],
            generated_at__date=timezone.now().date()
        ).exists():
            SuggestionHistory.objects.create(
                user=request.user,
                suggestion_text=s['text'],
                category=s['category']
            )

    # Fetch history
    history = SuggestionHistory.objects.filter(user=request.user)[:30]

    return render(request, 'analyzer/suggestions.html', {
        'suggestions': raw_suggestions,
        'history': history,
    })


@login_required
def rate_suggestion(request, pk):
    """Rate a suggestion as helpful or not (AJAX)."""
    suggestion = get_object_or_404(SuggestionHistory, pk=pk, user=request.user)
    helpful = request.GET.get('helpful', 'true') == 'true'
    suggestion.is_helpful = helpful
    suggestion.is_read = True
    suggestion.save()
    return JsonResponse({'status': 'success'})



@login_required
def alerts_view(request):
    generate_alerts(request.user)
    alerts = Alert.objects.filter(user=request.user, is_dismissed=False)[:30]
    return render(request, 'analyzer/alerts.html', {'alerts': alerts})


@login_required
def dismiss_alert(request, pk):
    """Dismiss an alert (AJAX)."""
    alert = get_object_or_404(Alert, pk=pk, user=request.user)
    alert.is_dismissed = True
    alert.is_read = True
    alert.save()
    return JsonResponse({'status': 'success'})



@login_required
def analytics_view(request):
    user = request.user
    now = timezone.now()
    month_ago = now - timedelta(days=30)

    # Compute metrics for last 30 days
    for i in range(30):
        day = (now - timedelta(days=i)).date()
        compute_daily_metrics(user, day)

    metrics = ProductivityMetrics.objects.filter(user=user, date__gte=month_ago.date()).order_by('date')

    # Prepare chart data
    dates = [m.date.strftime('%b %d') for m in metrics]
    productivity_scores = [round(m.productivity_score, 1) for m in metrics]
    study_hours = [round(m.total_study_minutes / 60, 1) for m in metrics]
    focus_scores = [round(m.avg_focus_score, 1) for m in metrics]
    distraction_ratios = [round(m.distraction_ratio * 100, 1) for m in metrics]

    # Behavior patterns
    patterns = BehaviorPattern.objects.filter(user=user, is_active=True)

    # Summary stats
    total_sessions = StudySession.objects.filter(user=user).count()
    total_study_hours = sum(s.duration_hours for s in StudySession.objects.filter(user=user))
    total_distractions_logged = DistractionLog.objects.filter(user=user).count()
    avg_productivity = metrics.aggregate(avg=Avg('productivity_score'))['avg'] or 0

    # Habit completion rates
    habits = Habit.objects.filter(user=user, is_active=True)
    habit_names = [h.name for h in habits]
    habit_stability = [h.stability_score for h in habits]

    context = {
        'dates': json.dumps(dates),
        'productivity_scores': json.dumps(productivity_scores),
        'study_hours': json.dumps(study_hours),
        'focus_scores': json.dumps(focus_scores),
        'distraction_ratios': json.dumps(distraction_ratios),
        'patterns': patterns,
        'total_sessions': total_sessions,
        'total_study_hours': round(total_study_hours, 1),
        'total_distractions_logged': total_distractions_logged,
        'avg_productivity': round(avg_productivity, 1),
        'habit_names': json.dumps(habit_names),
        'habit_stability': json.dumps(habit_stability),
    }
    return render(request, 'analyzer/analytics.html', context)


@login_required
def api_unread_count(request):
    """Return unread alert count for navbar badge."""
    count = Alert.objects.filter(user=request.user, is_read=False, is_dismissed=False).count()
    return JsonResponse({'count': count})
