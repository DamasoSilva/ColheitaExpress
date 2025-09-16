import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { 
  Package, 
  Users, 
  ShoppingCart, 
  Truck, 
  TrendingUp, 
  TrendingDown,
  Plus,
  Edit,
  Trash2,
  Eye,
  BarChart3,
  DollarSign
} from 'lucide-react'

function AdminDashboard() {
  const [activeTab, setActiveTab] = useState('overview')

  // Dados simulados para o dashboard
  const stats = [
    {
      title: 'Vendas Totais',
      value: 'R$ 45.231,89',
      change: '+20.1%',
      trend: 'up',
      icon: DollarSign
    },
    {
      title: 'Pedidos',
      value: '1.234',
      change: '+15.3%',
      trend: 'up',
      icon: ShoppingCart
    },
    {
      title: 'Produtos',
      value: '856',
      change: '+5.2%',
      trend: 'up',
      icon: Package
    },
    {
      title: 'Clientes',
      value: '2.847',
      change: '+12.8%',
      trend: 'up',
      icon: Users
    }
  ]

  const recentOrders = [
    {
      id: '#12345',
      customer: 'João Silva',
      total: 'R$ 299,99',
      status: 'confirmed',
      date: '2024-09-15'
    },
    {
      id: '#12346',
      customer: 'Maria Santos',
      total: 'R$ 1.299,99',
      status: 'shipped',
      date: '2024-09-15'
    },
    {
      id: '#12347',
      customer: 'Pedro Costa',
      total: 'R$ 199,99',
      status: 'delivered',
      date: '2024-09-14'
    },
    {
      id: '#12348',
      customer: 'Ana Oliveira',
      total: 'R$ 599,99',
      status: 'pending',
      date: '2024-09-14'
    }
  ]

  const products = [
    {
      id: 1,
      name: 'Smartphone Premium',
      category: 'Eletrônicos',
      price: 'R$ 1.299,99',
      stock: 45,
      status: 'active'
    },
    {
      id: 2,
      name: 'Notebook Gamer',
      category: 'Informática',
      price: 'R$ 2.499,99',
      stock: 12,
      status: 'active'
    },
    {
      id: 3,
      name: 'Fone Bluetooth',
      category: 'Eletrônicos',
      price: 'R$ 199,99',
      stock: 0,
      status: 'inactive'
    }
  ]

  const getStatusBadge = (status) => {
    const statusConfig = {
      pending: { variant: 'secondary', label: 'Pendente' },
      confirmed: { variant: 'default', label: 'Confirmado' },
      shipped: { variant: 'outline', label: 'Enviado' },
      delivered: { variant: 'default', label: 'Entregue' },
      active: { variant: 'default', label: 'Ativo' },
      inactive: { variant: 'destructive', label: 'Inativo' }
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
            <h1 className="text-2xl font-bold text-gray-900">Dashboard Administrativo</h1>
            <div className="flex items-center space-x-4">
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Novo Produto
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">Visão Geral</TabsTrigger>
            <TabsTrigger value="products">Produtos</TabsTrigger>
            <TabsTrigger value="orders">Pedidos</TabsTrigger>
            <TabsTrigger value="analytics">Relatórios</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {stats.map((stat, index) => (
                <Card key={index}>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
                    <stat.icon className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">{stat.value}</div>
                    <p className="text-xs text-muted-foreground flex items-center">
                      {stat.trend === 'up' ? (
                        <TrendingUp className="h-3 w-3 mr-1 text-green-500" />
                      ) : (
                        <TrendingDown className="h-3 w-3 mr-1 text-red-500" />
                      )}
                      {stat.change} em relação ao mês anterior
                    </p>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Recent Orders */}
            <Card>
              <CardHeader>
                <CardTitle>Pedidos Recentes</CardTitle>
                <CardDescription>
                  Últimos pedidos realizados na plataforma
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentOrders.map((order) => (
                    <div key={order.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div>
                          <p className="font-medium">{order.id}</p>
                          <p className="text-sm text-gray-600">{order.customer}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-4">
                        <div className="text-right">
                          <p className="font-medium">{order.total}</p>
                          <p className="text-sm text-gray-600">{order.date}</p>
                        </div>
                        {getStatusBadge(order.status)}
                        <Button variant="outline" size="sm">
                          <Eye className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="products" className="space-y-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between">
                <div>
                  <CardTitle>Gestão de Produtos</CardTitle>
                  <CardDescription>
                    Gerencie seu catálogo de produtos
                  </CardDescription>
                </div>
                <Button>
                  <Plus className="h-4 w-4 mr-2" />
                  Adicionar Produto
                </Button>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {products.map((product) => (
                    <div key={product.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div className="w-12 h-12 bg-gray-200 rounded-lg"></div>
                        <div>
                          <p className="font-medium">{product.name}</p>
                          <p className="text-sm text-gray-600">{product.category}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-4">
                        <div className="text-right">
                          <p className="font-medium">{product.price}</p>
                          <p className="text-sm text-gray-600">Estoque: {product.stock}</p>
                        </div>
                        {getStatusBadge(product.status)}
                        <div className="flex space-x-2">
                          <Button variant="outline" size="sm">
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button variant="outline" size="sm">
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="orders" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Gestão de Pedidos</CardTitle>
                <CardDescription>
                  Acompanhe e gerencie todos os pedidos
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentOrders.map((order) => (
                    <div key={order.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-4">
                        <div>
                          <p className="font-medium">{order.id}</p>
                          <p className="text-sm text-gray-600">{order.customer}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-4">
                        <div className="text-right">
                          <p className="font-medium">{order.total}</p>
                          <p className="text-sm text-gray-600">{order.date}</p>
                        </div>
                        {getStatusBadge(order.status)}
                        <div className="flex space-x-2">
                          <Button variant="outline" size="sm">
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button variant="outline" size="sm">
                            <Truck className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <BarChart3 className="h-5 w-5 mr-2" />
                    Vendas por Período
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
                    <p className="text-gray-500">Gráfico de vendas seria exibido aqui</p>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Package className="h-5 w-5 mr-2" />
                    Produtos Mais Vendidos
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span>Smartphone Premium</span>
                      <Badge>156 vendas</Badge>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Notebook Gamer</span>
                      <Badge>89 vendas</Badge>
                    </div>
                    <div className="flex justify-between items-center">
                      <span>Fone Bluetooth</span>
                      <Badge>67 vendas</Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default AdminDashboard
