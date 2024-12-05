let sortOrder = {};
document.addEventListener('DOMContentLoaded', () => {
    const filas = document.querySelectorAll('tr');
    const table = document.querySelector('table.table');
    const thElements = table.querySelectorAll('th');
    console.log(thElements)

    thElements.forEach((th) => {
        console.log('th', th)
        th.addEventListener('click', (event) => {
            event.preventDefault();
            const columnIndex = Array.prototype.indexOf.call(th.parentNode.children, th);
            const columnName = th.textContent.trim();
            // Toggle sort order
            if (!sortOrder[columnName]) {
            sortOrder[columnName] = 'asc';
            } else if (sortOrder[columnName] === 'asc') {
            sortOrder[columnName] = 'desc';
            } else if (sortOrder[columnName] === 'desc') {
            sortOrder[columnName] = 'both';
            }
            else {
                sortOrder[columnName] = 'asc';
            }
            // Update class
            th.className = th.className.replace(/sort-asc|sort-desc|sort-both/, `sort-${sortOrder[columnName]}`);

        // Call sortTable function
        sortTable(table, columnIndex, sortOrder[columnName]);
        });
    });

    function sortTable(table, columnIndex, sortOrder) {
        var rows = Array.prototype.slice.call(table.querySelectorAll('tbody tr'));
        rows.sort(function(rowA, rowB) {
            var cellA = rowA.cells[columnIndex].textContent;
            var cellB = rowB.cells[columnIndex].textContent;
            // Handle numerical values
            if (!isNaN(cellA) && !isNaN(cellB)) {
                return cellA - cellB;
            }
            // Default to string comparison
            return cellA.localeCompare(cellB);
        });
        // Sort order
        if (sortOrder === 'desc') {
            rows.reverse();
        }
        // Update the table
        rows.forEach(function(row) {
            table.querySelector('tbody').appendChild(row);
        });
    };

    filas.forEach(fila => {
        const productoId = fila.dataset.producto_id;
        const botonEditar = fila.querySelector(`#editar_${productoId}`);

      // boton borrar
        fila.querySelector('.delete-button').addEventListener('click', event => {
        event.preventDefault();
        const url = event.target.getAttribute('data-url');
        openDeleteWindow(event.target, 800, 600);
    });

        // boton editar
        botonEditar.addEventListener('click', event => {
            event.preventDefault();
            const formulario = document.getElementById(`form-editar-${productoId}`);
            formulario.submit();
            });
        });
        
        // boton cancelar
        cancelButton.addEventListener('click', () => {
            // Trigger the unload event when the cancel button is clicked
            window.opener.window.dispatchEvent(new Event('unload'));
            });
            //  boton actualizar
            submitButton.addEventListener('click', () => {
                // Trigger the unload event when the submit button is clicked
                window.opener.window.dispatchEvent(new Event('unload'));
            });

    // envia el formulario al servidor
    const formularios = document.querySelectorAll('[id^="form-editar-"]');
    formularios.forEach(formulario => {
        formulario.addEventListener('submit', event => {
        event.preventDefault();
        const formData = new FormData(formulario);
        fetch(formulario.dataset.url, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
          // Actualizar la tabla con los nuevos datos (si es necesario)
          // Mostrar mensaje de éxito o error
        })
        .catch(error => {
            console.error('Error:', error);
          // Mostrar mensaje de error
        });
    });
    });
    
});

// func para abrir una ventana al borrar o editar  
function openDeleteWindow(button, width, height) {
    const url = button.getAttribute('data-url');
    const left = (screen.width - width) / 2;
    const top = (screen.height - height) / 2;
    const windowFeatures = `width=${width},height=${height},left=${left},top=${top}`;
    const newWindow = window.open(url, '_blank', windowFeatures);
    newWindow.focus();
}