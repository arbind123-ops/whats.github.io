from django.contrib.auth.models import User, Group
from django.db import models
# Create your models here.


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class OrgnizationalInformation(TimeStamp):
    name = models.CharField(max_length=500)
    logo = models.ImageField(upload_to="organization")
    address = models.CharField(max_length=500)
    slogan = models.CharField(max_length=500, null=True, blank=True)
    contact_no = models.CharField(max_length=15)
    alt_contact_no = models.CharField(max_length=500, null=True, blank=True)
    map_location = models.CharField(max_length=500)
    email = models.EmailField(null=True, blank=True)
    about_us = models.TextField()
    privacy_policy = models.TextField(null=True, blank=True)
    show_popup = models.BooleanField(default=False)
    popup_image = models.ImageField(
        upload_to="organization", null=True, blank=True)
    facebook = models.CharField(max_length=500)
    instagram = models.CharField(max_length=500, null=True, blank=True)
    twitter = models.CharField(max_length=500, null=True, blank=True)
    youtube = models.CharField(max_length=500, null=True, blank=True)
    linkedin = models.CharField(max_length=500, null=True, blank=True)
    featured_photo = models.ImageField(upload_to="organization")
    featured_video_link = models.CharField(max_length=500)
    messenger_script = models.TextField(null=True, blank=True)
    google_analytics_script = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Admin(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=500)
    contact_no = models.CharField(max_length=15)
    address = models.CharField(max_length=500)
    email = models.EmailField(null=True, blank=True)
    image = models.ImageField(
        upload_to='team/admin/', blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        group, group_created = Group.objects.get_or_create(name="Admin")
        self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class Editor(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=500)
    contact_no = models.CharField(max_length=15)
    address = models.CharField(max_length=500)
    email = models.EmailField(null=True, blank=True)
    image = models.ImageField(
        upload_to='team/editor/', blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        group, group_created = Group.objects.get_or_create(name="Editor")
        self.user.groups.add(group)
        super().save(*args, **kwargs)

    def verified_news(self):
        verified_news = self.news_set.filter(is_verified=True)
        print(verified_news.count())
        return verified_news.count()

    def __str__(self):
        return self.full_name


class NewsCategory(TimeStamp):
    title = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(
        upload_to="news/main_category", null=True, blank=True)
    icon_character = models.CharField(max_length=500, null=True, blank=True)
    root = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class NewsSubCategory(TimeStamp):
    title = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, null=True, blank=True)
    main_category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="news/sub_category")
    icon_character = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title


class NewsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class NewsVerified(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_verified=True)


class News(TimeStamp):
    title = models.CharField(max_length=500)
    main_category = models.ForeignKey(
        NewsCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(
        NewsSubCategory, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to="news/news", null=True, blank=True)
    video_link = models.URLField(max_length=500, null=True, blank=True)
    content = models.TextField()
    view_count = models.BigIntegerField(default=0)
    editor = models.ForeignKey(
        Editor, on_delete=models.SET_NULL, null=True, blank=True)
    admin = models.ForeignKey(
        Admin, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    objects = NewsManager()
    verified = NewsVerified()

    def __str__(self):
        return self.title


class Comment(TimeStamp):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    commenter = models.CharField(max_length=500)
    email = models.EmailField()
    comment = models.TextField()

    def __str__(self):
        return self.commenter


class AdvertizementPosition(TimeStamp):
    position = models.CharField(max_length=500)
    total_number = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.position


class Advertizement(TimeStamp):
    position = models.ForeignKey(
        AdvertizementPosition, on_delete=models.CASCADE)
    organization = models.CharField(max_length=500)
    image = models.ImageField(upload_to="advertizements")
    link = models.URLField(max_length=500)
    expiry_date = models.DateTimeField(null=True, blank=True)
    view_count = models.BigIntegerField(default=1)
    clicks = models.BigIntegerField(default=1)

    def __str__(self):
        return self.organization


class Subscriber(TimeStamp):
    email = models.EmailField()

    def __str__(self):
        return self.email


class Contact(TimeStamp):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=50)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name
