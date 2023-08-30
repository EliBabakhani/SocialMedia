from typing import Any
from django import http
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateForm
from django.utils.text import slugify


class HomeView(View):
    def get(self,request):
        posts=Post.objects.all()
        return render(request, 'home/index.html',{'posts':posts})
    
class PostDetailView(View):
    def get(self, request,id,slug):
        post=Post.objects.get(id=id, slug=slug)
        return render(request, 'home/detail.html',{'post':post})
    

class PostDeleteView(LoginRequiredMixin,View):
    def get(self, request, id):
        post=Post.objects.get(id=id)
        if post.user.id==request.user.id:
            post.delete()
            messages.success(request,'Post deleted successfully', 'success')
            return redirect('home:home')
        messages.error(request,'You have no permission', 'danger')
        return redirect('home:home')

class PostUpdateView(LoginRequiredMixin, View):
    form_class=PostUpdateForm

    def setup(self, request, *args: Any, **kwargs: Any):
        self.post_instance=Post.objects.get(id=kwargs['id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args: Any, **kwargs: Any):
        post=self.post_instance
        if not post.user.id==request.user.id:
            messages.error(request,'there is problem with data','danger')
            return redirect('home:detail', post.id, post.slug)
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request, id):
        post=self.post_instance
        form=self.form_class(instance=post)
        return render(request, 'home/post_update.html', {'form':form})
    
    def post(self, request,id):
        post=self.post_instance
        form=self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.slug=slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'Post updated successfully','success')
            return redirect('home:home')
        messages.error(request,'invalid data','danger')
        return redirect('home:detail', post.id, post.slug)
