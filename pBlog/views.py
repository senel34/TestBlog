from django.shortcuts import render, render_to_response, get_object_or_404 #render html page
from django.http import HttpResponse, HttpResponseRedirect
from pBlog.forms import PostForm
from blogPost.models import WritePost
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import logout #for the logout function used in user authentication

def writepost(request):
    if request.method == 'POST':
        request.POST = request.POST.copy()
        form = PostForm(request.POST)
        if form.is_valid():
            
            #form.data['title'] = 'My huge magnum dong'
            WritePost.objects.create(date_posted=timezone.now(), blog_title=form.data['title'], blog_post=form.data['message'], post_author=request.user.username)
            return render(request,'blog_post.html',{'form':form})
    else:
        form = PostForm(initial={'title':'enter title...','message':'lorem ipsum....'})

    return render(request,'blog_post.html',{'form':form})

def readpost(request):
    if request.method == 'GET':
        post_list = WritePost.objects.filter(date_posted__lte=timezone.now()).order_by('-date_posted')
        page = request.GET.get('page',1) #get ?page= from request.GET
        post_paged = Paginator(post_list,3)
        try:
            posts = post_paged.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = post_paged.page(post_paged.num_pages)

    return render(request,'blog_read.html',{'posts':posts})

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def post_detail(request,slug):
    post = get_object_or_404(WritePost, slug=slug)
    post.slug = "writepost\\" + post.slug
    return render(request,'blog_detail.html',{'post':post})

