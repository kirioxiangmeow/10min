from django.shortcuts import render, redirect, Http404, HttpResponse
from tenMinutesApp.models import Article, Comment, Ticket
from tenMinutesApp.form import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate,login
from tenMinutesApp.userform import LoginForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request, cate=None):
    context = {}
    if cate is None:
        article_list = Article.objects.all()
    elif cate == 'editors':
        article_list = Article.objects.filter(editors_choice=True)
    else:
        article_list = Article.objects.all()
    page_robot = Paginator(article_list,6)
    page_num = request.GET.get('page')
    # page_list = []
    #
    # # print(type(page_robot.page_range))
    #
    # for i in page_robot.page_range:
    #     page_list.append(page_robot.page(i))
    # print(page_list)

    # 异常处理的基本格式：
    # try：
    #     pass 做没有报错下我希望它去正常处理的东西
    # except:
    #     pass  出现错误了，去处理错误
    try:
        article_list = page_robot.page(page_num)
    except EmptyPage:
        article_list = page_robot.page(page_robot.num_pages)
    except PageNotAnInteger:
        article_list = page_robot.page(1)
        #raise Http404('EmptyPage!')
    context['article_list'] = article_list
    return render(request, '10MINs.html', context)

# def detail_old(request, page_num):
#     #注意这一句(form = CommentForm),因为forms.Form没有obejcts方法，所以form = CommentForm.objects.all()这样写是错的，会产生AttributeError: type object 'CommentForm' has no attribute 'objects'方法。
#     if request.method == 'GET':
#
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         #成功的话就会提交姓名评论，不成功的话直接跳出下面的循环。
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             comment = form.cleaned_data['comment']
#             article = Article.objects.get(id=page_num)
#             c = Comment(name=name, comment=comment, belong_to=article) #创建一个叫做c的模型实例
#             c.save()
#             return redirect(to='detail', page_num=page_num) #跳转到叫detail的页面，detail以url的name的名称为准


def detail(request,  page_num, error_form=None):
    context = {}
    article_info = Article.objects.get(id=page_num)
    voter_id = request.user.id
    like_counts = Ticket.objects.filter(article_id=page_num).count()
    try:
        user_ticket_for_this_article = Ticket.objects.get(voter_id=voter_id, article_id=page_num)
        context['user_ticket'] = user_ticket_for_this_article
    except:
        pass
    context['article_info'] = article_info
    context['like_counts'] = like_counts

    #comment_list = Comment.objects.all()
    form = CommentForm
    article = Article.objects.get(id=page_num)
    best_comment = Comment.objects.filter(best_comment=True, belong_to=article)
    if best_comment:
        context['best_comment'] = best_comment[0]
    context['article'] = article
    #context['comment_list'] = comment_list
    if error_form is not None:
        context['form'] = error_form
    else:
        context['form'] = form
    return render(request, 'detail.html', context)

def detail_comment(request, page_num):
    form = CommentForm(request.POST)
    #成功的话就会提交姓名评论，不成功的话直接跳出下面的循环。
    if form.is_valid():
        name = form.cleaned_data['name']
        comment = form.cleaned_data['comment']
        article = Article.objects.get(id=page_num)
        c = Comment(name=name, comment=comment, belong_to=article) #创建一个叫做c的模型实例
        c.save()
    else:
        return detail(request, page_num, error_form=form)
    return redirect(to='detail', page_num=page_num) #跳转到叫detail的页面，detail以url的name的名称为准

def index_login(request):
    context = {}
    if request.method == 'GET':
        form = AuthenticationForm
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(to='index')

    context['form'] = form
    return render(request,'register_login.html',context)

def index_register(request):
    context = {}
    if request.method == 'GET':
        form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='login')

    context['form'] = form
    return render(request,'register_login.html',context)

def detail_vote(request, page_num):
    voter_id = request.user.id
    try:
        user_ticket_for_this_article = Ticket.objects.get(voter_id=voter_id, article_id=page_num)
        user_ticket_for_this_article.choice = request.POST['vote']
        user_ticket_for_this_article.save()
    except ObjectDoesNotExist:
        new_ticket = Ticket(voter_id = voter_id, article_id=page_num, choice=request.POST['vote'])
        new_ticket.save()
    return redirect(to='detail', page_num=page_num)
