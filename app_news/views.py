from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from .models import News


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        login(self.request, user)
        return redirect(self.success_url)


def index(request):
    news = News.objects.all()
    return render(request, 'index.html', {'new_list': news})


class AddNewsView(LoginRequiredMixin, CreateView):
    template_name = 'news/add_news.html'
    model = News
    fields = ['news_title', 'news_description', 'news_image', 'news_content', 'news_category']
    success_url = '/'

    def form_valid(self, form):
        form.instance.news_author = self.request.user
        return super().form_valid(form)


class NewsListView(ListView):
    model = News
    template_name = 'news/news.html'
    paginate_by = 3


def about_news(request, pk):
    news = News.objects.get(id=pk)
    return render(request, 'news/about_news.html', {'new': news})


class UpdateNewsView(LoginRequiredMixin, UpdateView):
    template_name = 'news/edit_news.html'
    model = News
    fields = ['news_title', 'news_description', 'news_image', 'news_content', 'news_category']
    success_url = reverse_lazy('list_news')

    def form_valid(self, form):
        form.instance.news_author = self.request.user
        return super().form_valid(form)


class DeleteNewsView(LoginRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('list_news')
    template_name = 'news/confirm_delete.html'

    def get_queryset(self):
        return super().get_queryset().filter(news_author=self.request.user)
