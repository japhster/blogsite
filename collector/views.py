from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils import timezone

import datetime

from .models import Card,Collector

def get_collector(name):
    try:
        return Collector.objects.get(name=name)
    except Collector.DoesNotExist:
        return Collector.objects.create(name=name)    

# Create your views here.

def index(request):
    context = {
        "cards": Card.objects.all(),
        "collector": get_collector(request.user.username)
    }
    return render(request, "collector/index.html", context)

def card(request,card_id):
    card = get_object_or_404(Card, pk=card_id)
    is_owned = card.owned_by(request.user.username)
    context = {"card":card, "is_owned":is_owned}
    return render(request, "collector/card.html", context)

def buy_pack(request):
    return render(request, "collector/buy_card.html")

def search_results(request):
    search_string = request.POST["search"]
    relevant_cards = Card.objects.filter(name__icontains=search_string)
    collector = get_collector(request.user.username)
    return render(request, "collector/index.html", {"cards": relevant_cards, "collector":collector})
    
def my_collection(request):
    collector = get_collector(request.user.username)
    relevant_cards = collector.collection.all()
    return render(request, "collector/index.html", {"cards": relevant_cards, "collector":collector})
    
def collect(request):
    next = request.POST.get('next',reverse('collector:index'))
    collector = get_collector(request.user.username)
    collector.coins += collector.get_coins_to_collect()
    collector.last_collected_coins = timezone.now()
    collector.save()
    return HttpResponseRedirect(next)
    
def buy_card(request, card_id):
    card = get_object_or_404(Card, pk=card_id)
    collector = get_collector(request.user.username)
    if collector.coins >= card.value:
        collector.collection.add(card)
        collector.coins -= card.value
        collector.save()
        return HttpResponseRedirect(reverse("collector:my_collection"))
    else:
        return HttyResponseRedirect(reverse("collector:card", args=(card_id,)))
        
class NewCardView(LoginRequiredMixin, generic.edit.CreateView):
    model = Card
    fields = ['name','description','rarity']
    template_name = 'collector/new_card.html'
    
      
def create(request):
    name = request.POST['name']
    rarity = request.POST['rarity']
    description = request.POST['description']
    new_card = Card(name=name,description=description,rarity=rarity)
    new_card.save()
    return HttpResponseRedirect(reverse('collector:card', args=(new_card.pk,)))
