// grafico de prestmaos del cliente
document.addEventListener('DOMContentLoaded', () => {
    const prestamoSelect = document.getElementById('prestamo-select');
    const graficoTotalPagado = document.getElementById('grafico-total-pagado');
    let chart = null; // Variable para almacenar la instancia del gráfico

    prestamoSelect.addEventListener('change', function () {
        const prestamoId = this.value;

        // Verificar si se seleccionó un préstamo válido
        if (!prestamoId) {
            graficoTotalPagado.innerHTML = '<p>No hay préstamos disponibles.</p>';
            return;
        }

        // Hacer una solicitud AJAX a la API
        fetch(`/api/prestamos/${prestamoId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al obtener los datos del préstamo');
                }
                return response.json();
            })
            .then(data => {
                // Destruir el gráfico anterior si existe
                if (chart) {
                    chart.destroy();
                }

                // Crear un canvas para el gráfico
                const ctx = document.createElement('canvas');
                graficoTotalPagado.innerHTML = ''; // Limpiar el contenido anterior
                graficoTotalPagado.appendChild(ctx); // Agregar el canvas al div

                // Crear el gráfico circular con Chart.js
                chart = new Chart(ctx, {
                    type: 'pie',  // Tipo de gráfico circular
                    data: {
                        labels: ['Monto Pagado', 'Monto Pendiente'],  // Etiquetas
                        datasets: [{
                            label: 'Monto',
                            data: [data.monto_pago, data.monto_a_pagar],  // Datos
                            backgroundColor: ['#36A2EB', '#FF6384'],  // Colores
                            borderColor: ['#36A2EB', '#FF6384'],  // Bordes
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,  // Evita que el gráfico se ajuste automáticamente
                        plugins: {
                            legend: {
                                position: 'top',  // Posición de la leyenda
                            },
                            title: {
                                display: true,
                                text: `Préstamo ${prestamoId} - Monto Total: $${data.monto_prestamo}`  // Título del gráfico
                            }
                        }
                    }
                });
            })
            .catch(error => {
                console.error('Error:', error);
                graficoTotalPagado.innerHTML = '<p>Error al cargar los datos del préstamo.</p>';
            });
    });

    // Cargar datos iniciales para el primer préstamo (opcional)
    if (prestamoSelect.value) {
        prestamoSelect.dispatchEvent(new Event('change'));
    }
});

// Grafico de Volumen del cliente
// Obtener el contexto del canvas
const ctx = document.getElementById('volumenChart').getContext('2d');

// Datos para el gráfico
const volumenData = {
    labels: ['Volumen de Préstamos', 'Monto a Pagar', 'Interes'],
    datasets: [{
        label: 'Distribución del Volumen',
        data: [
            {{ balance_total }},          // Volumen de préstamos
            {{ total_monto_a_pagar }},
            {{ tasa_interes_total }}     // Monto a pagar
        ],
        backgroundColor: [
            '#36A2EB',  // Color para Volumen de Préstamos
            '#FF6384'   // Color para Monto a Pagar
        ],
        hoverOffset: 4
    }]
};

// Crear el gráfico circular
const volumenChart = new Chart(ctx, {
    type: 'pie',  // Tipo de gráfico circular
    data: volumenData,
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Distribución del Volumen de Préstamos'
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        let label = context.label || '';
                        if (label) {
                            label += ': ';
                        }
                        label += '$' + context.raw.toLocaleString();  // Formato de moneda
                        return label;
                    }
                }
            }
        }
    }
});

// paginacion de las tablas
// tabla-pago
document.addEventListener('DOMContentLoaded', () => {
    const filasPorPagina = 6; // Número de filas por página
    const tablaBody = document.getElementById('pago-tbody');
    const filas = tablaBody.getElementsByTagName('tr');
    const paginacion = document.getElementById('paginacion');

    // Función para mostrar una página específica
    function mostrarPagina(pagina) {
        // Ocultar todas las filas
        for (let i = 0; i < filas.length; i++) {
            filas[i].style.display = 'none';
        }

        // Mostrar solo las filas de la página actual
        const inicio = (pagina - 1) * filasPorPagina;
        const fin = inicio + filasPorPagina;
        for (let i = inicio; i < fin && i < filas.length; i++) {
            if (filas[i].cells.length === 5) { // Actualizar la condición para ignorar la fila "No hay pagos registrados."
                filas[i].style.display = '';
            }
        }
    }

    // Función para generar los botones de paginación
    function generarBotonesPaginacion() {
        // Ignorar la fila "No hay pagos registrados."
        const filasReales = filas.length - 1;
        const totalPaginas = Math.ceil(filasReales / filasPorPagina); // Calcular el número de páginas
        paginacion.innerHTML = ''; // Limpiar los botones anteriores

        for (let i = 1; i <= totalPaginas; i++) {
            const enlace = document.createElement('a');
            enlace.textContent = i;
            enlace.href = '#'; // Establecer el atributo href para que se comporte como un enlace
            enlace.addEventListener('click', (e) => {
                e.preventDefault(); // Evitar que el enlace recargue la página
                cambiarPagina(i);
            });
            paginacion.appendChild(enlace);
        }
    }

    // Función para cambiar de página
    function cambiarPagina(pagina) {
        mostrarPagina(pagina);
    }

    // Generar los botones de paginación y mostrar la primera página
    generarBotonesPaginacion();
    mostrarPagina(1);
});

// tabla prestamos
document.addEventListener('DOMContentLoaded', () => {
    const filasPorPagina = 6; // Número de filas por página
    const tablaBody = document.getElementById('prestamos-tbody');
    const filas = tablaBody.getElementsByTagName('tr');
    const paginacion = document.getElementById('prestamos-paginacion');

    // Función para mostrar una página específica
    function mostrarPagina(pagina) {
        // Ocultar todas las filas
        for (let i = 0; i < filas.length; i++) {
            filas[i].style.display = 'none';
        }

        // Mostrar solo las filas de la página actual
        const inicio = (pagina - 1) * filasPorPagina;
        const fin = inicio + filasPorPagina;
        for (let i = inicio; i < fin && i < filas.length; i++) {
            if (filas[i].cells.length === 6) { // Ignorar la fila "No hay pagos registrados."
                filas[i].style.display = '';
            }
        }
    }

    // Función para generar los botones de paginación
    function generarBotonesPaginacion() {
        const totalPaginas = Math.ceil(filas.length / filasPorPagina); // Calcular el número de páginas
        paginacion.innerHTML = ''; // Limpiar los botones anteriores

        for (let i = 1; i <= totalPaginas; i++) {
            const enlace = document.createElement('a');
            enlace.textContent = i;
            enlace.href = '#'; // Establecer el atributo href para que se comporte como un enlace
            enlace.addEventListener('click', (e) => {
                e.preventDefault(); // Evitar que el enlace recargue la página
                cambiarPagina(i);
            });
            paginacion.appendChild(enlace);
        }
    }

    // Función para cambiar de página
    function cambiarPagina(pagina) {
        mostrarPagina(pagina);
    }

    // Generar los botones de paginación y mostrar la primera página
    generarBotonesPaginacion();
    mostrarPagina(1);
});