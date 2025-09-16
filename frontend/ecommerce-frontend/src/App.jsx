import React, { useState } from 'react';
import { Button } from './components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card';
import { Badge } from './components/ui/badge';
import { ShoppingCart, User, Truck, Package, Star, Search, Menu, X } from 'lucide-react';
import AdminDashboard from './components/AdminDashboard';
import CustomerDashboard from './components/CustomerDashboard';
import DriverDashboard from './components/DriverDashboard';
import ProductList from './components/ProductList';
import ProductDetail from './components/ProductDetail';
import ShoppingCartComponent from './components/ShoppingCart';
import Checkout from './components/Checkout';
import OrderConfirmation from './components/OrderConfirmation';
import './App.css';

// Componente de Header
function Header({ userType, setUserType, currentView, setCurrentView, cartItems, onCartClick }) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const userTypes = [
    { value: 'customer', label: 'Cliente', icon: User },
    { value: 'admin', label: 'Administrador', icon: Package },
    { value: 'driver', label: 'Motorista', icon: Truck }
  ];

  const handleLoginClick = () => {
    setCurrentView(currentView === 'landing' ? 'dashboard' : 'landing');
  };

  const cartItemsCount = cartItems.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <header className="bg-white shadow-sm border-b sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <div className="flex-shrink-0 cursor-pointer" onClick={() => setCurrentView('landing')}>
              <h1 className="text-2xl font-bold text-primary">E-commerce SaaS</h1>
            </div>
          </div>

          {/* Navigation Desktop */}
          <nav className="hidden md:flex space-x-8">
            <button 
              onClick={() => setCurrentView('products')}
              className="text-gray-700 hover:text-primary transition-colors"
            >
              Produtos
            </button>
            <a href="#" className="text-gray-700 hover:text-primary transition-colors">Departamentos</a>
            <a href="#" className="text-gray-700 hover:text-primary transition-colors">Promoções</a>
            <a href="#" className="text-gray-700 hover:text-primary transition-colors">Contato</a>
          </nav>

          {/* User Type Selector & Actions */}
          <div className="hidden md:flex items-center space-x-4">
            <select 
              value={userType} 
              onChange={(e) => setUserType(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            >
              {userTypes.map(type => (
                <option key={type.value} value={type.value}>{type.label}</option>
              ))}
            </select>
            
            <Button variant="outline" size="sm">
              <Search className="h-4 w-4" />
            </Button>
            
            <Button variant="outline" size="sm" onClick={onCartClick}>
              <ShoppingCart className="h-4 w-4" />
              {cartItemsCount > 0 && (
                <Badge variant="destructive" className="ml-1">{cartItemsCount}</Badge>
              )}
            </Button>
            
            <Button size="sm" onClick={handleLoginClick}>
              <User className="h-4 w-4 mr-2" />
              {currentView === 'dashboard' ? 'Voltar' : 'Login'}
            </Button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t">
              <button 
                onClick={() => setCurrentView('products')}
                className="block px-3 py-2 text-gray-700 hover:text-primary w-full text-left"
              >
                Produtos
              </button>
              <a href="#" className="block px-3 py-2 text-gray-700 hover:text-primary">Departamentos</a>
              <a href="#" className="block px-3 py-2 text-gray-700 hover:text-primary">Promoções</a>
              <a href="#" className="block px-3 py-2 text-gray-700 hover:text-primary">Contato</a>
              <div className="pt-4 pb-3 border-t border-gray-200">
                <select 
                  value={userType} 
                  onChange={(e) => setUserType(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                >
                  {userTypes.map(type => (
                    <option key={type.value} value={type.value}>{type.label}</option>
                  ))}
                </select>
                <Button 
                  className="w-full mt-2" 
                  size="sm" 
                  onClick={onCartClick}
                >
                  <ShoppingCart className="h-4 w-4 mr-2" />
                  Carrinho ({cartItemsCount})
                </Button>
                <Button 
                  className="w-full mt-2" 
                  size="sm" 
                  onClick={handleLoginClick}
                >
                  <User className="h-4 w-4 mr-2" />
                  {currentView === 'dashboard' ? 'Voltar' : 'Login'}
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </header>
  );
}

// Componente de Hero Section
function HeroSection({ onShopNow }) {
  return (
    <section className="bg-gradient-to-r from-primary to-primary/80 text-white py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            Sua Plataforma de E-commerce Completa
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-white/90">
            Gerencie produtos, pedidos e entregas em uma única plataforma robusta e escalável
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" variant="secondary" className="text-lg px-8 py-3" onClick={onShopNow}>
              Começar a Comprar
            </Button>
            <Button size="lg" variant="outline" className="text-lg px-8 py-3 border-white text-white hover:bg-white hover:text-primary">
              Ver Demo
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
}

// Componente de Features
function FeaturesSection() {
  const features = [
    {
      icon: Package,
      title: "Gestão de Produtos",
      description: "Controle completo de estoque, departamentos e promoções com interface intuitiva."
    },
    {
      icon: ShoppingCart,
      title: "Sistema de Pedidos",
      description: "Processamento eficiente de pedidos com múltiplos métodos de pagamento."
    },
    {
      icon: Truck,
      title: "Rastreamento de Entregas",
      description: "Acompanhamento em tempo real das entregas com interface para motoristas."
    },
    {
      icon: User,
      title: "Múltiplos Perfis",
      description: "Interfaces específicas para administradores, clientes e motoristas."
    }
  ];

  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Funcionalidades Principais
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Uma plataforma completa com todas as ferramentas necessárias para seu e-commerce
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <Card key={index} className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="mx-auto w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="h-6 w-6 text-primary" />
                </div>
                <CardTitle className="text-xl">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-gray-600">
                  {feature.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}

// Componente de Produtos em Destaque
function FeaturedProducts({ onAddToCart, onViewProduct }) {
  const products = [
    {
      id: 1,
      name: "Smartphone Premium",
      price: 1299.99,
      originalPrice: 1499.99,
      image: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop",
      rating: 4.8,
      reviews: 124,
      badge: "Promoção",
      stock_quantity: 15,
      department: { name: "Eletrônicos" }
    },
    {
      id: 2,
      name: "Notebook Gamer",
      price: 2499.99,
      image: "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=300&fit=crop",
      rating: 4.9,
      reviews: 89,
      badge: "Destaque",
      stock_quantity: 8,
      department: { name: "Eletrônicos" }
    },
    {
      id: 3,
      name: "Fone Bluetooth",
      price: 199.99,
      originalPrice: 249.99,
      image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=300&fit=crop",
      rating: 4.7,
      reviews: 256,
      badge: "Oferta",
      stock_quantity: 25,
      department: { name: "Eletrônicos" }
    },
    {
      id: 4,
      name: "Smart Watch",
      price: 399.99,
      image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop",
      rating: 4.6,
      reviews: 178,
      badge: "Novo",
      stock_quantity: 12,
      department: { name: "Eletrônicos" }
    }
  ];

  return (
    <section className="py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Produtos em Destaque
          </h2>
          <p className="text-xl text-gray-600">
            Confira nossa seleção especial de produtos
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {products.map((product) => (
            <Card key={product.id} className="group hover:shadow-xl transition-all duration-300 overflow-hidden">
              <div className="relative cursor-pointer" onClick={() => onViewProduct(product.id)}>
                <img 
                  src={product.image} 
                  alt={product.name}
                  className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                />
                <Badge 
                  variant={product.badge === 'Promoção' ? 'destructive' : 'secondary'}
                  className="absolute top-2 left-2"
                >
                  {product.badge}
                </Badge>
              </div>
              
              <CardContent className="p-4">
                <h3 className="font-semibold text-lg mb-2 group-hover:text-primary transition-colors cursor-pointer"
                    onClick={() => onViewProduct(product.id)}>
                  {product.name}
                </h3>
                
                <div className="flex items-center mb-2">
                  <div className="flex items-center">
                    {[...Array(5)].map((_, i) => (
                      <Star 
                        key={i} 
                        className={`h-4 w-4 ${i < Math.floor(product.rating) ? 'text-yellow-400 fill-current' : 'text-gray-300'}`} 
                      />
                    ))}
                  </div>
                  <span className="text-sm text-gray-600 ml-2">({product.reviews})</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-2xl font-bold text-primary">
                      R$ {product.price.toFixed(2)}
                    </span>
                    {product.originalPrice && (
                      <span className="text-sm text-gray-500 line-through ml-2">
                        R$ {product.originalPrice.toFixed(2)}
                      </span>
                    )}
                  </div>
                  <Button size="sm" className="ml-2" onClick={() => onAddToCart(product)}>
                    <ShoppingCart className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}

// Componente de Footer
function Footer() {
  return (
    <footer className="bg-gray-900 text-white py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">E-commerce SaaS</h3>
            <p className="text-gray-400">
              Plataforma completa para seu negócio online com gestão integrada de produtos, pedidos e entregas.
            </p>
          </div>
          
          <div>
            <h4 className="font-semibold mb-4">Produtos</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-white transition-colors">Eletrônicos</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Informática</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Casa & Jardim</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Esportes</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-semibold mb-4">Empresa</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-white transition-colors">Sobre Nós</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Carreiras</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Imprensa</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Contato</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-semibold mb-4">Suporte</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-white transition-colors">Central de Ajuda</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Política de Privacidade</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Termos de Uso</a></li>
              <li><a href="#" className="hover:text-white transition-colors">FAQ</a></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2024 E-commerce SaaS. Todos os direitos reservados.</p>
        </div>
      </div>
    </footer>
  );
}

// Componente de Landing Page
function LandingPage({ userType, setUserType, currentView, setCurrentView, cartItems, onCartClick, onAddToCart, onViewProduct, onShopNow }) {
  return (
    <div className="min-h-screen bg-white">
      <Header 
        userType={userType} 
        setUserType={setUserType} 
        currentView={currentView} 
        setCurrentView={setCurrentView}
        cartItems={cartItems}
        onCartClick={onCartClick}
      />
      <main>
        <HeroSection onShopNow={onShopNow} />
        <FeaturesSection />
        <FeaturedProducts onAddToCart={onAddToCart} onViewProduct={onViewProduct} />
      </main>
      <Footer />
    </div>
  );
}

// Componente Principal
function App() {
  const [userType, setUserType] = useState('customer');
  const [currentView, setCurrentView] = useState('landing');
  const [cartItems, setCartItems] = useState([]);
  const [selectedProductId, setSelectedProductId] = useState(null);
  const [orderData, setOrderData] = useState(null);

  const handleAddToCart = (product) => {
    const existingItem = cartItems.find(item => item.id === product.id);
    
    if (existingItem) {
      setCartItems(cartItems.map(item =>
        item.id === product.id
          ? { ...item, quantity: item.quantity + (product.quantity || 1) }
          : item
      ));
    } else {
      setCartItems([...cartItems, { ...product, quantity: product.quantity || 1 }]);
    }
    
    alert(`${product.name} adicionado ao carrinho!`);
  };

  const handleUpdateCartQuantity = (itemId, newQuantity) => {
    setCartItems(cartItems.map(item =>
      item.id === itemId ? { ...item, quantity: newQuantity } : item
    ));
  };

  const handleRemoveFromCart = (itemId) => {
    setCartItems(cartItems.filter(item => item.id !== itemId));
  };

  const handleCheckout = (items, total) => {
    setCurrentView('checkout');
  };

  const handleOrderComplete = (orderData) => {
    setOrderData(orderData);
    setCartItems([]);
    setCurrentView('order-confirmation');
  };

  const handleViewProduct = (productId) => {
    setSelectedProductId(productId);
    setCurrentView('product-detail');
  };

  const handleCartClick = () => {
    setCurrentView('cart');
  };

  const handleShopNow = () => {
    setCurrentView('products');
  };

  const handleContinueShopping = () => {
    setCurrentView('landing');
  };

  // Renderizar a view apropriada
  const renderCurrentView = () => {
    switch (currentView) {
      case 'landing':
        return (
          <LandingPage 
            userType={userType} 
            setUserType={setUserType} 
            currentView={currentView} 
            setCurrentView={setCurrentView}
            cartItems={cartItems}
            onCartClick={handleCartClick}
            onAddToCart={handleAddToCart}
            onViewProduct={handleViewProduct}
            onShopNow={handleShopNow}
          />
        );
      
      case 'products':
        return (
          <div>
            <Header 
              userType={userType} 
              setUserType={setUserType} 
              currentView={currentView} 
              setCurrentView={setCurrentView}
              cartItems={cartItems}
              onCartClick={handleCartClick}
            />
            <ProductList onAddToCart={handleAddToCart} onViewProduct={handleViewProduct} />
          </div>
        );
      
      case 'product-detail':
        return (
          <div>
            <Header 
              userType={userType} 
              setUserType={setUserType} 
              currentView={currentView} 
              setCurrentView={setCurrentView}
              cartItems={cartItems}
              onCartClick={handleCartClick}
            />
            <ProductDetail 
              productId={selectedProductId}
              onAddToCart={handleAddToCart}
              onBack={() => setCurrentView('products')}
            />
          </div>
        );
      
      case 'cart':
        return (
          <div>
            <Header 
              userType={userType} 
              setUserType={setUserType} 
              currentView={currentView} 
              setCurrentView={setCurrentView}
              cartItems={cartItems}
              onCartClick={handleCartClick}
            />
            <ShoppingCartComponent 
              cartItems={cartItems}
              onUpdateQuantity={handleUpdateCartQuantity}
              onRemoveItem={handleRemoveFromCart}
              onCheckout={handleCheckout}
            />
          </div>
        );
      
      case 'checkout':
        const total = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0) + 15 + (cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0) * 0.05);
        return (
          <div>
            <Header 
              userType={userType} 
              setUserType={setUserType} 
              currentView={currentView} 
              setCurrentView={setCurrentView}
              cartItems={cartItems}
              onCartClick={handleCartClick}
            />
            <Checkout 
              cartItems={cartItems}
              total={total}
              onOrderComplete={handleOrderComplete}
            />
          </div>
        );
      
      case 'order-confirmation':
        return (
          <div>
            <Header 
              userType={userType} 
              setUserType={setUserType} 
              currentView={currentView} 
              setCurrentView={setCurrentView}
              cartItems={cartItems}
              onCartClick={handleCartClick}
            />
            <OrderConfirmation 
              orderData={orderData}
              onContinueShopping={handleContinueShopping}
            />
          </div>
        );
      
      case 'dashboard':
        // Renderizar dashboard baseado no tipo de usuário
        switch (userType) {
          case 'admin':
            return <AdminDashboard onLogout={() => setCurrentView('landing')} />;
          case 'customer':
            return <CustomerDashboard onLogout={() => setCurrentView('landing')} />;
          case 'driver':
            return <DriverDashboard onLogout={() => setCurrentView('landing')} />;
          default:
            return <CustomerDashboard onLogout={() => setCurrentView('landing')} />;
        }
      
      default:
        return (
          <LandingPage 
            userType={userType} 
            setUserType={setUserType} 
            currentView={currentView} 
            setCurrentView={setCurrentView}
            cartItems={cartItems}
            onCartClick={handleCartClick}
            onAddToCart={handleAddToCart}
            onViewProduct={handleViewProduct}
            onShopNow={handleShopNow}
          />
        );
    }
  };

  return (
    <div className="min-h-screen">
      {renderCurrentView()}
    </div>
  );
}

export default App;
