from django.urls import path
from .views import HomePageView, AuthenticationView, CreateClientView, ProfilView, LoanRequestView, BankNewsView, AddNewsView, logout_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),  
    path('authentication/', AuthenticationView.as_view(), name='authentication'),  
    path('create_client/', CreateClientView.as_view(), name='create_client'),  
    path('profil/', ProfilView.as_view(), name='profil'),  
    path('loan_request/', LoanRequestView.as_view(), name='loan_request'),
    path('news/', BankNewsView.as_view(), name='news'),
    path('add_news/', AddNewsView.as_view(), name='add_news'),
    path('logout/', logout_view, name='logout'),
    
]