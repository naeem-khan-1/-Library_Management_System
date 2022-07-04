
from django.urls import path

from authentication.BusinessLogic.NeglectDefaultAuthentications import neglect_authentication
from library_app.Views import RacksView, BooksView


urlpatterns = [
    path('racks_list_count_user', neglect_authentication(RacksView.ShowRacksUserList), name='ShowRacksList'),
    path('racks_list_count', neglect_authentication(RacksView.ShowRacksList), name='ShowRacksList'),
    path('racks_list', neglect_authentication(RacksView.RacksListView), name='RacksListView'),
    path('racks_view', neglect_authentication(RacksView.RacksView), name='RacksView'),
    path('racks_view/<int:pk>', neglect_authentication(RacksView.RacksDetailedView)),

    path('show_books_details_user', neglect_authentication(BooksView.ShowBooksUserList), name='ShowRackBooksList'),
    path('show_rack_books_details_user', neglect_authentication(BooksView.ShowRackBooksUserList), name='ShowRackBooksUserList'),
    path('show_rack_books_details', neglect_authentication(BooksView.ShowRackBooksList), name='ShowRackBooksList'),
    path('show_books_details', neglect_authentication(BooksView.ShowBooksList), name='ShowBooksList'),
    path('books_list', neglect_authentication(BooksView.BooksListView)),
    path('books_view', neglect_authentication(BooksView.BooksView)),
    path('books_view/<int:pk>', neglect_authentication(BooksView.BooksDetailedView)),
]

