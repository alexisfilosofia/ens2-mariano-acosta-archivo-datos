# Archivo, datos y memoria escolar

Sitio estático institucional para la divulgación del trabajo con datos históricos del Archivo Escolar de la Escuela Normal Superior en Lenguas Vivas N.º 2 "Mariano Acosta".

La página presenta una primera instancia de trabajo sobre el Libro Registro de Matrícula correspondiente al período 1910-1915, concebida como una plataforma ampliable para incorporar nuevos documentos, períodos, variables, visualizaciones y recursos pedagógicos.

## Contenido

- Página principal: `index.html`
- Estilos: `styles.css`
- Espacio preparado para logo institucional: `assets/logo-mariano-acosta.png`
- Espacio preparado para gráficos: `assets/graficos/`
- Espacio preparado para mapas: `assets/mapas/`

## Privacidad y patrimonio

El sitio está diseñado para trabajar con datos agregados y visualizaciones generales. No publica nombres individuales de estudiantes, domicilios exactos individualizados, documentos de identidad ni datos personales del equipo de trabajo.

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
