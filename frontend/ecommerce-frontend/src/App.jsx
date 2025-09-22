import React, { useState, useEffect } from 'react';
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
import ApiService from './services/api';
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
              <h1 className="text-2xl font-bold text-primary">ColheitaExpress</h1>
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
            Hortifruti Online com Entrega Rápida
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-white/90">
            Produtos frescos e selecionados direto do produtor para sua mesa
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
      title: "Produtos Frescos",
      description: "Frutas, verduras e legumes selecionados diariamente com garantia de qualidade."
    },
    {
      icon: ShoppingCart,
      title: "Compra Fácil",
      description: "Processo de compra simples e rápido com múltiplas formas de pagamento."
    },
    {
      icon: Truck,
      title: "Entrega Rápida",
      description: "Entrega no mesmo dia para produtos frescos com embalagem adequada."
    },
    {
      icon: User,
      title: "Atendimento Personalizado",
      description: "Suporte especializado para ajudar na escolha dos melhores produtos."
    }
  ];

  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Por que Escolher o ColheitaExpress?
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Qualidade, frescor e conveniência em cada compra
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
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadFeaturedProducts = async () => {
      try {
        setLoading(true);
        const response = await ApiService.getFeaturedProducts();
        setProducts(response.results || []);
      } catch (err) {
        console.error('Erro ao carregar produtos em destaque:', err);
        setError('Erro ao carregar produtos');
        // Fallback para dados estáticos em caso de erro
        setProducts([
          {
            id: 1,
            name: "Banana Prata",
            price: 4.99,
            originalPrice: 6.99,
            image: "/images/banana.jpg",
            rating: 4.8,
            reviews: 124,
            badge: "Promoção",
            stock_quantity: 50,
            department: { name: "Frutas" },
            unit: "kg"
          },
          {
            id: 2,
            name: "Tomate Italiano",
            price: 8.99,
            image: "/images/tomato.jpg",
            rating: 4.9,
            reviews: 89,
            badge: "Fresco",
            stock_quantity: 30,
            department: { name: "Legumes" },
            unit: "kg"
          },
          {
            id: 3,
            name: "Alface Americana",
            price: 3.49,
            originalPrice: 4.99,
            image: "/images/lettuce.jpg",
            rating: 4.7,
            reviews: 256,
            badge: "Oferta",
            stock_quantity: 25,
            department: { name: "Verduras" },
            unit: "unidade"
          },
          {
            id: 4,
            name: "Laranja Lima",
            price: 5.99,
            image: "/images/orange.jpg",
            rating: 4.6,
            reviews: 178,
            badge: "Doce",
            stock_quantity: 40,
            department: { name: "Frutas" },
            unit: "kg"
          }
        ]);
      } finally {
        setLoading(false);
      }
    };

    loadFeaturedProducts();
  }, []);

  if (loading) {
    return (
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <p>Carregando produtos...</p>
          </div>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <p className="text-red-600">{error}</p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Produtos Frescos em Destaque
          </h2>
          <p className="text-xl text-gray-600">
            Selecionados especialmente para você
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {products.map((product) => (
            <Card key={product.id} className="group hover:shadow-xl transition-all duration-300 overflow-hidden">
              <div className="relative cursor-pointer" onClick={() => onViewProduct(product.id)}>
                <img 
                  src={product.primary_image || product.image || "/images/placeholder.jpg"} 
                  alt={product.name}
                  className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                />
                <Badge 
                  variant={product.badge === 'Promoção' ? 'destructive' : 'secondary'}
                  className="absolute top-2 left-2"
                >
                  {product.badge || 'Fresco'}
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
                        className={`h-4 w-4 ${i < Math.floor(product.rating || 4.5) ? 'text-yellow-400 fill-current' : 'text-gray-300'}`} 
                      />
                    ))}
                  </div>
                  <span className="text-sm text-gray-600 ml-2">({product.reviews || 0})</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-2xl font-bold text-primary">
                      R$ {parseFloat(product.current_price || product.price).toFixed(2)}
                    </span>
                    <span className="text-sm text-gray-500 ml-1">/{product.unit || 'kg'}</span>
                    {product.originalPrice && (
                      <span className="text-sm text-gray-500 line-through ml-2">
                        R$ {parseFloat(product.originalPrice).toFixed(2)}
                      </span>
                    )}
                  </div>
                  <Button size="sm" className="ml-2" onClick={(e) => {
                    e.stopPropagation();
                    onAddToCart(product);
                  }}>
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
            <h3 className="text-xl font-bold mb-4">ColheitaExpress</h3>
            <p className="text-gray-400">
              Hortifruti online com produtos frescos e entrega rápida. Qualidade garantida direto do produtor para sua mesa.
            </p>
          </div>
          
          <div>
            <h4 className="font-semibold mb-4">Produtos</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="#" className="hover:text-white transition-colors">Frutas</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Verduras</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Legumes</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Orgânicos</a></li>
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
          <p>&copy; 2024 ColheitaExpress. Todos os direitos reservados.</p>
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

  const addToCart = (product) => {
    setCartItems(prevItems => {
      const existingItem = prevItems.find(item => item.id === product.id);
      if (existingItem) {
        return prevItems.map(item =>
          item.id === product.id 
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      } else {
        return [...prevItems, { 
          ...product, 
          quantity: 1,
          // Garantir que temos os campos necessários
          current_price: product.current_price || product.price,
          department_name: product.department_name || product.department?.name,
          stock_quantity: product.stock_quantity || 0
        }];
      }
    });
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
            onAddToCart={addToCart}
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
            <ProductList onAddToCart={addToCart} onViewProduct={handleViewProduct} />
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
              onAddToCart={addToCart}
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
            onAddToCart={addToCart}
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
