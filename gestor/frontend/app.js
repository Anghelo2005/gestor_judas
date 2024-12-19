const apiUrl = "http://localhost:5000/api";

// Función para registrar un producto
document.getElementById("producto-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const producto = {
        nombre: document.getElementById("nombre").value,
        categoria: document.getElementById("categoria").value,
        precio_unitario: parseFloat(document.getElementById("precio").value),
        stock_inicial: parseInt(document.getElementById("stock").value, 10),
        rfid: document.getElementById("rfid").value,
    };

    try {
        const response = await fetch(`${apiUrl}/productos`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(producto),
        });
        const data = await response.json();

        if (response.ok) {
            document.getElementById("mensaje-registro").textContent = data.message;
            cargarProductos(); // Actualizar lista de productos
        } else {
            document.getElementById("mensaje-registro").textContent = data.error;
        }
    } catch (error) {
        console.error("Error:", error);
    }
});

// Función para cargar productos
async function cargarProductos() {
    try {
        const response = await fetch(`${apiUrl}/productos`);
        const productos = await response.json();

        const lista = document.getElementById("lista-productos");
        lista.innerHTML = ""; // Limpiar lista

        productos.forEach((producto) => {
            const div = document.createElement("div");
            div.innerHTML = `
                <strong>${producto.nombre}</strong> - ${producto.categoria} - Stock: ${producto.stock_actual}
                <button onclick="actualizarStock(${producto.id}, 'entrada')">+1</button>
                <button onclick="actualizarStock(${producto.id}, 'salida')">-1</button>
                <button onclick="eliminarProducto(${producto.id})">Eliminar</button>
            `;
            lista.appendChild(div);
        });
    } catch (error) {
        console.error("Error:", error);
    }
}

// Función para actualizar stock
async function actualizarStock(id, accion) {
    try {
        const response = await fetch(`${apiUrl}/productos/${id}/stock`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ accion, cantidad: 1 }),
        });
        const data = await response.json();

        if (response.ok) {
            cargarProductos(); // Actualizar lista de productos
        } else {
            alert(data.error);
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

// Función para eliminar un producto
async function eliminarProducto(id) {
    try {
        const response = await fetch(`${apiUrl}/productos/${id}`, {
            method: "DELETE",
        });
        const data = await response.json();

        if (response.ok) {
            cargarProductos(); // Actualizar lista de productos
        } else {
            alert(data.error);
        }
    } catch (error) {
        console.error("Error al eliminar producto:", error);
    }
}

// Función para cargar estadísticas
async function cargarEstadisticas() {
    try {
        const response = await fetch(`${apiUrl}/estadisticas`);
        const stats = await response.json();

        const statsDiv = document.getElementById("estadisticas");
        statsDiv.innerHTML = `
            <p>Total de Productos: ${stats.total_productos}</p>
            <p>Total de Movimientos: ${stats.total_movimientos}</p>
            <p>Productos con Bajo Stock: ${stats.productos_bajo_stock}</p>
        `;
    } catch (error) {
        console.error("Error al cargar estadísticas:", error);
    }
}

// Función para cargar productos con bajo stock
async function cargarBajoStock() {
    try {
        const response = await fetch(`${apiUrl}/productos/bajo_stock`);
        const productos = await response.json();

        const bajoStockDiv = document.getElementById("bajo-stock");
        bajoStockDiv.innerHTML = "<h3>Productos con Bajo Stock</h3>";

        productos.forEach((producto) => {
            const div = document.createElement("div");
            div.innerHTML = `
                <p>${producto.nombre} - Stock Actual: ${producto.stock_actual} (Reordenar: ${producto.nivel_reorden})</p>
            `;
            bajoStockDiv.appendChild(div);
        });
    } catch (error) {
        console.error("Error al cargar productos con bajo stock:", error);
    }
}

// Función para obtener y mostrar el último RFID
async function obtenerUltimoRFID() {
    try {
        const response = await fetch(`${apiUrl}/ultimo_rfid`);
        const data = await response.json();
        if (data.rfid) {
            document.getElementById("rfid").value = data.rfid;
        }
    } catch (error) {
        console.error("Error al obtener RFID:", error);
    }
}

// Llamar a obtenerUltimoRFID cada 2 segundos
setInterval(obtenerUltimoRFID, 2000);

// Inicializar
cargarProductos();
cargarEstadisticas();
cargarBajoStock();
