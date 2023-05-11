from rest_framework import serializers
from logistic.models import Product, StockProduct, Stock

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = '__all__'

    def create(self, validated_data):

        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        
        for position in positions:
            StockProduct.objects.create(stock=stock, **position)
        
        return stock

    def update(self, instance, validated_data):
        
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)

        for pos in positions:
            StockProduct.objects.update_or_create(
                stock=stock,
                product=pos['product'],
                defaults={'stock': stock, 'product': pos['product'], 'quantity': pos['quantity'], 'price': pos['price']}
            )
        return stock

