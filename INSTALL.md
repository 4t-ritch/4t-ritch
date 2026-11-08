# 4tRitch // PS2 CYBERCORE — kit de GitHub

Este kit preserva la composición del arte aprobado (en vez de recrearlo con cajas y fuentes nuevas). El README se compone de **36 fragmentos de imagen con enlaces independientes**.

## Instalación

1. Haz un respaldo del README actual de `4tRitch/4tRitch`.
2. Copia **README.md** y la carpeta **assets/** completa a la raíz del repositorio.
3. Haz commit/push a `main` y abre tu perfil.
4. La variante `README-TEXT-CORRECTED.md` corrige los textos *dentro de las tarjetas* de Okaimono, webcore-ui y Clikity; para usarla renómbrala a `README.md`.

## Qué funciona

- Las 3 tarjetas de proyectos abren sus enlaces correspondientes.
- Los 10 iconos tecnológicos abren su sitio oficial o repositorio relacionado.
- Las 4 opciones del menú lateral usan anclas locales; las zonas del footer también son enlaces.
- `whoami` y `system status` son imágenes con enlaces útiles.
- El reproductor es una ilustración; pulsarlo abre Spotify, pero **no reproduce nada dentro de GitHub**.

## Limitaciones y decisiones técnicas

- **El texto dentro de los PNG no es editable desde Markdown.** La variante corregida reemplaza únicamente las columnas de texto de las tarjetas con una tipografía y textura similar.
- Al ser varios fragmentos de una misma composición, las partes se unen con un solo `<p>` y separadores `<br />` para no heredar márgenes entre párrafos en GitHub.
- No se utilizan CSS, JavaScript ni mapas de imágenes, que GitHub no permite en un README.
- Las ilustraciones son estáticas. En móvil se reduce la escala y el texto puede ser pequeño.
- `previews/` contiene capturas **locales aproximadas**, no capturas tomadas desde GitHub.com.
- Los textos de la maqueta original eran conceptos visuales: por ejemplo Okaimono no es una CLI de compras, y Clikity no es una CLI/TUI. El bloque de texto accesible y la variante corregida contienen las descripciones correctas.

## Contenido

- `README.md`: fidelidad visual máxima con el arte aprobado.
- `README-TEXT-CORRECTED.md`: variante con texto de tarjetas corregido.
- `assets/`: cada pieza enlazable (incluye 3 tarjetas alternativas con texto corregido).
- `assets/reference-art.png`: el arte aprobado del cual se derivan las piezas.
- `source/rebuild.py`: regenera los fragmentos a partir de las imágenes de referencia.

## Nota sobre enlaces internos

GitHub puede normalizar anclas HTML en ciertos contextos. Si tus anclas internas no funcionan, usa los enlaces externos de las tarjetas y los enlaces de navegación textual.

## Variante adicional: paneles individuales completos

Además se incluye `README-COMPLETE-PANELS.md` y `assets/complete-panels/`. Esta opción utiliza 10 recursos independientes, cada uno entero (no bandas cortadas). Conserva el diseño original, pero el menú lateral se comporta como un solo enlace; los enlaces individuales están en el desplegable de navegación textual.
