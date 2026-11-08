# Instalación — 4tRitch PS2 / Cybercore profile

Este paquete está pensado para **el repositorio de perfil `4tRitch/4tRitch`**, no para sustituir la interfaz de GitHub.

## Qué se verá

- El banner, los paneles, el stack, los proyectos y el reproductor retro se renderizan como **PNG estáticos** dentro del README.
- **Los tres proyectos destacados son enlaces reales**: Okaimono, webcore-ui y Clikity.
- Los rótulos del menú y los botones del reproductor **son decorativos**. GitHub no permite ejecutar JavaScript ni aplicar tu propio CSS al README.
- La fuente usada es Noto (Google Fonts) **pre-renderizada en las imágenes**, así que no depende de fuentes instaladas en el equipo de quien visita el perfil.

## Probar en el repositorio

1. Descarga y descomprime el ZIP.
2. Conserva las rutas `README.md` y `assets/` en la **raíz** de tu repositorio `4tRitch/4tRitch`.
3. Haz un commit y publica los cambios:

```bash
git clone https://github.com/4tRitch/4tRitch.git
cd 4tRitch
# Copia el README.md y la carpeta assets/ del ZIP aquí.
git add README.md assets/
git commit -m "style: ps2 cybercore profile readme"
git push origin main
```

Antes de reemplazar, puedes guardar tu README actual como `README.backup.md`.

## En qué consiste el ZIP

- `README.md` — código HTML/Markdown listo para GitHub.
- `assets/` — nueve imágenes de producción, sin enlaces a servidores de imágenes externos.
- `PREVIEW.png` — composición local de los assets para revisar el diseño.
- `source/art/` — recortes de ambientación de la maqueta generada anteriormente.
- `source/render.py` — fuente Python que vuelve a renderizar las imágenes y el preview.
- `source/requirements.txt` — dependencias del script opcional.

## Cómo retocar los textos o los colores

Edita `source/render.py` y ejecuta `python source/render.py` tras instalar las dependencias. La fuente Noto Sans Mono, Noto Serif y Noto Sans CJK se usa solamente **para generar** los PNG: no necesitas subir fuentes a GitHub. En Arch, las fuentes suelen estar disponibles instalando `noto-fonts` y `noto-fonts-cjk` con `pacman`.

El script de edición es opcional: **el README y los PNG ya funcionan sin Python.**

## Detalles para personalizar

- Los enlaces están en `README.md`.
- El tema de música del diseño es ficticio, rotulado como **DEMO TRACK**, para no fingir que reproduce audio real.
- Okaimono está descrito como gestor de anime, no como carrito o asistente de compras. Clikity está descrito como cliente de ClickUp con Tauri.
- Los fondos/recortes proceden del mockup realizado para esta conversación. Para cambiarlos, sustituye los PNG de `source/art/` y vuelve a ejecutar el script.
