from django.core.management.base import BaseCommand
from decimal import Decimal
from grocery_app.models import Category, Product

class Command(BaseCommand):
    help = 'Create sample categories and products for testing'

    def handle(self, *args, **options):
        # Create categories
        cats = [
            ('Fruits & Vegetables', 'Fresh produce including fruits and vegetables'),
            ('Dairy & Eggs', 'Fresh dairy products and eggs'),
            ('Beverages', 'Soft drinks, juices, and other beverages'),
            ('Bakery', 'Fresh bread, pastries, and baked goods'),
        ]

        for name, desc in cats:
            Category.objects.get_or_create(name=name, defaults={'description': desc})

        # Create products
        products = [
            ('Fresh Apples', 'Fruits & Vegetables', 'Fresh, crispy red apples', '2.99', 100),
            ('Whole Milk', 'Dairy & Eggs', 'Fresh whole milk, 1 gallon', '3.99', 50),
            ('Cola 2L', 'Beverages', 'Refreshing cola drink, 2L bottle', '1.99', 200),
            ('Whole Grain Bread', 'Bakery', 'Freshly baked whole grain bread', '3.49', 30),
        ]

        for name, cat_name, desc, price, stock in products:
            cat = Category.objects.get(name=cat_name)
            prod, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'category': cat,
                    'description': desc,
                    'price': Decimal(price),
                    'stock': stock,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {prod.name}'))
            else:
                self.stdout.write(self.style.NOTICE(f'Product already exists: {prod.name}'))

        self.stdout.write(self.style.SUCCESS('Seeding complete.'))
