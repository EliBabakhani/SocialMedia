from django.shortcuts import render
from django.views import View
from .models import Post


class HomeView(View):
    def get(self,request):
        posts=Post.objects.all()
        return render(request, 'home/index.html',{'posts':posts})
    
class PostDetailView(View):
    def get(self, request,id,slug):
        post=Post.objects.get(id=id, slug=slug)
        return render(request, 'home/detail.html',{'post':post})