import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { 
  Truck, 
  MapPin, 
  Package, 
  Clock, 
  CheckCircle,
  XCircle,
  Navigation,
  Phone,
  User,
  Calendar,
  Route,
  Star
} from 'lucide-react'

function DriverDashboard() {
  const [activeTab, setActiveTab] = useState('deliveries')

  // Dados simulados para o dashboard do motorista
  const todayDeliveries = [
    {
      id: 'D001',
      orderNumber: '#12345',
      customerName: 'João Silva',
      customerPhone: '+55 11 99999-9999',
      address: 'Rua das Flores, 123 - Vila Madalena, São Paulo - SP',
      zipCode: '01234-567',
      items: [
        { name: 'Smartphone Premium', quantity: 1 },
        { name: 'Capa Protetora', quantity: 1 }
      ],
      status: 'assigned',
      estimatedTime: '14:30',
      priority: 'normal'
    },
    {
      id: 'D002',
      orderNumber: '#12346',
      customerName: 'Maria Santos',
      customerPhone: '+55 11 88888-8888',
      address: 'Av. Paulista, 1000 - Bela Vista, São Paulo - SP',
      zipCode: '01310-100',
      items: [
        { name: 'Notebook Gamer', quantity: 1 }
      ],
      status: 'in_transit',
      estimatedTime: '15:45',
      priority: 'high'
    },
    {
      id: 'D003',
      orderNumber: '#12347',
      customerName: 'Pedro Costa',
      customerPhone: '+55 11 77777-7777',
      address: 'Rua Augusta, 500 - Consolação, São Paulo - SP',
      zipCode: '01305-000',
      items: [
        { name: 'Fone Bluetooth', quantity: 2 },
        { name: 'Carregador Portátil', quantity: 1 }
      ],
      status: 'delivered',
      estimatedTime: '13:15',
      deliveredTime: '13:10',
      priority: 'normal'
    }
  ]

  const driverStats = {
    todayDeliveries: 8,
    completedDeliveries: 5,
    pendingDeliveries: 3,
    totalDistance: '45.2 km',
    averageRating: 4.8,
    totalRatings: 156
  }

  const getStatusBadge = (status) => {
    const statusConfig = {
      assigned: { variant: 'secondary', label: 'Atribuída', icon: Clock },
      picked_up: { variant: 'default', label: 'Coletada', icon: Package },
      in_transit: { variant: 'outline', label: 'Em Trânsito', icon: Truck },
      delivered: { variant: 'default', label: 'Entregue', icon: CheckCircle },
      failed: { variant: 'destructive', label: 'Falha', icon: XCircle }
    }
    
    const config = statusConfig[status] || { variant: 'secondary', label: status, icon: Clock }
    const Icon = config.icon
    
    return (
      <Badge variant={config.variant} className="flex items-center gap-1">
        <Icon className="h-3 w-3" />
        {config.label}
      </Badge>
    )
  }

  const getPriorityBadge = (priority) => {
    const priorityConfig = {
      high: { variant: 'destructive', label: 'Alta' },
      normal: { variant: 'secondary', label: 'Normal' },
      low: { variant: 'outline', label: 'Baixa' }
    }
    
    const config = priorityConfig[priority] || { variant: 'secondary', label: priority }
    return <Badge variant={config.variant}>{config.label}</Badge>
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-2xl font-bold text-gray-900">Dashboard do Motorista</h1>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="flex items-center gap-2">
                <Star className="h-4 w-4 text-yellow-500" />
                {driverStats.averageRating} ({driverStats.totalRatings} avaliações)
              </Badge>
              <Button>
                <Route className="h-4 w-4 mr-2" />
                Iniciar Rota
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Entregas Hoje</CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{driverStats.todayDeliveries}</div>
              <p className="text-xs text-muted-foreground">
                {driverStats.completedDeliveries} concluídas, {driverStats.pendingDeliveries} pendentes
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Distância Total</CardTitle>
              <Route className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{driverStats.totalDistance}</div>
              <p className="text-xs text-muted-foreground">
                Percorrida hoje
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Taxa de Sucesso</CardTitle>
              <CheckCircle className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {Math.round((driverStats.completedDeliveries / driverStats.todayDeliveries) * 100)}%
              </div>
              <p className="text-xs text-muted-foreground">
                Entregas bem-sucedidas
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Avaliação</CardTitle>
              <Star className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold flex items-center">
                {driverStats.averageRating}
                <Star className="h-5 w-5 text-yellow-500 ml-1" />
              </div>
              <p className="text-xs text-muted-foreground">
                {driverStats.totalRatings} avaliações
              </p>
            </CardContent>
          </Card>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="deliveries">Entregas de Hoje</TabsTrigger>
            <TabsTrigger value="route">Minha Rota</TabsTrigger>
            <TabsTrigger value="history">Histórico</TabsTrigger>
          </TabsList>

          <TabsContent value="deliveries" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Entregas Programadas</CardTitle>
                <CardDescription>
                  Lista de entregas para hoje ({new Date().toLocaleDateString('pt-BR')})
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {todayDeliveries.map((delivery) => (
                    <div key={delivery.id} className="border rounded-lg p-6">
                      <div className="flex justify-between items-start mb-4">
                        <div>
                          <div className="flex items-center space-x-2 mb-2">
                            <h3 className="font-semibold text-lg">{delivery.orderNumber}</h3>
                            {getStatusBadge(delivery.status)}
                            {getPriorityBadge(delivery.priority)}
                          </div>
                          <p className="text-sm text-gray-600">Entrega ID: {delivery.id}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm text-gray-600">Previsão</p>
                          <p className="font-semibold">{delivery.estimatedTime}</p>
                          {delivery.deliveredTime && (
                            <p className="text-sm text-green-600">Entregue às {delivery.deliveredTime}</p>
                          )}
                        </div>
                      </div>

                      {/* Customer Info */}
                      <div className="bg-gray-50 rounded-lg p-4 mb-4">
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center space-x-2">
                            <User className="h-4 w-4 text-gray-600" />
                            <span className="font-medium">{delivery.customerName}</span>
                          </div>
                          <Button variant="outline" size="sm">
                            <Phone className="h-4 w-4 mr-2" />
                            Ligar
                          </Button>
                        </div>
                        <div className="flex items-start space-x-2">
                          <MapPin className="h-4 w-4 text-gray-600 mt-1" />
                          <div>
                            <p className="text-sm">{delivery.address}</p>
                            <p className="text-sm text-gray-600">CEP: {delivery.zipCode}</p>
                          </div>
                        </div>
                      </div>

                      {/* Items */}
                      <div className="mb-4">
                        <h4 className="font-medium mb-2 flex items-center">
                          <Package className="h-4 w-4 mr-2" />
                          Itens para Entrega
                        </h4>
                        <div className="space-y-1">
                          {delivery.items.map((item, index) => (
                            <p key={index} className="text-sm text-gray-600">
                              {item.quantity}x {item.name}
                            </p>
                          ))}
                        </div>
                      </div>

                      {/* Actions */}
                      <div className="flex space-x-2">
                        {delivery.status === 'assigned' && (
                          <>
                            <Button size="sm">
                              <Package className="h-4 w-4 mr-2" />
                              Coletar
                            </Button>
                            <Button variant="outline" size="sm">
                              <Navigation className="h-4 w-4 mr-2" />
                              Navegar
                            </Button>
                          </>
                        )}
                        {delivery.status === 'in_transit' && (
                          <>
                            <Button size="sm">
                              <CheckCircle className="h-4 w-4 mr-2" />
                              Confirmar Entrega
                            </Button>
                            <Button variant="outline" size="sm">
                              <XCircle className="h-4 w-4 mr-2" />
                              Reportar Problema
                            </Button>
                          </>
                        )}
                        {delivery.status === 'delivered' && (
                          <Badge variant="default" className="flex items-center gap-1">
                            <CheckCircle className="h-3 w-3" />
                            Entrega Concluída
                          </Badge>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="route" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Route className="h-5 w-5 mr-2" />
                  Rota Otimizada
                </CardTitle>
                <CardDescription>
                  Rota calculada para máxima eficiência
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-96 bg-gray-100 rounded-lg flex items-center justify-center">
                  <div className="text-center">
                    <MapPin className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600">Mapa da rota seria exibido aqui</p>
                    <p className="text-sm text-gray-500 mt-2">
                      Integração com Google Maps ou similar
                    </p>
                  </div>
                </div>
                <div className="mt-4 flex justify-between items-center">
                  <div className="text-sm text-gray-600">
                    <p>Distância total: <span className="font-medium">12.5 km</span></p>
                    <p>Tempo estimado: <span className="font-medium">45 min</span></p>
                  </div>
                  <Button>
                    <Navigation className="h-4 w-4 mr-2" />
                    Iniciar Navegação
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="history" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Histórico de Entregas</CardTitle>
                <CardDescription>
                  Suas entregas dos últimos 30 dias
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                    <div className="bg-green-50 p-4 rounded-lg">
                      <p className="text-2xl font-bold text-green-600">142</p>
                      <p className="text-sm text-green-700">Entregas Concluídas</p>
                    </div>
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <p className="text-2xl font-bold text-blue-600">456.8 km</p>
                      <p className="text-sm text-blue-700">Distância Percorrida</p>
                    </div>
                    <div className="bg-yellow-50 p-4 rounded-lg">
                      <p className="text-2xl font-bold text-yellow-600">4.9</p>
                      <p className="text-sm text-yellow-700">Avaliação Média</p>
                    </div>
                  </div>
                  
                  <div className="text-center py-8">
                    <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-600">Histórico detalhado seria exibido aqui</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default DriverDashboard
