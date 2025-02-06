from django.db import models
from django.contrib.auth.models import User  # Ensure this is imported before using User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.users.storage import S3MediaStorage





class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    infinite_flight_username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/',storage=S3MediaStorage(), blank=True, null=True, default='default_profile_pic.jpg')
    bio = models.TextField(default='New Member')
    created_at = models.DateTimeField(auto_now_add=True)
    rank = models.CharField(max_length=50, choices=[('Membership Pending', 'Membership Pending'),
                                                    ('Cadet Under Review', 'Cadet Under Review'),
                                                    ('Cadet', 'Cadet'),
                                                    ('Second Officer', 'Second Officer'),
                                                    ('First Officer Under Review', 'First Officer Under Review'),
                                                    ('First Officer', 'First Officer')], default='Membership Pending')
    
    membership_complete = models.BooleanField(default=False)  # Corrected
    role = models.CharField(max_length=100,  default='Pilot')



    def __str__(self):
        return f"{self.user.username}'s profile"
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rank', 'infinite_flight_username')
    list_filter = ('rank',)
    search_fields = ('user__username', 'infinite_flight_username')

    # Adding action buttons for reviewing/approving
    actions = ['approve_application', 'reject_application']

    def approve_application(self, request, queryset):
        queryset.update(rank='Cadet')
        self.message_user(request, "Applications have been approved.")
        # You can send an email after approval, as an example:
        for profile in queryset:
            self.send_approval_email(profile.user, "approved")

    def reject_application(self, request, queryset):
        queryset.update(rank='Membership Pending')
        self.message_user(request, "Applications have been rejected.")
        # You can send an email after rejection
        for profile in queryset:
            self.send_approval_email(profile.user, "rejected")

    def send_approval_email(self, user, status):
        subject = "Membership Application Status"
        message = f"Hello {user.username},\n\nYour membership application has been {status}."
        send_mail(subject, message, 'no-reply@yourairline.com', [user.email])

admin.site.register(Profile, ProfileAdmin)

    

# Signal to create Profile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
