# Pizzería Chevery — Backend API (FastAPI)

API RESTful desarrollada en **FastAPI** y conectada a una base de datos relacional **MariaDB**, diseñada exclusivamente para soportar el flujo del frontend de Pizzería Chevery (Home, Menú, Carrito y Confirmación de Pedido con Ticket).

## Requisitos Previos

* Python 3.10 o superior.
* MariaDB instalado localmente.
* Gestor de paquetes `pip` o `uv`.

## Estructura del Proyecto

```
pizzeria_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada y configuración de CORS
│   ├── database.py          # Conexión SQLAlchemy con MariaDB
│   ├── models.py            # Modelos ORM (Tablas DDL)
│   ├── schemas.py           # Esquemas Pydantic v2 (Request/Response)
│   ├── services.py          # Lógica de negocio (Promo 2x1 y manejo seguro de FKs)
│   └── routers/
│       ├── __init__.py
│       ├── catalogo.py      # Endpoints de Pizzas y Masas
│       ├── carritos.py      # Endpoints de Carrito y Carrito-Pizzas
│       └── tickets.py       # Endpoints de Checkout y Tickets
├── seed.sql                 # Datos iniciales (Catálogos y especialidades)
└── requirements.txt
```

## Configuración y Líneas que se Deben Editar

### 1. Variables de Conexión a Base de Datos

Abre el archivo `app/database.py` y edita la línea de conexión para apuntar a tu instancia local de MariaDB con tu usuario y contraseña:

* **Archivo a editar:** `app/database.py`
* **Líneas a modificar (alrededor de la línea 6-10):**

```python
# EDITA AQUÍ: Cambia 'tu_usuario', 'tu_password' y '127.0.0.1:3306' según tu entorno local
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mariadb+pymysql://tu_usuario:tu_password@127.0.0.1:3306/pizzeria_chevery?charset=utf8mb4"
)
```

### 2. Configuración de CORS en Producción

Por defecto, la API permite conexiones desde cualquier origen (`allow_origins=["*"]`). Si deseas restringir el acceso únicamente a tu frontend local o de producción, edita `app/main.py`:

* **Archivo a editar:** `app/main.py`
* **Líneas a modificar (alrededor de la línea 15):**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://tudominio-pizzeria.com"], # EDITA AQUÍ tus dominios permitidos
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

## Inserción de Datos Iniciales (Seeders)

Para que los menús, precios y tamaños aparezcan en el frontend, debes poblar los catálogos ejecutando el script `seed.sql` en tu gestor de MariaDB (DBeaver, HeidiSQL o consola CLI):

1. Crea la base de datos vacía:
   ```sql
   CREATE DATABASE IF NOT EXISTS pizzeria_chevery CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. Ejecuta el contenido completo del archivo **`seed.sql`**:

```sql
USE pizzeria_chevery;

-- ==========================================
-- 1. CATÁLOGO DE TAMAÑOS
-- ==========================================
INSERT INTO TAMANO (id_tamano, nombre, orden) VALUES
(1, 'Chica', 1),
(2, 'Mediana', 2),
(3, 'Familiar', 3);

-- ==========================================
-- 2. CATÁLOGO DE TIPOS DE MASA
-- ==========================================
INSERT INTO MASA (id_masa, nombre, precio_extra, activo) VALUES
(1, 'Tradicional', 0.00, TRUE),
(2, 'Fina y Crujiente', 0.00, TRUE),
(3, 'Orilla Rellena de Queso', 30.00, TRUE),
(4, 'Orilla Queso + Pepperoni', 45.00, TRUE);

-- ==========================================
-- 3. CATÁLOGO DE PIZZAS (Especialidades)
-- ==========================================
INSERT INTO PIZZA (id_pizza, sabor, descripcion, imagen_url, etiqueta, destacado, activo) VALUES
(1, 'La Clásica (Pepperoni)', 'Queso mozzarella derretido y generosas rodajas de pepperoni tradicional.', '/assets/pizzas/pepperoni.jpg', 'MÁS VENDIDA', TRUE, TRUE),
(2, 'Hawaiana', 'Jamón selecto, piña dulce en trozos y extra queso mozzarella fundido.', '/assets/pizzas/hawaiana.jpg', 'TROPICAL', TRUE, TRUE),
(3, 'La Mexicana', 'Chorizo, jalapeño en rodajas, cebolla morada y deliciosa base de frijoles.', '/assets/pizzas/mexicana.jpg', 'LOCAL', TRUE, TRUE),
(4, 'Carnes Frías', 'Salami, pepperoni, jamón, salchicha y crujiente tocino ahumado.', '/assets/pizzas/carnes_frias.jpg', 'ESPECIAL', FALSE, TRUE),
(5, 'Vegetariana', 'Champiñones, pimiento verde, cebolla, aceitunas negras y jitomate fresco.', '/assets/pizzas/vegetariana.jpg', 'VEGETARIANA', FALSE, TRUE);

-- ==========================================
-- 4. RELACIÓN PRECIOS Y STOCK POR TAMAÑO
-- ==========================================
INSERT INTO PIZZA_TAMANO (id_pizza_tamano, id_pizza, id_tamano, precio, stock) VALUES
(1, 1, 1, 110.00, 25),
(2, 1, 2, 160.00, 30),
(3, 1, 3, 220.00, 15),
(4, 2, 1, 120.00, 25),
(5, 2, 2, 170.00, 30),
(6, 2, 3, 230.00, 15),
(7, 3, 1, 135.00, 20),
(8, 3, 2, 185.00, 25),
(9, 3, 3, 250.00, 10),
(10, 4, 1, 145.00, 20),
(11, 4, 2, 195.00, 25),
(12, 4, 3, 270.00, 10),
(13, 5, 1, 130.00, 20),
(14, 5, 2, 180.00, 25),
(15, 5, 3, 240.00, 10);
```

## Instalación y Ejecución

1. **Situarse en la carpeta del proyecto:**
   ```bash
   cd pizzeria_api
   ```

2. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar el servidor de desarrollo con Uvicorn:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

4. **Verificar la documentación interactiva:**
   Abre tu navegador en: `http://localhost:8000/docs`