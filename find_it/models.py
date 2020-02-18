from django.db import models
from PIL import Image


class ProductSearch(models.Model):
    keyword = models.CharField(max_length=250)

    def __str__(self):
        return self.keyword

    class Meta:
        verbose_name = "Product Search"
        verbose_name_plural = "Products Search"


class MarketplaceSource(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    logo = models.ImageField(upload_to='ecommerce_media', default='default.png')
    link = models.URLField()

    class Meta:
        verbose_name = "Marketplace Source"
        verbose_name_plural = "Marketplace Sources"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.logo.path)

        if img.height > 300 or img.width > 300:
            out_size = (300, 300)
            img.thumbnail(out_size)
            img.save(self.logo.path)

