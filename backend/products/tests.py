from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal
from .models import Department, Product, ProductImage, Stock, ProductReview

User = get_user_model()


class DepartmentModelTest(TestCase):
    """Testes para o modelo Department"""
    
    def setUp(self):
        self.department_data = {
            'name': 'Eletrônicos',
            'description': 'Produtos eletrônicos diversos',
            'slug': 'eletronicos'
        }
    
    def test_create_department(self):
        """Teste de criação de departamento"""
        department = Department.objects.create(**self.department_data)
        self.assertEqual(department.name, self.department_data['name'])
        self.assertEqual(department.slug, self.department_data['slug'])
        self.assertTrue(department.is_active)
    
    def test_department_str_representation(self):
        """Teste da representação string do departamento"""
        department = Department.objects.create(**self.department_data)
        self.assertEqual(str(department), self.department_data['name'])
    
    def test_unique_name(self):
        """Teste de unicidade do nome"""
        Department.objects.create(**self.department_data)
        
        with self.assertRaises(IntegrityError):
            Department.objects.create(**self.department_data)
    
    def test_unique_slug(self):
        """Teste de unicidade do slug"""
        Department.objects.create(**self.department_data)
        
        duplicate_data = self.department_data.copy()
        duplicate_data['name'] = 'Eletrônicos 2'
        
        with self.assertRaises(IntegrityError):
            Department.objects.create(**duplicate_data)


class ProductModelTest(TestCase):
    """Testes para o modelo Product"""
    
    def setUp(self):
        self.department = Department.objects.create(
            name='Eletrônicos',
            slug='eletronicos'
        )
        
        self.product_data = {
            'name': 'Smartphone X',
            'description': 'Um smartphone avançado',
            'short_description': 'Smartphone top de linha',
            'slug': 'smartphone-x',
            'department': self.department,
            'price': Decimal('1200.00'),
            'promotional_price': Decimal('1000.00'),
            'weight': Decimal('0.200'),
            'dimensions': '15x7x0.8 cm'
        }
    
    def test_create_product(self):
        """Teste de criação de produto"""
        product = Product.objects.create(**self.product_data)
        self.assertEqual(product.name, self.product_data['name'])
        self.assertEqual(product.department, self.department)
        self.assertEqual(product.price, self.product_data['price'])
        self.assertTrue(product.is_active)
        self.assertFalse(product.is_featured)
    
    def test_product_str_representation(self):
        """Teste da representação string do produto"""
        product = Product.objects.create(**self.product_data)
        self.assertEqual(str(product), self.product_data['name'])
    
    def test_current_price_without_promotion(self):
        """Teste do preço atual sem promoção"""
        product_data = self.product_data.copy()
        product_data['is_on_promotion'] = False
        product = Product.objects.create(**product_data)
        
        self.assertEqual(product.current_price, product.price)
    
    def test_current_price_with_promotion(self):
        """Teste do preço atual com promoção"""
        product_data = self.product_data.copy()
        product_data['is_on_promotion'] = True
        product = Product.objects.create(**product_data)
        
        self.assertEqual(product.current_price, product.promotional_price)
    
    def test_discount_percentage(self):
        """Teste do cálculo de porcentagem de desconto"""
        product_data = self.product_data.copy()
        product_data['is_on_promotion'] = True
        product = Product.objects.create(**product_data)
        
        expected_discount = ((product.price - product.promotional_price) / product.price) * 100
        self.assertEqual(product.discount_percentage, round(expected_discount, 2))
    
    def test_discount_percentage_without_promotion(self):
        """Teste de desconto sem promoção"""
        product_data = self.product_data.copy()
        product_data['is_on_promotion'] = False
        product = Product.objects.create(**product_data)
        
        self.assertEqual(product.discount_percentage, 0)
    
    def test_stock_quantity_empty(self):
        """Teste de quantidade em estoque vazia"""
        product = Product.objects.create(**self.product_data)
        self.assertEqual(product.stock_quantity, 0)
        self.assertFalse(product.is_in_stock)
    
    def test_stock_quantity_with_stock(self):
        """Teste de quantidade em estoque com produtos"""
        product = Product.objects.create(**self.product_data)
        
        # Adicionar estoque
        Stock.objects.create(
            product=product,
            quantity=50,
            movement_type='in',
            reason='Estoque inicial'
        )
        
        self.assertEqual(product.stock_quantity, 50)
        self.assertTrue(product.is_in_stock)
    
    def test_unique_slug(self):
        """Teste de unicidade do slug"""
        Product.objects.create(**self.product_data)
        
        duplicate_data = self.product_data.copy()
        duplicate_data['name'] = 'Smartphone Y'
        
        with self.assertRaises(IntegrityError):
            Product.objects.create(**duplicate_data)
    
    def test_price_validation(self):
        """Teste de validação de preço"""
        invalid_data = self.product_data.copy()
        invalid_data['price'] = Decimal('-10.00')
        
        product = Product(**invalid_data)
        with self.assertRaises(ValidationError):
            product.full_clean()


class StockModelTest(TestCase):
    """Testes para o modelo Stock"""
    
    def setUp(self):
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
        
        self.user = User.objects.create_user(
            email='admin@example.com',
            password='testpass123',
            full_name='Admin User',
            cpf_cnpj='12345678901'
        )
    
    def test_create_stock_entry(self):
        """Teste de criação de entrada de estoque"""
        stock = Stock.objects.create(
            product=self.product,
            quantity=100,
            movement_type='in',
            reason='Estoque inicial',
            created_by=self.user
        )
        
        self.assertEqual(stock.product, self.product)
        self.assertEqual(stock.quantity, 100)
        self.assertEqual(stock.movement_type, 'in')
        self.assertEqual(stock.created_by, self.user)
    
    def test_stock_str_representation(self):
        """Teste da representação string do estoque"""
        stock = Stock.objects.create(
            product=self.product,
            quantity=50,
            movement_type='out',
            reason='Venda'
        )
        
        expected = f"{self.product.name} - Saída: 50"
        self.assertEqual(str(stock), expected)
    
    def test_stock_calculation(self):
        """Teste de cálculo de estoque"""
        # Entrada de estoque
        Stock.objects.create(
            product=self.product,
            quantity=100,
            movement_type='in',
            reason='Compra'
        )
        
        # Saída de estoque
        Stock.objects.create(
            product=self.product,
            quantity=30,
            movement_type='out',
            reason='Venda'
        )
        
        # Ajuste de estoque
        Stock.objects.create(
            product=self.product,
            quantity=5,
            movement_type='adjustment',
            reason='Correção'
        )
        
        # O cálculo real seria feito no modelo Product
        total_stock = self.product.stock_quantity
        self.assertEqual(total_stock, 75)  # 100 - 30 + 5


class ProductImageTest(TestCase):
    """Testes para o modelo ProductImage"""
    
    def setUp(self):
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
    
    def test_create_product_image(self):
        """Teste de criação de imagem do produto"""
        image = ProductImage.objects.create(
            product=self.product,
            alt_text='Smartphone X - Vista frontal',
            order=1
        )
        
        self.assertEqual(image.product, self.product)
        self.assertEqual(image.alt_text, 'Smartphone X - Vista frontal')
        self.assertEqual(image.order, 1)
    
    def test_product_image_str_representation(self):
        """Teste da representação string da imagem"""
        image = ProductImage.objects.create(
            product=self.product,
            order=1
        )
        
        expected = f"Imagem de {self.product.name}"
        self.assertEqual(str(image), expected)


class ProductReviewTest(TestCase):
    """Testes para o modelo ProductReview"""
    
    def setUp(self):
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
        
        self.customer = User.objects.create_user(
            email='customer@example.com',
            password='testpass123',
            full_name='Customer User',
            cpf_cnpj='12345678901'
        )
    
    def test_create_product_review(self):
        """Teste de criação de avaliação do produto"""
        review = ProductReview.objects.create(
            product=self.product,
            customer=self.customer,
            rating=5,
            title='Excelente produto',
            comment='Muito satisfeito com a compra'
        )
        
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.customer, self.customer)
        self.assertEqual(review.rating, 5)
        self.assertFalse(review.is_approved)
    
    def test_review_str_representation(self):
        """Teste da representação string da avaliação"""
        review = ProductReview.objects.create(
            product=self.product,
            customer=self.customer,
            rating=4,
            title='Bom produto',
            comment='Recomendo'
        )
        
        expected = f"{self.product.name} - 4 estrelas por {self.customer.full_name}"
        self.assertEqual(str(review), expected)
    
    def test_unique_review_per_customer(self):
        """Teste de unicidade de avaliação por cliente"""
        ProductReview.objects.create(
            product=self.product,
            customer=self.customer,
            rating=5,
            title='Primeira avaliação',
            comment='Primeira avaliação'
        )
        
        with self.assertRaises(IntegrityError):
            ProductReview.objects.create(
                product=self.product,
                customer=self.customer,
                rating=3,
                title='Segunda avaliação',
                comment='Segunda avaliação'
            )
