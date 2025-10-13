/**
 * Búsqueda Avanzada en Tiempo Real
 * Sistema de gestión de plazos judiciales
 */

class AdvancedSearch {
    constructor() {
        this.searchInput = document.getElementById('busqueda-input');
        this.searchForm = document.getElementById('filtro-form');
        this.resultsContainer = document.getElementById('search-results');
        this.searchHistory = this.loadSearchHistory();
        this.debounceTimer = null;
        this.minSearchLength = 2;
        
        this.init();
    }
    
    init() {
        if (!this.searchInput) return;
        
        // Búsqueda en tiempo real con debounce
        this.searchInput.addEventListener('input', (e) => {
            this.handleSearchInput(e);
        });
        
        // Búsqueda al presionar Enter
        this.searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.performSearch();
            }
        });
        
        // Mostrar historial al hacer focus
        this.searchInput.addEventListener('focus', () => {
            this.showSearchHistory();
        });
        
        // Ocultar historial al hacer blur
        this.searchInput.addEventListener('blur', () => {
            setTimeout(() => this.hideSearchHistory(), 200);
        });
        
        // Inicializar tooltips
        this.initTooltips();
        
        // Configurar atajos de teclado
        this.setupKeyboardShortcuts();
    }
    
    handleSearchInput(e) {
        const query = e.target.value.trim();
        
        // Limpiar timer anterior
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }
        
        // Si la búsqueda es muy corta, limpiar resultados
        if (query.length < this.minSearchLength) {
            this.clearSearchResults();
            return;
        }
        
        // Debounce: esperar 300ms antes de buscar
        this.debounceTimer = setTimeout(() => {
            this.performSearch();
        }, 300);
    }
    
    async performSearch() {
        const query = this.searchInput.value.trim();
        
        if (query.length < this.minSearchLength) {
            this.clearSearchResults();
            return;
        }
        
        try {
            // Mostrar indicador de carga
            this.showLoadingIndicator();
            
            // Realizar búsqueda AJAX
            const response = await fetch(`/calendario/?busqueda=${encodeURIComponent(query)}&ajax=1`);
            const data = await response.json();
            
            // Procesar resultados
            this.displaySearchResults(data);
            
            // Guardar en historial
            this.saveToHistory(query);
            
        } catch (error) {
            console.error('Error en búsqueda:', error);
            this.showError('Error al realizar la búsqueda');
        } finally {
            this.hideLoadingIndicator();
        }
    }
    
    displaySearchResults(data) {
        if (!this.resultsContainer) return;
        
        if (data.results && data.results.length > 0) {
            this.resultsContainer.innerHTML = this.buildResultsHTML(data.results, data.query);
            this.resultsContainer.style.display = 'block';
        } else {
            this.resultsContainer.innerHTML = `
                <div class="search-no-results">
                    <i class="bi bi-search"></i>
                    <p>No se encontraron resultados para "${data.query}"</p>
                </div>
            `;
            this.resultsContainer.style.display = 'block';
        }
    }
    
    buildResultsHTML(results, query) {
        let html = `<div class="search-results-header">
            <h6><i class="bi bi-search"></i> Resultados para "${query}" (${results.length})</h6>
        </div>`;
        
        results.forEach(plazo => {
            html += `
                <div class="search-result-item" data-plazo-id="${plazo.id}">
                    <div class="result-main">
                        <h6 class="result-title">${this.highlightText(plazo.tipo_documento, query)}</h6>
                        <p class="result-subtitle">${plazo.procedimiento}</p>
                    </div>
                    <div class="result-details">
                        <span class="badge badge-${this.getEstadoClass(plazo.estado)}">${plazo.estado}</span>
                        <small class="text-muted">Vence: ${plazo.fecha_vencimiento}</small>
                    </div>
                    <div class="result-actions">
                        <a href="/plazo/${plazo.id}/" class="btn btn-sm btn-outline-primary">
                            <i class="bi bi-eye"></i> Ver
                        </a>
                    </div>
                </div>
            `;
        });
        
        return html;
    }
    
    highlightText(text, query) {
        if (!query) return text;
        
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }
    
    getEstadoClass(estado) {
        const classes = {
            'corriendo': 'success',
            'vencido': 'danger',
            'pendiente': 'warning',
            'suspendido': 'secondary',
            'esperando proveído': 'info'
        };
        return classes[estado] || 'secondary';
    }
    
    clearSearchResults() {
        if (this.resultsContainer) {
            this.resultsContainer.style.display = 'none';
            this.resultsContainer.innerHTML = '';
        }
    }
    
    showLoadingIndicator() {
        if (this.resultsContainer) {
            this.resultsContainer.innerHTML = `
                <div class="search-loading">
                    <div class="spinner-border spinner-border-sm" role="status">
                        <span class="visually-hidden">Buscando...</span>
                    </div>
                    <span>Buscando...</span>
                </div>
            `;
            this.resultsContainer.style.display = 'block';
        }
    }
    
    hideLoadingIndicator() {
        // El indicador se reemplaza con los resultados
    }
    
    showError(message) {
        if (this.resultsContainer) {
            this.resultsContainer.innerHTML = `
                <div class="search-error">
                    <i class="bi bi-exclamation-triangle"></i>
                    <p>${message}</p>
                </div>
            `;
            this.resultsContainer.style.display = 'block';
        }
    }
    
    // Historial de búsquedas
    loadSearchHistory() {
        try {
            return JSON.parse(localStorage.getItem('searchHistory') || '[]');
        } catch {
            return [];
        }
    }
    
    saveToHistory(query) {
        if (!query || query.length < 2) return;
        
        // Remover duplicados
        this.searchHistory = this.searchHistory.filter(item => item !== query);
        
        // Agregar al inicio
        this.searchHistory.unshift(query);
        
        // Limitar a 10 elementos
        this.searchHistory = this.searchHistory.slice(0, 10);
        
        // Guardar en localStorage
        localStorage.setItem('searchHistory', JSON.stringify(this.searchHistory));
    }
    
    showSearchHistory() {
        if (this.searchHistory.length === 0) return;
        
        if (!this.resultsContainer) return;
        
        let html = '<div class="search-history"><h6><i class="bi bi-clock-history"></i> Búsquedas recientes</h6>';
        
        this.searchHistory.forEach(query => {
            html += `
                <div class="history-item" onclick="this.selectHistoryItem('${query}')">
                    <i class="bi bi-search"></i>
                    <span>${query}</span>
                </div>
            `;
        });
        
        html += '</div>';
        
        this.resultsContainer.innerHTML = html;
        this.resultsContainer.style.display = 'block';
    }
    
    hideSearchHistory() {
        // Se oculta automáticamente al hacer blur
    }
    
    selectHistoryItem(query) {
        this.searchInput.value = query;
        this.performSearch();
    }
    
    initTooltips() {
        // Inicializar tooltips de Bootstrap
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl + K para enfocar búsqueda
            if (e.ctrlKey && e.key === 'k') {
                e.preventDefault();
                this.searchInput.focus();
            }
            
            // Escape para limpiar búsqueda
            if (e.key === 'Escape') {
                this.searchInput.value = '';
                this.clearSearchResults();
            }
        });
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new AdvancedSearch();
});

// Función global para seleccionar del historial
window.selectHistoryItem = function(query) {
    const searchInput = document.getElementById('busqueda-input');
    if (searchInput) {
        searchInput.value = query;
        // Disparar evento de búsqueda
        searchInput.dispatchEvent(new Event('input'));
    }
};
