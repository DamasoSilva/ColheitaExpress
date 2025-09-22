// Configuração da API para conectar frontend ao backend
const API_BASE_URL = 'http://localhost:8000/api';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Produtos
  async getProducts(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    const endpoint = `/products/${queryString ? `?${queryString}` : ''}`;
    return this.request(endpoint);
  }

  async getProduct(slug) {
    return this.request(`/products/${slug}/`);
  }

  async getFeaturedProducts() {
    return this.request('/products/?is_featured=true');
  }

  // Departamentos
  async getDepartments() {
    return this.request('/departments/');
  }

  async getDepartment(id) {
    return this.request(`/departments/${id}/`);
  }

  // Busca
  async searchProducts(query, filters = {}) {
    const params = {
      search: query,
      ...filters,
    };
    return this.getProducts(params);
  }
}

export default new ApiService();

