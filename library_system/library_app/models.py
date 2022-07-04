from django.db import models


class Racks(models.Model):
    rack_name = models.CharField(max_length=200, blank=True, null=True)


class Books(models.Model):
    racks = models.ForeignKey(Racks, on_delete=models.CASCADE, related_name="books_racks")
    book_title = models.CharField(max_length=200, blank=True, null=True)
    author = models.CharField(max_length=200, blank=True, null=True)
    published_year = models.CharField(max_length=200, blank=True, null=True)