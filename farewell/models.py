from django.db import models


class Friend(models.Model):
    """
    Model to store information about each friend for the farewell website.
    """
    name = models.CharField(
        max_length=100,
        help_text="Full name of the friend"
    )
    
    nickname = models.CharField(
        max_length=50,
        help_text="Nickname or preferred name"
    )
    
    photo = models.ImageField(
        upload_to='friend_photos/',
        help_text="Profile photo of the friend"
    )
    
    memory_text = models.TextField(
        help_text="A short emotional note or memory about the friend"
    )

    future_goal = models.CharField(
        max_length=200,
        help_text="What do they want to become? (e.g., CEO, Traveler, Scientist)",
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Friend'
        verbose_name_plural = 'Friends'
    
    def __str__(self):
        return f"{self.name} ({self.nickname})"


class Event(models.Model):
    """
    Model to represent a memory event/album (e.g., Pongal, Tour, Farewell).
    """
    title = models.CharField(
        max_length=200,
        help_text="Event name (e.g., Pongal Celebration, College Tour)"
    )
    cover_image = models.ImageField(
        upload_to='event_covers/',
        help_text="Cover image for the event album"
    )
    date = models.DateField(
        help_text="Date of the event"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Short description of the event"
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.title


class EventPhoto(models.Model):
    """
    Model for individual photos inside an event album.
    """
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='photos',
        help_text="The event this photo belongs to"
    )
    image = models.ImageField(
        upload_to='event_photos/',
        help_text="The photo"
    )
    caption = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="Optional caption for the photo"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Event Photo'
        verbose_name_plural = 'Event Photos'

    def __str__(self):
        return f"{self.event.title} - {self.caption or 'Photo'}"


class TimelineEvent(models.Model):
    """
    Model for the Timeline Journey — milestones from 1st year to Final year.
    """
    title = models.CharField(
        max_length=200,
        help_text="e.g., First Day of College, Pongal Celebration"
    )
    date = models.DateField(
        help_text="When this happened"
    )
    description = models.TextField(
        help_text="What happened during this event"
    )
    image = models.ImageField(
        upload_to='timeline/',
        blank=True,
        null=True,
        help_text="Optional image for this milestone"
    )

    class Meta:
        ordering = ['date']
        verbose_name = 'Timeline Event'
        verbose_name_plural = 'Timeline Events'

    def __str__(self):
        return f"{self.title} ({self.date})"


class FunAward(models.Model):
    """
    Model for Fun Awards — funny titles given to friends.
    """
    title = models.CharField(
        max_length=200,
        help_text="The award name (e.g., Sothu Mootai, Silent Killer)"
    )
    winner = models.ForeignKey(
        Friend,
        on_delete=models.CASCADE,
        related_name='awards',
        help_text="The friend who won this award"
    )
    icon_or_image = models.ImageField(
        upload_to='awards/',
        blank=True,
        null=True,
        help_text="Optional icon/image for the award"
    )

    class Meta:
        verbose_name = 'Fun Award'
        verbose_name_plural = 'Fun Awards'

    def __str__(self):
        return f"{self.title} — {self.winner.name}"


class SlamMessage(models.Model):
    """
    Digital Slam Book — visitors write messages for a specific friend.
    """
    friend = models.ForeignKey(
        Friend,
        on_delete=models.CASCADE,
        related_name='slam_messages',
        help_text="Who is this message for?"
    )
    sender_name = models.CharField(
        max_length=100,
        help_text="Who is writing this message?"
    )
    message = models.TextField(
        help_text="The slam book message"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Slam Message'
        verbose_name_plural = 'Slam Messages'

    def __str__(self):
        return f"{self.sender_name} → {self.friend.name}"
