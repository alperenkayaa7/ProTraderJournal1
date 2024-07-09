from django import forms
from .models import Account, Trade, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'account_name', 'account_balance', 'account_r',
            'daily_profit_target_r', 'daily_loss_limit_r',
            'daily_operation_limit', 'profit_streak_limit',
            'loss_streak_limit', 'operation_profit_limit',
            'operation_loss_limit', 'favorites_tickers',
            'favorites_timeframes', 'favorites_strategies',
            'loss_profit_calculated_balance'
        ]

class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = [
            'account', 'ticker', 'entry_price', 'stop_price', 'tp_price', 'trade_type',
            'commission', 'timeframe', 'trend', 'risk_r', 'quantity',
            'chart', 'comments', 'emotions_before'
        ]
        widgets = {
            'entry_price': forms.NumberInput(attrs={'step': '0.00001'}),
            'stop_price': forms.NumberInput(attrs={'step': '0.00001'}),
            'tp_price': forms.NumberInput(attrs={'step': '0.00001'}),
            'close_price': forms.NumberInput(attrs={'step': '0.00001'}),
            'risk_r': forms.NumberInput(attrs={'step': '0.01'}),
            'commission': forms.NumberInput(attrs={'step': '0.01'}),
        }

class TradeUpdateForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = [
            'close_price', 'emotions_during', 'emotions_after', 'trade_result',
            'visibility', 'session', 'close_date'
        ]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date']

class AccountSelectForm(forms.Form):
    account = forms.ModelChoiceField(queryset=Account.objects.none(), empty_label="Select Account")

    def __init__(self, user, *args, **kwargs):
        super(AccountSelectForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(owner=user)
