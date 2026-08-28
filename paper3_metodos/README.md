# Paper 3: materiales metodológicos reproducibles

Versión científica vigente: `v1.1-paper3`

**Del folio a la evidencia: un protocolo reproducible para registros escolares manuscritos**

Autor: Alexis Marcelo Perissé
ORCID: https://orcid.org/0009-0007-8671-9823

## Alcance

Esta carpeta contiene materiales públicos y reproducibles para documentar el protocolo de transcripción estructurada, resolución contextual, normalización, control de calidad y validación humana aplicado a registros escolares manuscritos del período 1910-1915.

La release trabaja exclusivamente con documentación metodológica y resultados agregados. No incluye datos individuales del corpus, nombres de estudiantes, nombres de padres o tutores, domicilios históricos individualizados, coordenadas individuales, fotografías de los libros, planillas completas de validación, discrepancias fila por fila ni bases restringidas.

## Resultados canónicos

| Métrica | Resultado |
| --- | ---: |
| Corpus total | 1.438 registros |
| Muestra independiente | 180 registros |
| Comparaciones conceptuales | 1.980 |
| Coincidencias | 1.867 |
| Concordancia semántica/resuelta | 94,29% |
| Concordancia ponderada por composición anual | 94,41% |
| IC95% bootstrap | 92,70%-95,98% |
| Sensibilidad excluyendo vacío-vacío | 93,29% |
| Acuerdo interrevisor | 1.080/1.080 |
| Resolución de marcas IDEM | 397/398 |

El intervalo bootstrap corresponde al estimador ponderado por composición anual. Se informa como agregado proveniente del workflow restringido; las réplicas no pueden reconstruirse desde los agregados públicos porque los insumos fila por fila no se publican.

Estas métricas no son CER, WER ni accuracy de un motor HTR. Lo evaluado es el pipeline de transcripción estructurada, resolución contextual, normalización, QA y validación humana. Un `IDEM` expandido correctamente al valor heredado cuenta como concordancia semántica bajo el contrato original.

## Reproducibilidad

Para ejecutar el notebook desde la raíz del repositorio:

```bash
python -m pip install -r paper3_metodos/reproducibility/requirements.txt
jupyter nbconvert --to notebook --execute paper3_metodos/notebooks/paper3_reproducibility.ipynb --output /tmp/paper3_reproducibility_executed.ipynb
```

El notebook usa sólo tablas agregadas publicadas en `paper3_metodos/data/`. Los resultados derivados de revisión restringida se documentan como agregados y no permiten reconstruir casos individuales.

## DOI

- DOI de versión: https://doi.org/10.5281/zenodo.22135344
- DOI conceptual: https://doi.org/10.5281/zenodo.22134990

## Historial

`v1.0-paper3` fue superseded porque sus distribuciones públicas por campo y año eran incorrectas, aunque sus totales globales eran correctos. El historial resumido está en `CHANGELOG.md`.

## Licencia

Los materiales metodológicos públicos se distribuyen bajo CC BY 4.0. Ver `../LICENSE.md`.
