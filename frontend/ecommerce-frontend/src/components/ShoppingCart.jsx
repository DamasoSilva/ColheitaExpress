import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Input } from './ui/input';
import { Separator } from './ui/separator';
import { ShoppingCart, Plus, Minus, Trash2, CreditCard } from 'lucide-react';

const ShoppingCartComponent = ({ cartItems, onUpdateQuantity, onRemoveItem, onCheckout }) => {
  const [couponCode, setCouponCode] = useState('');
  const [discount, setDiscount] = useState(0);

  const subtotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const shipping = subtotal > 100 ? 0 : 15.00; // Frete grátis acima de R$ 100
  const tax = subtotal * 0.05; // 5% de impostos
  const total = subtotal + shipping + tax - discount;

  const handleQuantityChange = (itemId, newQuantity) => {
    if (newQuantity < 1) return;
    onUpdateQuantity(itemId, newQuantity);
  };

  const handleApplyCoupon = () => {
    // Simular cupons de desconto
    const coupons = {
      'DESCONTO10': 0.10,
      'BEMVINDO': 0.15,
      'FRETE20': 0.20
    };

    if (coupons[couponCode.toUpperCase()]) {
      const discountAmount = subtotal * coupons[couponCode.toUpperCase()];
      setDiscount(discountAmount);
    } else {
      alert('Cupom inválido');
    }
  };

  if (cartItems.length === 0) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card className="max-w-2xl mx-auto">
          <CardContent className="text-center py-12">
            <ShoppingCart className="h-16 w-16 mx-auto text-gray-400 mb-4" />
            <h2 className="text-2xl font-semibold mb-2">Seu carrinho está vazio</h2>
            <p className="text-gray-600 mb-6">
              Adicione alguns produtos ao seu carrinho para continuar
            </p>
            <Button onClick={() => window.location.href = '/'}>
              Continuar Comprando
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Lista de Itens do Carrinho */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <ShoppingCart className="h-5 w-5 mr-2" />
                Carrinho de Compras ({cartItems.length} {cartItems.length === 1 ? 'item' : 'itens'})
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {cartItems.map((item, index) => (
                <div key={item.id}>
                  <div className="flex items-center space-x-4">
                    {/* Imagem do Produto */}
                    <div className="w-20 h-20 bg-gradient-to-br from-gray-100 to-gray-200 rounded-lg flex items-center justify-center">
                      <span className="text-2xl">📦</span>
                    </div>

                    {/* Informações do Produto */}
                    <div className="flex-1">
                      <h3 className="font-semibold text-lg">{item.name}</h3>
                      <p className="text-gray-600 text-sm">{item.department?.name}</p>
                      <div className="flex items-center mt-2">
                        <Badge variant="outline" className="text-xs">
                          Em estoque: {item.stock_quantity}
                        </Badge>
                      </div>
                    </div>

                    {/* Controles de Quantidade */}
                    <div className="flex items-center space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                        disabled={item.quantity <= 1}
                      >
                        <Minus className="h-4 w-4" />
                      </Button>
                      
                      <Input
                        type="number"
                        value={item.quantity}
                        onChange={(e) => handleQuantityChange(item.id, parseInt(e.target.value) || 1)}
                        className="w-16 text-center"
                        min="1"
                        max={item.stock_quantity}
                      />
                      
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
                        disabled={item.quantity >= item.stock_quantity}
                      >
                        <Plus className="h-4 w-4" />
                      </Button>
                    </div>

                    {/* Preço */}
                    <div className="text-right">
                      <div className="font-semibold text-lg">
                        R$ {(item.price * item.quantity).toFixed(2)}
                      </div>
                      <div className="text-sm text-gray-600">
                        R$ {item.price.toFixed(2)} cada
                      </div>
                    </div>

                    {/* Botão Remover */}
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => onRemoveItem(item.id)}
                      className="text-red-600 hover:text-red-700"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                  
                  {index < cartItems.length - 1 && <Separator className="mt-4" />}
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* Resumo do Pedido */}
        <div className="lg:col-span-1">
          <Card className="sticky top-4">
            <CardHeader>
              <CardTitle>Resumo do Pedido</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Cupom de Desconto */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Cupom de Desconto</label>
                <div className="flex space-x-2">
                  <Input
                    placeholder="Digite o cupom"
                    value={couponCode}
                    onChange={(e) => setCouponCode(e.target.value)}
                  />
                  <Button variant="outline" onClick={handleApplyCoupon}>
                    Aplicar
                  </Button>
                </div>
                {discount > 0 && (
                  <p className="text-sm text-green-600">
                    ✓ Cupom aplicado: -R$ {discount.toFixed(2)}
                  </p>
                )}
              </div>

              <Separator />

              {/* Cálculos */}
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>Subtotal</span>
                  <span>R$ {subtotal.toFixed(2)}</span>
                </div>
                
                <div className="flex justify-between">
                  <span>Frete</span>
                  <span className={shipping === 0 ? 'text-green-600' : ''}>
                    {shipping === 0 ? 'Grátis' : `R$ ${shipping.toFixed(2)}`}
                  </span>
                </div>
                
                <div className="flex justify-between">
                  <span>Impostos</span>
                  <span>R$ {tax.toFixed(2)}</span>
                </div>
                
                {discount > 0 && (
                  <div className="flex justify-between text-green-600">
                    <span>Desconto</span>
                    <span>-R$ {discount.toFixed(2)}</span>
                  </div>
                )}
              </div>

              <Separator />

              <div className="flex justify-between text-lg font-semibold">
                <span>Total</span>
                <span>R$ {total.toFixed(2)}</span>
              </div>

              {shipping === 0 && (
                <div className="text-sm text-green-600 text-center">
                  🎉 Você ganhou frete grátis!
                </div>
              )}

              {subtotal < 100 && (
                <div className="text-sm text-blue-600 text-center">
                  Adicione mais R$ {(100 - subtotal).toFixed(2)} para ganhar frete grátis
                </div>
              )}

              <Button 
                className="w-full" 
                size="lg"
                onClick={() => onCheckout(cartItems, total)}
              >
                <CreditCard className="h-4 w-4 mr-2" />
                Finalizar Compra
              </Button>

              <Button variant="outline" className="w-full">
                Continuar Comprando
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ShoppingCartComponent;
