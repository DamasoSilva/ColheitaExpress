import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Input } from './ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { ShoppingCart, Star, Search, Filter } from 'lucide-react';

const ProductList = ({ onAddToCart }) => {
  const [products, setProducts] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDepartment, setSelectedDepartment] = useState('');
  const [sortBy, setSortBy] = useState('name');

  useEffect(() => {
    fetchProducts();
    fetchDepartments();
  }, []);

  const fetchProducts = async () => {
    try {
      // Simular dados de produtos para demonstração
      const mockProducts = [
        {
          id: 1,
          name: 'Smartphone Galaxy Pro',
          description: 'Smartphone avançado com câmera de 108MP e 5G',
          price: 1299.99,
          department: { id: 1, name: 'Eletrônicos' },
          is_featured: true,
          stock_quantity: 25,
          images: []
        },
        {
          id: 2,
          name: 'Notebook Gamer Ultra',
          description: 'Notebook para jogos com RTX 4060 e 16GB RAM',
          price: 3499.99,
          department: { id: 1, name: 'Eletrônicos' },
          is_featured: true,
          stock_quantity: 10,
          images: []
        },
        {
          id: 3,
          name: 'Livro: Python para Iniciantes',
          description: 'Aprenda Python do zero com exemplos práticos',
          price: 89.90,
          department: { id: 2, name: 'Livros' },
          is_featured: false,
          stock_quantity: 50,
          images: []
        },
        {
          id: 4,
          name: 'Fone de Ouvido Bluetooth',
          description: 'Fone sem fio com cancelamento de ruído',
          price: 299.99,
          department: { id: 1, name: 'Eletrônicos' },
          is_featured: false,
          stock_quantity: 30,
          images: []
        },
        {
          id: 5,
          name: 'Camiseta Tech Premium',
          description: 'Camiseta 100% algodão com estampa tecnológica',
          price: 59.90,
          department: { id: 3, name: 'Roupas' },
          is_featured: false,
          stock_quantity: 100,
          images: []
        },
        {
          id: 6,
          name: 'Mouse Gamer RGB',
          description: 'Mouse óptico com iluminação RGB e 12000 DPI',
          price: 149.99,
          department: { id: 1, name: 'Eletrônicos' },
          is_featured: false,
          stock_quantity: 40,
          images: []
        }
      ];
      
      setProducts(mockProducts);
      setLoading(false);
    } catch (error) {
      console.error('Erro ao buscar produtos:', error);
      setLoading(false);
    }
  };

  const fetchDepartments = async () => {
    try {
      const mockDepartments = [
        { id: 1, name: 'Eletrônicos' },
        { id: 2, name: 'Livros' },
        { id: 3, name: 'Roupas' }
      ];
      setDepartments(mockDepartments);
    } catch (error) {
      console.error('Erro ao buscar departamentos:', error);
    }
  };

  const filteredProducts = products
    .filter(product => 
      product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      product.description.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .filter(product => 
      selectedDepartment === '' || product.department.id.toString() === selectedDepartment
    )
    .sort((a, b) => {
      switch (sortBy) {
        case 'price_asc':
          return a.price - b.price;
        case 'price_desc':
          return b.price - a.price;
        case 'name':
        default:
          return a.name.localeCompare(b.name);
      }
    });

  const handleAddToCart = (product) => {
    if (onAddToCart) {
      onAddToCart(product);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Filtros e Busca */}
      <div className="mb-8 space-y-4">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
            <Input
              placeholder="Buscar produtos..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
          
          <Select value={selectedDepartment} onValueChange={setSelectedDepartment}>
            <SelectTrigger className="w-full md:w-48">
              <Filter className="h-4 w-4 mr-2" />
              <SelectValue placeholder="Departamento" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="">Todos os departamentos</SelectItem>
              {departments.map(dept => (
                <SelectItem key={dept.id} value={dept.id.toString()}>
                  {dept.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Select value={sortBy} onValueChange={setSortBy}>
            <SelectTrigger className="w-full md:w-48">
              <SelectValue placeholder="Ordenar por" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="name">Nome A-Z</SelectItem>
              <SelectItem value="price_asc">Menor preço</SelectItem>
              <SelectItem value="price_desc">Maior preço</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Grid de Produtos */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {filteredProducts.map(product => (
          <Card key={product.id} className="group hover:shadow-lg transition-shadow duration-300">
            <CardHeader className="p-0">
              <div className="aspect-square bg-gradient-to-br from-gray-100 to-gray-200 rounded-t-lg flex items-center justify-center relative overflow-hidden">
                {product.is_featured && (
                  <Badge className="absolute top-2 left-2 bg-red-500">
                    Destaque
                  </Badge>
                )}
                <div className="text-6xl text-gray-400">📦</div>
                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 transition-all duration-300"></div>
              </div>
            </CardHeader>
            
            <CardContent className="p-4">
              <div className="mb-2">
                <Badge variant="outline" className="text-xs">
                  {product.department.name}
                </Badge>
              </div>
              
              <CardTitle className="text-lg mb-2 line-clamp-2">
                {product.name}
              </CardTitle>
              
              <CardDescription className="text-sm text-gray-600 mb-3 line-clamp-2">
                {product.description}
              </CardDescription>
              
              <div className="flex items-center justify-between mb-3">
                <div className="text-2xl font-bold text-green-600">
                  R$ {product.price.toFixed(2)}
                </div>
                <div className="flex items-center text-yellow-500">
                  <Star className="h-4 w-4 fill-current" />
                  <span className="text-sm text-gray-600 ml-1">4.5</span>
                </div>
              </div>
              
              <div className="text-sm text-gray-500 mb-3">
                {product.stock_quantity > 0 ? (
                  <span className="text-green-600">
                    ✓ {product.stock_quantity} em estoque
                  </span>
                ) : (
                  <span className="text-red-600">✗ Fora de estoque</span>
                )}
              </div>
            </CardContent>
            
            <CardFooter className="p-4 pt-0">
              <Button 
                className="w-full"
                onClick={() => handleAddToCart(product)}
                disabled={product.stock_quantity === 0}
              >
                <ShoppingCart className="h-4 w-4 mr-2" />
                {product.stock_quantity > 0 ? 'Adicionar ao Carrinho' : 'Indisponível'}
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>

      {filteredProducts.length === 0 && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🔍</div>
          <h3 className="text-xl font-semibold mb-2">Nenhum produto encontrado</h3>
          <p className="text-gray-600">
            Tente ajustar os filtros ou termos de busca
          </p>
        </div>
      )}
    </div>
  );
};

export default ProductList;
