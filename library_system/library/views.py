from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Book, Author, BorrowRecord
from datetime import date


def index(request):
    edit_mode = request.GET.get('edit_mode') == 'true'
    books = Book.objects.all()
    authors = Author.objects.all()
    new_edit_mode = 'false' if edit_mode else 'true'
    edit_button_text = 'Save' if edit_mode else 'Edit'

    context = {
        'books': books,
        'authors': authors,
        'edit_mode': edit_mode,
        'new_edit_mode': new_edit_mode,
        'edit_button_text': edit_button_text,
    }
    return render(request, 'library/index.html', context)

def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_name = request.POST.get('author')
        total_quantity = request.POST.get('total_quantity')
        available_quantity = request.POST.get('available_quantity')

        author, created = Author.objects.get_or_create(name=author_name)
        book = Book(title=title, author=author, total_quantity=total_quantity, available_quantity=available_quantity)
        book.save()
        messages.success(request, 'Book added successfully.')
    return redirect('index')

def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.available_quantity > 0:
        book.available_quantity -= 1
        book.save()
        BorrowRecord.objects.create(book=book, borrower='John Doe', borrow_date=date.today())
        messages.success(request, 'Book borrowed successfully.')
    else:
        messages.error(request, 'No available copies left.')
    return redirect('index')

def my_books(request):
    borrowed_books = BorrowRecord.objects.filter(borrower='John Doe')
    context = {
        'borrowed_books': borrowed_books,
    }
    return render(request, 'library/my_books.html', context)

def return_book(request, pk):
    record = get_object_or_404(BorrowRecord, pk=pk)
    record.book.available_quantity += 1
    record.book.save()
    record.delete()
    messages.success(request, 'Book returned successfully.')
    return redirect('my_books')

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    messages.success(request, 'Book deleted successfully.')
    return redirect('index')

def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        author_name = request.POST.get('author')
        total_quantity = request.POST.get('total_quantity')
        available_quantity = request.POST.get('available_quantity')

        author, created = Author.objects.get_or_create(name=author_name)
        book.title = title
        book.author = author
        book.total_quantity = total_quantity
        book.available_quantity = available_quantity
        book.save()
        messages.success(request, 'Book updated successfully.')
    return redirect('index')
