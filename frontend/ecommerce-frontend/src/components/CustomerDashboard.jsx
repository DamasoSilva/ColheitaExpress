import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { 
  Package, 
  ShoppingCart, 
  Heart, 
  User, 
  MapPin,
  CreditCard,
  Star,
  Truck,
  Eye,
  RotateCcw,
  Plus
} from 'lucide-react'

function CustomerDashboard() {
  const [activeTab, setActiveTab] = useState('orders')

  // Dados simulados para o dashboard do cliente
  const customerOrders = [
    {
      id: '#12345',
      date: '2024-09-15',
      total: 'R$ 299,99',
      status: 'delivered',
      items: 2,
      trackingCode: 'BR123456789',
      deliveryDate: '2024-09-18'
    },
    {
      id: '#12346',
      date: '2024-09-10',
      total: 'R$ 1.299,99',
      status: 'shipped',
      items: 1,
      trackingCode: 'BR987654321',
      estimatedDelivery: '2024-09-16'
    },
    {
      id: '#12347',
      date: '2024-09-05',
      total: 'R$ 199,99',
      status: 'processing',
      items: 3,
      trackingCode: null
    }
  ]

  const favoriteProducts = [
    {
      id: 1,
      name: 'Smartphone Premium',
      price: 'R$ 1.299,99',
      originalPrice: 'R$ 1.499,99',
      image: 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=150&h=150&fit=crop',
      inStock: true,
      discount: 13
    },
    {
      id: 2,
      name: 'Fone Bluetooth',
      price: 'R$ 199,99',
      originalPrice: 'R$ 249,99',
      image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=150&h=150&fit=crop',
      inStock: true,
      discount: 20
    },
    {
      id: 3,
      name: 'Smart Watch',
      price: 'R$ 399,99',
      image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=150&h=150&fit=crop',
      inStock: false
    }
  ]

  const customerInfo = {
    name: 'João Silva',
    email: 'joao.silva@email.com',
    phone: '+55 11 99999-9999',
    cpf: '123.456.789-01',
    address: {
      street: 'Rua das Flores, 123',
      city: 'São Paulo',
      state: 'SP',
      zipCode: '01234-567'
    }
  }

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { variant: 'secondary', label: 'Pendente' },
      processing: { variant: 'default', label: 'Processando' },
      shipped: { variant: 'outline', label: 'Enviado' },
      delivered: { variant: 'default', label: 'Entregue' },
      cancelled: { variant: 'destructive', label: 'Cancelado' }
    }
    
    const config = statusConfig[status] || { variant: 'secondary', label: status }
    return <Badge variant={config.variant}>{config.label}</Badge>
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-2xl font-bold text-gray-900">Minha Conta</h1>
            <div className="flex items-center space-x-4">
              <Button variant="outline">
                <ShoppingCart className="h-4 w-4 mr-2" />
                Continuar Comprando
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader className="text-center">
                <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                  <User className="h-10 w-10 text-primary" />
                </div>
                <CardTitle>{customerInfo.name}</CardTitle>
                <CardDescription>{customerInfo.email}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <Button variant="ghost" className="w-full justify-start">
                    <Package className="h-4 w-4 mr-2" />
                    Meus Pedidos
                  </Button>
                  <Button variant="ghost" className="w-full justify-start">
                    <Heart className="h-4 w-4 mr-2" />
                    Lista de Desejos
                  </Button>
                  <Button variant="ghost" className="w-full justify-start">
                    <MapPin className="h-4 w-4 mr-2" />
                    Endereços
                  </Button>
                  <Button variant="ghost" className="w-full justify-start">
                    <CreditCard className="h-4 w-4 mr-2" />
                    Pagamentos
                  </Button>
                  <Button variant="ghost" className="w-full justify-start">
                    <User className="h-4 w-4 mr-2" />
                    Dados Pessoais
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="orders">Pedidos</TabsTrigger>
                <TabsTrigger value="favorites">Favoritos</TabsTrigger>
                <TabsTrigger value="profile">Perfil</TabsTrigger>
                <TabsTrigger value="addresses">Endereços</TabsTrigger>
              </TabsList>

              <TabsContent value="orders" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Meus Pedidos</CardTitle>
                    <CardDescription>
                      Acompanhe o status dos seus pedidos
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {customerOrders.map((order) => (
                        <div key={order.id} className="border rounded-lg p-6">
                          <div className="flex justify-between items-start mb-4">
                            <div>
                              <h3 className="font-semibold text-lg">{order.id}</h3>
                              <p className="text-sm text-gray-600">Pedido realizado em {order.date}</p>
                            </div>
                            <div className="text-right">
                              <p className="font-semibold text-lg">{order.total}</p>
                              {getStatusBadge(order.status)}
                            </div>
                          </div>
                          
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                            <div>
                              <p className="text-gray-600">Itens</p>
                              <p className="font-medium">{order.items} produto(s)</p>
                            </div>
                            {order.trackingCode && (
                              <div>
                                <p className="text-gray-600">Código de Rastreamento</p>
                                <p className="font-medium">{order.trackingCode}</p>
                              </div>
                            )}
                            {order.deliveryDate && (
                              <div>
                                <p className="text-gray-600">Entregue em</p>
                                <p className="font-medium">{order.deliveryDate}</p>
                              </div>
                            )}
                            {order.estimatedDelivery && (
                              <div>
                                <p className="text-gray-600">Previsão de Entrega</p>
                                <p className="font-medium">{order.estimatedDelivery}</p>
                              </div>
                            )}
                          </div>
                          
                          <div className="flex justify-end space-x-2 mt-4">
                            <Button variant="outline" size="sm">
                              <Eye className="h-4 w-4 mr-2" />
                              Ver Detalhes
                            </Button>
                            {order.status === 'shipped' && (
                              <Button variant="outline" size="sm">
                                <Truck className="h-4 w-4 mr-2" />
                                Rastrear
                              </Button>
                            )}
                            {order.status === 'delivered' && (
                              <Button variant="outline" size="sm">
                                <RotateCcw className="h-4 w-4 mr-2" />
                                Comprar Novamente
                              </Button>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="favorites" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Lista de Desejos</CardTitle>
                    <CardDescription>
                      Produtos que você salvou para comprar depois
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {favoriteProducts.map((product) => (
                        <div key={product.id} className="border rounded-lg p-4">
                          <div className="flex space-x-4">
                            <img 
                              src={product.image} 
                              alt={product.name}
                              className="w-20 h-20 object-cover rounded-lg"
                            />
                            <div className="flex-1">
                              <h3 className="font-semibold">{product.name}</h3>
                              <div className="flex items-center space-x-2 mt-2">
                                <span className="text-lg font-bold text-primary">{product.price}</span>
                                {product.originalPrice && (
                                  <>
                                    <span className="text-sm text-gray-500 line-through">{product.originalPrice}</span>
                                    <Badge variant="destructive" className="text-xs">
                                      -{product.discount}%
                                    </Badge>
                                  </>
                                )}
                              </div>
                              <div className="flex space-x-2 mt-3">
                                <Button size="sm" disabled={!product.inStock}>
                                  <ShoppingCart className="h-4 w-4 mr-2" />
                                  {product.inStock ? 'Adicionar ao Carrinho' : 'Fora de Estoque'}
                                </Button>
                                <Button variant="outline" size="sm">
                                  <Heart className="h-4 w-4" />
                                </Button>
                              </div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="profile" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Dados Pessoais</CardTitle>
                    <CardDescription>
                      Gerencie suas informações pessoais
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Nome Completo
                        </label>
                        <p className="text-lg">{customerInfo.name}</p>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          E-mail
                        </label>
                        <p className="text-lg">{customerInfo.email}</p>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Telefone
                        </label>
                        <p className="text-lg">{customerInfo.phone}</p>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          CPF
                        </label>
                        <p className="text-lg">{customerInfo.cpf}</p>
                      </div>
                    </div>
                    <div className="mt-6">
                      <Button>Editar Informações</Button>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="addresses" className="space-y-6">
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between">
                    <div>
                      <CardTitle>Endereços</CardTitle>
                      <CardDescription>
                        Gerencie seus endereços de entrega
                      </CardDescription>
                    </div>
                    <Button>
                      <Plus className="h-4 w-4 mr-2" />
                      Novo Endereço
                    </Button>
                  </CardHeader>
                  <CardContent>
                    <div className="border rounded-lg p-4">
                      <div className="flex justify-between items-start">
                        <div>
                          <h3 className="font-semibold">Endereço Principal</h3>
                          <p className="text-gray-600 mt-2">
                            {customerInfo.address.street}<br />
                            {customerInfo.address.city}, {customerInfo.address.state}<br />
                            CEP: {customerInfo.address.zipCode}
                          </p>
                        </div>
                        <Badge>Principal</Badge>
                      </div>
                      <div className="flex space-x-2 mt-4">
                        <Button variant="outline" size="sm">Editar</Button>
                        <Button variant="outline" size="sm">Remover</Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </div>
    </div>
  )
}

export default CustomerDashboard
