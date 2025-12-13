/**
 * API Integration for Boss Shop
 * Connects frontend with Django SQLite database
 */

// API Configuration
const API_CONFIG = {
    BASE_URL: 'http://localhost:8000/api',
    ENDPOINTS: {
        HEALTH: '/health/',
        CATEGORIES: '/categories/',
        PRODUCTS: '/products/',
        ORDERS: '/orders/',
        LOGIN: '/login/',
        REGISTER: '/register/',
        PROFILE: '/profile/'
    }
};

// API Helper Class
class BossShopAPI {
    constructor() {
        this.baseURL = API_CONFIG.BASE_URL;
        this.token = localStorage.getItem('authToken');
    }

    // Get authentication headers
    getHeaders(includeAuth = false) {
        const headers = {
            'Content-Type': 'application/json',
        };

        if (includeAuth && this.token) {
            headers['Authorization'] = `Token ${this.token}`;
        }

        return headers;
    }

    // Generic API request method
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: this.getHeaders(options.auth),
            ...options
        };

        try {
            console.log(`🌐 API Request: ${options.method || 'GET'} ${url}`);
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            console.log(`✅ API Response:`, data);
            return { success: true, data };
        } catch (error) {
            console.error(`❌ API Error:`, error);
            return { success: false, error: error.message };
        }
    }

    // Health Check
    async checkHealth() {
        return await this.request(API_CONFIG.ENDPOINTS.HEALTH);
    }

    // Categories
    async getCategories() {
        return await this.request(API_CONFIG.ENDPOINTS.CATEGORIES);
    }

    // Products
    async getProducts(categorySlug = null) {
        let endpoint = API_CONFIG.ENDPOINTS.PRODUCTS;
        if (categorySlug) {
            endpoint += `?category=${categorySlug}`;
        }
        return await this.request(endpoint);
    }

    async getProduct(id) {
        return await this.request(`${API_CONFIG.ENDPOINTS.PRODUCTS}${id}/`);
    }

    // Authentication
    async login(email, password) {
        return await this.request(API_CONFIG.ENDPOINTS.LOGIN, {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    }

    async register(userData) {
        return await this.request(API_CONFIG.ENDPOINTS.REGISTER, {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    // User Profile
    async getProfile() {
        return await this.request(API_CONFIG.ENDPOINTS.PROFILE, { auth: true });
    }

    async updateProfile(userData) {
        return await this.request(API_CONFIG.ENDPOINTS.PROFILE, {
            method: 'PUT',
            auth: true,
            body: JSON.stringify(userData)
        });
    }

    // Orders
    async getOrders() {
        return await this.request(API_CONFIG.ENDPOINTS.ORDERS, { auth: true });
    }

    async createOrder(orderData) {
        return await this.request(API_CONFIG.ENDPOINTS.ORDERS, {
            method: 'POST',
            auth: true,
            body: JSON.stringify(orderData)
        });
    }
}

// Global API instance
const api = new BossShopAPI();

// Database Status Checker
class DatabaseStatus {
    constructor() {
        this.statusElement = null;
        this.init();
    }

    init() {
        this.createStatusIndicator();
        this.checkStatus();
        // Check status every 30 seconds
        setInterval(() => this.checkStatus(), 30000);
    }

    createStatusIndicator() {
        // Create status indicator if it doesn't exist
        if (!document.getElementById('db-status')) {
            const statusDiv = document.createElement('div');
            statusDiv.id = 'db-status';
            statusDiv.style.cssText = `
                position: fixed;
                top: 10px;
                right: 10px;
                padding: 8px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
                z-index: 9999;
                transition: all 0.3s ease;
                cursor: pointer;
            `;
            document.body.appendChild(statusDiv);
            this.statusElement = statusDiv;

            // Click to show details
            statusDiv.addEventListener('click', () => this.showDetails());
        } else {
            this.statusElement = document.getElementById('db-status');
        }
    }

    async checkStatus() {
        const result = await api.checkHealth();
        
        if (result.success) {
            this.updateStatus('online', 'DB Online', '#4CAF50');
        } else {
            this.updateStatus('offline', 'DB Offline', '#f44336');
        }
    }

    updateStatus(status, text, color) {
        if (this.statusElement) {
            this.statusElement.textContent = `🗄️ ${text}`;
            this.statusElement.style.backgroundColor = color;
            this.statusElement.style.color = 'white';
            this.statusElement.dataset.status = status;
        }
    }

    showDetails() {
        const status = this.statusElement.dataset.status;
        const message = status === 'online' 
            ? 'Banco de dados SQLite conectado e funcionando!' 
            : 'Banco de dados não está respondendo. Verifique se o servidor Django está rodando.';
        
        alert(`Status do Banco de Dados:\n\n${message}\n\nEndpoint: ${API_CONFIG.BASE_URL}`);
    }
}

// Product Loader for Homepage
class ProductLoader {
    constructor() {
        this.loadedCategories = new Set();
    }

    async loadCategoryProducts(categorySlug, containerId) {
        if (this.loadedCategories.has(categorySlug)) {
            return; // Already loaded
        }

        const container = document.getElementById(containerId);
        if (!container) return;

        // Show loading
        this.showLoading(container);

        try {
            const result = await api.getProducts(categorySlug);
            
            if (result.success && result.data.length > 0) {
                this.renderProducts(result.data, container);
                this.loadedCategories.add(categorySlug);
                console.log(`✅ Loaded ${result.data.length} products for category: ${categorySlug}`);
            } else {
                this.showNoProducts(container);
            }
        } catch (error) {
            console.error(`Error loading products for ${categorySlug}:`, error);
            this.showError(container);
        }
    }

    showLoading(container) {
        container.innerHTML = `
            <div class="loading-products">
                <i class="fas fa-spinner fa-spin"></i>
                <p>Carregando produtos do banco de dados...</p>
            </div>
        `;
    }

    showNoProducts(container) {
        container.innerHTML = `
            <div class="no-products">
                <i class="fas fa-box-open"></i>
                <p>Nenhum produto encontrado nesta categoria.</p>
            </div>
        `;
    }

    showError(container) {
        container.innerHTML = `
            <div class="error-products">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Erro ao carregar produtos. Verifique a conexão com o banco de dados.</p>
            </div>
        `;
    }

    renderProducts(products, container) {
        const productsHTML = products.map(product => `
            <div class="product-card flash-product" data-product-id="${product.id}">
                <div class="product-image">
                    <img src="${product.image || 'https://via.placeholder.com/300x300?text=Produto'}" 
                         alt="${product.name}" class="product-img">
                    <button class="wishlist-btn"><i class="far fa-heart"></i></button>
                </div>
                <div class="product-info">
                    <div class="product-category">${product.category_name || 'Produto'}</div>
                    <h3>${product.name}</h3>
                    <div class="product-rating">
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="fas fa-star"></i>
                        <i class="far fa-star"></i>
                        <span>(${Math.floor(Math.random() * 200) + 50})</span>
                    </div>
                    <div class="product-price">
                        <span class="new-price">R$ ${parseFloat(product.price).toFixed(2).replace('.', ',')}</span>
                    </div>
                    <button class="add-to-cart-btn flash-btn" onclick="addToCartFromDB('${product.name}', ${product.price}, ${product.id})">
                        <i class="fas fa-shopping-cart"></i> Comprar Agora
                    </button>
                </div>
            </div>
        `).join('');

        container.innerHTML = `<div class="products-grid flash-products">${productsHTML}</div>`;
    }
}

// Enhanced cart function that works with database
function addToCartFromDB(productName, price, productId) {
    // Check if user is logged in
    const isLoggedIn = localStorage.getItem('authToken');
    
    if (!isLoggedIn) {
        showLoginModal();
        showNotification('Você precisa estar logado para adicionar produtos ao carrinho!', 'warning');
        return;
    }

    // Add to cart with database product ID
    const existingCart = JSON.parse(localStorage.getItem('cart') || '[]');
    const existingItem = existingCart.find(item => item.productId === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        existingCart.push({
            productId: productId,
            name: productName,
            price: price,
            quantity: 1
        });
    }
    
    localStorage.setItem('cart', JSON.stringify(existingCart));
    updateCartCount();
    showNotification(`${productName} adicionado ao carrinho!`, 'success');
    
    console.log(`🛒 Product added to cart from database: ID ${productId}`);
}

// Category Tab Handler
class CategoryTabs {
    constructor() {
        this.productLoader = new ProductLoader();
        this.init();
    }

    init() {
        // Add click handlers to category tabs
        document.addEventListener('click', (e) => {
            if (e.target.matches('.tab-btn')) {
                this.handleTabClick(e.target);
            }
        });

        // Load initial category (moda)
        setTimeout(() => {
            this.loadCategoryOnDemand('moda');
        }, 1000);
    }

    handleTabClick(tabBtn) {
        const category = tabBtn.dataset.category;
        if (category) {
            this.loadCategoryOnDemand(category);
        }
    }

    loadCategoryOnDemand(categorySlug) {
        const containerId = `${categorySlug}-content`;
        this.productLoader.loadCategoryProducts(categorySlug, containerId);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initializing Boss Shop API Integration...');
    
    // Initialize database status checker
    new DatabaseStatus();
    
    // Initialize category tabs and product loading
    new CategoryTabs();
    
    // Load categories for navigation
    loadCategories();
    
    console.log('✅ Boss Shop API Integration initialized!');
});

// Load categories for navigation menu
async function loadCategories() {
    const result = await api.getCategories();
    
    if (result.success) {
        console.log(`📂 Loaded ${result.data.length} categories from database`);
        // You can update navigation menu here if needed
    }
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        z-index: 10000;
        animation: slideInRight 0.3s ease;
    `;
    
    // Set background color based on type
    const colors = {
        success: '#4CAF50',
        error: '#f44336',
        warning: '#ff9800',
        info: '#2196F3'
    };
    
    notification.style.backgroundColor = colors[type] || colors.info;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .loading-products, .no-products, .error-products {
        text-align: center;
        padding: 40px 20px;
        color: #666;
    }
    
    .loading-products i {
        font-size: 2rem;
        color: #ff6b35;
        margin-bottom: 10px;
    }
    
    .no-products i, .error-products i {
        font-size: 3rem;
        margin-bottom: 15px;
        opacity: 0.5;
    }
`;
document.head.appendChild(style);

// Export API instance for global use
window.BossShopAPI = api;