from django.shortcuts import render, get_object_or_404, redirect
from .models import Account, Trade
from .forms import AccountForm, TradeForm, UserRegisterForm, UserLoginForm, UserForm, ProfileForm, AccountSelectForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .serializers import AccountSerializer, TradeSerializer
from rest_framework import viewsets
from uuid import UUID  # UUID modülünü import ediyoruz

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer

def home_view(request):
    if request.user.is_authenticated:
        accounts = Account.objects.filter(owner=request.user)
        return render(request, 'journal/home.html', {'accounts': accounts})
    return render(request, 'journal/home.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'journal/register.html', {'form': form})

@login_required
def profile_view(request):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    return render(request, 'journal/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'journal/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def account_list(request):
    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'journal/account_list.html', {'accounts': accounts})

@login_required
def account_detail(request, pk):
    account = get_object_or_404(Account, pk=UUID(pk), owner=request.user)  # UUID ile kontrol ediyoruz
    return render(request, 'journal/account_detail.html', {'account': account})

@login_required
def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.owner = request.user
            account.save()
            return redirect('account_list')
    else:
        form = AccountForm()
    return render(request, 'journal/account_form.html', {'form': form})

@login_required
def account_edit(request, pk):
    account = get_object_or_404(Account, pk=UUID(pk), owner=request.user)  # UUID ile kontrol ediyoruz
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('account_detail', pk=account.pk)
    else:
        form = AccountForm(instance=account)
    return render(request, 'journal/account_form.html', {'form': form})

@login_required
def account_delete(request, pk):
    account = get_object_or_404(Account, pk=UUID(pk), owner=request.user)  # UUID ile kontrol ediyoruz
    account.delete()
    return redirect('account_list')

@login_required
def trade_list(request, pk):
    account = get_object_or_404(Account, pk=UUID(pk), owner=request.user)  # UUID ile kontrol ediyoruz
    trades = Trade.objects.filter(account=account)
    return render(request, 'journal/trade_list.html', {'account': account, 'trades': trades})

@login_required
def trade_detail(request, pk):
    trade = get_object_or_404(Trade, pk=pk, trade_owner=request.user)
    return render(request, 'journal/trade_detail.html', {'trade': trade})

@login_required
def trade_create(request):
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.trade_owner = request.user
            trade.save()
            return redirect('trade_detail', pk=trade.pk)
    else:
        form = TradeForm()
    return render(request, 'journal/trade_form.html', {'form': form})

@login_required
def trade_edit(request, pk):
    trade = get_object_or_404(Trade, pk=pk, trade_owner=request.user)
    if request.method == 'POST':
        form = TradeForm(request.POST, instance=trade)
        if form.is_valid():
            form.save()
            return redirect('trade_list', pk=trade.account.pk)
    else:
        form = TradeForm(instance=trade)
    return render(request, 'journal/trade_form.html', {'form': form})

@login_required
def trade_delete(request, pk):
    trade = get_object_or_404(Trade, pk=pk, trade_owner=request.user)
    trade.delete()
    return redirect('trade_list', pk=trade.account.pk)

@login_required
def user_trades(request):
    if request.method == 'POST':
        form = AccountSelectForm(request.user, request.POST)
        if form.is_valid():
            account = form.cleaned_data['account']
            trades = Trade.objects.filter(account=account)
            return render(request, 'journal/user_trades.html', {'trades': trades, 'form': form})
    else:
        form = AccountSelectForm(request.user)
    return render(request, 'journal/user_trades.html', {'form': form})
