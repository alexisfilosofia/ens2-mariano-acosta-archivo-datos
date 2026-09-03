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

## Diseño de muestreo verificable

La población objetivo es el corpus cerrado de 1.438 registros. Se utilizó `pandas.DataFrame.sample` 2.2.3 para realizar muestreo simple pseudoaleatorio sin reemplazo dentro de cada año. La auditoría asistida seleccionó 30 registros por año mediante la semilla `20260822 + año`. Luego se ordenó la muestra por año, número de hoja y número de orden, con faltantes al final. Sobre esa secuencia se seleccionaron 10 registros por año para el control no prellenado, mediante la semilla `20260822 + 10000 + año`. Por lo tanto, el control de 60 está anidado en la muestra de 180.

La asignación uniforme asegura cobertura de los seis años, pero no reproduce la composición anual del corpus. Las estimaciones poblacionales utilizan ponderación por los tamaños conocidos de los estratos. Los tamaños de 30 y 10 casos por año se definieron por cobertura temporal y carga de revisión viable, no mediante un cálculo de potencia a priori.

El archivo `reproducibility/sampling_design.json` registra las semillas por año, el orden del marco, el entorno de software y tres compromisos SHA-256: uno para la secuencia completa del marco restringido y uno para cada membresía. Su canonicalización usa únicamente `anio_libro` e `id_registro`; los compromisos se publican como un único resumen criptográfico y no exponen la lista de identificadores. El 3 de septiembre de 2026 se reprodujeron ambas selecciones contra el baseline prevalidación y la planilla cerrada: coincidieron los 180 registros de la auditoría y los 60 del control; este último quedó confirmado como subconjunto exacto del primero.

## Validación independiente

La muestra asistida contiene 180 registros y 1.980 comparaciones conceptuales. Sus valores del pipeline estaban prellenados para el cotejo humano, por lo que el 94,29% informado describe una auditoría `human-in-the-loop` y no una lectura ciega.

El control no prellenado cubre 60 registros y 1.080 comparaciones sustantivas. Dos revisores leyeron los mismos folios de manera independiente, sin consultar el baseline ni la respuesta del otro. Se observaron 1.075 acuerdos exactos entre revisores (99,54%). Los cinco desacuerdos humanos se conservan como tales y no se adjudican en una referencia única. El baseline se compara por separado contra A y contra B.

## Qué se publica

La rama pública incluye:

- tablas agregadas de validación;
- concordancia por campo;
- concordancia por año;
- sensibilidad excluyendo comparaciones vacío-vacío;
- acuerdo agregado entre revisores;
- resumen del bootstrap;
- notebook reproducible sanitizado;
- especificación y verificador del muestreo;
- compromisos SHA-256 del marco y las membresías restringidas;
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
- listas de pertenencia o identificadores fila por fila.

## Interpretación

Las métricas publicadas no son CER, WER ni accuracy de un motor HTR. La concordancia reportada corresponde al resultado agregado del pipeline completo bajo reglas explícitas de resolución contextual, normalización y validación humana. La reproducibilidad pública alcanza el código, las métricas agregadas, el diseño y los compromisos criptográficos; la verificación de la pertenencia exacta requiere acceso autorizado a los insumos restringidos.
