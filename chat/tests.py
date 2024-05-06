from django.test import TestCase

from chat.models import Shop, User
from django.urls import reverse


class MyTestCase(TestCase):

    def test_model(self):
        self.assertGreater(User.objects.all().count(), 1)  # Userが1件以上存在する
        self.assertGreater(Shop.objects.all().count(), 1)  # Shopが1件以上存在する

        # modelの作成
        user = User.objects.create(name="HIKARU")
        shop = Shop.objects.create(
            name="Product 1", money=100, size=5, quantity=10, color="Red", manager=user
        )

        # modelの中身を確認
        self.assertEqual(shop.name, "Product 1")
        self.assertEqual(str(shop), "Product 1")
        self.assertEqual(shop.money, 100)
        self.assertEqual(shop.size, 5)
        self.assertEqual(shop.quantity, 10)
        self.assertEqual(shop.color, "Red")
        self.assertEqual(shop.manager, user)

        # userを削除するとshopのmanagerはnullになる
        user.delete()
        shop.refresh_from_db()
        self.assertIsNone(shop.manager)

    def test_urls(self):
        # GET
        self.assertEqual(self.client.get(reverse("index")).status_code, 200)
        self.assertEqual(
            self.client.get(reverse("room", kwargs={"room_name": "room"})).status_code, 200
        )
        # POST
        post_data = "id=1&field=name&type=text&value=New Value"  # リクエストボディの文字列
        response = self.client.post(
            reverse("room", kwargs={"room_name": "room"}),
            data=post_data,
            content_type="application/x-www-form-urlencoded"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = self.client.get(reverse("room", kwargs={"room_name": "room"}))
        self.assertContains(response, 'spreadsheet')

    def test_views(self):
        response = self.client.get(reverse("room", kwargs={"room_name": "room"}))
        params = {
            'check': 'チェック:',
            'fields': [
                'id', 'name', 'money', 'size', 'quantity', 'color', 'date', 'time',
                'sold', 'note', 'manager', 'manager_check'
            ],
            'colHeaders': [
                'ID', '商品名', '金額', '大きさ', '個数', '色', '日付', '時間',
                '売り切れ', '備考', '担当者', '担当者チェック'
            ],
            'columns': [
                {'data': 0, 'type': 'numeric'}, {'data': 1, 'type': 'text'},
                {'data': 2, 'type': 'numeric'}, {'data': 3, 'type': 'numeric'},
                {'data': 4, 'type': 'numeric'}, {'data': 5, 'type': 'text'},
                {'data': 6, 'type': 'date', 'dateFormat': 'YYYY-MM-DD'},
                {'data': 7, 'type': 'time', 'timeFormat': 'HH:mm'},
                {'data': 8, 'type': 'text'},
                {'data': 9, 'type': 'text'},
                {'data': 10, 'type': 'dropdown', 'source': ['', 'hikaru', 'taro', 'hanako']},
                {'data': 11, 'type': 'checkbox', 'className': 'htCenter htMiddle'}
            ]
        }
        self.assertEqual(response.context["check"], params['check'])
        self.assertEqual(response.context["fields"], params['fields'])
        self.assertEqual(response.context["colHeaders"], params['colHeaders'])
        self.assertEqual(response.context["columns"], params['columns'])
