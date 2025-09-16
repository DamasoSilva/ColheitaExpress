import React, { useState, useEffect, useRef } from 'react';
import { Search, Filter, X } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { Card, CardContent } from './ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';

const SearchBar = ({ onSearch, onFilter, departments = [], className = "" }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    department: '',
    minPrice: '',
    maxPrice: '',
    sortBy: 'name',
    inStock: false
  });
  
  const searchRef = useRef(null);
  const suggestionsRef = useRef(null);

  // Simulação de sugestões de busca
  const mockSuggestions = [
    'Smartphone Samsung Galaxy',
    'iPhone 15 Pro',
    'Notebook Dell Inspiron',
    'MacBook Air M2',
    'Fone de Ouvido Sony',
    'AirPods Pro',
    'Smart TV LG',
    'PlayStation 5',
    'Xbox Series X',
    'Nintendo Switch'
  ];

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        searchRef.current && 
        !searchRef.current.contains(event.target) &&
        suggestionsRef.current &&
        !suggestionsRef.current.contains(event.target)
      ) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    if (searchTerm.length > 2) {
      const filtered = mockSuggestions.filter(suggestion =>
        suggestion.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setSuggestions(filtered.slice(0, 5));
      setShowSuggestions(true);
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  }, [searchTerm]);

  const handleSearch = (term = searchTerm) => {
    if (term.trim()) {
      onSearch(term.trim());
      setShowSuggestions(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setSearchTerm(suggestion);
    handleSearch(suggestion);
  };

  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilter(newFilters);
  };

  const clearFilters = () => {
    const clearedFilters = {
      department: '',
      minPrice: '',
      maxPrice: '',
      sortBy: 'name',
      inStock: false
    };
    setFilters(clearedFilters);
    onFilter(clearedFilters);
  };

  const activeFiltersCount = Object.values(filters).filter(value => 
    value !== '' && value !== false && value !== 'name'
  ).length;

  return (
    <div className={`relative ${className}`}>
      {/* Barra de Busca Principal */}
      <div className="relative" ref={searchRef}>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
          <Input
            type="text"
            placeholder="Buscar produtos..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            className="pl-10 pr-20 h-12 text-lg"
          />
          <div className="absolute right-2 top-1/2 transform -translate-y-1/2 flex gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowFilters(!showFilters)}
              className="relative"
            >
              <Filter className="h-4 w-4" />
              {activeFiltersCount > 0 && (
                <Badge 
                  variant="destructive" 
                  className="absolute -top-2 -right-2 h-5 w-5 p-0 flex items-center justify-center text-xs"
                >
                  {activeFiltersCount}
                </Badge>
              )}
            </Button>
            <Button onClick={() => handleSearch()} size="sm">
              Buscar
            </Button>
          </div>
        </div>

        {/* Sugestões de Busca */}
        {showSuggestions && suggestions.length > 0 && (
          <Card 
            ref={suggestionsRef}
            className="absolute top-full left-0 right-0 z-50 mt-1 shadow-lg"
          >
            <CardContent className="p-0">
              {suggestions.map((suggestion, index) => (
                <div
                  key={index}
                  className="px-4 py-3 hover:bg-gray-50 cursor-pointer border-b last:border-b-0 flex items-center"
                  onClick={() => handleSuggestionClick(suggestion)}
                >
                  <Search className="h-4 w-4 text-gray-400 mr-3" />
                  <span className="text-sm">{suggestion}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        )}
      </div>

      {/* Painel de Filtros */}
      {showFilters && (
        <Card className="mt-4 shadow-lg">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Filtros</h3>
              <div className="flex gap-2">
                <Button variant="outline" size="sm" onClick={clearFilters}>
                  Limpar Filtros
                </Button>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  onClick={() => setShowFilters(false)}
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Departamento */}
              <div>
                <label className="block text-sm font-medium mb-2">Departamento</label>
                <Select 
                  value={filters.department} 
                  onValueChange={(value) => handleFilterChange('department', value)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Todos os departamentos" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="">Todos os departamentos</SelectItem>
                    {departments.map((dept) => (
                      <SelectItem key={dept.id} value={dept.id.toString()}>
                        {dept.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Faixa de Preço */}
              <div>
                <label className="block text-sm font-medium mb-2">Preço Mínimo</label>
                <Input
                  type="number"
                  placeholder="R$ 0,00"
                  value={filters.minPrice}
                  onChange={(e) => handleFilterChange('minPrice', e.target.value)}
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Preço Máximo</label>
                <Input
                  type="number"
                  placeholder="R$ 999,99"
                  value={filters.maxPrice}
                  onChange={(e) => handleFilterChange('maxPrice', e.target.value)}
                />
              </div>

              {/* Ordenação */}
              <div>
                <label className="block text-sm font-medium mb-2">Ordenar por</label>
                <Select 
                  value={filters.sortBy} 
                  onValueChange={(value) => handleFilterChange('sortBy', value)}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="name">Nome A-Z</SelectItem>
                    <SelectItem value="-name">Nome Z-A</SelectItem>
                    <SelectItem value="price">Menor Preço</SelectItem>
                    <SelectItem value="-price">Maior Preço</SelectItem>
                    <SelectItem value="-created_at">Mais Recentes</SelectItem>
                    <SelectItem value="created_at">Mais Antigos</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Filtros Adicionais */}
            <div className="mt-4 flex flex-wrap gap-4">
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={filters.inStock}
                  onChange={(e) => handleFilterChange('inStock', e.target.checked)}
                  className="rounded border-gray-300"
                />
                <span className="text-sm">Apenas produtos em estoque</span>
              </label>
            </div>

            {/* Filtros Ativos */}
            {activeFiltersCount > 0 && (
              <div className="mt-4 pt-4 border-t">
                <h4 className="text-sm font-medium mb-2">Filtros Ativos:</h4>
                <div className="flex flex-wrap gap-2">
                  {filters.department && (
                    <Badge variant="secondary" className="flex items-center gap-1">
                      Departamento: {departments.find(d => d.id.toString() === filters.department)?.name}
                      <X 
                        className="h-3 w-3 cursor-pointer" 
                        onClick={() => handleFilterChange('department', '')}
                      />
                    </Badge>
                  )}
                  {filters.minPrice && (
                    <Badge variant="secondary" className="flex items-center gap-1">
                      Min: R$ {filters.minPrice}
                      <X 
                        className="h-3 w-3 cursor-pointer" 
                        onClick={() => handleFilterChange('minPrice', '')}
                      />
                    </Badge>
                  )}
                  {filters.maxPrice && (
                    <Badge variant="secondary" className="flex items-center gap-1">
                      Max: R$ {filters.maxPrice}
                      <X 
                        className="h-3 w-3 cursor-pointer" 
                        onClick={() => handleFilterChange('maxPrice', '')}
                      />
                    </Badge>
                  )}
                  {filters.inStock && (
                    <Badge variant="secondary" className="flex items-center gap-1">
                      Em estoque
                      <X 
                        className="h-3 w-3 cursor-pointer" 
                        onClick={() => handleFilterChange('inStock', false)}
                      />
                    </Badge>
                  )}
                  {filters.sortBy !== 'name' && (
                    <Badge variant="secondary" className="flex items-center gap-1">
                      Ordenação: {filters.sortBy}
                      <X 
                        className="h-3 w-3 cursor-pointer" 
                        onClick={() => handleFilterChange('sortBy', 'name')}
                      />
                    </Badge>
                  )}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default SearchBar;

