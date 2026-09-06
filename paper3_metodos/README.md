# Paper 3: materiales metodológicos reproducibles

Versión científica archivada: `v1.4.1-paper3`  
La release citada es una instantánea inmutable; el desarrollo posterior de `main` no modifica su contenido.

**Del folio a la evidencia: un protocolo reproducible para registros escolares manuscritos**

Autor: Alexis Marcelo Perissé  
ORCID: https://orcid.org/0009-0007-8671-9823

## Propósito de este repositorio

Este directorio reúne los materiales públicos necesarios para inspeccionar la arquitectura metodológica del Paper 3 y reproducir sus controles agregados sin exponer documentación individual ni anticipar en esta superficie las conclusiones sustantivas del manuscrito.

La documentación pública permite revisar:

- el diseño de muestreo y sus semillas;
- los verificadores de pertenencia muestral;
- las reglas versionadas de equivalencia;
- la evaluación del tamiz automático de consistencia;
- los análisis de sensibilidad;
- la dependencia documental por folio;
- la auditoría retrospectiva de propagación contextual;
- la política de apertura, privacidad y trazabilidad.

Los resultados científicos detallados, su interpretación y su discusión pertenecen al manuscrito y a las versiones científicas archivadas correspondientes.

## Reproducibilidad de las métricas agregadas

```bash
python -m pip install -r paper3_metodos/reproducibility/requirements.txt
jupyter nbconvert --to notebook --execute paper3_metodos/notebooks/paper3_reproducibility.ipynb --output /tmp/paper3_reproducibility_executed.ipynb
```

## Reproducibilidad del muestreo

El diseño completo está declarado en `reproducibility/sampling_design.json`. La auditoría asistida se obtuvo mediante muestreo simple sin reemplazo dentro de cada año, con 30 registros por estrato y semilla `20260822 + año`. El control no prellenado se seleccionó dentro de esa muestra ya ordenada, con 10 registros por año y semilla `20260822 + 10000 + año`.

La verificación pública de la coherencia del diseño no requiere datos restringidos:

```bash
python paper3_metodos/reproducibility/verify_sampling.py
```

Una auditoría autorizada puede verificar también la pertenencia exacta, sin imprimir identificadores individuales:

```bash
python paper3_metodos/reproducibility/verify_sampling.py \
  --baseline /ruta/base_restringida_prevalidacion_v1.csv \
  --closed-workbook /ruta/plantillas_validacion_manual_cerrada_v1.xlsm
```

El verificador reproduce las selecciones y las compara con compromisos SHA-256 públicos del marco ordenado y de las membresías. Los compromisos certifican el conjunto completo, pero no revelan qué registros fueron seleccionados.

## Evaluación del tamiz automático de consistencia

El repositorio incluye una evaluación cuantitativa de las banderas automáticas frente a la auditoría humana. Las reglas se interpretan como un tamiz selectivo de anomalías formalizadas, no como un detector general de discrepancias ni como sustituto de la lectura humana.

La salida agregada está en `outputs/qa_screening_summary.csv`. Una auditoría autorizada puede regenerarla sin exponer identificadores:

```bash
python paper3_metodos/reproducibility/evaluate_qa_screening.py \
  /ruta/base_restringida_prevalidacion_v1.csv \
  /ruta/discrepancias_validacion_independiente_final.csv \
  /tmp/qa_screening_summary.csv
```

## Sensibilidad a las reglas de equivalencia

La concordancia principal se evaluó mediante comparadores anidados y deterministas para medir cuánto depende el resultado de decisiones explícitas de normalización, tipado y equivalencia.

Las reglas completas están versionadas en `reproducibility/equivalence_rules_v1.json`. Las resoluciones de IDEM, las fechas resueltas, la equivalencia numérica de edad y el tratamiento de faltantes forman parte del contrato histórico evaluado.

Una auditoría autorizada puede reproducir solo salidas agregadas:

```bash
python paper3_metodos/reproducibility/evaluate_equivalence_sensitivity.py \
  /ruta/base_restringida_prevalidacion_v1.csv \
  /ruta/plantillas_validacion_manual_cerrada_v1.xlsm \
  /tmp/equivalence_sensitivity_summary.csv \
  /tmp/equivalence_sensitivity_by_field.csv
```

Las salidas públicas agregadas se encuentran en `outputs/equivalence_sensitivity_summary.csv` y `outputs/equivalence_sensitivity_by_field.csv`. El diccionario de nacionalidades es cerrado y específico de este corpus; no constituye una ontología universal ni debe trasladarse a otros períodos o instituciones sin nueva justificación documental.

## Sensibilidad a la dependencia por folio

El repositorio incorpora un análisis específico para evaluar la posible dependencia entre registros que comparten folio. El intervalo principal reproduce el mecanismo efectivo de selección y se complementa con análisis de sensibilidad documental y controles robustos.

Una auditoría autorizada puede regenerar únicamente resultados agregados:

```bash
python paper3_metodos/reproducibility/evaluate_folio_dependence.py \
  /ruta/base_restringida_prevalidacion_v1.csv \
  /ruta/plantillas_validacion_manual_cerrada_v1.xlsm \
  /tmp/folio_dependence_summary.csv \
  /tmp/folio_dependence_by_year.csv
```

Las salidas públicas son `outputs/folio_dependence_summary.csv` y `outputs/folio_dependence_by_year.csv`. Este análisis no convierte retrospectivamente el diseño en un muestreo por conglomerados ni identifica causas físicas o paleográficas de la heterogeneidad.

## Auditoría retrospectiva de propagación contextual

El script público `reproducibility/evaluate_contextual_propagation.py` reconstruye el universo de valores contextuales iguales al registro precedente dentro del mismo folio y clasifica únicamente los sitios pertenecientes a la auditoría asistida. El script requiere el baseline congelado y la planilla cerrada, pero emite solo conteos agregados: no imprime ni guarda identificadores, localizadores documentales, valores o clasificaciones fila por fila.

```bash
python paper3_metodos/reproducibility/evaluate_contextual_propagation.py \
  --baseline /ruta/base_restringida_prevalidacion_v1.csv \
  --closed-workbook /ruta/plantillas_validacion_manual_cerrada_v1.xlsm \
  --output /tmp/contextual_propagation_summary.csv \
  --check-canonical
```

La salida pública canónica está en `outputs/contextual_propagation_summary.csv`. Los sitios inventariados son candidatos de repetición adyacente, no errores inferidos ni marcas paleográficas clasificadas sin consulta de la fuente.

## Alcance de la apertura

La publicación permite recomputar métricas agregadas y auditar el diseño muestral. La reproducción exacta de la pertenencia requiere acceso autorizado al marco y a las planillas cerradas; no se publican registros, localizadores ni identificadores fila por fila.

Esta distinción evita presentar la reproducibilidad computacional pública como si equivaliera a acceso abierto a documentación personal histórica.

## Privacidad

Los datos individuales, direcciones exactas, coordenadas, imágenes y discrepancias fila por fila permanecen restringidos. Los desacuerdos humanos se conservan como tales y no se fusionan retrospectivamente en una referencia única.

## DOI

DOI conceptual: https://doi.org/10.5281/zenodo.22134990

Para reproducir una instantánea exacta debe citarse el DOI específico de esa versión. El DOI conceptual identifica la familia completa y permite localizar su historial.

## Historial

Ver `CHANGELOG.md`.