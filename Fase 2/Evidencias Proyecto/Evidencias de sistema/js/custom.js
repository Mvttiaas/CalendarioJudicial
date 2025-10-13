// JavaScript personalizado para Calendario Judicial

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar popovers de Bootstrap
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts después de 5 segundos
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Validación de RUT chileno en tiempo real
    var rutInputs = document.querySelectorAll('input[name="rut_causa"]');
    rutInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            formatRUT(e.target);
        });
    });

    // Confirmación para acciones destructivas
    var deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            var message = this.getAttribute('data-confirm') || '¿Está seguro de que desea realizar esta acción?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Auto-submit de formularios de filtro
    var filterSelects = document.querySelectorAll('select[name="tipo_documento"], select[name="procedimiento"], select[name="estado"]');
    filterSelects.forEach(function(select) {
        select.addEventListener('change', function() {
            this.form.submit();
        });
    });

    // Actualizar estados automáticamente cada 5 minutos
    setInterval(updatePlazoStates, 300000); // 5 minutos

    // Efectos de hover en cards
    var cards = document.querySelectorAll('.card-stat');
    cards.forEach(function(card) {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});

// Función para formatear RUT chileno
function formatRUT(input) {
    let value = input.value.replace(/[^0-9kK]/g, '');
    
    if (value.length > 1) {
        let rutNumber = value.slice(0, -1);
        let dv = value.slice(-1);
        
        // Formatear número con puntos
        let formattedNumber = rutNumber.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        
        input.value = formattedNumber + '-' + dv;
    }
}

// Función para validar RUT chileno
function validateRUT(rut) {
    if (!rut || rut.length < 2) return false;
    
    let cleanRUT = rut.replace(/[^0-9kK]/g, '');
    if (cleanRUT.length < 2) return false;
    
    let number = cleanRUT.slice(0, -1);
    let dv = cleanRUT.slice(-1).toUpperCase();
    
    // Calcular dígito verificador
    let sum = 0;
    let multiplier = 2;
    
    for (let i = number.length - 1; i >= 0; i--) {
        sum += parseInt(number[i]) * multiplier;
        multiplier = multiplier === 7 ? 2 : multiplier + 1;
    }
    
    let remainder = sum % 11;
    let calculatedDV = 11 - remainder;
    
    if (calculatedDV === 11) calculatedDV = '0';
    else if (calculatedDV === 10) calculatedDV = 'K';
    else calculatedDV = calculatedDV.toString();
    
    return dv === calculatedDV;
}

// Función para actualizar estados de plazos
function updatePlazoStates() {
    fetch('/api/actualizar-estados/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.actualizados > 0) {
            console.log(`Estados actualizados: ${data.actualizados} plazos`);
            showNotification(`Se actualizaron ${data.actualizados} plazos`, 'info');
        }
    })
    .catch(error => {
        console.error('Error actualizando estados:', error);
    });
}

// Función para obtener el token CSRF
function getCSRFToken() {
    var token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    var alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove después de 3 segundos
    setTimeout(function() {
        var bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 3000);
}

// Función para confirmar eliminación
function confirmarEliminacion(mensaje) {
    return confirm(mensaje || '¿Está seguro de que desea eliminar este plazo?');
}

// Función para calcular fecha de vencimiento (simulación)
function calcularFechaVencimiento(fechaInicio, diasPlazo, tipoDia) {
    // Esta es una simulación básica
    // En producción, esto debería hacerse en el servidor
    var fecha = new Date(fechaInicio);
    fecha.setDate(fecha.getDate() + parseInt(diasPlazo));
    
    return fecha.toISOString().split('T')[0];
}

// Función para exportar datos
function exportarDatos(formato) {
    var url = formato === 'pdf' ? '/exportar/pdf/' : '/exportar/ics/';
    var params = new URLSearchParams(window.location.search);
    
    if (params.toString()) {
        url += '?' + params.toString();
    }
    
    window.location.href = url;
}

// Función para filtrar tabla en tiempo real
function filtrarTabla(inputId, columnIndex) {
    var input = document.getElementById(inputId);
    var table = document.querySelector('table');
    var rows = table.querySelectorAll('tbody tr');
    
    var filter = input.value.toLowerCase();
    
    rows.forEach(function(row) {
        var cell = row.cells[columnIndex];
        if (cell) {
            var text = cell.textContent.toLowerCase();
            row.style.display = text.includes(filter) ? '' : 'none';
        }
    });
}

// Función para ordenar tabla
function ordenarTabla(columnIndex) {
    var table = document.querySelector('table');
    var tbody = table.querySelector('tbody');
    var rows = Array.from(tbody.querySelectorAll('tr'));
    
    var isAscending = table.getAttribute('data-sort-direction') !== 'asc';
    
    rows.sort(function(a, b) {
        var aText = a.cells[columnIndex].textContent.trim();
        var bText = b.cells[columnIndex].textContent.trim();
        
        if (isAscending) {
            return aText.localeCompare(bText);
        } else {
            return bText.localeCompare(aText);
        }
    });
    
    rows.forEach(function(row) {
        tbody.appendChild(row);
    });
    
    table.setAttribute('data-sort-direction', isAscending ? 'asc' : 'desc');
}

// Función para mostrar/ocultar columnas
function toggleColumn(columnIndex) {
    var table = document.querySelector('table');
    var rows = table.querySelectorAll('tr');
    
    rows.forEach(function(row) {
        var cell = row.cells[columnIndex];
        if (cell) {
            cell.style.display = cell.style.display === 'none' ? '' : 'none';
        }
    });
}

// Función para imprimir página
function imprimirPagina() {
    window.print();
}

// Función para copiar al portapapeles
function copiarAlPortapapeles(texto) {
    navigator.clipboard.writeText(texto).then(function() {
        showNotification('Copiado al portapapeles', 'success');
    }).catch(function(err) {
        console.error('Error copiando al portapapeles:', err);
        showNotification('Error al copiar', 'danger');
    });
}

// Función para generar QR (si se implementa)
function generarQR(texto) {
    // Implementar generación de QR si es necesario
    console.log('Generando QR para:', texto);
}

// Función para validar formulario antes de enviar
function validarFormulario(formId) {
    var form = document.getElementById(formId);
    if (!form) return true;
    
    var inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    var isValid = true;
    
    inputs.forEach(function(input) {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Función para mostrar loading
function mostrarLoading(elemento) {
    var loading = document.createElement('div');
    loading.className = 'spinner-border spinner-border-sm me-2';
    loading.setAttribute('role', 'status');
    loading.innerHTML = '<span class="visually-hidden">Cargando...</span>';
    
    elemento.prepend(loading);
    elemento.disabled = true;
}

// Función para ocultar loading
function ocultarLoading(elemento) {
    var loading = elemento.querySelector('.spinner-border');
    if (loading) {
        loading.remove();
    }
    elemento.disabled = false;
}
