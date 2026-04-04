"""
Management command to seed realistic demo data for presentation.
Usage: python manage.py seed_demo_data
"""

import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

from analyzer.models import (
    StudySession, DistractionLog, Habit, Task,
    ProductivityMetrics, SuggestionHistory, BehaviorPattern, Alert
)
from analyzer.suggestion_engine import compute_daily_metrics, detect_patterns, generate_alerts, analyze_and_suggest


class Command(BaseCommand):
    help = 'Seed the database with realistic demo data for presentation'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding demo data...')

        # Create demo user
        user, created = User.objects.get_or_create(
            username='demo',
            defaults={'email': 'demo@example.com'}
        )
        if created:
            user.set_password('demo1234')
            user.save()
            self.stdout.write(self.style.SUCCESS('  ✅ Created user: demo / demo1234'))
        else:
            self.stdout.write('  ℹ️  User "demo" already exists')

        now = timezone.now()
        today = now.date()

        subjects = [
            'Mathematics', 'Physics', 'Computer Science', 'Data Structures',
            'Operating Systems', 'Database Management', 'Web Programming',
            'Statistics', 'English', 'Digital Electronics'
        ]

        distraction_types = [
            'social_media', 'phone', 'daydreaming', 'entertainment',
            'internet', 'food', 'noise', 'people', 'fatigue'
        ]

        # --- Create 30 days of study sessions ---
        self.stdout.write('  📚 Creating study sessions...')
        for day_offset in range(30, 0, -1):
            day = now - timedelta(days=day_offset)
            num_sessions = random.choice([0, 1, 1, 2, 2, 2, 3, 3])

            for _ in range(num_sessions):
                hour = random.choice([8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 20])
                start = day.replace(hour=hour, minute=random.randint(0, 59))
                duration = random.randint(20, 150)
                end = start + timedelta(minutes=duration)

                # Focus scores trend upward slightly over time
                base_focus = min(3 + (30 - day_offset) * 0.1, 7)
                focus = max(1, min(10, int(base_focus + random.gauss(0, 2))))

                StudySession.objects.create(
                    user=user,
                    subject=random.choice(subjects),
                    start_time=start,
                    end_time=end,
                    focus_score=focus,
                    notes=random.choice([
                        '', '', '',  # Often empty
                        'Good session, felt productive',
                        'Struggled to concentrate',
                        'Really engaging material',
                        'Tired but pushed through',
                        'Need to review this topic again',
                    ])
                )

        # --- Create distractions ---
        self.stdout.write('  📱 Creating distraction logs...')
        sessions = StudySession.objects.filter(user=user)
        for session in random.sample(list(sessions), min(40, sessions.count())):
            num_distractions = random.choice([0, 1, 1, 1, 2, 2, 3])
            for _ in range(num_distractions):
                DistractionLog.objects.create(
                    user=user,
                    session=session,
                    distraction_type=random.choice(distraction_types),
                    duration_minutes=random.randint(2, 20),
                    context=random.choice([
                        'Instagram notification popped up',
                        'Friend texted me',
                        'Got hungry, went to kitchen',
                        'Started watching YouTube',
                        'Roommate started talking',
                        'Noise from outside',
                        'Felt sleepy after lunch',
                        'Checked WhatsApp groups',
                        'Random internet browsing',
                        '',
                    ]),
                    timestamp=session.start_time + timedelta(minutes=random.randint(5, max(10, int(session.duration_minutes) - 5)))
                )

        # --- Create habits ---
        self.stdout.write('  🔥 Creating habits...')
        habit_data = [
            ('Read for 30 minutes', 'Read textbooks or educational material daily', 'daily', 18, 21, 25),
            ('Morning revision', 'Revise previous day notes every morning', 'daily', 12, 15, 18),
            ('Solve 5 problems', 'Practice solving at least 5 problems daily', 'daily', 8, 10, 12),
            ('Weekly review', 'Review weekly progress every Sunday', 'weekly', 3, 4, 4),
            ('Exercise 20 min', 'Physical activity for mental clarity', 'daily', 5, 7, 9),
        ]
        for name, desc, freq, streak, longest, total in habit_data:
            Habit.objects.create(
                user=user,
                name=name,
                description=desc,
                target_frequency=freq,
                current_streak=streak,
                longest_streak=longest,
                total_completions=total,
                last_completed=today - timedelta(days=random.choice([0, 0, 0, 1])),
                is_active=True,
            )

        # --- Create tasks ---
        self.stdout.write('  ✅ Creating tasks...')
        task_data = [
            ('Complete DBMS assignment', 'high', 'pending', 2),
            ('Prepare for OS viva', 'urgent', 'pending', 1),
            ('Submit WPL mini project', 'urgent', 'in_progress', 3),
            ('Read Chapter 7 - Normalization', 'medium', 'pending', 5),
            ('Practice SQL queries', 'medium', 'pending', 4),
            ('Review linked list notes', 'low', 'completed', -2),
            ('Complete Java lab experiment', 'high', 'completed', -1),
            ('Study for mid-semester exam', 'high', 'completed', -5),
        ]
        for title, priority, status, deadline_offset in task_data:
            task = Task.objects.create(
                user=user,
                title=title,
                priority=priority,
                status=status,
                deadline=now + timedelta(days=deadline_offset),
            )
            if status == 'completed':
                task.completed_at = now + timedelta(days=deadline_offset - 1)
                task.save()

        # --- Compute metrics for all days ---
        self.stdout.write('  📊 Computing productivity metrics...')
        for day_offset in range(30, -1, -1):
            day = (now - timedelta(days=day_offset)).date()
            compute_daily_metrics(user, day)

        # --- Detect patterns ---
        self.stdout.write('  🧠 Detecting behavior patterns...')
        detect_patterns(user)

        # --- Generate alerts ---
        self.stdout.write('  🔔 Generating alerts...')
        generate_alerts(user)

        # --- Generate suggestions ---
        self.stdout.write('  💡 Generating suggestions...')
        suggestions = analyze_and_suggest(user)
        for s in suggestions:
            SuggestionHistory.objects.create(
                user=user,
                suggestion_text=s['text'],
                category=s['category'],
            )

        # Add some historical alerts
        Alert.objects.create(user=user, alert_type='streak_milestone', severity='success',
                           title='🎉 7-day streak: Read for 30 minutes!',
                           message='Amazing! You maintained this habit for 7 days straight.')
        Alert.objects.create(user=user, alert_type='improvement', severity='success',
                           title='📈 Productivity improved by 23%',
                           message='Your productivity score improved significantly this week. Keep it up!')

        self.stdout.write(self.style.SUCCESS('\n✨ Demo data seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('   Login: demo / demo1234'))
        self.stdout.write(self.style.SUCCESS('   Run: python manage.py runserver'))
