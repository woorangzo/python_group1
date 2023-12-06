# from django.db import models
#
#
# class Prediction(models.Model):
#     ######objects = None
#     stock_nm = models.CharField(max_length=20)
#     stock_cd = models.CharField(max_length=20)
#     stock_dt = models.DateField
#     last_actual_close = models.DecimalField(max_digits=10, decimal_places=2)
#     predicted_close = models.DecimalField(max_digits=10, decimal_places=2)
#     change_rate = models.FloatField()
#     last_actual_volume = models.IntegerField()
#     graph_image = models.ImageField(upload_to='prediction_graphs/')
#
#
# class Stock(models.Model):
#     stock_cd = models.CharField(max_length=20, primary_key=True)
#     stock_dt = models.DateField
#     stock_volume = models.BigIntegerField()
#     stock_rate = models.FloatField()
#     open_price = models.DecimalField(max_digits=10, decimal_places=2)
#     close_price = models.DecimalField(max_digits=10, decimal_places=2)
#     high_price = models.DecimalField(max_digits=10, decimal_places=2)
#     low_price = models.DecimalField(max_digits=10, decimal_places=2)
#
#     class Meta:
#         db_table = 'stock'
#
#
# class Info(models.Model):
#     stock_cd = models.CharField(max_length=20, primary_key=True)
#     stock_nm = models.CharField(max_length=20)
#
#
#
