from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, TradeViewSet, register_view, login_view, profile_view, logout_view, home_view, account_list, account_detail, account_create, account_edit, account_delete, trade_list, trade_detail, trade_create, trade_edit, trade_delete, user_trades

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'trades', TradeViewSet)

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('accounts/', account_list, name='account_list'),
    path('accounts/<uuid:pk>/', account_detail, name='account_detail'),
    path('accounts/create/', account_create, name='account_create'),
    path('accounts/<uuid:pk>/edit/', account_edit, name='account_edit'),
    path('accounts/<uuid:pk>/delete/', account_delete, name='account_delete'),
    path('trades/<uuid:pk>/', trade_list, name='trade_list'),
    path('trades/<uuid:pk>/', trade_detail, name='trade_detail'),
    path('trades/create/', trade_create, name='trade_create'),
    path('trades/<uuid:pk>/edit/', trade_edit, name='trade_edit'),
    path('trades/<uuid:pk>/delete/', trade_delete, name='trade_delete'),
    path('user_trades/', user_trades, name='user_trades'),
    path('api/', include(router.urls)),
]
