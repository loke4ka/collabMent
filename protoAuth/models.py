from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Phone Number')
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=False, related_name='related_friends')
    
    # Поле для хранения токена чата
    chat_token = models.CharField(max_length=200, blank=True, null=True)

    # Доп поля для настроек
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True, choices=GENDER_CHOICES)
    user_type = models.CharField(max_length=20, blank=True, null=True, choices=[('Job Seeker', 'Job Seeker'), ('Employer', 'Employer')])

    def __str__(self):
        return self.username
    
def user_directory_path(instance, filename):
    return f'media/profile_files/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    professional_field = models.CharField(max_length=100, blank=True, null=True)
    education = models.CharField(max_length=100, blank=True, null=True)
    education_date = models.CharField(max_length=100, blank=True, null=True)
    name_institution = models.CharField(max_length=100, blank=True, null=True)

    desired_position = models.CharField(max_length=100, blank=True, null=True)
    type_of_work = models.CharField(max_length=100, blank=True, null=True)
    operating_mode = models.CharField(max_length=100, blank=True, null=True)
    name_organization = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)

    current_job = models.CharField(max_length=100, blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    experience_name = models.CharField(max_length=100, blank=True, null=True)
    citizenship = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    passage_time = models.CharField(max_length=100, blank=True, null=True)

    location = models.CharField(max_length=100, blank=True, null=True)
    personal_qualities = models.TextField(blank=True, null=True)
    certificates = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    resume = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    profile_photo = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Friendship(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_friendships')
    friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friend_friendships')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'friend']


class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.author.username}"


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Repost(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
