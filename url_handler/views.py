from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import shorturl
import random, string
from django.conf import settings

# Create your views here.

HOST_URL=settings.ALLOWED_HOSTS[0]
def home(request, query=None):
    if not query or query is None:
        return redirect(dashboard)
        # return render(request, 'home.html')
    else:
        try:
            check = shorturl.objects.get(short_query=query)
            check.visits = check.visits + 1
            check.save()
            url_to_redirect = check.original_url
            return redirect(url_to_redirect)
        except shorturl.DoesNotExist:
            return render(request, 'home.html', {'error': "error"})


@login_required(login_url='login')
def dashboard(request):
    usr = request.user
    urls = shorturl.objects.filter(user=usr)
    return render(request, 'dashboard.html', {'base':HOST_URL,'urls': urls})


def randomgen():
    return ''.join(random.choice(string.ascii_letters) for _ in range(6))


@login_required(login_url='login')
def generate(request):
    if request.method == 'POST':
        # generate
        if request.POST['original'] and request.POST['short']:
            # generate based on user input
            usr = request.user
            original = request.POST['original']
            short = request.POST['short']
            check = shorturl.objects.filter(short_query=short)
            if not check:
                newurl = shorturl(
                    user=usr,
                    original_url=original,
                    short_query=short,
                )
                newurl.save()
                return redirect(dashboard)
            else:
                messages.error(request, "Already Exists")
                return redirect(dashboard)
        elif request.POST['original']:
            # generate randomly
            usr = request.user
            original = request.POST['original']
            generated = False
            while not generated:
                short = randomgen()
                check = shorturl.objects.filter(short_query=short)
                if not check:
                    newurl = shorturl(
                        user=usr,
                        original_url=original,
                        short_query=short,
                    )
                    newurl.save()
                    return redirect(dashboard)
                else:
                    continue
        else:
            messages.error(request, "Empty Fields")
            return redirect(dashboard)
    else:
        return redirect(dashboard)