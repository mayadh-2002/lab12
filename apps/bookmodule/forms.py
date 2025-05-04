from django import forms
from .models import Book
from .models import Student, Address
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'image', 'bio']
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class StudentForm(forms.ModelForm):
    addresses = forms.ModelMultipleChoiceField(queryset=Address.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Student
        fields = ['name', 'age', 'addresses']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city']