import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Separator } from './ui/separator';
import { RadioGroup, RadioGroupItem } from './ui/radio-group';
import { Checkbox } from './ui/checkbox';
import { CreditCard, Truck, MapPin, User, Phone, Mail, Lock } from 'lucide-react';

const Checkout = ({ cartItems, total, onOrderComplete }) => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    // Dados pessoais
    fullName: '',
    email: '',
    phone: '',
    cpf: '',
    
    // Endereço de entrega
    zipCode: '',
    street: '',
    number: '',
    complement: '',
    neighborhood: '',
    city: '',
    state: '',
    
    // Pagamento
    paymentMethod: 'credit_card',
    cardNumber: '',
    cardName: '',
    cardExpiry: '',
    cardCvv: '',
    installments: '1',
    
    // Observações
    notes: ''
  });

  const [loading, setLoading] = useState(false);
  const [acceptTerms, setAcceptTerms] = useState(false);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmitOrder = async () => {
    if (!acceptTerms) {
      alert('Você deve aceitar os termos e condições');
      return;
    }

    setLoading(true);
    
    try {
      // Simular processamento do pedido
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const orderData = {
        items: cartItems,
        total: total,
        customer: formData,
        orderNumber: `PED-${Date.now()}`,
        status: 'confirmed'
      };
      
      onOrderComplete(orderData);
    } catch (error) {
      console.error('Erro ao processar pedido:', error);
      alert('Erro ao processar pedido. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const renderStep1 = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4 flex items-center">
          <User className="h-5 w-5 mr-2" />
          Dados Pessoais
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="fullName">Nome Completo *</Label>
            <Input
              id="fullName"
              value={formData.fullName}
              onChange={(e) => handleInputChange('fullName', e.target.value)}
              placeholder="Seu nome completo"
              required
            />
          </div>
          <div>
            <Label htmlFor="email">E-mail *</Label>
            <Input
              id="email"
              type="email"
              value={formData.email}
              onChange={(e) => handleInputChange('email', e.target.value)}
              placeholder="seu@email.com"
              required
            />
          </div>
          <div>
            <Label htmlFor="phone">Telefone *</Label>
            <Input
              id="phone"
              value={formData.phone}
              onChange={(e) => handleInputChange('phone', e.target.value)}
              placeholder="(11) 99999-9999"
              required
            />
          </div>
          <div>
            <Label htmlFor="cpf">CPF *</Label>
            <Input
              id="cpf"
              value={formData.cpf}
              onChange={(e) => handleInputChange('cpf', e.target.value)}
              placeholder="000.000.000-00"
              required
            />
          </div>
        </div>
      </div>

      <Separator />

      <div>
        <h3 className="text-lg font-semibold mb-4 flex items-center">
          <MapPin className="h-5 w-5 mr-2" />
          Endereço de Entrega
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="zipCode">CEP *</Label>
            <Input
              id="zipCode"
              value={formData.zipCode}
              onChange={(e) => handleInputChange('zipCode', e.target.value)}
              placeholder="00000-000"
              required
            />
          </div>
          <div>
            <Label htmlFor="street">Rua *</Label>
            <Input
              id="street"
              value={formData.street}
              onChange={(e) => handleInputChange('street', e.target.value)}
              placeholder="Nome da rua"
              required
            />
          </div>
          <div>
            <Label htmlFor="number">Número *</Label>
            <Input
              id="number"
              value={formData.number}
              onChange={(e) => handleInputChange('number', e.target.value)}
              placeholder="123"
              required
            />
          </div>
          <div>
            <Label htmlFor="complement">Complemento</Label>
            <Input
              id="complement"
              value={formData.complement}
              onChange={(e) => handleInputChange('complement', e.target.value)}
              placeholder="Apto, bloco, etc."
            />
          </div>
          <div>
            <Label htmlFor="neighborhood">Bairro *</Label>
            <Input
              id="neighborhood"
              value={formData.neighborhood}
              onChange={(e) => handleInputChange('neighborhood', e.target.value)}
              placeholder="Nome do bairro"
              required
            />
          </div>
          <div>
            <Label htmlFor="city">Cidade *</Label>
            <Input
              id="city"
              value={formData.city}
              onChange={(e) => handleInputChange('city', e.target.value)}
              placeholder="Nome da cidade"
              required
            />
          </div>
          <div>
            <Label htmlFor="state">Estado *</Label>
            <Input
              id="state"
              value={formData.state}
              onChange={(e) => handleInputChange('state', e.target.value)}
              placeholder="SP"
              required
            />
          </div>
        </div>
      </div>
    </div>
  );

  const renderStep2 = () => (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold mb-4 flex items-center">
          <CreditCard className="h-5 w-5 mr-2" />
          Forma de Pagamento
        </h3>
        
        <RadioGroup 
          value={formData.paymentMethod} 
          onValueChange={(value) => handleInputChange('paymentMethod', value)}
          className="space-y-4"
        >
          <div className="flex items-center space-x-2 p-4 border rounded-lg">
            <RadioGroupItem value="credit_card" id="credit_card" />
            <Label htmlFor="credit_card" className="flex-1">
              <div className="flex items-center">
                <CreditCard className="h-4 w-4 mr-2" />
                Cartão de Crédito
              </div>
              <p className="text-sm text-gray-600">Visa, Mastercard, Elo</p>
            </Label>
          </div>
          
          <div className="flex items-center space-x-2 p-4 border rounded-lg">
            <RadioGroupItem value="pix" id="pix" />
            <Label htmlFor="pix" className="flex-1">
              <div className="flex items-center">
                <span className="text-lg mr-2">🏦</span>
                PIX
              </div>
              <p className="text-sm text-gray-600">Pagamento instantâneo</p>
            </Label>
          </div>
          
          <div className="flex items-center space-x-2 p-4 border rounded-lg">
            <RadioGroupItem value="boleto" id="boleto" />
            <Label htmlFor="boleto" className="flex-1">
              <div className="flex items-center">
                <span className="text-lg mr-2">📄</span>
                Boleto Bancário
              </div>
              <p className="text-sm text-gray-600">Vencimento em 3 dias úteis</p>
            </Label>
          </div>
        </RadioGroup>

        {formData.paymentMethod === 'credit_card' && (
          <div className="mt-6 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <Label htmlFor="cardNumber">Número do Cartão *</Label>
                <Input
                  id="cardNumber"
                  value={formData.cardNumber}
                  onChange={(e) => handleInputChange('cardNumber', e.target.value)}
                  placeholder="0000 0000 0000 0000"
                  required
                />
              </div>
              <div>
                <Label htmlFor="cardName">Nome no Cartão *</Label>
                <Input
                  id="cardName"
                  value={formData.cardName}
                  onChange={(e) => handleInputChange('cardName', e.target.value)}
                  placeholder="Nome como está no cartão"
                  required
                />
              </div>
              <div>
                <Label htmlFor="cardExpiry">Validade *</Label>
                <Input
                  id="cardExpiry"
                  value={formData.cardExpiry}
                  onChange={(e) => handleInputChange('cardExpiry', e.target.value)}
                  placeholder="MM/AA"
                  required
                />
              </div>
              <div>
                <Label htmlFor="cardCvv">CVV *</Label>
                <Input
                  id="cardCvv"
                  value={formData.cardCvv}
                  onChange={(e) => handleInputChange('cardCvv', e.target.value)}
                  placeholder="123"
                  required
                />
              </div>
              <div>
                <Label htmlFor="installments">Parcelas</Label>
                <select 
                  id="installments"
                  value={formData.installments}
                  onChange={(e) => handleInputChange('installments', e.target.value)}
                  className="w-full p-2 border rounded-md"
                >
                  <option value="1">1x de R$ {total.toFixed(2)} (à vista)</option>
                  <option value="2">2x de R$ {(total / 2).toFixed(2)}</option>
                  <option value="3">3x de R$ {(total / 3).toFixed(2)}</option>
                  <option value="6">6x de R$ {(total / 6).toFixed(2)}</option>
                  <option value="12">12x de R$ {(total / 12).toFixed(2)}</option>
                </select>
              </div>
            </div>
          </div>
        )}
      </div>

      <Separator />

      <div>
        <Label htmlFor="notes">Observações (opcional)</Label>
        <textarea
          id="notes"
          value={formData.notes}
          onChange={(e) => handleInputChange('notes', e.target.value)}
          placeholder="Alguma observação sobre a entrega..."
          className="w-full p-2 border rounded-md h-20 resize-none"
        />
      </div>
    </div>
  );

  const renderStep3 = () => (
    <div className="space-y-6">
      <h3 className="text-lg font-semibold mb-4">Revisão do Pedido</h3>
      
      {/* Resumo dos Produtos */}
      <Card>
        <CardHeader>
          <CardTitle>Produtos</CardTitle>
        </CardHeader>
        <CardContent>
          {cartItems.map(item => (
            <div key={item.id} className="flex justify-between items-center py-2">
              <div>
                <span className="font-medium">{item.name}</span>
                <span className="text-gray-600 ml-2">x{item.quantity}</span>
              </div>
              <span>R$ {(item.price * item.quantity).toFixed(2)}</span>
            </div>
          ))}
          <Separator className="my-4" />
          <div className="flex justify-between font-semibold text-lg">
            <span>Total</span>
            <span>R$ {total.toFixed(2)}</span>
          </div>
        </CardContent>
      </Card>

      {/* Dados de Entrega */}
      <Card>
        <CardHeader>
          <CardTitle>Entrega</CardTitle>
        </CardHeader>
        <CardContent>
          <p><strong>{formData.fullName}</strong></p>
          <p>{formData.street}, {formData.number}</p>
          {formData.complement && <p>{formData.complement}</p>}
          <p>{formData.neighborhood}, {formData.city} - {formData.state}</p>
          <p>CEP: {formData.zipCode}</p>
        </CardContent>
      </Card>

      {/* Forma de Pagamento */}
      <Card>
        <CardHeader>
          <CardTitle>Pagamento</CardTitle>
        </CardHeader>
        <CardContent>
          {formData.paymentMethod === 'credit_card' && (
            <p>Cartão de Crédito - {formData.installments}x</p>
          )}
          {formData.paymentMethod === 'pix' && <p>PIX</p>}
          {formData.paymentMethod === 'boleto' && <p>Boleto Bancário</p>}
        </CardContent>
      </Card>

      {/* Termos e Condições */}
      <div className="flex items-center space-x-2">
        <Checkbox 
          id="terms" 
          checked={acceptTerms}
          onCheckedChange={setAcceptTerms}
        />
        <Label htmlFor="terms" className="text-sm">
          Aceito os <a href="#" className="text-blue-600 underline">termos e condições</a> e a <a href="#" className="text-blue-600 underline">política de privacidade</a>
        </Label>
      </div>
    </div>
  );

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        {/* Progress Steps */}
        <div className="flex items-center justify-center mb-8">
          <div className="flex items-center space-x-4">
            <div className={`flex items-center justify-center w-8 h-8 rounded-full ${step >= 1 ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>
              1
            </div>
            <div className={`w-16 h-1 ${step >= 2 ? 'bg-blue-600' : 'bg-gray-200'}`}></div>
            <div className={`flex items-center justify-center w-8 h-8 rounded-full ${step >= 2 ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>
              2
            </div>
            <div className={`w-16 h-1 ${step >= 3 ? 'bg-blue-600' : 'bg-gray-200'}`}></div>
            <div className={`flex items-center justify-center w-8 h-8 rounded-full ${step >= 3 ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>
              3
            </div>
          </div>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>
              {step === 1 && 'Dados de Entrega'}
              {step === 2 && 'Pagamento'}
              {step === 3 && 'Confirmação'}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {step === 1 && renderStep1()}
            {step === 2 && renderStep2()}
            {step === 3 && renderStep3()}

            <div className="flex justify-between mt-8">
              {step > 1 && (
                <Button variant="outline" onClick={() => setStep(step - 1)}>
                  Voltar
                </Button>
              )}
              
              {step < 3 ? (
                <Button 
                  onClick={() => setStep(step + 1)}
                  className="ml-auto"
                >
                  Continuar
                </Button>
              ) : (
                <Button 
                  onClick={handleSubmitOrder}
                  disabled={loading || !acceptTerms}
                  className="ml-auto"
                >
                  {loading ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Processando...
                    </>
                  ) : (
                    <>
                      <Lock className="h-4 w-4 mr-2" />
                      Finalizar Pedido
                    </>
                  )}
                </Button>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Checkout;
