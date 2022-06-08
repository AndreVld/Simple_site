import json

from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView

from django.core.mail import EmailMessage
from django.conf import settings

from .forms import PostForm
from .models import Post, Certificates, Info
from .common import send_telegram


def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=data['login'], password=data['password'])
        print(request.body)
        if user is not None and user.is_active:
            login(request, user)
            return JsonResponse('Authenticated successfully', safe=False)
        return JsonResponse('', status=404, safe=False)


class Logout(LogoutView):
    pass


class HomeView(ListView):
    template_name = 'base/home.html'

    def get_queryset(self):
        return Post.objects.only('slug', 'thumbnail', 'headline', 'sub_headline', 'tags', ) \
            .prefetch_related('tags').filter(active=True).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeView, self).get_context_data()
        context['certificates'] = Certificates.objects.filter(active=True).order_by('?')
        context['info'] = Info.objects.first()
        return context


def read_post(request, slug):
    if request.method == 'GET' and request.is_ajax():
        post_exist = Post.objects.filter(slug=slug, active=True).exists()

        if post_exist:
            post = Post.objects.only('headline', 'git', 'content', ).get(slug=slug)
            result = render_to_string('base/includes/inc_read_post.html', {'post': post})
            return JsonResponse({"result": result}, status=200)
        else:
            errors = "Sorry! Post does not exists!"
            return JsonResponse({"errors": errors}, status=404)


class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = 'base/create_update.html'
    form_class = PostForm
    success_url = reverse_lazy('home')


class UpdatePostView(LoginRequiredMixin, UpdateView):
    template_name = 'base/create_update.html'
    form_class = PostForm
    model = Post
    success_url = reverse_lazy('home')


def send_email(request):
    if request.method == 'POST':
        name = request.POST['name']
        email_address = request.POST['email']
        message = request.POST['message']

        template = render_to_string('base/email_template.html', {
            'name': name,
            'email': email_address,
            'message': message,
        })

        email = EmailMessage(
            name,
            template,
            settings.EMAIL_HOST_USER,
            ['email@email.com'],
        )
        email.fail_silently = False
        email.send()

        send_telegram(
            f'NAME :\t {name}\n\n'
            f'EMAIL :\t {email_address}\n\n'
            f'MESSAGE :\t {message}'
        )

        return HttpResponse(render_to_string('base/message_sent.html'))

    else:
        return HttpResponseRedirect(reverse('home'))
