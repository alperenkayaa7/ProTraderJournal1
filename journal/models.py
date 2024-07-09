from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import json

class SQLiteJSONField(models.TextField):
    def db_type(self, connection):
        return 'TEXT'
    
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return json.loads(value)
    
    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                raise ValidationError("Invalid JSON")
        return value
    
    def get_prep_value(self, value):
        if value is None:
            return value
        return json.dumps(value)

class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_name = models.CharField(max_length=100)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    account_r = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    daily_profit_target_r = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    daily_loss_limit_r = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    daily_operation_limit = models.IntegerField(null=True, blank=True)
    profit_streak_limit = models.IntegerField(null=True, blank=True)
    loss_streak_limit = models.IntegerField(null=True, blank=True)
    operation_profit_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    operation_loss_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    favorites_tickers = SQLiteJSONField(blank=True, null=True)
    favorites_timeframes = SQLiteJSONField(blank=True, null=True)
    favorites_strategies = SQLiteJSONField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    loss_profit_calculated_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.account_name

class Trade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)
    entry_price = models.DecimalField(max_digits=10, decimal_places=5, validators=[MinValueValidator(0)])
    stop_price = models.DecimalField(max_digits=10, decimal_places=5, validators=[MinValueValidator(0)])
    tp_price = models.DecimalField(max_digits=10, decimal_places=5, validators=[MinValueValidator(0)])
    close_price = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    trade_type = models.CharField(max_length=4, choices=[('BUY', 'Buy'), ('SELL', 'Sell')])
    commission = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    timeframe = models.CharField(max_length=10, null=True, blank=True)
    trend = models.CharField(max_length=10, null=True, blank=True)
    risk_r = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    chart = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='trade_images/', null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    emotions_before = models.CharField(max_length=255, null=True, blank=True)
    emotions_during = models.CharField(max_length=255, null=True, blank=True)
    emotions_after = models.CharField(max_length=255, null=True, blank=True)
    trade_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    trade_result = models.CharField(max_length=255, null=True, blank=True)
    visibility = models.CharField(max_length=255, null=True, blank=True)
    session = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    open_date = models.DateTimeField(auto_now_add=True)
    close_date = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trade_type} {self.quantity} {self.ticker} @ {self.entry_price}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
