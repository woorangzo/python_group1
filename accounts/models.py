from django.db import models


class StockData(models.Model):
    stock_cd = models.CharField(max_length=20)
    stock_dt = models.DateField()
    stock_volume = models.BigIntegerField()
    stock_rate = models.FloatField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    plot_image = models.ImageField(upload_to='pic/', blank=True, null=True)
    prediction_image = models.ImageField(upload_to='pic/', blank=True, null=True)

    def __str__(self):
        return f"{self.stock_cd} - {self.stock_dt}"
    # def get_plot_image_url(self):
    #     if self.plot_image:
    #         return self.plot_image.url
    #     return None
