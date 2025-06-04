import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.factories import CategoryFactory, ProductFactory


class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory()
        self.product.category.add(self.category)

        self.order = OrderFactory(user=self.user)
        self.order.product.add(self.product)

    def test_order(self):
        response = self.client.get(reverse("order-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)
        self.assertEqual(
            order_data["results"][0]["product"][0]["title"], self.product.title
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["price"], self.product.price
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["active"], self.product.active
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["category"][0]["title"],
            self.category.title,
        )

    def test_create_order(self):
        new_user = UserFactory()
        self.client.force_authenticate(user=new_user)

        product = ProductFactory()
        data = json.dumps({"products_id": [product.id], "user": new_user.id})

        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=new_user)
        self.assertEqual(created_order.user, new_user)
        self.assertIn(product, created_order.product.all())
