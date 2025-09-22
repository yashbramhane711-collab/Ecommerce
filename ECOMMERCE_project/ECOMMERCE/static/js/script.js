// E-Commerce Store JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Cart quantity validation
    const quantityInputs = document.querySelectorAll('input[name="quantity"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const max = parseInt(this.getAttribute('max'));
            const min = parseInt(this.getAttribute('min'));
            let value = parseInt(this.value);
            
            if (isNaN(value)) {
                this.value = min;
            } else if (value > max) {
                this.value = max;
                showToast('Maximum quantity available is ' + max, 'warning');
            } else if (value < min) {
                this.value = min;
            }
        });
    });

    // Add to cart animation
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const productName = this.getAttribute('data-product-name');
            showToast(productName + ' added to cart!', 'success');
            
            // Add animation to cart icon
            const cartIcon = document.querySelector('.bi-cart');
            if (cartIcon) {
                cartIcon.classList.add('cart-animate');
                setTimeout(() => {
                    cartIcon.classList.remove('cart-animate');
                }, 1000);
            }
        });
    });

    // Search functionality
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchTerm = this.querySelector('input[name="q"]').value.trim();
            if (searchTerm === '') {
                e.preventDefault();
                showToast('Please enter a search term', 'warning');
            }
        });
    }

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Price filter
    const priceFilter = document.getElementById('priceFilter');
    if (priceFilter) {
        priceFilter.addEventListener('input', function() {
            document.getElementById('priceValue').textContent = '$' + this.value;
            filterProducts();
        });
    }

    // Category filter
    const categoryFilters = document.querySelectorAll('.category-filter');
    categoryFilters.forEach(filter => {
        filter.addEventListener('change', filterProducts);
    });

    // Toast notification function
    function showToast(message, type = 'info') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        // Add to container
        const toastContainer = document.getElementById('toastContainer') || createToastContainer();
        toastContainer.appendChild(toast);
        
        // Initialize and show toast
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove toast after it's hidden
        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    }

    function createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
        return container;
    }

    function filterProducts() {
        // This would be implemented for client-side filtering
        console.log('Filtering products...');
    }

    // Lazy loading for images
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.getAttribute('data-src');
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add to wishlist functionality
    const wishlistButtons = document.querySelectorAll('.wishlist-btn');
    wishlistButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.classList.toggle('active');
            const productId = this.getAttribute('data-product-id');
            const isActive = this.classList.contains('active');
            
            // Here you would typically make an API call to update the wishlist
            showToast(isActive ? 'Added to wishlist' : 'Removed from wishlist', 'info');
        });
    });

    // Stock level indicators
    function updateStockIndicators() {
        const stockElements = document.querySelectorAll('[data-stock]');
        stockElements.forEach(element => {
            const stock = parseInt(element.getAttribute('data-stock'));
            if (stock < 5) {
                element.classList.add('text-danger');
                element.classList.add('fw-bold');
            } else if (stock < 10) {
                element.classList.add('text-warning');
            }
        });
    }

    updateStockIndicators();
});

// Cart counter animation
const cartCounter = {
    increment: function() {
        const counter = document.querySelector('.cart-count');
        if (counter) {
            counter.classList.add('count-up');
            setTimeout(() => {
                counter.classList.remove('count-up');
            }, 300);
        }
    },
    
    decrement: function() {
        const counter = document.querySelector('.cart-count');
        if (counter) {
            counter.classList.add('count-down');
            setTimeout(() => {
                counter.classList.remove('count-down');
            }, 300);
        }
    }
};

// Currency formatter
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}