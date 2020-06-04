from hashlib import md5
import logging

from django.apps import apps
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import (
    HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect,
    HttpResponseBadRequest, HttpResponseServerError, Http404,
)
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse

from django.contrib.auth import authenticate, login as login_auth, logout as logout_auth
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages

from .commonarticles import SLUG_NAME_TRANSLATION_FROM_CZ, COMMON_ARTICLES_CREATIVE_PAGES
from .forms import LoginForm
from .models import CommonArticle, News, Dating, UserProfile, CreativePage, CreativePageConcept
from .users import migrate_user

# Get an instance of a logger
logger = logging.getLogger(__name__)

VALID_SKINS = ['light', 'dark']
DEFAULT_LIST_SIZE = 5

def index(request):
    news_list = News.objects.order_by('-datum')

    paginator = Paginator(news_list, DEFAULT_LIST_SIZE)
    page = request.GET.get('z_s', 1)

    news = paginator.get_page(page)

    return render(request, 'news/list.html', {'news': news})


def creative_page_list(request, creative_page_slug):
    creative_page = get_object_or_404(CreativePage, slug=creative_page_slug)
    app, model_class_name = creative_page.model_class.split('.')
    model_class = apps.get_model(app, model_class_name)

    # For Common Articles, Creative Page is stored in attribute 'rubrika' as slug
    # For everything else, Creative Page is determined by its model class
    if model_class_name == 'commonarticle':
        article_list = model_class.objects.filter(schvaleno='a', rubrika=creative_page_slug).order_by('-datum')
    else:
        article_list = model_class.objects.filter(schvaleno='a').order_by('-datum')


    if creative_page_slug in ['galerie', 'fotogalerie']:
        default_limit = 18
    else:
        default_limit = DEFAULT_LIST_SIZE
    
    paginator = Paginator(article_list, default_limit)
    page = request.GET.get('z_s', 1)

    articles = paginator.get_page(page)

    try:
        concept = creative_page.creativepageconcept
    except CreativePageConcept.DoesNotExist:
        concept = None

    return render(request, 'creative-pages/%s-list.html' % model_class_name, {
        'heading': creative_page.name,
        'articles': articles,
        'creative_page_slug': creative_page.slug,
        'concept': concept,
    })


def creation_detail(request, creative_page_slug, article_id, article_slug):

    creative_page = get_object_or_404(CreativePage, slug=creative_page_slug)
    app, model_class_name = creative_page.model_class.split('.')
    model_class = apps.get_model(app, model_class_name)

    article = get_object_or_404(model_class, id=article_id)
    if article.get_slug() != article_slug:
        return HttpResponsePermanentRedirect(
            reverse('ddcz:common-article-detail', kwargs={
                'creative_page_slug': creative_page_slug,
                'article_id': article.pk,
                'article_slug': article.get_slug(),
            })
        )

    return render(request, 'creative-pages/%s-detail.html' % model_class_name, {
        'heading': creative_page.name,
        'article': article,
        'creative_page_slug': creative_page_slug,
    })

def creative_page_concept(request, creative_page_slug):
    creative_page = get_object_or_404(CreativePage, slug=creative_page_slug)
    try:
        concept = creative_page.creativepageconcept
    except CreativePageConcept.DoesNotExist:
        raise Http404

    return render(request, 'creative-pages/concept.html', {
        'heading': creative_page.name,
        'creative_page_slug': creative_page_slug,
        'concept': concept,
    })


def dating(request):

    item_list = Dating.objects.order_by('-datum')

    paginator = Paginator(item_list, DEFAULT_LIST_SIZE)
    page = request.GET.get('z_s', 1)

    items = paginator.get_page(page)



    return render(request, 'dating/list.html', {
        'items': items
    })

def change_skin(request):
    new_skin = request.GET.get('skin', 'light')
    if new_skin not in VALID_SKINS:
        return HttpResponseBadRequest("Nerozpoznán skin, který bych mohl nastavit.")

    request.session['skin'] = new_skin

    return HttpResponseRedirect("/")


def logout(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Use POST.")

    referer = request.META.get('HTTP_REFERER', '/')

    logout_auth(request)
    return HttpResponseRedirect(referer)
    

def login(request):
    """
    Log user in from one of the two sources:
        
        * Normal Django's authentication framework
        * Legacy DDCZ database

    If user is able to log in from legacy database table and does not have
    corresponding user object, create it for him.

    After this version of the site will become the default one, also delete User's
    password from the legacy table and consider them "migrated".

    Note that it is unusal for this form to handle only POST data and creates
    a bit of a weird experience with the form--but given the form is present
    on each and every page, it feels better to do this than to feed this kind
    of POST handling to every view. 
    """

    if request.method != 'POST':
        return HttpResponseBadRequest("Use POST.")

    referer = request.META.get('HTTP_REFERER', '/')

    form = LoginForm(request.POST)

    if not form.is_valid():
        return HttpResponseRedirect(referer)

    user = authenticate(username=form.cleaned_data['nick'], password=form.cleaned_data['password'])
    if user is not None:
        login_auth(request, user)
        return HttpResponseRedirect(referer)
    else:
        m = md5()
        #TODO: Encoding needs verification
        # This needs to be done since passwords, of course, can contain
        # non-ascii characters that affect hashing
        m.update(form.cleaned_data['password'].encode('cp1250'))
        old_insecure_hashed_password = m.hexdigest()

        try:
            profile = UserProfile.objects.get(nick_uzivatele=form.cleaned_data['nick'])
        except UserProfile.DoesNotExist:
            messages.error(request, 'Špatný nick a nebo heslo')
            return HttpResponseRedirect(referer)

        if profile.psw_uzivatele != old_insecure_hashed_password:
            messages.error(request, 'Špatný nick a nebo heslo')
            return HttpResponseRedirect(referer)

        else:
            migrate_user(profile=profile, password=form.cleaned_data['password'])
            user = authenticate(username=form.cleaned_data['nick'], password=form.cleaned_data['password'])

            if not user:
                return HttpResponseServerError("Chyba během migrace na nový systém! Prosím kontaktujte Almada")

            login_auth(request, user)

            #TODO: For first-time login, bunch of stuff happens. Inspect legacy login and reimplement

            return HttpResponseRedirect(referer)

def password_reset(request):
    if request.method == 'GET':
        form = PasswordResetForm()
    elif request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            try:
                user = UserProfile.objects.get(
                    email_uzivatele=form.cleaned_data['email']
                )
                form.save()
                logger.info("Send password reset link to %s" % form.cleaned_data['email'])
            except UserProfile.DoesNotExist:
                logger.info("Not sending password reset for invalid email %s" % form.data['email'])
            
            messages.add_message(request, messages.SUCCESS, 'Pokud je e-mail platný, odeslali jsme na něj odkaz pro reset hesla.')

    else:
        return HttpResponseBadRequest("Use GET or POST")

    return render(request, 'users/password-reset.html', {
        'password_reset_form': form,
    })

def user_profile(request, user_profile_id, nick_slug):

    user_profile = get_object_or_404(UserProfile, id=user_profile_id)
    
    return render(request, 'users/detail.html', {
        'profile': user_profile,
    })
