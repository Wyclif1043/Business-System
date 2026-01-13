from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    commission_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def total_sales_amount(self):
        return self.quantity * self.product.selling_price

    def total_commission(self):
        return self.quantity * self.product.commission_per_unit

    def total_cost(self):
        return self.quantity * self.product.cost_per_unit

    def profit(self):
        return self.total_sales_amount() - self.total_cost() - self.total_commission()


class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
