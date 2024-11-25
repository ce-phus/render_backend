from django.db import models
import random 
import string

from django.core.files import File
from io import BytesIO
from PIL import Image, ImageFile
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from apps.common.models import TimeStampedUUIDModel

from apps.profiles.models import Profile

User = get_user_model()

    
class Post(TimeStampedUUIDModel):
    class AdvertType(models.TextChoices):
        FOR_SALE = "For Sale", _("For Sale")
        FOR_RENT = "For Rent", _("For Rent")
        AUCTION = "Auction", _("Auction")


    user = models.ForeignKey(
        User,
        verbose_name=_("Seller or Buyer"),
        related_name="agent_buyer",
        on_delete=models.DO_NOTHING,
    )

    title = models.CharField(verbose_name=_("Post Title"), max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    ref_code = models.CharField(
        verbose_name=_("Post Reference Code"),
        max_length=255,
        unique=True,
        blank=True,
    )
    def get_default_profile():
        default_profile = Profile.objects.first()
        return default_profile.pk if default_profile else None  

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=get_default_profile)

    model = models.CharField(
        verbose_name=_("Model"),
        max_length=250,
        default="",
    )

    is_featured = models.BooleanField(default=False)
    description = models.TextField(
        verbose_name=_("Description"),
        default="",
    )
    country = CountryField(
        verbose_name=_("Country"),
        default="KE",
        blank_label="(select country)",
    )
    city = models.CharField(verbose_name=_("City"), max_length=180, default="Nairobi")
    postal_code = models.CharField(
        verbose_name=_("Postal Code"), max_length=100, default="140"
    )
    street_address = models.CharField(
        verbose_name=_("Street Address"), max_length=150, default="Aventh Avenue"
    )
    price = models.DecimalField(
        verbose_name=_("Price"), max_digits=12, decimal_places=2, default=0.0
    )
    
    advert_type = models.CharField(
        verbose_name=_("Advert Type"),
        max_length=50,
        choices=AdvertType.choices,
        default=AdvertType.FOR_SALE,
    )


    cover_photo = models.ImageField(
        verbose_name=_("Main Photo"), default="/tractor_sample.jpg", null=True, blank=True
    )

    published_status = models.BooleanField(
        verbose_name=_("Published Status"), default=False
    )
    views = models.IntegerField(verbose_name=_("Total Views"), default=0)

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.description = str.capitalize(self.description)
        self.ref_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )
        super(Post, self).save(*args, **kwargs)
    
    def get_thumbnail(self):
        if self.cover_photo:
            return self.get_thumbnail.url
        else:
            if self.image:
                self.cover_photo = self.make_thumbnail(self.image)
                self.save()
                return self.cover_photo.url
            else:
                return ""
    def make_thumbnail(dels, image, size=(300, 200)):
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        img = Image.open(image)
        img.thumbnail(size)
        thumb = BytesIO()
        img.save(thumb, 'JPEG', quality=85)
        thumbnail = File(thumb, name=image.name)
        return thumbnail

   
class PostView(TimeStampedUUIDModel):
    ip = models.CharField(verbose_name=_("IP Address"), max_length=250)
    post = models.ForeignKey(
        Post, related_name="post_views", on_delete=models.CASCADE
    )

    def __str__(self):
        return(
            f"Total views on - {self.post.title} is - {self.post.views} view(s)"
        )
    
    class Meta:
        verbose_name = "Total Views on Post"
        verbose_name_plural = "Total Post Views"

class PostPhoto(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='posts/photos/', null=True, blank=True)

    def __str__(self) -> str:
        return f'Photo of {self.post.title}'