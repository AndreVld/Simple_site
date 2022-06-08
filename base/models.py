from django.db import models
from pytils.translit import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from random import randint


class Tag(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Post(models.Model):
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='thumbnail/%Y/%m/%d',
                                  default='images/placeholder.png')
    headline = models.CharField(max_length=256)
    sub_headline = models.CharField(max_length=256, null=True, blank=True)
    content = RichTextUploadingField(null=True, blank=True)
    active = models.BooleanField(default=False)
    git = models.URLField(unique=True, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.slug is None:
            slug = slugify(self.headline)
            exist_slug = Post.objects.filter(slug=slug).exists()

            while exist_slug:
                slug = f'{slug}_{randint(99, 999)}'
                exist_slug = Post.objects.filter(slug=slug).exists()

            self.slug = slug
        super(Post, self).save()

    def __str__(self):
        return self.headline


class Info(models.Model):
    about_me = models.TextField(blank=True)
    email = models.EmailField(max_length=128)
    telegram = models.URLField()
    img = models.ImageField(blank=True, null=True, upload_to='img/%Y/%m/%d', default='images/placeholder.png')

    def __str__(self):
        return self.email


class Certificates(models.Model):
    image = models.ImageField(upload_to='certificates/%Y/%m/%d')
    link = models.URLField(unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Certificate'
