from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal
from .models import Order, OrderItem, Cart, CartItem
from products.models import Department, Product, Stock
from coupons.models import Coupon

User = get_user_model()


class CartModelTest(TestCase):
    """Testes para o modelo Cart"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='customer@example.com',
            password='testpass123',
            full_name='Customer User',
            cpf_cnpj='12345678901'
        )
        
        self.department = Department.objects.create(
            name='Eletrônicos',
            slug='eletronicos'
        )
        
        self.product = Product.objects.create(
            name='Smartphone X',
            description='Um smartphone avançado',
            slug='smartphone-x',
            department=self.department,
            price=Decimal('1200.00')
        )
        
        # Adicionar estoque
        Stock.objects.create(
            product=self.product,
            quantity=100,
            movement_type='in',
            reason='Estoque inicial'
        )
    
    def test_create_cart(self):
        """Teste de criação de carrinho"""
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)
        self.assertEqual(cart.total_items, 0)
        self.assertEqual(cart.total_amount, Decimal('0.00'))
    
    def test_cart_str_representation(self):
        """Teste da representação string do carrinho"""
        cart = Cart.objects.create(user=self.user)
        expected = f"Carrinho de {self.user.full_name}"
        self.assertEqual(str(cart), expected)
    
    def test_add_item_to_cart(self):
        """Teste de adição de item ao carrinho"""
        cart = Cart.objects.create(user=self.user)
        
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2,
            unit_price=self.product.price
        )
        
        self.assertEqual(cart_item.cart, cart)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.total_price, Decimal('2400.00'))


class OrderModelTest(TestCase):
    """Testes para o modelo Order"""
    
    def setUp(self):
        self.customer = User.objects.create_user(
            email='customer@example.com',
            password='testpass123',
            full_name='Customer User',
            cpf_cnpj='12345678901',
            street_address='Rua Teste, 123',
            city='São Paulo',
            state='SP',
            postal_code='01234567'
        )
        
        self.department = Department.objects.create(
            name='Eletrônicos',
            slug='eletronicos'
        )
        
        self.product = Product.objects.create(
            name='Smartphone X',
            description='Um smartphone avançado',
            slug='smartphone-x',
            department=self.department,
            price=Decimal('1200.00')
        )
        
        # Adicionar estoque
        Stock.objects.create(
            product=self.product,
            quantity=100,
            movement_type='in',
            reason='Estoque inicial'
        )
    
    def test_create_order(self):
        """Teste de criação de pedido"""
        order = Order.objects.create(
            customer=self.customer,
            status='pending',
            total_amount=Decimal('1200.00'),
            shipping_address=self.customer.get_full_address(),
            payment_method='credit_card'
        )
        
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.total_amount, Decimal('1200.00'))
        self.assertIsNotNone(order.order_number)
    
    def test_order_str_representation(self):
        """Teste da representação string do pedido"""
        order = Order.objects.create(
            customer=self.customer,
            status='pending',
            total_amount=Decimal('1200.00')
        )
        
        expected = f"Pedido {order.order_number} - {self.customer.full_name}"
        self.assertEqual(str(order), expected)
