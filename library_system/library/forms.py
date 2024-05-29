from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Book, BorrowRecord, Author, CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'password1', 'password2', 'is_admin']


class CustomAuthenticationForm(AuthenticationForm):
    pass


class BookForm(forms.ModelForm):
    author_name = forms.CharField(max_length=100, required=False, label='Author Name')

    class Meta:
        model = Book
        fields = ['title', 'author', 'total_quantity', 'available_quantity']

    def save(self, commit=True):
        author_name = self.cleaned_data.get('author_name')
        if author_name:
            author, created = Author.objects.get_or_create(name=author_name)
            self.instance.author = author
        return super().save(commit=commit)


class BorrowRecordForm(forms.ModelForm):
    borrow_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    return_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = BorrowRecord
        fields = ['book', 'borrower', 'borrow_date', 'return_date']


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    is_admin = forms.BooleanField(required=False, label='Register as admin')

    class Meta:
        model = CustomUser
        fields = ('username', 'phone_number', 'password1', 'password2', 'is_admin')


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'total_quantity', 'available_quantity']


class BorrowRecordForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['book', 'borrower', 'borrow_date', 'return_date']
