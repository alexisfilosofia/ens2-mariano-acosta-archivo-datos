# Archivo, datos y memoria escolar

**Ciencia de datos reproducible aplicada a registros histórico-educativos (Buenos Aires, 1910–1915).**

Este repositorio reúne materiales públicos de investigación, metodología y divulgación vinculados con el Archivo Escolar de la ENS N.º 2 "Mariano Acosta". El proyecto forma parte de un Trabajo Final Integrador de Maestría en Ciencia de Datos y está orientado a transformar documentación histórica en evidencia cuantitativa reproducible, auditable y compatible con restricciones de privacidad.

## Qué demuestra técnicamente este proyecto

El trabajo implementa y documenta un flujo de datos que incluye:

- estructuración y normalización de registros documentales históricos;
- reglas explícitas de validación y control de calidad;
- trazabilidad y versionado de decisiones metodológicas;
- muestreo reproducible, auditoría asistida y control humano no prellenado;
- evaluación cuantitativa de reglas automáticas de consistencia;
- análisis de sensibilidad de criterios de equivalencia;
- análisis de dependencia documental por folio;
- producción de resultados agregados reproducibles;
- análisis cuantitativo y geoespacial;
- publicación sanitizada que separa reproducibilidad computacional de acceso a datos personales.

## En breve

- **Período:** 1910–1915.
- **Corpus canónico:** 1.438 registros.
- **Versión científica vigente:** `v1.4-paper3`.
- **Materiales metodológicos reproducibles:** `paper3_metodos/`.
- **DOI conceptual:** https://doi.org/10.5281/zenodo.22134990

Los DOI específicos de cada versión se encuentran en el historial de Zenodo.

## Arquitectura metodológica

La documentación pública permite inspeccionar la lógica del pipeline sin exponer registros individuales. El módulo `paper3_metodos/` contiene:

- `notebooks/`: cuadernos de reproducción de métricas agregadas;
- `reproducibility/`: requisitos, diseño muestral, verificadores y reglas versionadas;
- `outputs/`: salidas públicas agregadas;
- `protocolo/`: documentación metodológica;
- `data/`: insumos públicos o sanitizados compatibles con la política de apertura;
- `CHANGELOG.md`: historial de cambios científicos y metodológicos.

La documentación metodológica detallada está en [`paper3_metodos/README.md`](paper3_metodos/README.md).

## Reproducibilidad

Las métricas agregadas del Paper 3 pueden regenerarse a partir de los materiales públicos:

```bash
python -m pip install -r paper3_metodos/reproducibility/requirements.txt
jupyter nbconvert --to notebook --execute \
  paper3_metodos/notebooks/paper3_reproducibility.ipynb \
  --output /tmp/paper3_reproducibility_executed.ipynb
```

El diseño muestral también puede verificarse públicamente sin acceder a información restringida:

```bash
python paper3_metodos/reproducibility/verify_sampling.py
```

Para auditorías autorizadas, los verificadores admiten las bases restringidas correspondientes y comparan la selección reproducida con compromisos SHA-256 públicos sin imprimir identificadores individuales.

## Calidad de datos y validación

La versión metodológica vigente documenta, entre otros controles:

- auditoría asistida sobre una muestra estratificada;
- control no prellenado con doble lectura separada;
- acuerdo interrevisor;
- resolución controlada de marcas `IDEM`;
- evaluación del tamiz automático de consistencia;
- sensibilidad a reglas de equivalencia;
- sensibilidad a dependencia por folio.

El objetivo no es presentar las reglas automáticas como sustituto de la lectura humana, sino medir explícitamente su alcance y conservar los desacuerdos cuando corresponda.

## Privacidad y apertura responsable

El repositorio publica únicamente resultados agregados y materiales metodológicos sanitizados. No contiene registros individuales, nombres de alumnos o tutores, domicilios individualizados, coordenadas individuales, fotografías de los libros, planillas completas ni discrepancias fila por fila.

La apertura está diseñada para permitir auditoría metodológica y reproducción de resultados agregados sin confundir reproducibilidad computacional con publicación irrestricta de documentación personal histórica.

## Autor y citación

**Alexis Marcelo Perissé**  
ORCID: https://orcid.org/0009-0007-8671-9823

Para citar el proyecto, consultar [`CITATION.cff`](CITATION.cff) y el registro conceptual de Zenodo:

https://doi.org/10.5281/zenodo.22134990
