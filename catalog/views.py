from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin # Для расширения полномочий авторизованных пользователей
from django.contrib.auth.mixins import PermissionRequiredMixin # Для расширения полномочий работников
from django.views import generic

from django.contrib.auth.decorators import permission_required
from .forms import RenewBookForm # Импортировать форму из файла с описанием форм
from .forms import RenewBookModelForm # Импортировать форму из файла с описанием форм
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

def index(request):
    # Генерация отображения для домашней страницы сайта
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_books_first = Book.objects.filter(title__icontains='First').count()
    num_genres = Genre.objects.all().count()
    num_authors = Author.objects.count() # Метод 'all()' применяется по умолчанию

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    #В первую очередь мы получаем значение 'num_visits' из сессии, возвращая 0, если оно не было установлено ранее.
    # Каждый раз при получении запроса, мы увеличиваем данное значение на единицу и сохраняем его обратно в сессии
    # (до следующего посещения данной страницы пользователем).
    # Затем переменная num_visits передается в шаблон через переменную контекста context.

    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances':num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_books_first': num_books_first, 'num_genres':num_genres,
                 'num_visits': num_visits
                 },
    )

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned') # Ограничение доступа к отображению
def renew_book_librarian(request, pk):
    #
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # Если POST запрос
    if request.method == 'POST':

        # Создаем форму и связываем ее с моделью
        form = RenewBookForm(request.POST)

        # Проверка валидности формы
        if form.is_valid():
            # Создаем экземпляр формы и заполняем данными из запроса (связывание, binding):
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # После выполнения условий формы перенаправляем пользователя на страницу всех занятых кнниг
            return HttpResponseRedirect(reverse('all-borrowed') )

    # Если это GET (или другой метод), тогда создаем форму по умолчанию
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form1 = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})
        form2 = RenewBookModelForm(initial={'due_back': proposed_renewal_date, })

    return render(request, 'catalog/book_renew_librarian.html', {'form1': form1,'form2': form2, 'bookinst':book_inst})

class AuthorCreate(PermissionRequiredMixin, CreateView): # Параметр PermissionRequiredMixin, необходим для ограничения прав доступа
    model = Author
    fields = '__all__'
    initial={'date_of_death':'12/10/2016',}
    permission_required = 'catalog.can_mark_returned' # Разрешение для работников

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']
    permission_required = 'catalog.can_mark_returned'

# Классу AuthorDelete не нужно показывать каких либо полей, таким образом их не нужно и декларировать.
# Тем не менее, вам нужно указать success_url.
class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'