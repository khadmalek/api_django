from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View, ListView, FormView
from .forms import LoginForm, CreateClientForm, RequestForm, NewsForm
from .models import User, LoanRequest, News
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.shortcuts import redirect



# Create your views here.



# region -home page
class HomePageView(View):       # OK +-
    template_name = "home_page.html"

    def get(self, request):
        return render(request, self.template_name)


# region -authentication
class AuthenticationView(View) :    # OK +-
    template_name = "authentication.html"
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("profil")
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        message = ""
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"],)
            if user is not None:
                login(request, user)
                return redirect("profil")
            else:
                message = "Identifiants invalides."
        return render(request, self.template_name, {"form": form, "message": message})


# region -Deconnexion
def logout_view(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès')
    return redirect('home')


# region -create profil
class CreateClientView(View) :      # OK+-
    model = User
    form_class = CreateClientForm
    template_name = 'create_client.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            form.save()
            messages.success(request, "Compte créé avec succès!")
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


# region -profil view
class ProfilView(View) :            # OK+
    template_name = 'profil.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, self.template_name, {'user': user})
    
# region -bank news
class BankNewsView(View):
    template_name = 'news.html'

    def get(self, request):
        news_list = News.objects.all().order_by('-publication_date')
        return render(request, self.template_name, {'news_list': news_list})
    
    def post(self, request):
        if request.POST.get('action') == 'delete':
            news_id = request.POST.get('news_id')
            if news_id:
                news = News.objects.get(id=news_id)
                # Vérifier que seul l'auteur ou un superuser peut supprimer
                if request.user == news.author or request.user.is_superuser:
                    news.delete()
                    messages.success(request, 'Article supprimé avec succès')
                else:
                    messages.error(request, 'Vous n\'avez pas la permission de supprimer cet article')
        return redirect('news')


class AddNewsView(LoginRequiredMixin, View):        # LoginRequiredMixin remplace if not request.user.is_authenticated
    template_name = 'create_news.html'
    form_class = NewsForm
    
    def test_func(self):
        return self.request.user.user_type == "conseiller" or self.request.user.is_superuser
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'Article ajouté avec succès')
            return redirect('news')
        return render(request, self.template_name, {'form': form})


# region -loan request
class LoanRequestView(View) :       # OK+-
    model = LoanRequest
    form_class = RequestForm
    template_name = 'loan_request.html'
    context_object_name = 'loan_request'
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            loan_request = form.save()
            messages.success(request, 'Demande de prêt enregistrée avec succès')
            return redirect('home') 
        return render(request, self.template_name, {'form': form})    

    


# region -chat
class ChatView(View) : 
    pass


# region -BONUS
# class EditProfilView(View) :    # bonus (avec possibilité de mofifier password)
#     pass

# class PasswordResetView(View) :         # bonus
#     pass
