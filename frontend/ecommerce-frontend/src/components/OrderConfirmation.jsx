import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';
import { CheckCircle, Package, Truck, CreditCard, Download, Home } from 'lucide-react';

const OrderConfirmation = ({ orderData, onContinueShopping }) => {
  const estimatedDelivery = new Date();
  estimatedDelivery.setDate(estimatedDelivery.getDate() + 5); // 5 dias úteis

  const handleDownloadReceipt = () => {
    // Simular download do comprovante
    const receiptData = `
COMPROVANTE DE COMPRA
=====================

Pedido: ${orderData.orderNumber}
Data: ${new Date().toLocaleDateString('pt-BR')}
Cliente: ${orderData.customer.fullName}

PRODUTOS:
${orderData.items.map(item => 
  `${item.quantity}x ${item.name} - R$ ${(item.price * item.quantity).toFixed(2)}`
).join('\n')}

TOTAL: R$ ${orderData.total.toFixed(2)}

Obrigado pela sua compra!
    `;

    const blob = new Blob([receiptData], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `comprovante-${orderData.orderNumber}.txt`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-3xl mx-auto">
        {/* Confirmação Principal */}
        <Card className="mb-8">
          <CardContent className="text-center py-12">
            <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
            <h1 className="text-3xl font-bold text-green-600 mb-2">
              Pedido Confirmado!
            </h1>
            <p className="text-xl text-gray-600 mb-4">
              Seu pedido foi realizado com sucesso
            </p>
            <div className="bg-gray-100 rounded-lg p-4 inline-block">
              <p className="text-sm text-gray-600">Número do pedido</p>
              <p className="text-2xl font-bold">{orderData.orderNumber}</p>
            </div>
          </CardContent>
        </Card>

        {/* Próximos Passos */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Próximos Passos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center space-x-4 p-4 bg-blue-50 rounded-lg">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                    1
                  </div>
                </div>
                <div>
                  <h3 className="font-semibold">Confirmação por E-mail</h3>
                  <p className="text-sm text-gray-600">
                    Enviamos um e-mail de confirmação para {orderData.customer.email}
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-4 p-4 bg-yellow-50 rounded-lg">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-yellow-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                    2
                  </div>
                </div>
                <div>
                  <h3 className="font-semibold">Processamento</h3>
                  <p className="text-sm text-gray-600">
                    Seu pedido será processado em até 1 dia útil
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-4 p-4 bg-green-50 rounded-lg">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                    3
                  </div>
                </div>
                <div>
                  <h3 className="font-semibold">Entrega</h3>
                  <p className="text-sm text-gray-600">
                    Previsão de entrega: {estimatedDelivery.toLocaleDateString('pt-BR')}
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Resumo do Pedido */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Package className="h-5 w-5 mr-2" />
              Resumo do Pedido
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {orderData.items.map(item => (
                <div key={item.id} className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                      📦
                    </div>
                    <div>
                      <h4 className="font-medium">{item.name}</h4>
                      <p className="text-sm text-gray-600">
                        Quantidade: {item.quantity}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold">
                      R$ {(item.price * item.quantity).toFixed(2)}
                    </p>
                    <p className="text-sm text-gray-600">
                      R$ {item.price.toFixed(2)} cada
                    </p>
                  </div>
                </div>
              ))}
              
              <Separator />
              
              <div className="flex justify-between text-lg font-semibold">
                <span>Total</span>
                <span>R$ {orderData.total.toFixed(2)}</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Informações de Entrega */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Truck className="h-5 w-5 mr-2" />
                Entrega
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <p><strong>{orderData.customer.fullName}</strong></p>
                <p>{orderData.customer.street}, {orderData.customer.number}</p>
                {orderData.customer.complement && (
                  <p>{orderData.customer.complement}</p>
                )}
                <p>{orderData.customer.neighborhood}</p>
                <p>{orderData.customer.city} - {orderData.customer.state}</p>
                <p>CEP: {orderData.customer.zipCode}</p>
              </div>
              <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                <p className="text-sm font-medium text-blue-800">
                  Previsão de entrega
                </p>
                <p className="text-blue-600">
                  {estimatedDelivery.toLocaleDateString('pt-BR')}
                </p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <CreditCard className="h-5 w-5 mr-2" />
                Pagamento
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {orderData.customer.paymentMethod === 'credit_card' && (
                  <>
                    <p><strong>Cartão de Crédito</strong></p>
                    <p>Parcelado em {orderData.customer.installments}x</p>
                    <Badge variant="outline" className="text-green-600">
                      ✓ Aprovado
                    </Badge>
                  </>
                )}
                {orderData.customer.paymentMethod === 'pix' && (
                  <>
                    <p><strong>PIX</strong></p>
                    <Badge variant="outline" className="text-green-600">
                      ✓ Pago
                    </Badge>
                  </>
                )}
                {orderData.customer.paymentMethod === 'boleto' && (
                  <>
                    <p><strong>Boleto Bancário</strong></p>
                    <Badge variant="outline" className="text-yellow-600">
                      ⏳ Aguardando pagamento
                    </Badge>
                  </>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Ações */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button onClick={handleDownloadReceipt} variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Baixar Comprovante
          </Button>
          
          <Button onClick={() => window.location.href = '/customer-dashboard'}>
            <Package className="h-4 w-4 mr-2" />
            Acompanhar Pedido
          </Button>
          
          <Button onClick={onContinueShopping}>
            <Home className="h-4 w-4 mr-2" />
            Continuar Comprando
          </Button>
        </div>

        {/* Informações Adicionais */}
        <Card className="mt-8">
          <CardContent className="text-center py-6">
            <h3 className="font-semibold mb-2">Precisa de Ajuda?</h3>
            <p className="text-gray-600 mb-4">
              Nossa equipe está pronta para ajudar você
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button variant="outline" size="sm">
                📞 (11) 3000-0000
              </Button>
              <Button variant="outline" size="sm">
                📧 suporte@ecommerce.com
              </Button>
              <Button variant="outline" size="sm">
                💬 Chat Online
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default OrderConfirmation;
