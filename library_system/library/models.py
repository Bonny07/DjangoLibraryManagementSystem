from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    total_quantity = models.PositiveIntegerField()
    available_quantity = models.PositiveIntegerField()
    published_date = models.DateField(null=True, blank=True)  # 修改此行

class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.CharField(max_length=100)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
