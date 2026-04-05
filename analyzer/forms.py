from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StudySession, DistractionLog, Habit, Task


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control bg-dark text-light border-secondary',
                'placeholder': field.label,
            })


class StudySessionForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control bg-dark text-light border-secondary'
        })
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control bg-dark text-light border-secondary'
        })
    )

    class Meta:
        model = StudySession
        fields = ['subject', 'start_time', 'end_time', 'focus_score', 'notes']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'placeholder': 'e.g., Mathematics, Physics...'
            }),
            'focus_score': forms.Select(attrs={
                'class': 'form-select bg-dark text-light border-secondary'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'rows': 3,
                'placeholder': 'Any notes about this session...'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        if start and end and end <= start:
            raise forms.ValidationError("End time must be after start time.")
        return cleaned_data


class DistractionForm(forms.ModelForm):
    class Meta:
        model = DistractionLog
        fields = ['session', 'distraction_type', 'duration_minutes', 'context']
        widgets = {
            'session': forms.Select(attrs={
                'class': 'form-select bg-dark text-light border-secondary'
            }),
            'distraction_type': forms.Select(attrs={
                'class': 'form-select bg-dark text-light border-secondary'
            }),
            'duration_minutes': forms.NumberInput(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'min': 1,
                'placeholder': 'Minutes lost'
            }),
            'context': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'rows': 2,
                'placeholder': 'What triggered this distraction?'
            }),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['session'].queryset = StudySession.objects.filter(user=user).order_by('-start_time')
        self.fields['session'].required = False


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description', 'target_frequency']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'placeholder': 'e.g., Read for 30 minutes'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'rows': 2,
                'placeholder': 'Describe this habit...'
            }),
            'target_frequency': forms.Select(attrs={
                'class': 'form-select bg-dark text-light border-secondary'
            }),
        }


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control bg-dark text-light border-secondary'
        })
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'placeholder': 'Task title...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'rows': 2,
                'placeholder': 'Task details...'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select bg-dark text-light border-secondary'
            }),
        }
