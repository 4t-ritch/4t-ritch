# 4tRitch // PS2 Cybercore — versión sin cortes internos

El README reproduce el diseño violeta aprobado usando **paneles completos**. La versión anterior fragmentaba `WHOAMI` y `SYSTEM STATUS` horizontalmente en varias filas, por eso GitHub introducía cortes visuales en las palabras, los marcos y la información.

## Instalación

1. Respalda el `README.md` actual de `4tRitch/4tRitch`.
2. Copia `README.md` y **toda** la carpeta `assets/` a la raíz del repositorio.
3. Haz commit y push a `main`. GitHub mostrará el nuevo README en tu perfil.

No se realizaron cambios en tu repositorio desde esta conversación.

## Archivos y variantes

- `README.md`: **recomendado**. Sin cortes internos y con cada tarjeta de proyecto enlazada. El stack y el footer son imágenes completas. El menú abre la sección de navegación de texto.
- `README-MORE-LINKS.md`: aspecto visual muy parecido, pero cada icono de tecnología y cada región del footer llevan a su propio enlace. Usa cortes **verticales de altura completa** en estas dos franjas; puede haber una diferencia de un píxel en las uniones por el redondeo del navegador. Renómbralo a `README.md` para usarlo.
- `README-CORRECTED.md`: misma disposición que la versión recomendada, pero reemplaza los textos equivocados de las tarjetas con descripciones reales. Esta variante pierde un poco de fidelidad en la zona de texto, aunque mantiene las ilustraciones y marcos.
- `previews/DEFAULT-DESKTOP.png`, `LINKED-DESKTOP.png`, `CORRECTED-DESKTOP.png`: capturas de pruebas locales con los assets del README. **No son capturas del sitio GitHub.com**.
- `previews/ASSEMBLED-SOURCE.png`: montaje sin modificaciones del diseño original para comparar límites de las piezas.
- `source/approved-art.png`, `source/art-with-corrected-text.png`: ilustraciones fuente que permiten regenerar los assets.
- `source/layout.json` y `source/rebuild.py`: coordenadas y script para regenerar cada imagen (requiere Pillow).

## Qué es realmente clicable

Las tarjetas de Okaimono, webcore-ui y Clikity enlazan a sus destinos. El panel de menú lleva al desplegable de navegación, `WHOAMI` abre los repositorios, el estado del sistema enlaza a los dotfiles y el reproductor abre una explicación. También hay enlaces de texto accesibles a proyectos, stack y contacto. En `README-MORE-LINKS.md`, cada tecnología y control del footer tiene enlace propio.

GitHub no admite JavaScript, CSS personalizado ni mapas de imagen interactivos en el README. Por tanto, no es posible tener zonas clicables distintas dentro de **una misma imagen** ni hacer funcionar los botones del reproductor. La solución usa imágenes independientes, completas y sin solapar filas internas.

## Importante sobre los textos

El diseño artístico aprobado incluía textos de ejemplo incorrectos: Okaimono no es una CLI de compras y Clikity no es una TUI. La navegación textual y `README-CORRECTED.md` usan las descripciones reales.
