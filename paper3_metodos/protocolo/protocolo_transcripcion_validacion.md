# Protocolo público de transcripción, resolución y validación

## Objeto

Este protocolo documenta la versión pública y reproducible del procedimiento usado para convertir registros escolares manuscritos en evidencia agregada auditable. El flujo no evalúa una transcripción óptica aislada, sino un pipeline compuesto por transcripción estructurada, resolución contextual, normalización, control de calidad y validación humana.

## Unidad de trabajo

La unidad analítica pública es el registro de inscripción. La release cubre el período 1910-1915 y documenta un corpus total de 1.438 registros. Los materiales abiertos trabajan con agregados y no publican registros individuales.

## Etapas del pipeline

1. Relevamiento documental y definición de campos.
2. Transcripción estructurada por registro.
3. Resolución contextual de marcas de repetición como `IDEM`.
4. Normalización controlada de valores para análisis agregado.
5. Control de calidad interno.
6. Selección de muestra independiente estratificada.
7. Validación humana contra la fuente restringida.
8. Consolidación de métricas agregadas.
9. Publicación de resultados reproducibles no identificables.

## Regla metodológica sobre `IDEM`

Un `IDEM` expandido correctamente al valor heredado no es un error. El contrato original de transcripción permitía registrar directamente el valor resuelto cuando la marca de repetición era interpretable por contexto. Por eso, la validación pública evalúa concordancia semántica/resuelta y no equivalencia literal de signos gráficos.

En la muestra auditada se evaluaron 398 marcas de repetición/IDEM y 397 fueron resueltas correctamente por el pipeline.

## Validación independiente

La muestra independiente contiene 180 registros y 1.980 comparaciones conceptuales. La validación compara salidas estructuradas y resueltas contra revisión humana, con una métrica agregada de concordancia semántica/resuelta.

La doble revisión documentada cubre 60 registros y 1.080 comparaciones sustantivas, con 1.075 acuerdos exactos entre revisores independientes (99,54%). Los cinco desacuerdos humanos se conservan como tales y no se adjudican en una referencia única.

## Qué se publica

La release pública incluye:

- tablas agregadas de validación;
- concordancia por campo;
- concordancia por año;
- sensibilidad excluyendo comparaciones vacío-vacío;
- acuerdo agregado entre revisores;
- resumen del bootstrap;
- notebook reproducible sanitizado;
- manifiesto de hashes;
- notas de release.

## Qué no se publica

La release excluye:

- nombres de estudiantes;
- nombres de padres o tutores;
- domicilios históricos individualizados;
- coordenadas individuales;
- fotografías de los libros;
- planillas completas de validación;
- discrepancias fila por fila;
- bases restringidas;
- identificadores que permitan reconstruir personas concretas.

## Interpretación

Las métricas publicadas no son CER, WER ni accuracy de un motor HTR. La concordancia reportada corresponde al resultado agregado del pipeline completo bajo reglas explícitas de resolución contextual, normalización y validación humana.
