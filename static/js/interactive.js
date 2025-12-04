/**
 * JavaScript interactivo para el BookStore
 * Incluye: eventos, efectos visuales, AJAX, validaciones
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeEffects();
    initializeDynamicSearch();
    initializeFormValidation();
});

/**
 * Efectos visuales: hover, transiciones, animaciones
 */
function initializeEffects() {
    // Efecto hover en enlaces de libros
    const bookLinks = document.querySelectorAll('a[href*="/books/"]');
    bookLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.color = '#d9534f';
            this.style.transition = 'all 0.3s ease';
            this.style.textDecoration = 'underline';
            this.style.fontWeight = 'bold';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.color = '';
            this.style.textDecoration = '';
            this.style.fontWeight = '';
        });
    });

    // Efecto hover en enlaces de editoriales
    const publisherLinks = document.querySelectorAll('a[href*="/publishers/"]');
    publisherLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.color = '#5cb85c';
            this.style.transition = 'all 0.3s ease';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.color = '';
        });
    });

    // Efecto de fade-in para imágenes
    const images = document.querySelectorAll('img.cover-book');
    images.forEach(img => {
        img.style.opacity = '0';
        img.style.transition = 'opacity 0.6s ease-in';
        
        img.addEventListener('load', function() {
            this.style.opacity = '1';
        });
        
        if (img.complete) {
            img.style.opacity = '1';
        }
    });
}

/**
 * Búsqueda dinámica con AJAX (sin recargar página)
 */
function initializeDynamicSearch() {
    const searchForm = document.querySelector('form');
    const searchInput = document.querySelector('input[name="search"]');
    
    if (!searchForm || !searchInput) return;

    // Búsqueda en tiempo real mientras escribes
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        
        // Mostrar indicador de carga
        const indicator = document.createElement('span');
        indicator.id = 'loading-indicator';
        indicator.textContent = ' (buscando...)';
        indicator.style.color = '#999';
        indicator.style.fontSize = '0.9em';
        
        if (!document.getElementById('loading-indicator')) {
            searchInput.parentNode.appendChild(indicator);
        }

        searchTimeout = setTimeout(() => {
            performAjaxSearch(this.value);
        }, 500);
    });
}

/**
 * Realiza búsqueda AJAX
 */
function performAjaxSearch(searchTerm) {
    const currentUrl = window.location.pathname;
    const params = new URLSearchParams();
    params.append('search', searchTerm);

    // Usar Fetch API para AJAX
    fetch(`${currentUrl}?${params.toString()}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        // Extraer solo la lista de resultados
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newContent = doc.querySelector('ul') || doc.querySelector('.detalle-contenido');
        
        if (newContent) {
            const currentContent = document.querySelector('ul') || document.querySelector('.detalle-contenido');
            if (currentContent) {
                // Efecto de fade-out y fade-in
                currentContent.style.opacity = '0.5';
                currentContent.style.transition = 'opacity 0.3s ease';
                
                setTimeout(() => {
                    currentContent.innerHTML = newContent.innerHTML;
                    currentContent.style.opacity = '1';
                }, 300);
            }
        }
        
        // Ocultar indicador
        const indicator = document.getElementById('loading-indicator');
        if (indicator) indicator.remove();
    })
    .catch(error => {
        console.error('Error en búsqueda AJAX:', error);
        const indicator = document.getElementById('loading-indicator');
        if (indicator) indicator.remove();
    });
}

/**
 * Validación de formularios en tiempo real
 */
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required], textarea[required]');
        
        inputs.forEach(input => {
            // Validar mientras escribes
            input.addEventListener('input', function() {
                validateField(this);
            });
            
            // Validar al perder foco
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });

        // Validar al enviar
        form.addEventListener('submit', function(e) {
            let isValid = true;
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Por favor, completa todos los campos requeridos', 'error');
            }
        });
    });
}

/**
 * Valida un campo individual
 */
function validateField(field) {
    let isValid = true;
    let message = '';

    // Validación de campo requerido
    if (field.hasAttribute('required') && !field.value.trim()) {
        isValid = false;
        message = 'Este campo es requerido';
    }
    
    // Validación de email
    if (field.type === 'email' && field.value.trim()) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(field.value)) {
            isValid = false;
            message = 'Email inválido';
        }
    }
    
    // Validación de número
    if (field.type === 'number' && field.value.trim()) {
        if (isNaN(field.value)) {
            isValid = false;
            message = 'Debe ser un número';
        }
    }

    // Mostrar feedback visual
    if (!isValid) {
        field.style.borderColor = '#d9534f';
        field.style.backgroundColor = '#fff5f5';
        showFieldError(field, message);
    } else {
        field.style.borderColor = '#5cb85c';
        field.style.backgroundColor = '#f5fff5';
        clearFieldError(field);
    }

    return isValid;
}

/**
 * Muestra error en un campo
 */
function showFieldError(field, message) {
    let errorDiv = field.nextElementSibling;
    
    if (!errorDiv || !errorDiv.classList.contains('field-error')) {
        errorDiv = document.createElement('small');
        errorDiv.className = 'field-error';
        errorDiv.style.color = '#d9534f';
        errorDiv.style.display = 'block';
        errorDiv.style.marginTop = '5px';
        field.parentNode.insertBefore(errorDiv, field.nextSibling);
    }
    
    errorDiv.textContent = message;
}

/**
 * Limpia error de un campo
 */
function clearFieldError(field) {
    const errorDiv = field.nextElementSibling;
    if (errorDiv && errorDiv.classList.contains('field-error')) {
        errorDiv.remove();
    }
}

/**
 * Muestra notificaciones al usuario
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 4px;
        font-size: 14px;
        z-index: 9999;
        animation: slideIn 0.3s ease;
        ${type === 'error' ? 'background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;' : 
          type === 'success' ? 'background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb;' :
          'background-color: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb;'}
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    // Auto-remover después de 4 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// Agregar animaciones CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
