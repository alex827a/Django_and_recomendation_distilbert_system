from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.core.paginator import Paginator

from.forms import NewItemForm,EditItemForm,ReviewForm
from.models import Item,Category,Review

def items(request):
    query=request.GET.get('query','')
    category_id=request.GET.get('category', 0)
    categories=Category.objects.all()
    items=Item.objects.filter(is_sold=False)

    if category_id:
        items=items.filter(category_id=category_id)

    if query:
        items=items.filter(Q(name__icontains=query) | Q(description__icontains=query) )

    return render(request,'item/items.html',{

        'items':items,
        'query':query,
        'categories':categories,
        'category_id':int(category_id),
    })
# Create your views here.

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[:5]
    reviews = item.reviews.all()
    item_marketplaces = item.marketplaces.all()

    review_form = None

    if request.user.is_authenticated:
        if request.method == 'POST':
            review_form = ReviewForm(request.POST)
            if not Review.objects.filter(item=item, user=request.user).exists():
                if review_form.is_valid():
                    review = review_form.save(commit=False)
                    review.item = item
                    review.user = request.user
                    review.save()
                    messages.success(request, 'Your review has been added!')
                    return redirect('item:detail', pk=item.pk)
                else:
                    messages.error(request, 'There was an error in your form.')
            else:
                messages.error(request, "You've already reviewed this product.")
        else:
            review_form = ReviewForm()

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
        'reviews': reviews,
        'review_form': review_form,
        'item_marketplaces': item_marketplaces,
    })

def add_review(request, pk):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = get_object_or_404(Item, pk=pk)
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been added!')
            return redirect('item:detail', pk=pk)
    else:
        return redirect('item:detail', pk=pk)
@login_required
def new(request):
    if request.method=='POST':
        form=NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item=form.save(commit=False)
            item.created_by=request.user
            item.save()

            return redirect('item:detail',pk=item.id)
    else:    
        form=NewItemForm()
    
    return render(request,'item/form.html',{
        'form':form,
        'title':'New Item',


    })
@login_required
def edit(request,pk):
    item=get_object_or_404(Item,pk=pk,created_by=request.user)

    if request.method=='POST':
        form=EditItemForm(request.POST, request.FILES,instance=item)
        if form.is_valid():
            form.save()
            return redirect('item:detail',pk=item.id)
    else:    
        form=EditItemForm(instance=item)
    
    return render(request,'item/form.html',{
        'form':form,
        'title':'Edit Item',


    })
@login_required
def delete(request,pk):
    item=get_object_or_404(Item,pk=pk,created_by=request.user)
    item.delete()

    return redirect('dashboard:index')
@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated!')
            # Item page redirections
            return redirect('item:detail', pk=review.item.pk)
        else:
            print(form.errors.as_data()) 
            messages.error(request, 'There was an error with your review form.')
    
    # If method POST or Form not valid, return user on ite, page
 
    return redirect('item:detail', pk=review.item.pk)
def edit_review_view(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('some_view_name')  
    else:
        form = ReviewForm(instance=review)
    return render(request, 'edit_review.html', {'form': form})    


def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    paginator = Paginator(items, 9)  # 9 item on page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'item/items.html', {
        'items': page_obj,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    })
