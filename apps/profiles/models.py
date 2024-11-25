from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


from apps.common.models import TimeStampedUUIDModel

User = get_user_model()

class Gender(models.TextChoices):
    MALE = "Male", _("Male")
    FEMALE = "Female", _("Female")
    OTHER = "Other", _("Other")

class Profile(TimeStampedUUIDModel):
    user = models.OneToOneField(User, related_name="profile", on_delete= models.CASCADE)
    phone_number = PhoneNumberField(
        verbose_name =_("Phone Number"), max_length= 30, default="+0112989425"
    )
    about_me = models.TextField(
        verbose_name=_("About me"), default="say something about yourself"
    )
    facebook_url = models.URLField(
        max_length=200, verbose_name=_("Facebook URL"), default='www.facebook.com'
    )
    instagram_url = models.URLField(
        max_length=200, verbose_name=_("Instagram URL"), default='www.instagram.com'
    )
    twitter_url = models.URLField(
        max_length=200, verbose_name=_("Twitter URL"), default='www.twitter.com'
    )
    threads_url = models.URLField(
        max_length=200, verbose_name=_("Threads URL"), default='www.threads.com'
    )

    profile_photo = models.ImageField(
        verbose_name=_("Profile Photo"), default="/profile_default.jpg"
    )
    gender = models.CharField(
        verbose_name=_("Gender"),
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=20
    )
    country = CountryField(
        verbose_name=_("Country"), default="KE", blank=False, null=False
    )
    city = models.CharField(
        verbose_name=_("City"),
        max_length=180,
        default="Nairobi",
        blank=False,
        null=False,
    )

    postal_code = models.CharField(
        verbose_name=_("Postal Code"), max_length=100, default="140"
    )
    street_address = models.CharField(
        verbose_name=_("Street Address"), max_length=150, default="Aventh Avenue"
    )
    
    is_buyer = models.BooleanField(
        verbose_name=_("Buyer"),
        default=False,
        help_text=_("Are you looking to Buy a Property?"),
    )
    is_seller = models.BooleanField(
        verbose_name=_("Seller"),
        default=False,
        help_text=_("Are you looking to sell a property?"),
    )
    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    num_reviews = models.IntegerField(
        verbose_name=_("Number of Reviews"), default=0, null=True, blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s profile"
