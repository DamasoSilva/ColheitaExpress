import React, { useState, useEffect } from 'react';
import { Star, ThumbsUp, ThumbsDown, Flag, User, CheckCircle } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Textarea } from './ui/textarea';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Progress } from './ui/progress';
import { Separator } from './ui/separator';

const StarRating = ({ rating, onRatingChange, readonly = false, size = "md" }) => {
  const [hoverRating, setHoverRating] = useState(0);
  
  const sizeClasses = {
    sm: "h-4 w-4",
    md: "h-5 w-5",
    lg: "h-6 w-6"
  };

  return (
    <div className="flex items-center gap-1">
      {[1, 2, 3, 4, 5].map((star) => (
        <Star
          key={star}
          className={`${sizeClasses[size]} cursor-pointer transition-colors ${
            star <= (hoverRating || rating)
              ? 'text-yellow-400 fill-current'
              : 'text-gray-300'
          }`}
          onMouseEnter={() => !readonly && setHoverRating(star)}
          onMouseLeave={() => !readonly && setHoverRating(0)}
          onClick={() => !readonly && onRatingChange && onRatingChange(star)}
        />
      ))}
    </div>
  );
};

const ReviewForm = ({ productId, onSubmit, onCancel }) => {
  const [rating, setRating] = useState(0);
  const [title, setTitle] = useState('');
  const [comment, setComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (rating === 0) {
      alert('Por favor, selecione uma avaliação');
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit({
        product: productId,
        rating,
        title: title.trim(),
        comment: comment.trim()
      });
      
      // Reset form
      setRating(0);
      setTitle('');
      setComment('');
    } catch (error) {
      console.error('Erro ao enviar avaliação:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Escrever Avaliação</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">
              Sua Avaliação *
            </label>
            <StarRating rating={rating} onRatingChange={setRating} size="lg" />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Título da Avaliação
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Resumo da sua experiência"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              maxLength={100}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Comentário
            </label>
            <Textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Conte sobre sua experiência com este produto..."
              rows={4}
              maxLength={500}
            />
            <div className="text-xs text-gray-500 mt-1">
              {comment.length}/500 caracteres
            </div>
          </div>

          <div className="flex gap-2">
            <Button 
              type="submit" 
              disabled={isSubmitting || rating === 0}
              className="flex-1"
            >
              {isSubmitting ? 'Enviando...' : 'Enviar Avaliação'}
            </Button>
            <Button 
              type="button" 
              variant="outline" 
              onClick={onCancel}
              disabled={isSubmitting}
            >
              Cancelar
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
};

const ReviewItem = ({ review, onHelpful, onReport }) => {
  const [isHelpful, setIsHelpful] = useState(false);
  const [helpfulCount, setHelpfulCount] = useState(review.helpful_count || 0);

  const handleHelpful = async () => {
    try {
      await onHelpful(review.id);
      setIsHelpful(!isHelpful);
      setHelpfulCount(prev => isHelpful ? prev - 1 : prev + 1);
    } catch (error) {
      console.error('Erro ao marcar como útil:', error);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <Card className="mb-4">
      <CardContent className="pt-6">
        <div className="flex items-start gap-4">
          <Avatar>
            <AvatarImage src={review.user?.avatar} />
            <AvatarFallback>
              <User className="h-4 w-4" />
            </AvatarFallback>
          </Avatar>

          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className="font-medium">
                {review.user?.name || 'Usuário Anônimo'}
              </span>
              {review.verified_purchase && (
                <Badge variant="secondary" className="text-xs">
                  <CheckCircle className="h-3 w-3 mr-1" />
                  Compra Verificada
                </Badge>
              )}
            </div>

            <div className="flex items-center gap-2 mb-2">
              <StarRating rating={review.rating} readonly size="sm" />
              <span className="text-sm text-gray-600">
                {formatDate(review.created_at)}
              </span>
            </div>

            {review.title && (
              <h4 className="font-medium mb-2">{review.title}</h4>
            )}

            {review.comment && (
              <p className="text-gray-700 mb-3">{review.comment}</p>
            )}

            <div className="flex items-center gap-4 text-sm">
              <button
                onClick={handleHelpful}
                className={`flex items-center gap-1 hover:text-primary transition-colors ${
                  isHelpful ? 'text-primary' : 'text-gray-600'
                }`}
              >
                <ThumbsUp className="h-4 w-4" />
                Útil ({helpfulCount})
              </button>

              <button
                onClick={() => onReport(review.id)}
                className="flex items-center gap-1 text-gray-600 hover:text-red-600 transition-colors"
              >
                <Flag className="h-4 w-4" />
                Denunciar
              </button>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

const ReviewSummary = ({ reviews }) => {
  const totalReviews = reviews.length;
  const averageRating = totalReviews > 0 
    ? reviews.reduce((sum, review) => sum + review.rating, 0) / totalReviews 
    : 0;

  const ratingDistribution = [5, 4, 3, 2, 1].map(rating => {
    const count = reviews.filter(review => review.rating === rating).length;
    const percentage = totalReviews > 0 ? (count / totalReviews) * 100 : 0;
    return { rating, count, percentage };
  });

  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle>Avaliações dos Clientes</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Resumo Geral */}
          <div className="text-center">
            <div className="text-4xl font-bold text-primary mb-2">
              {averageRating.toFixed(1)}
            </div>
            <StarRating rating={Math.round(averageRating)} readonly size="lg" />
            <div className="text-sm text-gray-600 mt-2">
              Baseado em {totalReviews} avaliações
            </div>
          </div>

          {/* Distribuição de Estrelas */}
          <div className="space-y-2">
            {ratingDistribution.map(({ rating, count, percentage }) => (
              <div key={rating} className="flex items-center gap-2">
                <span className="text-sm w-8">{rating}★</span>
                <Progress value={percentage} className="flex-1" />
                <span className="text-sm text-gray-600 w-8">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

const ReviewSystem = ({ productId, userCanReview = false }) => {
  const [reviews, setReviews] = useState([]);
  const [showReviewForm, setShowReviewForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState('newest');

  useEffect(() => {
    fetchReviews();
  }, [productId, sortBy]);

  const fetchReviews = async () => {
    try {
      setLoading(true);
      
      // Simulação de dados de avaliações
      const mockReviews = [
        {
          id: 1,
          user: { name: 'João Silva', avatar: null },
          rating: 5,
          title: 'Excelente produto!',
          comment: 'Superou minhas expectativas. Qualidade excepcional e entrega rápida.',
          created_at: '2024-09-10T10:00:00Z',
          verified_purchase: true,
          helpful_count: 12
        },
        {
          id: 2,
          user: { name: 'Maria Santos', avatar: null },
          rating: 4,
          title: 'Muito bom',
          comment: 'Produto de boa qualidade, apenas o preço que poderia ser melhor.',
          created_at: '2024-09-08T15:30:00Z',
          verified_purchase: true,
          helpful_count: 8
        },
        {
          id: 3,
          user: { name: 'Pedro Costa', avatar: null },
          rating: 5,
          title: 'Recomendo!',
          comment: 'Já é o segundo que compro. Qualidade consistente.',
          created_at: '2024-09-05T09:15:00Z',
          verified_purchase: true,
          helpful_count: 5
        }
      ];

      setReviews(mockReviews);
    } catch (error) {
      console.error('Erro ao buscar avaliações:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitReview = async (reviewData) => {
    try {
      // Simular envio da avaliação
      const newReview = {
        id: Date.now(),
        user: { name: 'Você', avatar: null },
        ...reviewData,
        created_at: new Date().toISOString(),
        verified_purchase: true,
        helpful_count: 0
      };

      setReviews(prev => [newReview, ...prev]);
      setShowReviewForm(false);
    } catch (error) {
      console.error('Erro ao enviar avaliação:', error);
      throw error;
    }
  };

  const handleHelpful = async (reviewId) => {
    // Implementar lógica de marcar como útil
    console.log('Marcar como útil:', reviewId);
  };

  const handleReport = async (reviewId) => {
    // Implementar lógica de denúncia
    console.log('Denunciar avaliação:', reviewId);
    alert('Avaliação denunciada. Obrigado pelo feedback!');
  };

  if (loading) {
    return <div className="text-center py-8">Carregando avaliações...</div>;
  }

  return (
    <div className="space-y-6">
      <ReviewSummary reviews={reviews} />

      {/* Botão para Escrever Avaliação */}
      {userCanReview && !showReviewForm && (
        <div className="text-center">
          <Button onClick={() => setShowReviewForm(true)}>
            Escrever Avaliação
          </Button>
        </div>
      )}

      {/* Formulário de Avaliação */}
      {showReviewForm && (
        <ReviewForm
          productId={productId}
          onSubmit={handleSubmitReview}
          onCancel={() => setShowReviewForm(false)}
        />
      )}

      {/* Filtros e Ordenação */}
      {reviews.length > 0 && (
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">
            Avaliações ({reviews.length})
          </h3>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md text-sm"
          >
            <option value="newest">Mais Recentes</option>
            <option value="oldest">Mais Antigas</option>
            <option value="highest">Maior Avaliação</option>
            <option value="lowest">Menor Avaliação</option>
            <option value="helpful">Mais Úteis</option>
          </select>
        </div>
      )}

      <Separator />

      {/* Lista de Avaliações */}
      <div>
        {reviews.length > 0 ? (
          reviews.map((review) => (
            <ReviewItem
              key={review.id}
              review={review}
              onHelpful={handleHelpful}
              onReport={handleReport}
            />
          ))
        ) : (
          <div className="text-center py-8 text-gray-500">
            Ainda não há avaliações para este produto.
            {userCanReview && (
              <div className="mt-2">
                <Button 
                  variant="outline" 
                  onClick={() => setShowReviewForm(true)}
                >
                  Seja o primeiro a avaliar!
                </Button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ReviewSystem;

