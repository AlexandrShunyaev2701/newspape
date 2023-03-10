from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
    

class PostList(ListView):
    model = Post
    ordering = '-data_time_create'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 1

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["time_now"] = datetime.utcnow()

        return context

    
class OnePost(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'


class PostSearch(ListView):
    model = Post
    ordering = '-data_time_create'
    template_name = 'search.html'
    context_object_name = 'news'


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        posts = form.save(commit=False)
        posts.position = 'P'
        posts.save()
        return super().form_valid(form)


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.position = 'N'
        news.save()
        return super().form_valid(form)


class PostEdit(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.position = 'P'
        news.save()
        return super().form_valid(form)


class NewsEdit(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.position = 'N'
        news.save()
        return super().form_valid(form)


class PostDelet(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')