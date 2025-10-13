// Sistema de Temas y Mejoras de Interfaz

class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        this.createThemeToggle();
        this.applyTheme(this.currentTheme);
        this.setupKeyboardShortcuts();
        this.setupAnimations();
        this.setupFormElements();
        this.setupDragAndDrop();
    }

    createThemeToggle() {
        // Usar el botón que ya existe en el HTML
        const toggle = document.getElementById('theme-toggle');
        if (toggle) {
            toggle.addEventListener('click', () => {
                this.toggleTheme();
            });
        }
    }

    toggleTheme() {
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(this.currentTheme);
        localStorage.setItem('theme', this.currentTheme);
        
        // Actualizar icono del botón
        const toggle = document.getElementById('theme-toggle');
        const icon = document.getElementById('theme-icon');
        if (toggle && icon) {
            if (this.currentTheme === 'dark') {
                icon.className = 'bi bi-sun-fill';
                toggle.title = 'Cambiar a modo claro';
            } else {
                icon.className = 'bi bi-moon-fill';
                toggle.title = 'Cambiar a modo oscuro';
            }
        }
    }

    applyTheme(theme) {
        // Aplicar transición suave
        document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
        
        // Aplicar tema
        document.documentElement.setAttribute('data-theme', theme);
        
        // Actualizar meta theme-color
        const metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (metaThemeColor) {
            metaThemeColor.content = theme === 'dark' ? '#0d1117' : '#ffffff';
        }
        
        // Actualizar icono del botón de tema
        const toggle = document.getElementById('theme-toggle');
        const icon = document.getElementById('theme-icon');
        if (toggle && icon) {
            if (theme === 'dark') {
                icon.className = 'bi bi-sun-fill';
                toggle.title = 'Cambiar a modo claro';
            } else {
                icon.className = 'bi bi-moon-fill';
                toggle.title = 'Cambiar a modo oscuro';
            }
        }
        
        // Actualizar iconos y elementos específicos
        this.updateThemeElements(theme);
        
        // Remover transición después de aplicar
        setTimeout(() => {
            document.body.style.transition = '';
        }, 300);
    }

    updateThemeElements(theme) {
        // Actualizar iconos de Bootstrap si existen
        const icons = document.querySelectorAll('.bi');
        icons.forEach(icon => {
            if (theme === 'dark') {
                icon.style.color = 'var(--color-text-primary)';
            } else {
                icon.style.color = '';
            }
        });

        // Actualizar elementos específicos que podrían no heredar el tema
        const elementsToUpdate = document.querySelectorAll('.card, .table, .form-control, .form-select, .btn-outline-primary, .btn-outline-secondary');
        elementsToUpdate.forEach(element => {
            element.style.transition = 'all 0.3s ease';
        });
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl + T para cambiar tema
            if (e.ctrlKey && e.key === 't') {
                e.preventDefault();
                this.toggleTheme();
            }
            
            // Ctrl + K para búsqueda rápida
            if (e.ctrlKey && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.querySelector('#busqueda-input');
                if (searchInput) {
                    searchInput.focus();
                    searchInput.select();
                }
            }
        });
    }

    setupAnimations() {
        // Animación de entrada para elementos (solo cards y botones)
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        });

        // Solo observar cards y botones, sin alertas
        document.querySelectorAll('.card, .btn').forEach(el => {
            observer.observe(el);
        });
    }

    setupFormElements() {
        // Solo manejar elementos de formulario específicos, no dropdowns de navegación
        const formSelects = document.querySelectorAll('form .form-select');
        formSelects.forEach(select => {
            // Prevenir interferencia con eventos de dropdown
            select.addEventListener('mousedown', function(e) {
                e.stopPropagation();
            });
            
            select.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        });
    }

    setupDragAndDrop() {
        // Implementar drag and drop básico para elementos
        const draggableElements = document.querySelectorAll('[draggable="true"]');
        
        draggableElements.forEach(element => {
            element.addEventListener('dragstart', (e) => {
                e.target.classList.add('dragging');
                e.dataTransfer.effectAllowed = 'move';
                e.dataTransfer.setData('text/html', e.target.outerHTML);
            });

            element.addEventListener('dragend', (e) => {
                e.target.classList.remove('dragging');
            });
        });

        // Drop zones
        const dropZones = document.querySelectorAll('.drop-zone');
        dropZones.forEach(zone => {
            zone.addEventListener('dragover', (e) => {
                e.preventDefault();
                zone.classList.add('drag-over');
            });

            zone.addEventListener('dragleave', () => {
                zone.classList.remove('drag-over');
            });

            zone.addEventListener('drop', (e) => {
                e.preventDefault();
                zone.classList.remove('drag-over');
                // Aquí se puede implementar la lógica de drop
            });
        });
    }
}

// Utilidades de interfaz
class UIUtils {
    static showNotification(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 1060; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        // Auto-remove después de la duración
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, duration);
    }

    static showLoading(element, show = true) {
        if (show) {
            element.classList.add('loading');
            const spinner = document.createElement('div');
            spinner.className = 'spinner';
            spinner.id = 'loading-spinner';
            element.appendChild(spinner);
        } else {
            element.classList.remove('loading');
            const spinner = document.getElementById('loading-spinner');
            if (spinner) {
                spinner.remove();
            }
        }
    }

    static formatRUT(input) {
        let value = input.value.replace(/[^0-9kK]/g, '');
        if (value.length > 1) {
            value = value.slice(0, -1).replace(/\B(?=(\d{3})+(?!\d))/g, '.') + '-' + value.slice(-1);
        }
        input.value = value;
    }

    static setupTooltips() {
        // Inicializar tooltips de Bootstrap
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    static setupPopovers() {
        // Inicializar popovers de Bootstrap
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }
}

// Mejoras de accesibilidad
class AccessibilityEnhancer {
    constructor() {
        this.setupFocusManagement();
        this.setupKeyboardNavigation();
        this.setupScreenReaderSupport();
    }

    setupFocusManagement() {
        // Mejorar navegación con teclado
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });
    }

    setupKeyboardNavigation() {
        // Navegación con flechas en listas
        const lists = document.querySelectorAll('.list-group, .table tbody');
        lists.forEach(list => {
            list.addEventListener('keydown', (e) => {
                const items = Array.from(list.querySelectorAll('a, button, [tabindex="0"]'));
                const currentIndex = items.indexOf(document.activeElement);
                
                if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    const nextIndex = (currentIndex + 1) % items.length;
                    items[nextIndex].focus();
                } else if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    const prevIndex = currentIndex === 0 ? items.length - 1 : currentIndex - 1;
                    items[prevIndex].focus();
                }
            });
        });
    }

    setupScreenReaderSupport() {
        // Agregar labels para screen readers
        const buttons = document.querySelectorAll('button:not([aria-label]):not([title])');
        buttons.forEach(button => {
            if (!button.textContent.trim()) {
                button.setAttribute('aria-label', 'Botón');
            }
        });
    }
}

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar gestor de temas
    window.themeManager = new ThemeManager();
    
    // Inicializar utilidades de interfaz
    window.uiUtils = UIUtils;
    
    // Inicializar mejoras de accesibilidad
    window.accessibilityEnhancer = new AccessibilityEnhancer();
    
    // Configurar tooltips y popovers
    UIUtils.setupTooltips();
    UIUtils.setupPopovers();
    
    // Configurar validación de RUT en tiempo real
    document.querySelectorAll('input[pattern*="rut"], input[name*="rut"]').forEach(input => {
        input.addEventListener('input', () => {
            UIUtils.formatRUT(input);
        });
    });
    
    // Notificación de bienvenida removida - las teclas rápidas están disponibles pero no se anuncian
});

// Exportar para uso global
window.ThemeManager = ThemeManager;
window.UIUtils = UIUtils;
window.AccessibilityEnhancer = AccessibilityEnhancer;
