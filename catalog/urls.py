from django.urls import include, path
from django.conf.urls import url

from . import views

#app_name = 'Catalog'
urlpatterns = [
    # Регулярные выражения
    url(r'^$', views.index, name='index'),
    url(r'^books/$', views.BookListView.as_view(), name='books'), # Каталог книг
    url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'), # Информация о книге
    url(r'^authors/$', views.AuthorListView.as_view(), name='authors'), # Каталог авторов
    url(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'), # Информация об авторе
    url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'), # Страница со книгами авторизованного пользователя
    url(r'^borrowed/$', views.LoanedBooksAllListView.as_view(), name='all-borrowed'),
]

# Формы
urlpatterns += [
    url(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),

    url(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),  # Форма создания Экземпляра Автора
    url(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),    # Изменение информации об Авторе
    url(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),  # Удаление Автора

    url(r'^book/create/$', views.BookCreate.as_view(), name='book_create'),
    url(r'^book/(?P<pk>\d+)/update/$', views.BookUpdate.as_view(), name='book_update'),
    url(r'^book/(?P<pk>\d+)/delete/$', views.BookDelete.as_view(), name='book_delete'),
]