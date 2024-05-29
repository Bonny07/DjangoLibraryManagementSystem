from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm, BookForm, BorrowRecordForm
from django.contrib import messages
from .models import Book, Author, BorrowRecord
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from datetime import date
from django.contrib.admin.views.decorators import staff_member_required

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = form.cleaned_data['is_admin']
            user.is_superuser = form.cleaned_data['is_admin']
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def redirect_user(request):
    if request.user.is_admin:
        return redirect('index')
    else:
        return redirect('my_books')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, Author


@login_required
def index(request):
    edit_mode = 'edit_mode' in request.GET and request.GET['edit_mode'] == 'true'
    new_edit_mode = not edit_mode
    edit_button_text = 'Edit Mode' if not edit_mode else 'View Mode'

    id_query = request.GET.get('id_query', '')
    title_query = request.GET.get('title_query', '')
    author_query = request.GET.get('author_query', '')

    books = Book.objects.all()
    if id_query:
        books = books.filter(id=id_query)
    if title_query:
        books = books.filter(title__icontains=title_query)
    if author_query:
        books = books.filter(author__name__icontains=author_query)

    authors = Author.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        author_name = request.POST.get('author')
        total_quantity = request.POST.get('total_quantity')
        available_quantity = request.POST.get('available_quantity')

        if title and author_name and total_quantity and available_quantity:
            author, created = Author.objects.get_or_create(name=author_name)
            Book.objects.create(
                title=title,
                author=author,
                total_quantity=int(total_quantity),
                available_quantity=int(available_quantity)
            )
            messages.success(request, 'Book added successfully')
            return redirect('index')
        else:
            messages.error(request, 'Please fill out all fields.')

    context = {
        'books': books,
        'authors': authors,
        'edit_mode': edit_mode,
        'new_edit_mode': 'true' if not edit_mode else 'false',
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
        BorrowRecord.objects.create(book=book, borrower=request.user.username, borrow_date=date.today())
        messages.success(request, 'Book borrowed successfully.')
    else:
        messages.error(request, 'No available copies left.')
    return redirect('index')


@login_required
def my_books(request):
    borrowed_books = BorrowRecord.objects.filter(borrower=request.user.username)
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


@staff_member_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    messages.success(request, 'Book deleted successfully.')
    return redirect('index')


@staff_member_required
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


def custom_logout(request):
    logout(request)
    return redirect('login')


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def redirect_user(request):
    if request.user.is_superuser:
        return redirect('admin:index')
    else:
        return redirect('index')
