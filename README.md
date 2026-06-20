# Archivo, datos y memoria escolar

Sitio estático institucional para la divulgación del trabajo con datos históricos del Archivo Escolar de la Escuela Normal Superior en Lenguas Vivas N.º 2 "Mariano Acosta".

La página presenta una primera instancia de trabajo sobre el Libro Registro de Matrícula correspondiente al período 1910-1915, concebida como una plataforma ampliable para incorporar nuevos documentos, períodos, variables, visualizaciones y recursos pedagógicos.

## Contenido

- Página principal: `index.html`
- Estilos: `styles.css`
- Logo institucional: `assets/logo-mariano-acosta.png`
- Gráficos agregados: `assets/graficos/`
- Mapa de calor estático agregado: `assets/mapas/`

## Assets incorporados

- `assets/logo-mariano-acosta.png`: imagen institucional provista para la página.
- `assets/graficos/`: gráficos agregados y publicables reutilizados desde materiales sanitizados del proyecto geoespacial.
- `assets/mapas/mapa-calor-densidad-espacial.png`: mapa de calor estático incorporado como visualización agregada.
- `assets/mapas/mapa-domicilios-publico.html`: mapa interactivo público con celdas espaciales agregadas. No contiene nombres, direcciones individualizadas ni registros fila por fila.
- `assets/mapas/mapa-calor-publico.html`: mapa de calor interactivo público construido sobre las mismas celdas agregadas. Omite celdas con menos de 3 casos.

## Assets revisados y no incorporados

Se revisaron mapas HTML interactivos disponibles en repositorios locales relacionados. Los mapas originales con puntos, popups, nombres de estudiantes, profesiones de tutores o domicilios individualizados no se incorporan a esta página pública. En su lugar se publican versiones derivadas y agregadas. Cualquier mapa interactivo con coordenadas fila por fila requiere una revisión ética y una versión agregada o anonimizada antes de su publicación.

## Privacidad y patrimonio

El sitio está diseñado para trabajar con datos agregados y visualizaciones generales. No publica nombres individuales de estudiantes, direcciones individualizadas, documentos de identidad ni datos personales del equipo de trabajo.

El documento de referencia local `informe_PST_estadística.pdf` no se incluye en este repositorio porque contiene datos personales que no deben publicarse en una página abierta.

## Uso local

Abrir `index.html` directamente en el navegador o servir la carpeta con un servidor estático local:

```bash
python -m http.server 8000
```

Luego visitar:

```text
http://127.0.0.1:8000/
```
