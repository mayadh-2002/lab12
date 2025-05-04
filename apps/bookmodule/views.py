from django.shortcuts import render
from django.http import HttpResponse
from .models import Book,Student,Student1,Address
from .forms import StudentForm, AddressForm
from django.db.models import Q
from django.db.models import Sum, Avg, Max, Min,Count
from django.db import models  
from .models import Department,Course
from .forms import BookForm
from .forms import ProfileForm , Profile
from django.shortcuts import get_object_or_404, redirect
def index(request):
    return render(request, "bookmodule/index.html")
#def list_books(request):
   # return render(request, 'bookmodule/list_books.html')

def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')
 
def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html')
def search_books(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
        # now filter
        books = __getBooksList()
        newBooks = []
        for item in books:
            contained = False
            if isTitle and string in item['title'].lower(): contained = True
            if not contained and isAuthor and string in item['author'].lower():contained = True
            
            if contained: newBooks.append(item)
        return render(request, 'bookmodule/bookList.html', {'books':newBooks})

    return render(request, 'bookmodule/search.html')
def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]

def links(request):
    return render(request, 'bookmodule/html5/links.html')
def text_formatting(request):
    return render(request, 'bookmodule/html5/text_formatting.html')
def listing(request):
    return render(request, 'bookmodule/html5/listing.html')

def tables(request):
    return render(request, 'bookmodule/html5/tables.html')

def add_book(request):
    Book.objects.create(title='Continuous Delivery', author='J.Humble and D. Farley', price=120.00, edition=3)
    Book.objects.create(title='Reversing: Secrets of Reverse Engineering', author='E. Eilam', price=97.00, edition=2)
    Book.objects.create(title='The Hundred-Page Machine Learning Book', author='Andriy Burkov', price=100.00, edition=4)
    return HttpResponse("Books added successfully!")

def simple_query(request):
    mybooks = Book.objects.filter(title__icontains='and')
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def add_test_book(request):
    Book.objects.create(title='Code and Culture', author='Jane Doe', price=85.0, edition=2)
    return HttpResponse("Test book added!")
 

def complex_query(request):
    mybooks = Book.objects.filter(
        author__isnull=False,
        title__icontains='and',
        edition__gte=2
    ).exclude(price__lte=100)[:10]

    if mybooks:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
      return render(request, 'bookmodule/index.html')
    
def task1(request):
     books=Book.objects.filter(Q(price__lte = 80)) 
     return render(request, 'bookmodule/bookList.html', {'books':books})
def task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) & (Q(title__icontains='co') | Q(author__icontains='co'))
    )
    return render(request, 'bookmodule/booklist.html', {'books': books})
def task3(request):
    books = Book.objects.filter(
        Q(edition__lte=3) & ~(
            Q(title__icontains='co') | Q(author__icontains='co')
        )
    )
    return render(request, 'bookmodule/booklist.html', {'books': books})
def task4(request):
    books = Book.objects.all().order_by('title')  
    return render(request, 'bookmodule/booklist.html', {'books': books})
def task5(request):
    # استخدام الدوال التجميعية (aggregation functions)
    total_books = Book.objects.count()  # عدد الكتب
    total_price = Book.objects.aggregate(Sum('price'))['price__sum']   
    average_price = Book.objects.aggregate(Avg('price'))['price__avg']  
    max_price = Book.objects.aggregate(Max('price'))['price__max']  
    min_price = Book.objects.aggregate(Min('price'))['price__min']  

    context = {
        'total_books': total_books,
        'total_price': total_price,
        'average_price': average_price,
        'max_price': max_price,
        'min_price': min_price
    }

    return render(request, 'bookmodule/booklist.html', context)
def task7(request):
    city_counts = Student.objects.values('address__city').annotate(count=models.Count('id'))

    return render(request, 'bookmodule/city_student_count.html', {'city_counts': city_counts})

def task1_view(request):
    departments = Department.objects.annotate(student_count=Count('student1'))
    return render(request, 'bookmodule/task1.html', {'departments': departments})  

def task2_view(request):
    courses = Course.objects.annotate(student_count=Count('student1'))
    return render(request,'bookmodule/task2.html', {'courses': courses})
def task3_view(request):
    departments = Department.objects.all()
    oldest_students = []

    for dept in departments:
        student = Student1.objects.filter(department=dept).order_by('id').first()
        oldest_students.append({
            'department': dept.name,
            'student': student.name if student else 'No students'
        })

    return render(request, 'bookmodule/task3.html', {'data': oldest_students})
def task4_view(request):
    departments = Department.objects.annotate(student_count=Count('student1')) \
                                    .filter(student_count__gt=2) \
                                    .order_by('-student_count')
    return render(request, 'bookmodule/task4.html', {'departments': departments})
from django.shortcuts import render
from .models import Book  # استيراد النموذج الخاص بالكتب
from django.contrib.auth.decorators import login_required
from .models import Book
from django.shortcuts import render

@login_required(login_url='/users/login')
def list_books(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/list_books.html', {'books': books})
from django.shortcuts import render, redirect
from .models import Book
def add_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        price = request.POST['price']
        edition = request.POST['edition']
        book = Book(title=title, author=author, price=price,edition=edition)
        book.save()  # Save the new book to the database
        return redirect('list_books')  # Redirect to the list of books

    return render(request, 'bookmodule/add_book.html')  # Display the form to add a book
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book

def edit_book(request, id):
    book = get_object_or_404(Book, id=id)  # Get the book by ID
    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.price = request.POST['price']
        book.edition = request.POST['edition']
        book.save()  # Save the updated book
        return redirect('list_books')  # Redirect to the list of books

    return render(request, 'bookmodule/edit_book.html', {'book': book})  # Display the form with existing book data
from django.shortcuts import redirect, get_object_or_404
from .models import Book

def delete_book(request, id):
    book = get_object_or_404(Book, id=id)  # Get the book by ID
    book.delete()  # Delete the book from the database
    return redirect('list_books')  # Redirect to the list of books

def list_books2(request):
    books = Book.objects.all()
    return render(request, 'bookmodule/lab9_part2/list_books.html', {'books': books})
def add_book2(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books_part2')
    else:
        form = BookForm()
    return render(request, 'bookmodule/lab9_part2/add_book.html', {'form': form})
def edit_book2(request, id):
    book = Book.objects.get(id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books_part2')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookmodule/lab9_part2/edit_book.html', {'form': form})
def delete_book2(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect('list_books_part2')

def student_list(request):
    students = Student.objects.all()  # جلب جميع الطلاب من قاعدة البيانات
    return render(request, 'bookmodule/student_list.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            student = student_form.save()  # حفظ الطالب
            return redirect('student_list')  # إعادة التوجيه إلى صفحة عرض الطلاب
    else:
        student_form = StudentForm()

    return render(request, 'bookmodule/add_student.html', {'student_form': student_form})

# تحديث بيانات الطالب
def update_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        student_form = StudentForm(request.POST, instance=student)
        if student_form.is_valid():
            student_form.save()  # حفظ التعديلات
            return redirect('student_list')
    else:
        student_form = StudentForm(instance=student)

    return render(request, 'bookmodule/update_student.html', {'student_form': student_form})

def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()  # حذف الطالب
    return redirect('student_list')

def add_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)  # استخدام request.FILES للتعامل مع الملفات
        if form.is_valid():
            form.save()  # حفظ البيانات في قاعدة البيانات
            return redirect('profile_list')  # بعد حفظ البيانات، إعادة التوجيه إلى صفحة عرض البيانات
    else:
        form = ProfileForm()

    return render(request, 'bookmodule/add_profile.html', {'form': form})

def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'bookmodule/profile_list.html', {'profiles': profiles})
