from django import forms
from store.models import (
    Motherboard, Processor, GraphicCard, RAM, Storage, PowerSupply, Case, Brand, Offer, Store
)


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['store', 'price', 'quantity']

class ProductForm(forms.ModelForm):
    class Meta:
        fields = ['title', 'description', 'brand']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description']



class MotherboardForm(ProductForm):
    class Meta(ProductForm.Meta):
        model = Motherboard
        fields = ProductForm.Meta.fields + ['chipset', 'socket', 'memory']


class ProcessorForm(ProductForm):
    class Meta(ProductForm.Meta):
        model = Processor
        fields = ProductForm.Meta.fields + ['ghz', 'cores', 'cache']


class GraphicCardForm(ProductForm):
    class Meta(ProductForm.Meta):
        model = GraphicCard
        fields = ProductForm.Meta.fields + ['gb', 'memory_type']


class RAMForm(ProductForm):
    class Meta(ProductForm.Meta):
        model = RAM
        fields = ProductForm.Meta.fields + ['capacity', 'memory_type', 'mhz']


class StorageForm(ProductForm):
    class Meta(ProductForm.Meta):
        model = Storage
        fields = ProductForm.Meta.fields + ['capacity', 'interface']


class PowerSupplyForm(ProductForm):
    class Meta(ProductForm.Meta):
        model = PowerSupply
        fields = ProductForm.Meta.fields + ['wattage', 'modular']


class CaseForm(ProductForm):
    class Meta(ProductForm.Meta):
        model = Case
        fields = ProductForm.Meta.fields + ['height', 'width', 'depth']


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']

