from audioop import reverse

from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.http import HttpResponseForbidden
from .models import Basket, BasketItem



from store.models import Motherboard, Processor, GraphicCard, RAM, Storage, PowerSupply, Case, Brand, Offer, Store
from store.forms import MotherboardForm, ProcessorForm, GraphicCardForm, RAMForm, StorageForm, PowerSupplyForm, \
    CaseForm, BrandForm, OfferForm, StoreForm


def staff_required(function):
    return user_passes_test(lambda u: u.is_staff)(function)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def is_store_owner_or_admin(user, store):
    return user.is_superuser or store.owner == user

@login_required
def store_offers(request, store_id):
    """Просмотр офферов магазина (доступен всем)"""
    store = get_object_or_404(Store, id=store_id)
    offers = Offer.objects.filter(store=store)
    return render(request, 'offers/store_offers.html', {'store': store, 'offers': offers})

@login_required
def create_offer(request, product_type, product_id):
    """Создание предложения для товара (только владельцы магазинов и админы)"""
    model_map = {
        "motherboard": Motherboard,
        "processor": Processor,
        "graphic_card": GraphicCard,
        "ram": RAM,
        "storage": Storage,
        "power_supply": PowerSupply,
        "case": Case
    }

    model = model_map.get(product_type)
    if not model:
        raise Http404("Неверный тип продукта")

    product = get_object_or_404(model, id=product_id)
    stores = Store.objects.filter(owner=request.user)
    if not stores.exists():
        return HttpResponseForbidden("У вас нет магазинов для создания предложения.")

    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.store = form.cleaned_data['store']
            if not is_store_owner_or_admin(request.user, offer.store):
                return HttpResponseForbidden("Вы не можете добавить предложение в этот магазин.")
            setattr(offer, product_type, product)
            offer.save()
            return redirect(f'{product_type}s_list')
    else:
        form = OfferForm()

    return render(request, 'offers/offer_form.html', {'form': form, 'product': product, 'stores': stores})

@login_required
def delete_offer(request, offer_id):
    """Удаление предложения (только владелец магазина или админ)"""
    offer = get_object_or_404(Offer, id=offer_id)
    if not is_store_owner_or_admin(request.user, offer.store):
        return HttpResponseForbidden("Вы не можете удалить это предложение.")
    next_url = request.GET.get('next', f"{offer.get_product().__class__.__name__.lower()}s_list")
    offer.delete()
    return redirect(resolve_url(next_url))

@login_required
def edit_offer(request, offer_id):
    """Редактирование предложения (только владелец магазина или админ)"""
    offer = get_object_or_404(Offer, id=offer_id)
    if not is_store_owner_or_admin(request.user, offer.store):
        return HttpResponseForbidden("У вас нет прав для редактирования этого предложения.")
    if request.method == "POST":
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('store_detail', store_id=offer.store.id)
    else:
        form = OfferForm(instance=offer)
    return render(request, 'offers/offer_form.html', {'form': form, 'edit_mode': True})


def store_list(request):
    stores = Store.objects.all()
    return render(request, 'stores/stores_list.html', {'stores': stores})

def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    offers = Offer.objects.filter(store=store)
    return render(request, 'stores/store_detail.html', {'store': store, 'offers': offers})

@login_required
def store_create(request):
    if not hasattr(request.user, 'seller_profile'):
        return HttpResponseForbidden("Вы не можете создать магазин.")

    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            store.save()
            return redirect('store_detail', store_id=store.id)
    else:
        form = StoreForm()
    return render(request, 'stores/store_form.html', {'form': form})

@login_required
def store_update(request, store_id):
    store = get_object_or_404(Store, id=store_id)

    if store.owner != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("Вы не можете редактировать этот магазин.")

    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            return redirect('store_detail', store_id=store.id)
    else:
        form = StoreForm(instance=store)

    return render(request, 'stores/store_form.html', {'form': form, 'store': store})

@login_required
def store_delete(request, store_id):
    store = get_object_or_404(Store, id=store_id)

    if store.owner != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("Вы не можете удалить этот магазин.")

    if request.method == 'POST':
        store.delete()
        return redirect('stores_list')

    return render(request, 'stores/store_confirm_delete.html', {'store': store})

def staff_required(function):
    return user_passes_test(lambda u: u.is_superuser)(function)

# Список брендов (все могут просматривать)
def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'brands/brands_list.html', {'brands': brands})

@login_required
@staff_required
def add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('brands_list')  # Редирект на список брендов
    else:
        form = BrandForm()
    return render(request, 'brands/brand_form.html', {'form': form})

@login_required
@staff_required
def update_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            return redirect('brands_list')
    else:
        form = BrandForm(instance=brand)
    return render(request, 'brands/brand_form.html', {'form': form})

@login_required
@staff_required
def delete_brand(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    if request.method == 'POST':
        brand.delete()
        return redirect('brands_list')
    return render(request, 'brands/brand_confirm_delete.html', {'brand': brand})


def motherboards_list(request):
    motherboards = Motherboard.objects.prefetch_related("motherboard_offers")
    return render(request, "motherboards/motherboards_list.html", {"motherboards": motherboards})


def motherboard_detail(request, motherboard_id):
    motherboard = get_object_or_404(Motherboard, id = motherboard_id)
    return render(request, 'motherboards/motherboard_detail.html', {'motherboard':motherboard})


@login_required
def create_motherboard(request):
    """Создание нового товара (если его нет)"""
    if request.method == 'POST':
        form = MotherboardForm(request.POST)
        if form.is_valid():
            motherboard = form.save(commit=False)
            motherboard.save()
            return redirect('motherboards_list')
    else:
        form = MotherboardForm()

    return render(request, 'motherboards/motherboard_form.html', {'form': form})


@login_required
def update_motherboard(request, motherboard_id):
    motherboard = get_object_or_404(Motherboard, id=motherboard_id)
    if request.method == 'POST':
        form = MotherboardForm(request.POST, instance=motherboard)
        if form.is_valid():
            form.save()
            return redirect('motherboard_detail', motherboard_id = motherboard.id)
    else:
        form = MotherboardForm(instance=motherboard)
    return render(request, 'motherboards/motherboard_form.html', {'form':form})

@login_required
def delete_motherboard(request, motherboard_id):
    motherboard = get_object_or_404(Motherboard, id=motherboard_id)
    if request.method == 'POST':
        motherboard.delete()
        return redirect('motherboards_list')
    return render(request, 'motherboards/motherboard_confirm_delete.html', {'motherboard':motherboard})



def processor_list(request):
    processors = Processor.objects.prefetch_related("processor_offers")
    return render(request, 'processors/processors_list.html', {'processors':processors})

def processor_detail(request, processor_id):
    processor = get_object_or_404(Processor, id = processor_id)
    return render(request, 'processors/processor_detail.html', {'processor':processor})

@login_required
def create_processor(request):
    if request.method == 'POST':
        form = ProcessorForm(request.POST)
        if form.is_valid():
            processor = form.save(commit=False)
            processor.save()
            return redirect('processors_list')
    else:
        form = ProcessorForm()
    return render(request, 'processors/processor_form.html', {'form':form})

@login_required
def update_processor(request, processor_id):
    processor = get_object_or_404(Processor, id=processor_id)
    if request.method == 'POST':
        form = ProcessorForm(request.POST, instance=processor)
        if form.is_valid():
            form.save()
            return redirect('processor_detail', processor_id = processor.id)
    else:
        form = ProcessorForm(instance=processor)
    return render(request, 'processors/processor_form.html', {'form':form})

@login_required
def delete_processor(request, processor_id):
    processor = get_object_or_404(Processor, id=processor_id)
    if request.method == 'POST':
        processor.delete()
        return redirect('processors_list')
    return render(request, 'processors/processor_confirm_delete.html', {'processor':processor})



def graphic_card_list(request):
    graphic_cards = GraphicCard.objects.prefetch_related("graphic_card_offers")
    return render(request, 'graphic_cards/graphic_cards_list.html', {'graphic_cards':graphic_cards})

def graphic_card_detail(request, graphic_card_id):
    graphic_card = get_object_or_404(GraphicCard, id = graphic_card_id)
    return render(request, 'graphic_cards/graphic_card_detail.html', {'graphic_card':graphic_card})

@login_required
def create_graphic_card(request):
    if request.method == 'POST':
        form = GraphicCardForm(request.POST)
        if form.is_valid():
            graphic_card = form.save(commit=False)
            graphic_card.save()
            return redirect('graphic_cards_list')
    else:
        form = GraphicCardForm()
    return render(request, 'graphic_cards/graphic_card_form.html', {'form':form})

@login_required
def update_graphic_card(request, graphic_card_id):
    graphic_card = get_object_or_404(GraphicCard, id=graphic_card_id)
    if request.method == 'POST':
        form = GraphicCardForm(request.POST, instance=graphic_card)
        if form.is_valid():
            form.save()
            return redirect('graphic_card_detail', graphic_card_id = graphic_card.id)
    else:
        form = GraphicCardForm(instance=graphic_card)
    return render(request, 'graphic_cards/graphic_card_form.html', {'form':form})

@login_required
def delete_graphic_card(request, graphic_card_id):
    graphic_card = get_object_or_404(GraphicCard, id=graphic_card_id)
    if request.method == 'POST':
        graphic_card.delete()
        return redirect('graphic_cards_list')
    return render(request, 'graphic_cards/graphic_card_confirm_delete.html', {'graphic_card':graphic_card})



def ram_list(request):
    rams = RAM.objects.prefetch_related("ram_offers")
    return render(request, 'rams/rams_list.html', {'rams':rams})

def ram_detail(request, ram_id):
    ram = get_object_or_404(RAM, id = ram_id)
    return render(request, 'rams/ram_detail.html', {'ram':ram})

@login_required
def create_ram(request):
    if request.method == 'POST':
        form = RAMForm(request.POST)
        if form.is_valid():
            ram = form.save(commit=False)
            ram.save()
            return redirect('rams_list')
    else:
        form = RAMForm()
    return render(request, 'rams/ram_form.html', {'form':form})

@login_required
def update_ram(request, ram_id):
    ram = get_object_or_404(RAM, id=ram_id)
    if request.method == 'POST':
        form = RAMForm(request.POST, instance=ram)
        if form.is_valid():
            form.save()
            return redirect('ram_detail', ram_id = ram.id)
    else:
        form = RAMForm(instance=ram)
    return render(request, 'rams/ram_form.html', {'form':form})

@login_required
def delete_ram(request, ram_id):
    ram = get_object_or_404(RAM, id=ram_id)
    if request.method == 'POST':
        ram.delete()
        return redirect('rams_list')
    return render(request, 'rams/ram_confirm_delete.html', {'ram':ram})



def storages_list(request):
    storages = Storage.objects.prefetch_related("storage_offers")
    return render(request, 'storages/storages_list.html', {'storages':storages})

def storage_detail(request, storage_id):
    storage = get_object_or_404(Storage, id = storage_id)
    return render(request, 'storages/storage_detail.html', {'storage':storage})

@login_required
def create_storage(request):
    if request.method == 'POST':
        form = StorageForm(request.POST)
        if form.is_valid():
            storage = form.save(commit=False)
            storage.save()
            return redirect('storages_list')
    else:
        form = StorageForm()
    return render(request, 'storages/storage_form.html', {'form':form})

@login_required
def update_storage(request, storage_id):
    storage = get_object_or_404(Storage, id=storage_id)
    if request.method == 'POST':
        form = StorageForm(request.POST, instance=storage)
        if form.is_valid():
            form.save()
            return redirect('storage_detail', storage_id = storage.id)
    else:
        form = StorageForm(instance=storage)
    return render(request, 'storages/storage_form.html', {'form':form})

@login_required
def delete_storage(request, storage_id):
    storage = get_object_or_404(Storage, id=storage_id)
    if request.method == 'POST':
        storage.delete()
        return redirect('storages_list')
    return render(request, 'storages/storage_confirm_delete.html', {'storage':storage})




def power_supplys_list(request):
    power_supplys = PowerSupply.objects.prefetch_related("power_supply_offers")
    return render(request, 'power_supplys/power_supplys_list.html', {'power_supplys':power_supplys})

def power_supply_detail(request, power_supply_id):
    power_supply = get_object_or_404(PowerSupply, id = power_supply_id)
    return render(request, 'power_supplys/power_supply_detail.html', {'power_supply':power_supply})

@login_required
def create_power_supply(request):
    if request.method == 'POST':
        form = PowerSupplyForm(request.POST)
        if form.is_valid():
            power_supply = form.save(commit=False)
            power_supply.save()
            return redirect('power_supplys_list')
    else:
        form = PowerSupplyForm()
    return render(request, 'power_supplys/power_supply_form.html', {'form':form})

@login_required
def update_power_supply(request, power_supply_id):
    power_supply = get_object_or_404(PowerSupply, id=power_supply_id)
    if request.method == 'POST':
        form = PowerSupplyForm(request.POST, instance=power_supply)
        if form.is_valid():
            form.save()
            return redirect('power_supply_detail', power_supply_id = power_supply.id)
    else:
        form = PowerSupplyForm(instance=power_supply)
    return render(request, 'power_supplys/power_supply_form.html', {'form':form})

@login_required
def delete_power_supply(request, power_supply_id):
    power_supply = get_object_or_404(PowerSupply, id=power_supply_id)
    if request.method == 'POST':
        power_supply.delete()
        return redirect('power_supplys_list')
    return render(request, 'power_supplys/power_supply_confirm_delete.html', {'power_supply':power_supply})



def cases_list(request):
    cases = Case.objects.prefetch_related("case_offers").all()
    return render(request, 'cases/cases_list.html', {'cases':cases})

def case_detail(request, case_id):
    case = get_object_or_404(Case, id = case_id)
    return render(request, 'cases/case_detail.html', {'case':case})

@login_required
def create_case(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.save()
            return redirect('cases_list')
    else:
        form = CaseForm()
    return render(request, 'cases/case_form.html', {'form':form})

@login_required
def update_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            return redirect('case_detail', case_id = case.id)
    else:
        form = CaseForm(instance=case)
    return render(request, 'cases/case_form.html', {'form':form})

@login_required
def delete_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if request.method == 'POST':
        case.delete()
        return redirect('cases_list')
    return render(request, 'cases/case_confirm_delete.html', {'case':case})


@login_required
def add_to_basket(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    basket, created = Basket.objects.get_or_create(user=request.user)

    item, created = BasketItem.objects.get_or_create(basket=basket, offer=offer)
    if not created:
        item.quantity += 1
        item.save()

    return redirect('basket_view')


@login_required
def basket_view(request):
    basket, created = Basket.objects.get_or_create(user=request.user)
    return render(request, 'basket.html', {'basket': basket})


@login_required
def remove_from_basket(request, item_id):
    item = get_object_or_404(BasketItem, id=item_id, basket__user=request.user)
    item.delete()
    return redirect('basket_view')
