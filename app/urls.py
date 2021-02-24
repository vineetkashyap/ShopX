from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPassword
urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    # path('', views.home),
    path('product-detail/<int:id>', views.product_detail, name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),

    path('pluscart/',views.pluscart),
    path('minuscart/',views.minuscart),
    path('removecart/',views.removecart),


    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    
    path('orders/', views.orders, name='orders'),

    path('changepassword/',auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'), name='changepassword'),

    #password reset
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),

    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPassword),name='password_reset_confirm'),

    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),
#password reset end
    path('passwordchangedone/',auth_views.PasswordResetDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    path('mobile/', views.mobile, name='mobile'), 
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('registration/', views.CustomerRegistrationForm.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done,name='paymentdone'),
    path('search/', views.searchbar,name='search'),

]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
