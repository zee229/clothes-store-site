from django.urls import path

from products.views import ProductsListView, basket_add, basket_remove

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    # path('category/<int:category_id>', ProductsListView.as_view(), name='category'),
    # path('brand/<int:brand_id>', ProductsListView.as_view(), name='brand'),
    path('filters/category=<int:category_id>&brand=<int:brand_id>', ProductsListView.as_view(), name='filters'),
    path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
