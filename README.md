# ShopLook

Una app web para encontrar **locales de ropa cerca tuyo**.

Permite ver:
- Qué locales tenés cerca, en un mapa
- Cuáles tienen descuentos hoy y con qué billetera o banco virtual
- Si tienen stock y si son mayoristas
- Buscar prendas escribiendo ("ropa de fiesta") o **subiendo una foto**

> Estado: en desarrollo.

---

## Qué incluye

| Función | Estado |
|---|---|
| Pantalla de inicio con ofertas | Pendiente |
| Mapa de locales | Pendiente |
| Perfil de cada local | Pendiente |
| Buscador de prendas | Pendiente |
| Búsqueda por imagen (IA) | Pendiente |
| Reseñas de compradoras | Pendiente |

## Tecnologías

- Frontend: [completar]
- Backend: [completar]
- Base de datos: [completar]

## Cómo ejecutarlo

**1. Descargar el proyecto**
```bash
git clone [link-del-repo]
cd [nombre-del-repo]
```

**2. Iniciar el backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # En Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
flask run
```

**3. Iniciar el frontend** (en otra terminal)
```bash
cd frontend
npm install
npm run dev
```

> Las claves van en un archivo `.env` que **no se sube** a GitHub.

## Carpetas

```
backend/   → servidor, base de datos e IA
frontend/  → lo que ve el usuario
docs/      → diseños y notas
```

## Cómo trabajamos

1. Creamos una rama por cada función: `git checkout -b feature/mapa`
2. Hacemos commits chicos con mensajes claros
3. Subimos la rama y abrimos un Pull Request
4. La otra persona lo revisa y lo une a `main`

## Equipo

- Paula Agustina Penin
- Valentina Fernandez Alegre


## Licencia

[MIT] — ver el archivo `LICENSE`.
