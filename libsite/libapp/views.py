from django.shortcuts import render
# Import necessary classes
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from libapp.models import Book, Dvd, Libuser, Libitem, Suggestion
from django.http import Http404
from libapp.forms import SuggestionForm,loginForm,SearchlibForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
import random

from django.shortcuts import render_to_response
from libapp.forms import UserForm
# Create your views here.

def register(request):
    if request.method == 'POST':
        #err = 'invalid content,please input again!'
        form=UserForm(request.POST)
        if form.is_valid():
            user = Libuser.objects.create(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email = form.cleaned_data['email'],
                phone = form.cleaned_data['phone']
            )
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            #req.session['username'] = username
            user_login(request)
            return HttpResponseRedirect(reverse('libapp:index'))
        else:
            form=UserForm()
            return render(request,'libapp/register.html',{'form':form, 'fail':True})
    else:
        uf = UserForm()
    return render(request,'libapp/register.html',{'uf':uf})

def myitem(request):
    if request.user.is_authenticated():
        myitemlist = Libitem.objects.filter(user__username=request.user)
        if myitemlist:
            return render(request, 'libapp/myitems.html', {'myitemlist':myitemlist})
        else:
            return HttpResponse('You are not a Libuser!')
    else:
        return HttpResponse('Login first please')



def user_login(request):
    loginform = loginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        request.session["luckynum"] = random.randrange(0,10)
        request.session.set_expiry(10)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('libapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'libapp/login.html',{'loginform':loginform})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('libapp:index')))



def suggestions(request):
    suggestionlist = Suggestion.objects.all()[:10]
    return render(request, 'libapp/suggestions.html', {'suggestionlist': suggestionlist})

def newitem(request):
    suggestions = Suggestion.objects.all()
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.num_interested = 1
            suggestion.save()
            return HttpResponseRedirect(reverse('libapp:suggestions'))
        else:
            return render(request, 'libapp/newitem.html', {'form':form, 'suggestions':suggestions})
    else:
        form = SuggestionForm()
        return render(request, 'libapp/newitem.html', {'form':form, 'suggestions':suggestions})




def index(request):
    # booklist = Book.objects.all() [:10]
    # dvdlist = Dvd.objects.all() [:10]
    # itemlist = Libitem.objects.all().order_by('title')[:10]
    # response = HttpResponse()
    #
    # heading1 = '<p>' + 'List of books: ' + '</p>'
    # response.write(heading1)
    # for book in booklist:
    #     para = '<p>' + str(book) + '</p>'
    #     response.write(para)
    #
    # heading2 = '<p>' + 'List of dvds: ' + '</p>'
    # response.write(heading2)
    # for dvd in dvdlist:
    #     para = '<p>' + str(dvd) + '</p>'
    #     response.write(para)
    itemlist = Libitem.objects.all().order_by('title')[:10]
    #return response
    if request.session.get('luckynum',False):
        luckynum = request.session["luckynum"]
    else:
        luckynum = 0
    return render(request, 'libapp/index.html', {'itemlist': itemlist, 'luckynum':luckynum})




def about(request):
    response_about = HttpResponse()
    response_about.write('<p>' + 'This is a Library APP' + '</p>')
    visits = int(request.COOKIES.get('visits', '1'))
    response_about = render(request, 'libapp/about.html',{'visits': visits})
    response_about.set_cookie('visits', visits + 1,max_age=300)
    return response_about


def detail(request,item_id):

    try:
        item = Libitem.objects.get(pk=item_id)
    except Libitem.DoesNotExist:
        raise Http404

    response = HttpResponse()

    if item.itemtype == 'Book':
        book = Book.objects.get(pk=item_id)
        # title = '<p>' + item.title + '<p>\n'
        # pubyear = '<p>Pub date : ' + str(book.pubyr) + '</p>'
        # author_maker =  '<p>Author : ' + str(book.author) + '</p>'
        # response.write(title)
        # response.write(pubyear)
        # response.write(author_maker)
        # return response
        return render(request, 'libapp/detail.html', {'book': book})

    else:
        dvd = Dvd.objects.get(pk=item_id)
        # title = '<p>' + item.title + '<p>\n'
        # author_maker = '<p>Maker : ' + str(item.maker) + '</p>'
        # response.write(title)
        # response.write(author_maker)
        return render(request, 'libapp/detail.html', {'dvd': dvd})

# below modified by figo


def info(request,suggestion_id):
    info = Suggestion.objects.get(pk=suggestion_id)
    return render(request, 'libapp/info.html', {'info':   info})


def searchlib(request):
    if request.method == 'POST':
        form = SearchlibForm(request.POST)
        if request.POST.get("title")!='':
            booklist=Book.objects.filter(title__contains=request.POST.get("title"))
            dvdlist = Dvd.objects.filter(title__contains=request.POST.get("title"))
            if request.POST.get("by")!='':
                booklist = booklist.filter(author__contains=request.POST.get("by"))
                dvdlist = dvdlist.filter(maker__contains=request.POST.get("by"))
            return render(request, 'libapp/searchlib.html', {'form': form,'booklist':booklist,'dvdlist':dvdlist})
        elif request.POST.get("by")!='':
            booklist=Book.objects.filter(author__contains=request.POST.get("by"))
            dvdlist = Dvd.objects.filter(maker__contains=request.POST.get("by"))
            return render(request, 'libapp/searchlib.html', {'form': form,'booklist':booklist,'dvdlist':dvdlist})
        else:
            return render(request, 'libapp/searchlib.html', {'form': form})
    else:
        form = SearchlibForm()
        return render(request, 'libapp/searchlib.html', {'form': form})


