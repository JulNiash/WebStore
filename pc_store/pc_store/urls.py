"""
URL configuration for pc_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth.views import LogoutView



from store import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    path('', views.home, name='home'),

    path('admin/', admin.site.urls),

    path('brands/', views.brand_list, name='brands_list'),  # Добавил список брендов
    path('brands/add/', views.add_brand, name='add_brand'),
    path('brands/update/<int:brand_id>/', views.update_brand, name='update_brand'),
    path('brands/delete/<int:brand_id>/', views.delete_brand, name='delete_brand'),

    path('offers/create/<str:product_type>/<int:product_id>/', views.create_offer, name='create_offer'),
    path('offers/store/<int:store_id>/', views.store_offers, name='store_offers'),
    path('offers/edit/<int:offer_id>/', views.edit_offer, name='edit_offer'),
    path('offers/delete/<int:offer_id>/', views.delete_offer, name='delete_offer'),

    path('stores/', views.store_list, name='stores_list'),
    path('stores/<int:store_id>/', views.store_detail, name='store_detail'),
    path('stores/create/', views.store_create, name='store_create'),
    path('stores/update/<int:store_id>/', views.store_update, name='store_update'),
    path('stores/delete/<int:store_id>/', views.store_delete, name='store_delete'),

    path('motherboards/', views.motherboards_list, name='motherboards_list'),
    path('motherboards/<int:motherboard_id>/', views.motherboard_detail, name='motherboard_detail'),
    path('motherboards/create/', views.create_motherboard, name='create_motherboard'),
    path('motherboards/update/<int:motherboard_id>/', views.update_motherboard, name='update_motherboard'),
    path('motherboards/delete/<int:motherboard_id>/', views.delete_motherboard, name='delete_motherboard'),

    path('processors/', views.processor_list, name='processors_list'),
    path('processors/<int:processor_id>/', views.processor_detail, name='processor_detail'),
    path('processors/create/', views.create_processor, name='create_processor'),
    path('processors/update/<int:processor_id>/', views.update_processor, name='update_processor'),
    path('processors/delete/<int:processor_id>/', views.delete_processor, name='delete_processor'),

    path('graphic-cards/', views.graphic_card_list, name='graphic_cards_list'),
    path('graphic-cards/<int:graphic_card_id>/', views.graphic_card_detail, name='graphic_card_detail'),
    path('graphic-cards/create/', views.create_graphic_card, name='create_graphic_card'),
    path('graphic-cards/update/<int:graphic_card_id>/', views.update_graphic_card, name='update_graphic_card'),
    path('graphic-cards/delete/<int:graphic_card_id>/', views.delete_graphic_card, name='delete_graphic_card'),

    path('rams/', views.ram_list, name='rams_list'),
    path('rams/<int:ram_id>/', views.ram_detail, name='ram_detail'),
    path('rams/create/', views.create_ram, name='create_ram'),
    path('rams/update/<int:ram_id>/', views.update_ram, name='update_ram'),
    path('rams/delete/<int:ram_id>/', views.delete_ram, name='delete_ram'),

    path('storages/', views.storages_list, name='storages_list'),
    path('storages/<int:storage_id>/', views.storage_detail, name='storage_detail'),
    path('storages/create/', views.create_storage, name='create_storage'),
    path('storages/update/<int:storage_id>/', views.update_storage, name='update_storage'),
    path('storages/delete/<int:storage_id>/', views.delete_storage, name='delete_storage'),

    path('power_supplys/', views.power_supplys_list, name='power_supplys_list'),  # Исправил множественное число
    path('power_supplys/<int:power_supply_id>/', views.power_supply_detail, name='power_supply_detail'),
    path('power_supplys/create/', views.create_power_supply, name='create_power_supply'),
    path('power_supplys/update/<int:power_supply_id>/', views.update_power_supply, name='update_power_supply'),
    path('power_supplys/delete/<int:power_supply_id>/', views.delete_power_supply, name='delete_power_supply'),

    path('cases/', views.cases_list, name='cases_list'),
    path('cases/<int:case_id>/', views.case_detail, name='case_detail'),
    path('cases/create/', views.create_case, name='create_case'),
    path('cases/update/<int:case_id>/', views.update_case, name='update_case'),
    path('cases/delete/<int:case_id>/', views.delete_case, name='delete_case'),

    path('basket/', views.basket_view, name='basket_view'),
    path('basket/add/<int:offer_id>/', views.add_to_basket, name='add_to_basket'),
    path('basket/remove/<int:item_id>/', views.remove_from_basket, name='remove_from_basket'),
]
