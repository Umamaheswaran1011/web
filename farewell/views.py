from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .models import Friend, Event, EventPhoto, TimelineEvent, FunAward, SlamMessage
from .forms import FriendForm, EventForm, PhotoUploadForm, SlamBookForm, MilestoneForm


def farewell_index(request):
    """
    View to display all friends on the farewell page.
    Fetches all Friend objects and passes them to the template.
    """
    friends = Friend.objects.all()
    
    context = {
        'friends': friends,
        'page_title': 'Farewell Batch 2026 - The Anti-Gravity Squad',
    }
    
    return render(request, 'farewell/index.html', context)


def add_friend(request):
    """
    View to handle adding a new friend with a photo.
    """
    if request.method == 'POST':
        form = FriendForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('farewell:index' + '?msg=Friend added successfully! ✨')
    else:
        form = FriendForm()
    
    return render(request, 'farewell/add_friend.html', {
        'form': form, 
        'page_title': 'Add a Friend',
        'button_text': 'Add Friend'
    })


def delete_friend(request, pk):
    """
    View to delete a friend entry.
    """
    if request.method == 'POST':
        friend = get_object_or_404(Friend, pk=pk)
        friend.delete()
    return redirect('farewell:index' + '?msg=Friend removed')


def friend_detail(request, pk):
    """
    View to display details of a single friend,
    including Slam Book messages and form.
    """
    friend = get_object_or_404(Friend, pk=pk)
    slam_messages = friend.slam_messages.all()

    if request.method == 'POST':
        slam_form = SlamBookForm(request.POST)
        if slam_form.is_valid():
            SlamMessage.objects.create(
                friend=friend,
                sender_name=slam_form.cleaned_data['sender_name'],
                message=slam_form.cleaned_data['message'],
            )
            from django.urls import reverse
            return redirect(reverse('farewell:friend_detail', args=[pk]) + '?msg=Scrap pinned! 📌')
    else:
        slam_form = SlamBookForm()

    return render(request, 'farewell/friend_detail.html', {
        'friend': friend,
        'page_title': friend.name,
        'slam_messages': slam_messages,
        'slam_form': slam_form,
    })


def edit_friend(request, pk):
    """
    View to edit an existing friend's details.
    """
    friend = get_object_or_404(Friend, pk=pk)
    if request.method == 'POST':
        form = FriendForm(request.POST, request.FILES, instance=friend)
        if form.is_valid():
            form.save()
            from django.urls import reverse
            return redirect(reverse('farewell:friend_detail', args=[pk]) + '?msg=Friend updated! ✨')
    else:
        form = FriendForm(instance=friend)
    
    return render(request, 'farewell/add_friend.html', {
        'form': form, 
        'page_title': f'Edit {friend.name}',
        'button_text': 'Update Friend'
    })


def gallery_view(request):
    """
    View to list all events as album cards with photo counts.
    """
    events = Event.objects.annotate(photo_count=Count('photos')).order_by('-date')
    return render(request, 'farewell/gallery.html', {
        'events': events,
        'page_title': '📸 Memories Gallery',
    })


def event_detail_view(request, pk):
    """
    View to display all photos inside a specific event album.
    """
    event = get_object_or_404(Event, pk=pk)
    photos = event.photos.all()
    return render(request, 'farewell/event_detail.html', {
        'event': event,
        'photos': photos,
        'page_title': event.title,
    })


def add_event(request):
    """
    View to create a new Event album from the frontend.
    """
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('farewell:gallery' + '?msg=Event created! 📸')
    else:
        form = EventForm()

    return render(request, 'farewell/add_event.html', {
        'form': form,
        'page_title': '✨ Create New Event',
        'button_text': 'Create Event',
    })


def edit_event(request, pk):
    """
    View to edit an existing Event's details.
    """
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('farewell:event_detail', pk=pk)
    else:
        form = EventForm(instance=event)

    return render(request, 'farewell/add_event.html', {
        'form': form,
        'page_title': f'✏️ Edit {event.title}',
        'button_text': 'Update Event',
        'event': event,
    })


def delete_event(request, pk):
    """
    View to delete an entire Event album and all its photos.
    """
    if request.method == 'POST':
        event = get_object_or_404(Event, pk=pk)
        event.delete()
    return redirect('farewell:gallery')


def add_photos(request, pk):
    """
    View to upload multiple photos to a specific Event.
    Images come from raw HTML input, caption from the Django form.
    """
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST)
        files = request.FILES.getlist('images')
        if files:
            caption = form.data.get('caption', '').strip()
            for f in files:
                EventPhoto.objects.create(
                    event=event,
                    image=f,
                    caption=caption if caption else None,
                )
            from django.urls import reverse
            return redirect(reverse('farewell:event_detail', args=[pk]) + '?msg=Photos uploaded! 📸')
    else:
        form = PhotoUploadForm()

    return render(request, 'farewell/upload_photos.html', {
        'form': form,
        'event': event,
        'page_title': f'📷 Upload to {event.title}',
        'button_text': 'Upload Photos',
    })


def delete_photo(request, pk):
    """
    View to delete a single photo from an event.
    """
    if request.method == 'POST':
        photo = get_object_or_404(EventPhoto, pk=pk)
        event_pk = photo.event.pk
        photo.delete()
        return redirect('farewell:event_detail', pk=event_pk)
    return redirect('farewell:gallery')


def timeline_view(request):
    """
    View to display the college timeline journey.
    """
    events = TimelineEvent.objects.all()
    return render(request, 'farewell/timeline.html', {
        'events': events,
        'page_title': '🎓 Our College Journey',
    })


def awards_view(request):
    """
    View to display all fun awards.
    """
    awards = FunAward.objects.select_related('winner').all()
    return render(request, 'farewell/awards.html', {
        'awards': awards,
        'page_title': '🏆 Fun Awards',
    })


def add_milestone(request):
    """
    View to add a new timeline milestone from the frontend.
    """
    if request.method == 'POST':
        form = MilestoneForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            from django.urls import reverse
            return redirect(reverse('farewell:timeline') + '?msg=Memory saved! ✨')
    else:
        form = MilestoneForm()

    return render(request, 'farewell/add_milestone.html', {
        'form': form,
        'page_title': '📝 Add a Milestone',
    })


def edit_milestone(request, pk):
    """
    View to edit an existing timeline milestone.
    """
    milestone = get_object_or_404(TimelineEvent, pk=pk)
    if request.method == 'POST':
        form = MilestoneForm(request.POST, request.FILES, instance=milestone)
        if form.is_valid():
            form.save()
            from django.urls import reverse
            return redirect(reverse('farewell:timeline') + '?msg=Memory updated! ✏️')
    else:
        form = MilestoneForm(instance=milestone)

    return render(request, 'farewell/edit_milestone.html', {
        'form': form,
        'milestone': milestone,
        'page_title': f'✏️ Edit: {milestone.title}',
    })


def delete_milestone(request, pk):
    """
    View to delete a timeline milestone after POST confirmation.
    """
    milestone = get_object_or_404(TimelineEvent, pk=pk)
    if request.method == 'POST':
        milestone.delete()
        from django.urls import reverse
        return redirect(reverse('farewell:timeline') + '?msg=Memory removed 🗑️')

    return render(request, 'farewell/delete_milestone.html', {
        'milestone': milestone,
        'page_title': f'Delete: {milestone.title}',
    })



def custom_page_not_found(request, exception):
    """
    Custom 404 error page with scrapbook theme.
    """
    return render(request, 'farewell/404.html', {
        'page_title': 'Page Not Found',
    }, status=404)
