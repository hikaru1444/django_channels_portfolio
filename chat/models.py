from django.db import models
from django.contrib import admin


class ForeignKeyWithStrToField(models.ForeignKey):
    def __init__(self, *args, to_field=None, **kwargs):
        if to_field is None:
            raise ValueError("to_field is required")
        super().__init__(*args, to_field=to_field, **kwargs)

    def get_to_field(self):
        return self.to_field


class User(models.Model):
    name = models.CharField(verbose_name="担当者", max_length=100, default="no named", unique=True)

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(verbose_name="商品名", max_length=10, default="")
    money = models.IntegerField(verbose_name="金額", null=True)
    size = models.IntegerField(verbose_name="大きさ", null=True)
    quantity = models.IntegerField(verbose_name="個数", null=True)
    color = models.CharField(verbose_name="色", max_length=10, default="")
    date = models.DateField(verbose_name="日付", null=True)
    time = models.TimeField(verbose_name="時間", null=True)
    sold = models.CharField(verbose_name="売り切れ", max_length=10, default="")
    note = models.CharField(verbose_name="備考", max_length=10, default="")
    manager = ForeignKeyWithStrToField(
        User, to_field="name", verbose_name="担当者", on_delete=models.SET_NULL,
        null=True, blank=True
    )
    manager_check = models.BooleanField(verbose_name="担当者チェック", default=False)

    def __str__(self):
        return self.name


admin.site.register(Shop)
admin.site.register(User)
