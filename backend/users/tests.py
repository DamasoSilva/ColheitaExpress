from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from .serializers import UserRegistrationSerializer, UserLoginSerializer

User = get_user_model()


class UserModelTest(TestCase):
    """Testes para o modelo User"""
    
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'full_name': 'Test User',
            'cpf_cnpj': '12345678901',
            'phone': '+5511999999999',
            'street_address': 'Rua Teste, 123',
            'city': 'São Paulo',
            'state': 'SP',
            'postal_code': '01234567',
            'password': 'testpass123'
        }
    
    def test_create_user(self):
        """Teste de criação de usuário"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.full_name, self.user_data['full_name'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertEqual(user.user_type, 'customer')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """Teste de criação de superusuário"""
        user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123',
            full_name='Admin User',
            cpf_cnpj='98765432100'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.user_type, 'admin')
    
    def test_user_str_representation(self):
        """Teste da representação string do usuário"""
        user = User.objects.create_user(**self.user_data)
        expected = f"{self.user_data['full_name']} ({self.user_data['email']})"
        self.assertEqual(str(user), expected)
    
    def test_user_properties(self):
        """Teste das propriedades do usuário"""
        # Teste cliente
        customer = User.objects.create_user(**self.user_data)
        self.assertTrue(customer.is_customer)
        self.assertFalse(customer.is_admin)
        self.assertFalse(customer.is_driver)
        
        # Teste admin
        admin_data = self.user_data.copy()
        admin_data['email'] = 'admin@example.com'
        admin_data['user_type'] = 'admin'
        admin = User.objects.create_user(**admin_data)
        self.assertTrue(admin.is_admin)
        self.assertFalse(admin.is_customer)
        self.assertFalse(admin.is_driver)
        
        # Teste motorista
        driver_data = self.user_data.copy()
        driver_data['email'] = 'driver@example.com'
        driver_data['user_type'] = 'driver'
        driver = User.objects.create_user(**driver_data)
        self.assertTrue(driver.is_driver)
        self.assertFalse(driver.is_customer)
        self.assertFalse(driver.is_admin)
    
    def test_get_full_address(self):
        """Teste do método get_full_address"""
        user = User.objects.create_user(**self.user_data)
        expected_address = f"{self.user_data['street_address']}, {self.user_data['city']}, {self.user_data['state']}, {self.user_data['postal_code']}, {self.user_data['country']}"
        self.assertEqual(user.get_full_address(), expected_address)
    
    def test_unique_email(self):
        """Teste de unicidade do email"""
        User.objects.create_user(**self.user_data)
        
        duplicate_data = self.user_data.copy()
        duplicate_data['cpf_cnpj'] = '11111111111'
        
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**duplicate_data)
    
    def test_unique_cpf_cnpj(self):
        """Teste de unicidade do CPF/CNPJ"""
        User.objects.create_user(**self.user_data)
        
        duplicate_data = self.user_data.copy()
        duplicate_data['email'] = 'other@example.com'
        
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**duplicate_data)
    
    def test_cpf_cnpj_validation(self):
        """Teste de validação do CPF/CNPJ"""
        invalid_data = self.user_data.copy()
        invalid_data['cpf_cnpj'] = '123'  # CPF/CNPJ inválido
        
        user = User(**invalid_data)
        with self.assertRaises(ValidationError):
            user.full_clean()
    
    def test_phone_validation(self):
        """Teste de validação do telefone"""
        invalid_data = self.user_data.copy()
        invalid_data['phone'] = 'invalid_phone'
        
        user = User(**invalid_data)
        with self.assertRaises(ValidationError):
            user.full_clean()


class UserProfileTest(TestCase):
    """Testes para o modelo UserProfile"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            full_name='Test User',
            cpf_cnpj='12345678901'
        )
    
    def test_create_user_profile(self):
        """Teste de criação de perfil de usuário"""
        profile = UserProfile.objects.create(
            user=self.user,
            birth_date='1990-01-01',
            preferred_payment_method='credit_card'
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(str(profile.birth_date), '1990-01-01')
        self.assertEqual(profile.preferred_payment_method, 'credit_card')
    
    def test_profile_str_representation(self):
        """Teste da representação string do perfil"""
        profile = UserProfile.objects.create(user=self.user)
        expected = f"Perfil de {self.user.full_name}"
        self.assertEqual(str(profile), expected)


class UserSerializerTest(TestCase):
    """Testes para os serializers de usuário"""
    
    def test_user_registration_serializer_valid(self):
        """Teste de serializer de registro válido"""
        data = {
            'email': 'test@example.com',
            'full_name': 'Test User',
            'cpf_cnpj': '12345678901',
            'phone': '+5511999999999',
            'street_address': 'Rua Teste, 123',
            'city': 'São Paulo',
            'state': 'SP',
            'postal_code': '01234567',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.check_password(data['password']))
    
    def test_user_registration_serializer_password_mismatch(self):
        """Teste de serializer com senhas diferentes"""
        data = {
            'email': 'test@example.com',
            'full_name': 'Test User',
            'cpf_cnpj': '12345678901',
            'phone': '+5511999999999',
            'street_address': 'Rua Teste, 123',
            'city': 'São Paulo',
            'state': 'SP',
            'postal_code': '01234567',
            'password': 'testpass123',
            'password_confirm': 'differentpass'
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('As senhas não coincidem.', str(serializer.errors))


class UserAPITest(APITestCase):
    """Testes para as APIs de usuário"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            full_name='Test User',
            cpf_cnpj='12345678901'
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
    
    def test_user_registration_api(self):
        """Teste da API de registro de usuário"""
        url = '/api/auth/register/'
        data = {
            'email': 'newuser@example.com',
            'full_name': 'New User',
            'cpf_cnpj': '98765432100',
            'phone': '+5511888888888',
            'street_address': 'Rua Nova, 456',
            'city': 'Rio de Janeiro',
            'state': 'RJ',
            'postal_code': '12345678',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=data['email']).exists())
    
    def test_user_login_api(self):
        """Teste da API de login"""
        url = '/api/auth/login/'
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_user_login_invalid_credentials(self):
        """Teste de login com credenciais inválidas"""
        url = '/api/auth/login/'
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authenticated_user_profile(self):
        """Teste de acesso ao perfil do usuário autenticado"""
        url = '/api/auth/profile/'
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
    
    def test_unauthenticated_user_profile(self):
        """Teste de acesso ao perfil sem autenticação"""
        url = '/api/auth/profile/'
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_token_refresh(self):
        """Teste de renovação de token"""
        url = '/api/auth/token/refresh/'
        data = {
            'refresh': str(self.refresh)
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


class UserPermissionTest(TestCase):
    """Testes de permissões de usuário"""
    
    def setUp(self):
        self.customer = User.objects.create_user(
            email='customer@example.com',
            password='testpass123',
            full_name='Customer User',
            cpf_cnpj='12345678901',
            user_type='customer'
        )
        
        self.admin = User.objects.create_user(
            email='admin@example.com',
            password='testpass123',
            full_name='Admin User',
            cpf_cnpj='98765432100',
            user_type='admin'
        )
        
        self.driver = User.objects.create_user(
            email='driver@example.com',
            password='testpass123',
            full_name='Driver User',
            cpf_cnpj='11111111111',
            user_type='driver'
        )
    
    def test_customer_permissions(self):
        """Teste de permissões do cliente"""
        self.assertTrue(self.customer.is_customer)
        self.assertFalse(self.customer.is_staff)
        self.assertFalse(self.customer.has_perm('users.add_user'))
    
    def test_admin_permissions(self):
        """Teste de permissões do admin"""
        self.assertTrue(self.admin.is_admin)
        # Admin não é automaticamente staff, isso deve ser configurado separadamente
        self.assertFalse(self.admin.is_staff)
    
    def test_driver_permissions(self):
        """Teste de permissões do motorista"""
        self.assertTrue(self.driver.is_driver)
        self.assertFalse(self.driver.is_staff)
