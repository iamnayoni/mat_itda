from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, ExpressionWrapper, FloatField, F
from .models import Restaurant, REGION_CHOICES, CATEGORY_CHOICES, PRICE_CHOICES, VIBE_CHOICES, FACILITY_OPTIONS
from .forms import RestaurantForm


def restaurant_list(request):
    qs = Restaurant.objects.select_related('user').all()

    region = request.GET.get('region', '')
    category = request.GET.get('category', '')
    price = request.GET.get('price', '')
    vibe = request.GET.get('vibe', '')
    facilities = request.GET.getlist('facilities')
    sort = request.GET.get('sort', 'latest')
    q = request.GET.get('q', '')

    if region:
        qs = qs.filter(region=region)
    if category:
        qs = qs.filter(category=category)
    if price:
        qs = qs.filter(price_range=price)
    if vibe:
        qs = qs.filter(vibe=vibe)
    if facilities:
        for facility in facilities:
            qs = [r for r in qs if facility in (r.facilities or [])]
        # convert back — needed for annotation below
        ids = [r.id for r in qs]
        qs = Restaurant.objects.select_related('user').filter(id__in=ids)
    if q:
        qs = qs.filter(name__icontains=q)

    if sort == 'rating_desc':
        qs = sorted(qs, key=lambda r: r.rating_avg, reverse=True)
    elif sort == 'rating_asc':
        qs = sorted(qs, key=lambda r: r.rating_avg)
    else:
        # 필터 없을 때는 region 순으로 정렬 → template regroup이 올바르게 동작
        no_filter = not any([region, category, price, vibe, facilities, q])
        if no_filter:
            region_order = ['서울', '부산', '인천', '전주', '경주', '강릉', '제주']
            order_map = {r: i for i, r in enumerate(region_order)}
            qs_list = list(qs.order_by('-created_at'))
            qs = sorted(qs_list, key=lambda r: order_map.get(r.region, 99))
        elif hasattr(qs, 'order_by'):
            qs = qs.order_by('-created_at')

    context = {
        'restaurants': qs,
        'total': len(qs) if isinstance(qs, list) else qs.count(),
        'region_choices': REGION_CHOICES,
        'category_choices': CATEGORY_CHOICES,
        'price_choices': PRICE_CHOICES,
        'vibe_choices': VIBE_CHOICES,
        'facility_options': FACILITY_OPTIONS,
        'current': {
            'region': region,
            'category': category,
            'price': price,
            'vibe': vibe,
            'facilities': facilities,
            'sort': sort,
            'q': q,
        },
    }
    return render(request, 'restaurants/list.html', context)


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    return render(request, 'restaurants/detail.html', {'restaurant': restaurant})


@login_required
def restaurant_create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.user = request.user
            restaurant.save()
            return redirect('restaurant_detail', pk=restaurant.pk)
    else:
        form = RestaurantForm()
    return render(request, 'restaurants/form.html', {'form': form, 'action': '등록'})


@login_required
def restaurant_edit(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk, user=request.user)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('restaurant_detail', pk=restaurant.pk)
    else:
        form = RestaurantForm(instance=restaurant)
    return render(request, 'restaurants/form.html', {'form': form, 'action': '수정', 'restaurant': restaurant})


@login_required
def restaurant_delete(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk, user=request.user)
    if request.method == 'POST':
        restaurant.delete()
        return redirect('restaurant_list')
    return render(request, 'restaurants/confirm_delete.html', {'restaurant': restaurant})
