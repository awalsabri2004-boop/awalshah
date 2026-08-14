from django.shortcuts import render, redirect
from django.db.models import Sum, F  # Tambah F kat sini untuk darab Kuantiti * Harga
from django.contrib import messages
from .models import Item
from .forms import ItemForm

# 1. HALAMAN UTAMA (LIST, ADD & DASHBOARD)
def home(request):
    items = Item.objects.all()
    
    total_items = items.count()
    total_stock = items.aggregate(Sum('quantity'))['quantity__sum'] or 0
    
    # Kira TOTAL RM: Sum(Kuantiti * Harga)
    total_value = items.aggregate(total=Sum(F('quantity') * F('price')))['total'] or 0

    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Barang berjaya ditambah!')
            return redirect('home')

    context = {
        'items': items,
        'form': form,
        'total_items': total_items,
        'total_stock': total_stock,
        'total_value': total_value,  # Variable untuk TOTAL RM
    }
    return render(request, 'index.html', context)

# 2. FUNGSI PADAM BARANG (DELETE)
def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    messages.success(request, 'Barang berjaya dipadam!')
    return redirect('home')

# 3. FUNGSI KEMASKINI BARANG (EDIT)
def edit_item(request, item_id):
    item = Item.objects.get(id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Barang berjaya dikemaskini!')
            return redirect('home')
    else:
        form = ItemForm(instance=item)
    return render(request, 'edit.html', {'form': form, 'item': item})