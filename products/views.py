from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic import ListView, TemplateView

from common.views import TitleMixin
from products.models import Basket, Product, ProductBrand, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['is_promotion'] = True
        return context


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3  # 3 products / page
    title = 'Store - Catalog'
    chosen_category_id = None
    chosen_brand_id = None

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')  # from urls.py
        brand_id = self.kwargs.get('brand_id')
        filters = {}

        if category_id and category_id != 0:
            self.chosen_category_id = category_id
            filters['category_id'] = category_id
        if brand_id and brand_id != 0:
            self.chosen_brand_id = brand_id
            filters['brand_id'] = brand_id

        if filters:
            return queryset.filter(**filters)
        else:
            return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()

        context['categories'] = ProductCategory.objects.all()
        context['category_id'] = self.chosen_category_id

        context['brands'] = ProductBrand.objects.all()
        context['brand_id'] = self.chosen_brand_id

        return context


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
