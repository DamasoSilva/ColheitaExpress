from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
from decimal import Decimal

from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from .serializers import CartSerializer, CartItemSerializer


class CartView(generics.RetrieveAPIView):
    """
    Visualizar carrinho do usuário
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class AddToCartView(generics.CreateAPIView):
    """
    Adicionar item ao carrinho
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        
        if not product_id:
            return Response(
                {'error': 'product_id é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Produto não encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Verificar estoque
        if product.stock_quantity < quantity:
            return Response(
                {'error': 'Estoque insuficiente'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Obter ou criar carrinho
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Verificar se o item já existe no carrinho
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                'quantity': quantity,
                'unit_price': product.current_price
            }
        )
        
        if not item_created:
            # Item já existe, atualizar quantidade
            new_quantity = cart_item.quantity + quantity
            if product.stock_quantity < new_quantity:
                return Response(
                    {'error': 'Estoque insuficiente para a quantidade solicitada'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = new_quantity
            cart_item.save()
        
        # Retornar carrinho atualizado
        cart_serializer = CartSerializer(cart)
        return Response({
            'message': 'Item adicionado ao carrinho com sucesso',
            'cart': cart_serializer.data
        }, status=status.HTTP_201_CREATED)


class RemoveFromCartView(generics.DestroyAPIView):
    """
    Remover item do carrinho
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        
        if not product_id:
            return Response(
                {'error': 'product_id é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            
            # Retornar carrinho atualizado
            cart_serializer = CartSerializer(cart)
            return Response({
                'message': 'Item removido do carrinho com sucesso',
                'cart': cart_serializer.data
            }, status=status.HTTP_200_OK)
            
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response(
                {'error': 'Item não encontrado no carrinho'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class UpdateCartView(generics.UpdateAPIView):
    """
    Atualizar quantidade de item no carrinho
    """
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        
        if not product_id or quantity is None:
            return Response(
                {'error': 'product_id e quantity são obrigatórios'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        quantity = int(quantity)
        if quantity <= 0:
            return Response(
                {'error': 'Quantidade deve ser maior que zero'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            
            # Verificar estoque
            if cart_item.product.stock_quantity < quantity:
                return Response(
                    {'error': 'Estoque insuficiente'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            cart_item.quantity = quantity
            cart_item.save()
            
            # Retornar carrinho atualizado
            cart_serializer = CartSerializer(cart)
            return Response({
                'message': 'Carrinho atualizado com sucesso',
                'cart': cart_serializer.data
            }, status=status.HTTP_200_OK)
            
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response(
                {'error': 'Item não encontrado no carrinho'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class ClearCartView(generics.DestroyAPIView):
    """
    Limpar carrinho
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
            
            cart_serializer = CartSerializer(cart)
            return Response({
                'message': 'Carrinho limpo com sucesso',
                'cart': cart_serializer.data
            }, status=status.HTTP_200_OK)
            
        except Cart.DoesNotExist:
            return Response(
                {'message': 'Carrinho já está vazio'}, 
                status=status.HTTP_200_OK
            )


class CheckoutView(generics.CreateAPIView):
    """
    Finalizar compra (checkout)
    """
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
            
            if not cart.items.exists():
                return Response(
                    {'error': 'Carrinho está vazio'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Dados do pedido
            payment_method = request.data.get('payment_method', 'credit_card')
            shipping_address = request.data.get('shipping_address', request.user.get_full_address())
            notes = request.data.get('notes', '')
            
            # Calcular total
            total_amount = cart.total_amount
            
            # Criar pedido
            order = Order.objects.create(
                customer=request.user,
                status='pending',
                total_amount=total_amount,
                payment_method=payment_method,
                shipping_address=shipping_address,
                notes=notes
            )
            
            # Criar itens do pedido
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.unit_price
                )
                
                # Atualizar estoque (reduzir)
                # Aqui seria criado um registro de saída no Stock
                # Stock.objects.create(
                #     product=cart_item.product,
                #     quantity=-cart_item.quantity,
                #     movement_type='out',
                #     reason=f'Venda - Pedido {order.order_number}'
                # )
            
            # Limpar carrinho
            cart.items.all().delete()
            
            # Retornar dados do pedido
            from .serializers import OrderDetailSerializer
            order_serializer = OrderDetailSerializer(order)
            
            return Response({
                'message': 'Pedido criado com sucesso',
                'order': order_serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Carrinho não encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Erro ao processar pedido: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
