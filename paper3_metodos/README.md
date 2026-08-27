# Paper 3: materiales metodológicos reproducibles

Release pública `v1.0-paper3` para el artículo metodológico:

**Del folio a la evidencia: un protocolo reproducible para registros escolares manuscritos**

Autor: Alexis Marcelo Perissé
ORCID: https://orcid.org/0009-0007-8671-9823

## Alcance

Esta carpeta contiene materiales públicos y reproducibles para documentar el protocolo de transcripción estructurada, resolución contextual, normalización, control de calidad y validación humana aplicado a registros escolares manuscritos del período 1910-1915.

La release trabaja exclusivamente con documentación metodológica y resultados agregados. No incluye nombres de estudiantes, nombres de padres o tutores, domicilios históricos individualizados, coordenadas individuales, fotografías de los libros, planillas completas de validación, discrepancias fila por fila ni bases restringidas.

## Estructura

- `protocolo/`: descripción del protocolo público de transcripción, validación y resguardo.
- `notebooks/`: notebook reproducible sanitizado.
- `data/`: tablas agregadas necesarias para reproducir las métricas públicas.
- `reproducibility/`: dependencias, manifiesto SHA-256 y auditoría de privacidad.
- `release_notes.md`: notas de la release pública.

## Resultados públicos auditados

| Métrica | Resultado |
| --- | ---: |
| Corpus total | 1.438 registros |
| Muestra independiente | 180 registros |
| Comparaciones conceptuales | 1.980 |
| Coincidencias | 1.867 |
| Concordancia semántica/resuelta | 94,29% |
| Concordancia ponderada por composición anual | 94,41% |
| IC95% bootstrap | 92,70%-95,98% |
| Sensibilidad excluyendo 295 comparaciones vacío-vacío | 93,29% |
| Doble revisión | 60 registros |
| Acuerdo exacto entre revisores independientes | 100% sobre 1.080 comparaciones sustantivas |
| Marcas de repetición/IDEM evaluadas | 398 |
| Resueltas correctamente por el pipeline | 397 |

Estos resultados no deben describirse como CER, WER ni como "accuracy de un motor HTR". Lo evaluado es un pipeline de transcripción estructurada, resolución contextual, normalización, QA y validación humana.

Un `IDEM` expandido correctamente al valor heredado no se considera error, porque el contrato original de transcripción permitía producir directamente el valor resuelto.

## Reproducibilidad

Para ejecutar el notebook desde la raíz del repositorio:

```bash
python -m pip install -r paper3_metodos/reproducibility/requirements.txt
jupyter nbconvert --to notebook --execute paper3_metodos/notebooks/paper3_reproducibility.ipynb --output /tmp/paper3_reproducibility_executed.ipynb
```

El notebook usa sólo tablas agregadas publicadas en `paper3_metodos/data/`. Los resultados derivados de revisión restringida se documentan como agregados y no permiten reconstruir casos individuales.

## Privacidad

La publicación pública excluye materiales individualizantes y conserva fuera del repositorio abierto los datos restringidos. El archivo `reproducibility/privacy_audit.md` documenta los controles aplicados antes de la release.
