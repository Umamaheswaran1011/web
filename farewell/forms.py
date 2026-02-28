from django import forms
from .models import Friend, Event, EventPhoto, TimelineEvent


class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = [
            'name', 'nickname', 'photo',
            'memory_text', 'future_goal',
            'special_power', 'weakness', 'signature_dialogue',
        ]
        widgets = {
            # Basic info — notebook-line style
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
            }),
            'nickname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nickname (e.g. The Vanisher)',
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'memory_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share a memory...',
                'rows': 4,
            }),
            'future_goal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Future Goal (e.g. CEO)',
            }),
            # Trading card stats — scrapbook handwritten style
            'special_power': forms.TextInput(attrs={
                'class': 'scrapbook-input',
                'placeholder': 'e.g. Can sleep anywhere, anytime ⚡',
            }),
            'weakness': forms.TextInput(attrs={
                'class': 'scrapbook-input',
                'placeholder': 'e.g. Cannot say no to food 🍕',
            }),
            'signature_dialogue': forms.TextInput(attrs={
                'class': 'scrapbook-input',
                'placeholder': 'e.g. "Naan ready-aa, da!"',
            }),
        }
        labels = {
            'special_power': '⚡ Special Power',
            'weakness': '💀 Weakness',
            'signature_dialogue': '💬 Signature Dialogue',
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'cover_image', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event Name (e.g. Pongal Celebration)',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe this event...',
                'rows': 3,
            }),
        }


class PhotoUploadForm(forms.Form):
    """Form for photo upload."""
    caption = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Optional caption for all uploaded photos',
        }),
        label='Caption (optional)'
    )


class SlamBookForm(forms.Form):
    """Form for visitors to write slam book messages on a friend's profile."""
    sender_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name',
        }),
        label='Your Name'
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Write something memorable...',
            'rows': 4,
        }),
        label='Your Message'
    )


class MilestoneForm(forms.ModelForm):
    """Form for adding timeline milestones from the frontend."""
    class Meta:
        model = TimelineEvent
        fields = ['title', 'date', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'scrapbook-input',
                'placeholder': 'e.g., First Day of College...',
            }),
            'date': forms.DateInput(attrs={
                'class': 'scrapbook-input',
                'type': 'date',
            }),
            'description': forms.Textarea(attrs={
                'class': 'scrapbook-input',
                'placeholder': 'What happened during this memory...',
                'rows': 5,
            }),
            'image': forms.FileInput(attrs={
                'class': 'scrapbook-input scrapbook-file',
            }),
        }
