from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.forms import ModelForm


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='sub')
    sub_cat = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    slug = models.SlugField(allow_unicode=True, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='category', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:category', args=[self.slug, self.id])

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Product(models.Model):
    VARIANT = (
        ('Size', 'size'),
        ('Color', 'color'),
    )
    category = models.ManyToManyField(Category, blank=True)
    name = models.CharField(max_length=200)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveIntegerField()
    information = RichTextUploadingField(blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    available = models.BooleanField(default=True)
    status = models.CharField(max_length=200, blank=True, null=True, choices=VARIANT)
    image = models.ImageField(upload_to='product')
    favourite = models.ManyToManyField(User, blank=True, related_name='fa_user')
    like = models.ManyToManyField(User, blank=True, related_name='product_like')
    total_like = models.PositiveIntegerField(default=0)
    unlike = models.ManyToManyField(User, blank=True, related_name='product_unlike')
    total_unlike = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def total_like(self):
        return self.like.count()

    def total_unlike(self):
        return self.unlike.count()

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price


class Size(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Variants(models.Model):
    name = models.CharField(max_length=100)
    product_variant = models.ForeignKey(Product, on_delete=models.CASCADE)
    size_variant = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    color_variant = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()
    discount = models.PositiveIntegerField(blank=True, null=True)
    total_price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    @property
    def total_price(self):
        if not self.discount:
            return self.unit_price
        elif self.discount:
            total = (self.discount * self.unit_price) / 100
            return int(self.unit_price - total)
        return self.total_price


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='image/', blank=True)

    def __str__(self):
        return self.name


class Gallery(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='gallery/', blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    rate = models.PositiveIntegerField(default=1)
    create = jmodels.jDateTimeField(auto_now_add=True)
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, blank=True, null=True, related_name='comment_reply')
    is_reply = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'rate']


class ReplyForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

