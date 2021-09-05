from posts.forms import PostForm
from django.shortcuts import redirect, render
from posts.models import Post

def index(req):
    return redirect('post-list')

def post_list(req):
    context = {"posts": Post.objects.order_by('id')}
    return render(req, 'posts/post_list.html', context=context)


def post_detail(req, post_id):
    context = {"post": Post.objects.get(id=post_id)}
    return render(req, "posts/post_detail.html", context=context)


def post_create(req):
    if req.method == "POST":
        post_form = PostForm(req.POST)  # Bind request's body and Postform

    """
    Check the data is valid 
    if not, we will end the if statement
    and make user to fix it
    """
    try: # POST Request
        if post_form.is_valid():    
            new_post = post_form.save()
            return redirect('post-detail', post_id=new_post.id)
    except UnboundLocalError: # Get Request
        post_form = PostForm()

    return render(req, 'posts/post_form.html', {'form': post_form})

def post_update(req, post_id):
    post = Post.objects.get(id=post_id)
    
    if req.method == "POST":
        post_form = PostForm(req.POST, instance=post) # 이미 존재하는 instance 수정

        if post_form.is_valid():
            post_form.save()
            return redirect("post-detail", post_id=post.id)
    else:
        post_form = PostForm(instance=post)

    return render(req, "posts/post_form.html", context={'form': post_form})

def post_delete(req, post_id):
    post = Post.objects.get(id=post_id)
    if req.method == "POST":
        post.delete()
        return redirect('post-list')
    else:
        return render(req, "posts/post_confirm_delete.html", {'post': post})