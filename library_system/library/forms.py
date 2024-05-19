from django import forms
from .models import Book, BorrowRecord, Author

class BookForm(forms.ModelForm):
    author_name = forms.CharField(max_length=100, required=False, label='Author Name')

    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'total_quantity', 'available_quantity']

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
