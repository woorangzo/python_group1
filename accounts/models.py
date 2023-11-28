from django.db import models

from Dataset import CategoryInfo, StockInfo


# class StockData(models.Model):
#     stock_cd = models.CharField(max_length=20)
#     stock_dt = models.DateField()
#     stock_volume = models.BigIntegerField()
#     stock_rate = models.FloatField()
#     open_price = models.DecimalField(max_digits=10, decimal_places=2)
#     close_price = models.DecimalField(max_digits=10, decimal_places=2)
#     high_price = models.DecimalField(max_digits=10, decimal_places=2)
#     low_price = models.DecimalField(max_digits=10, decimal_places=2)
#     plot_image = models.ImageField(upload_to='pic/', blank=True, null=True)
#     prediction_image = models.ImageField(upload_to='pic/', blank=True, null=True)

    # def __str__(self):
    #     return f"{self.stock_cd} - {self.stock_dt}"
    # # def get_plot_image_url(self):
    # #     if self.plot_image:
    # #         return self.plot_image.url
    # #     return None

class Member(models.Model):
    member_id = models.CharField(max_length=100,primary_key=True)
    member_pw = models.CharField(max_length=100)
    member_repw = models.CharField(max_length=100,default='')
    phone = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(null=True)
    jumin = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Stock(models.Model):
    stock_cd = models.CharField(max_length=20)
    stock_dt = models.DateField()
    stock_volume = models.BigIntegerField()
    stock_rate = models.FloatField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)

class CategoryInfo(models.Model):
    stock_cd = models.CharField(max_length=20)
    category_nm = models.CharField(max_length=20)
    category_total = models.BigIntegerField()


class StockInfo(models.Model):
    stock_cd = models.CharField(max_length=20, primary_key=True)
    stock_nm = models.CharField(max_length=20)
    market_type = models.CharField(max_length=10)



