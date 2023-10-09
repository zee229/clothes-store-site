from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductBrand, ProductCategory
from products.views import ProductsListView


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)  # code 200
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'products.json', 'brands.json']
    paginate_by = ProductsListView.paginate_by

    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[:3]))

    def test_list_with_filters(self):
        category = ProductCategory.objects.first()
        brand = ProductBrand.objects.first()
        path = reverse('products:filters', kwargs={'category_id': category.id, 'brand_id': brand.id})
        response = self.client.get(path)

        self._common_tests(response)
        filters = {'category_id': category.id, 'brand_id': brand.id}
        self.assertEqual(
            list(response.context_data['object_list']),
            # list(self.products.filter(category_id=category.id))[:self.paginate_by]
            list(self.products.filter(**filters))[:self.paginate_by]
        )

    def _common_tests(self, response):
        """
        common for all tests in ProductsListViewTestCase
        usage: self._common_tests(response)
        """
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Catalog')
        self.assertTemplateUsed(response, 'products/products.html')
