import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Input } from './ui/input';
import { Separator } from './ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  ShoppingCart, 
  Star, 
  Heart, 
  Share2, 
  Truck, 
  Shield, 
  RotateCcw,
  Plus,
  Minus,
  ArrowLeft
} from 'lucide-react';

const ProductDetail = ({ productId, onAddToCart, onBack }) => {
  const [product, setProduct] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [selectedImage, setSelectedImage] = useState(0);
  const [loading, setLoading] = useState(true);
  const [isFavorite, setIsFavorite] = useState(false);

  useEffect(() => {
    fetchProduct();
  }, [productId]);

  const fetchProduct = async () => {
    try {
      // Simular dados do produto para demonstração
      const mockProduct = {
        id: productId,
        name: 'Smartphone Galaxy Pro Max',
        description: 'O mais avançado smartphone da linha Galaxy, com câmera profissional de 108MP, processador octa-core de última geração, 256GB de armazenamento e conectividade 5G ultra-rápida.',
        price: 1299.99,
        originalPrice: 1599.99,
        department: { id: 1, name: 'Eletrônicos' },
        is_featured: true,
        stock_quantity: 25,
        rating: 4.8,
        reviewsCount: 342,
        images: [
          'https://via.placeholder.com/600x600/3B82F6/FFFFFF?text=Frente',
          'https://via.placeholder.com/600x600/10B981/FFFFFF?text=Verso',
          'https://via.placeholder.com/600x600/F59E0B/FFFFFF?text=Lateral',
          'https://via.placeholder.com/600x600/EF4444/FFFFFF?text=Detalhes'
        ],
        specifications: {
          'Tela': '6.8" Super AMOLED',
          'Processador': 'Snapdragon 8 Gen 2',
          'Memória RAM': '12GB',
          'Armazenamento': '256GB',
          'Câmera Principal': '108MP + 12MP + 12MP',
          'Câmera Frontal': '40MP',
          'Bateria': '5000mAh',
          'Sistema Operacional': 'Android 14',
          'Conectividade': '5G, Wi-Fi 6E, Bluetooth 5.3',
          'Resistência': 'IP68'
        },
        features: [
          'Carregamento rápido de 45W',
          'Carregamento sem fio de 15W',
          'Resistente à água e poeira (IP68)',
          'Reconhecimento facial e digital',
          'Gravação de vídeo em 8K',
          'Modo noturno avançado'
        ],
        warranty: '12 meses de garantia oficial',
        shipping: {
          free: true,
          estimatedDays: '2-5 dias úteis',
          regions: 'Todo o Brasil'
        }
      };
      
      setProduct(mockProduct);
      setLoading(false);
    } catch (error) {
      console.error('Erro ao buscar produto:', error);
      setLoading(false);
    }
  };

  const handleQuantityChange = (newQuantity) => {
    if (newQuantity >= 1 && newQuantity <= product.stock_quantity) {
      setQuantity(newQuantity);
    }
  };

  const handleAddToCart = () => {
    if (onAddToCart && product) {
      onAddToCart({
        ...product,
        quantity: quantity
      });
    }
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: product.name,
        text: product.description,
        url: window.location.href
      });
    } else {
      navigator.clipboard.writeText(window.location.href);
      alert('Link copiado para a área de transferência!');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-semibold mb-4">Produto não encontrado</h2>
        <Button onClick={onBack}>Voltar</Button>
      </div>
    );
  }

  const discountPercentage = Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100);

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Breadcrumb */}
      <div className="flex items-center mb-6">
        <Button variant="ghost" onClick={onBack} className="mr-4">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Voltar
        </Button>
        <span className="text-gray-600">
          {product.department.name} / {product.name}
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Galeria de Imagens */}
        <div className="space-y-4">
          <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden">
            <img
              src={product.images[selectedImage]}
              alt={product.name}
              className="w-full h-full object-cover"
            />
          </div>
          
          <div className="grid grid-cols-4 gap-2">
            {product.images.map((image, index) => (
              <button
                key={index}
                onClick={() => setSelectedImage(index)}
                className={`aspect-square bg-gray-100 rounded-lg overflow-hidden border-2 ${
                  selectedImage === index ? 'border-blue-600' : 'border-transparent'
                }`}
              >
                <img
                  src={image}
                  alt={`${product.name} ${index + 1}`}
                  className="w-full h-full object-cover"
                />
              </button>
            ))}
          </div>
        </div>

        {/* Informações do Produto */}
        <div className="space-y-6">
          <div>
            <div className="flex items-center justify-between mb-2">
              <Badge variant="outline">{product.department.name}</Badge>
              <div className="flex items-center space-x-2">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setIsFavorite(!isFavorite)}
                >
                  <Heart className={`h-4 w-4 ${isFavorite ? 'fill-red-500 text-red-500' : ''}`} />
                </Button>
                <Button variant="ghost" size="sm" onClick={handleShare}>
                  <Share2 className="h-4 w-4" />
                </Button>
              </div>
            </div>
            
            <h1 className="text-3xl font-bold mb-4">{product.name}</h1>
            
            <div className="flex items-center space-x-4 mb-4">
              <div className="flex items-center">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    className={`h-5 w-5 ${
                      i < Math.floor(product.rating) 
                        ? 'text-yellow-400 fill-current' 
                        : 'text-gray-300'
                    }`}
                  />
                ))}
                <span className="ml-2 text-gray-600">
                  {product.rating} ({product.reviewsCount} avaliações)
                </span>
              </div>
            </div>

            <div className="space-y-2 mb-6">
              <div className="flex items-center space-x-4">
                <span className="text-3xl font-bold text-green-600">
                  R$ {product.price.toFixed(2)}
                </span>
                {product.originalPrice > product.price && (
                  <>
                    <span className="text-lg text-gray-500 line-through">
                      R$ {product.originalPrice.toFixed(2)}
                    </span>
                    <Badge className="bg-red-500">
                      -{discountPercentage}%
                    </Badge>
                  </>
                )}
              </div>
              <p className="text-sm text-gray-600">
                ou 12x de R$ {(product.price / 12).toFixed(2)} sem juros
              </p>
            </div>

            <p className="text-gray-700 mb-6">{product.description}</p>

            {/* Estoque */}
            <div className="mb-6">
              {product.stock_quantity > 0 ? (
                <div className="flex items-center text-green-600">
                  <span className="font-medium">✓ {product.stock_quantity} em estoque</span>
                </div>
              ) : (
                <div className="text-red-600">
                  <span className="font-medium">✗ Produto esgotado</span>
                </div>
              )}
            </div>

            {/* Quantidade e Compra */}
            <div className="space-y-4">
              <div className="flex items-center space-x-4">
                <label className="font-medium">Quantidade:</label>
                <div className="flex items-center space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleQuantityChange(quantity - 1)}
                    disabled={quantity <= 1}
                  >
                    <Minus className="h-4 w-4" />
                  </Button>
                  
                  <Input
                    type="number"
                    value={quantity}
                    onChange={(e) => handleQuantityChange(parseInt(e.target.value) || 1)}
                    className="w-20 text-center"
                    min="1"
                    max={product.stock_quantity}
                  />
                  
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleQuantityChange(quantity + 1)}
                    disabled={quantity >= product.stock_quantity}
                  >
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              <div className="space-y-3">
                <Button 
                  className="w-full" 
                  size="lg"
                  onClick={handleAddToCart}
                  disabled={product.stock_quantity === 0}
                >
                  <ShoppingCart className="h-5 w-5 mr-2" />
                  Adicionar ao Carrinho
                </Button>
                
                <Button variant="outline" className="w-full" size="lg">
                  Comprar Agora
                </Button>
              </div>
            </div>

            {/* Benefícios */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
              <div className="flex items-center space-x-2 text-sm">
                <Truck className="h-4 w-4 text-green-600" />
                <span>Frete grátis</span>
              </div>
              <div className="flex items-center space-x-2 text-sm">
                <Shield className="h-4 w-4 text-blue-600" />
                <span>Garantia oficial</span>
              </div>
              <div className="flex items-center space-x-2 text-sm">
                <RotateCcw className="h-4 w-4 text-purple-600" />
                <span>Troca grátis</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Abas de Informações */}
      <div className="mt-12">
        <Tabs defaultValue="description" className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="description">Descrição</TabsTrigger>
            <TabsTrigger value="specifications">Especificações</TabsTrigger>
            <TabsTrigger value="reviews">Avaliações</TabsTrigger>
            <TabsTrigger value="shipping">Entrega</TabsTrigger>
          </TabsList>
          
          <TabsContent value="description" className="mt-6">
            <Card>
              <CardContent className="pt-6">
                <h3 className="text-lg font-semibold mb-4">Sobre o Produto</h3>
                <p className="text-gray-700 mb-6">{product.description}</p>
                
                <h4 className="font-semibold mb-3">Principais Características:</h4>
                <ul className="space-y-2">
                  {product.features.map((feature, index) => (
                    <li key={index} className="flex items-center">
                      <span className="text-green-600 mr-2">✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </TabsContent>
          
          <TabsContent value="specifications" className="mt-6">
            <Card>
              <CardContent className="pt-6">
                <h3 className="text-lg font-semibold mb-4">Especificações Técnicas</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {Object.entries(product.specifications).map(([key, value]) => (
                    <div key={key} className="flex justify-between py-2 border-b">
                      <span className="font-medium">{key}:</span>
                      <span className="text-gray-700">{value}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          
          <TabsContent value="reviews" className="mt-6">
            <Card>
              <CardContent className="pt-6">
                <h3 className="text-lg font-semibold mb-4">Avaliações dos Clientes</h3>
                <div className="flex items-center space-x-4 mb-6">
                  <div className="text-4xl font-bold">{product.rating}</div>
                  <div>
                    <div className="flex items-center">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          className={`h-5 w-5 ${
                            i < Math.floor(product.rating) 
                              ? 'text-yellow-400 fill-current' 
                              : 'text-gray-300'
                          }`}
                        />
                      ))}
                    </div>
                    <p className="text-gray-600">{product.reviewsCount} avaliações</p>
                  </div>
                </div>
                
                {/* Simulação de algumas avaliações */}
                <div className="space-y-4">
                  <div className="border-b pb-4">
                    <div className="flex items-center space-x-2 mb-2">
                      <div className="flex">
                        {[...Array(5)].map((_, i) => (
                          <Star key={i} className="h-4 w-4 text-yellow-400 fill-current" />
                        ))}
                      </div>
                      <span className="font-medium">João Silva</span>
                      <span className="text-gray-500 text-sm">há 2 dias</span>
                    </div>
                    <p className="text-gray-700">
                      Excelente produto! A qualidade da câmera é impressionante e a bateria dura o dia todo.
                    </p>
                  </div>
                  
                  <div className="border-b pb-4">
                    <div className="flex items-center space-x-2 mb-2">
                      <div className="flex">
                        {[...Array(4)].map((_, i) => (
                          <Star key={i} className="h-4 w-4 text-yellow-400 fill-current" />
                        ))}
                        <Star className="h-4 w-4 text-gray-300" />
                      </div>
                      <span className="font-medium">Maria Santos</span>
                      <span className="text-gray-500 text-sm">há 1 semana</span>
                    </div>
                    <p className="text-gray-700">
                      Muito bom, mas achei um pouco pesado. No geral, recomendo!
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          
          <TabsContent value="shipping" className="mt-6">
            <Card>
              <CardContent className="pt-6">
                <h3 className="text-lg font-semibold mb-4">Informações de Entrega</h3>
                <div className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <Truck className="h-5 w-5 text-green-600" />
                    <div>
                      <p className="font-medium">Frete Grátis</p>
                      <p className="text-sm text-gray-600">Para todo o Brasil</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">📦</span>
                    <div>
                      <p className="font-medium">Prazo de Entrega</p>
                      <p className="text-sm text-gray-600">{product.shipping.estimatedDays}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    <Shield className="h-5 w-5 text-blue-600" />
                    <div>
                      <p className="font-medium">Garantia</p>
                      <p className="text-sm text-gray-600">{product.warranty}</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default ProductDetail;
