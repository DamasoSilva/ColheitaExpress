import React, { useState, useEffect, useRef } from 'react';
import { Bell, X, Check, Info, AlertTriangle, AlertCircle, Package, Truck, CreditCard } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { ScrollArea } from './ui/scroll-area';
import { Separator } from './ui/separator';

const NotificationIcon = ({ type }) => {
  const iconProps = { className: "h-4 w-4" };
  
  switch (type) {
    case 'order':
      return <Package {...iconProps} className="h-4 w-4 text-blue-600" />;
    case 'delivery':
      return <Truck {...iconProps} className="h-4 w-4 text-green-600" />;
    case 'payment':
      return <CreditCard {...iconProps} className="h-4 w-4 text-purple-600" />;
    case 'success':
      return <Check {...iconProps} className="h-4 w-4 text-green-600" />;
    case 'warning':
      return <AlertTriangle {...iconProps} className="h-4 w-4 text-yellow-600" />;
    case 'error':
      return <AlertCircle {...iconProps} className="h-4 w-4 text-red-600" />;
    default:
      return <Info {...iconProps} className="h-4 w-4 text-blue-600" />;
  }
};

const NotificationItem = ({ notification, onMarkAsRead, onRemove }) => {
  const formatTime = (timestamp) => {
    const now = new Date();
    const notificationTime = new Date(timestamp);
    const diffInMinutes = Math.floor((now - notificationTime) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Agora';
    if (diffInMinutes < 60) return `${diffInMinutes}m atrás`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h atrás`;
    return `${Math.floor(diffInMinutes / 1440)}d atrás`;
  };

  const getTypeColor = (type) => {
    switch (type) {
      case 'order': return 'bg-blue-50 border-blue-200';
      case 'delivery': return 'bg-green-50 border-green-200';
      case 'payment': return 'bg-purple-50 border-purple-200';
      case 'success': return 'bg-green-50 border-green-200';
      case 'warning': return 'bg-yellow-50 border-yellow-200';
      case 'error': return 'bg-red-50 border-red-200';
      default: return 'bg-gray-50 border-gray-200';
    }
  };

  return (
    <div 
      className={`p-4 border rounded-lg transition-all hover:shadow-sm ${
        notification.read ? 'bg-white' : getTypeColor(notification.type)
      }`}
    >
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 mt-1">
          <NotificationIcon type={notification.type} />
        </div>
        
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h4 className={`text-sm font-medium ${!notification.read ? 'font-semibold' : ''}`}>
                {notification.title}
              </h4>
              <p className="text-sm text-gray-600 mt-1">
                {notification.message}
              </p>
              <div className="flex items-center gap-2 mt-2">
                <span className="text-xs text-gray-500">
                  {formatTime(notification.timestamp)}
                </span>
                {!notification.read && (
                  <Badge variant="secondary" className="text-xs">
                    Nova
                  </Badge>
                )}
              </div>
            </div>
            
            <div className="flex items-center gap-1 ml-2">
              {!notification.read && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onMarkAsRead(notification.id)}
                  className="h-6 w-6 p-0"
                >
                  <Check className="h-3 w-3" />
                </Button>
              )}
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onRemove(notification.id)}
                className="h-6 w-6 p-0 text-gray-400 hover:text-red-600"
              >
                <X className="h-3 w-3" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const NotificationCenter = ({ isOpen, onClose, notifications, onMarkAsRead, onRemove, onMarkAllAsRead }) => {
  const unreadCount = notifications.filter(n => !n.read).length;

  if (!isOpen) return null;

  return (
    <Card className="absolute top-full right-0 mt-2 w-96 max-w-[90vw] shadow-lg z-50">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">Notificações</CardTitle>
          <div className="flex items-center gap-2">
            {unreadCount > 0 && (
              <Button
                variant="ghost"
                size="sm"
                onClick={onMarkAllAsRead}
                className="text-xs"
              >
                Marcar todas como lidas
              </Button>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={onClose}
              className="h-6 w-6 p-0"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>
        {unreadCount > 0 && (
          <p className="text-sm text-gray-600">
            {unreadCount} notificação{unreadCount !== 1 ? 'ões' : ''} não lida{unreadCount !== 1 ? 's' : ''}
          </p>
        )}
      </CardHeader>
      
      <Separator />
      
      <CardContent className="p-0">
        <ScrollArea className="h-96">
          {notifications.length > 0 ? (
            <div className="p-4 space-y-3">
              {notifications.map((notification) => (
                <NotificationItem
                  key={notification.id}
                  notification={notification}
                  onMarkAsRead={onMarkAsRead}
                  onRemove={onRemove}
                />
              ))}
            </div>
          ) : (
            <div className="p-8 text-center text-gray-500">
              <Bell className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>Nenhuma notificação</p>
            </div>
          )}
        </ScrollArea>
      </CardContent>
    </Card>
  );
};

const NotificationSystem = () => {
  const [notifications, setNotifications] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const notificationRef = useRef(null);

  useEffect(() => {
    // Simular notificações iniciais
    const mockNotifications = [
      {
        id: 1,
        type: 'order',
        title: 'Pedido Confirmado',
        message: 'Seu pedido #12345 foi confirmado e está sendo preparado.',
        timestamp: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
        read: false
      },
      {
        id: 2,
        type: 'delivery',
        title: 'Produto Enviado',
        message: 'Seu pedido #12344 foi enviado e chegará em 2 dias úteis.',
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        read: false
      },
      {
        id: 3,
        type: 'payment',
        title: 'Pagamento Aprovado',
        message: 'O pagamento do pedido #12343 foi aprovado com sucesso.',
        timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
        read: true
      }
    ];

    setNotifications(mockNotifications);

    // Simular novas notificações periodicamente
    const interval = setInterval(() => {
      const newNotification = {
        id: Date.now(),
        type: ['order', 'delivery', 'payment', 'success'][Math.floor(Math.random() * 4)],
        title: 'Nova Notificação',
        message: 'Esta é uma notificação de teste gerada automaticamente.',
        timestamp: new Date().toISOString(),
        read: false
      };

      setNotifications(prev => [newNotification, ...prev.slice(0, 9)]); // Manter apenas 10 notificações
    }, 30000); // Nova notificação a cada 30 segundos

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (notificationRef.current && !notificationRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const unreadCount = notifications.filter(n => !n.read).length;

  const handleMarkAsRead = (notificationId) => {
    setNotifications(prev =>
      prev.map(notification =>
        notification.id === notificationId
          ? { ...notification, read: true }
          : notification
      )
    );
  };

  const handleRemove = (notificationId) => {
    setNotifications(prev =>
      prev.filter(notification => notification.id !== notificationId)
    );
  };

  const handleMarkAllAsRead = () => {
    setNotifications(prev =>
      prev.map(notification => ({ ...notification, read: true }))
    );
  };

  const addNotification = (notification) => {
    const newNotification = {
      id: Date.now(),
      timestamp: new Date().toISOString(),
      read: false,
      ...notification
    };

    setNotifications(prev => [newNotification, ...prev]);
  };

  return (
    <div className="relative" ref={notificationRef}>
      <Button
        variant="ghost"
        size="sm"
        onClick={() => setIsOpen(!isOpen)}
        className="relative"
      >
        <Bell className="h-4 w-4" />
        {unreadCount > 0 && (
          <Badge 
            variant="destructive" 
            className="absolute -top-2 -right-2 h-5 w-5 p-0 flex items-center justify-center text-xs"
          >
            {unreadCount > 9 ? '9+' : unreadCount}
          </Badge>
        )}
      </Button>

      <NotificationCenter
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        notifications={notifications}
        onMarkAsRead={handleMarkAsRead}
        onRemove={handleRemove}
        onMarkAllAsRead={handleMarkAllAsRead}
      />
    </div>
  );
};

// Hook para usar o sistema de notificações
export const useNotifications = () => {
  const addNotification = (notification) => {
    // Esta função seria conectada ao contexto global de notificações
    console.log('Nova notificação:', notification);
  };

  return { addNotification };
};

export default NotificationSystem;

