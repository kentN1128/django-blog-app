from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post, Category, Tag, Comment, Reply
from blog.forms import CommentForm, ReplyForm
from django.db.models import Q

posts_per_page = 5

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    paginate_by = posts_per_page

    def get_queryset(self):
        posts = super().get_queryset()

        return posts.order_by('-updated_at')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if post.is_published or self.request.user.is_authenticated:
            return post
        else:
            raise Http404

class CategoryPostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = posts_per_page

    def get_queryset(self):
        slug = self.kwargs['slug']
        self.category = get_object_or_404(Category, slug=slug)

        return  super().get_queryset().filter(category=self.category)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context

class TagPostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    paginate_by = posts_per_page

    def get_queryset(self):
        slug =self.kwargs['slug']
        self.tag = get_object_or_404(Tag, slug=slug)

        return super().get_queryset().filter(tag=self.tag)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        return context

class SearchPostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    paginate_by = posts_per_page

    def get_queryset(self):
        self.query = self.request.GET.get('query') or ""
        queryset = super().get_queryset()
        if self.query:
            queryset = queryset.filter(
                Q(title__icontains=self.query)|Q(content__icontains=self.query)
            )
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)
        self.post_count = len(queryset)

        return queryset

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.query
        context["post_count"] = self.post_count
        return context

class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)

        post_pk = self.kwargs['post_pk']
        post = get_object_or_404(Post, pk=post_pk)

        comment.post = post
        comment.save()
        return redirect('post-detail', pk=post_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs['post_pk']
        context['post'] = get_object_or_404(Post, pk=post_pk)

        return context

class ReplyCreateView(CreateView):
    model = Reply
    form_class = ReplyForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        reply = form.save(commit=False)

        comment_pk = self.kwargs['comment_pk']
        comment = get_object_or_404(Comment, pk=comment_pk)

        reply.comment = comment
        reply.save()
        return redirect('post-detail', pk=comment.post.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs['comment_pk']
        context['comment'] = get_object_or_404(Comment, pk=comment_pk)

        return context


class CommentDeleteView(LoginRequiredMixin,DeleteView):
    model = Comment
    template_name = "blog/comment_delete.html"
    # success_url = reverse_lazy('post-detail')
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk':self.object.post.pk})


class ReplyDeleteView(LoginRequiredMixin,DeleteView):
    model = Reply
    template_name = "blog/comment_delete.html"
    # success_url = reverse_lazy('post-detail')
    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk':self.object.comment.post.pk})