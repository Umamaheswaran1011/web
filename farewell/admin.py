from django.contrib import admin
from .models import Friend, Event, EventPhoto, TimelineEvent, FunAward, SlamMessage


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Friend objects.
    """
    list_display = ('name', 'nickname', 'created_at')
    search_fields = ('name', 'nickname')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'nickname', 'photo')
        }),
        ('Memory', {
            'fields': ('memory_text',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class EventPhotoInline(admin.TabularInline):
    """Inline to upload multiple photos directly inside an Event."""
    model = EventPhoto
    extra = 3
    fields = ('image', 'caption')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'photo_count')
    search_fields = ('title',)
    list_filter = ('date',)
    inlines = [EventPhotoInline]

    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = '# Photos'


@admin.register(EventPhoto)
class EventPhotoAdmin(admin.ModelAdmin):
    list_display = ('event', 'caption', 'uploaded_at')
    list_filter = ('event',)
    search_fields = ('caption',)


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ('title',)
    list_filter = ('date',)
    ordering = ['date']


@admin.register(FunAward)
class FunAwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'winner')
    search_fields = ('title', 'winner__name')
    list_filter = ('winner',)


@admin.register(SlamMessage)
class SlamMessageAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'friend', 'created_at')
    search_fields = ('sender_name', 'message')
    list_filter = ('friend', 'created_at')
    readonly_fields = ('created_at',)
