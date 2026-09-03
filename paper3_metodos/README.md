# Paper 3: materiales metodológicos reproducibles

Versión científica archivada: `v1.3.1-paper3`  
Estado de la rama `main`: alineado con la auditoría de muestreo y los metadatos de la versión archivada.

**Del folio a la evidencia: un protocolo reproducible para registros escolares manuscritos**

Autor: Alexis Marcelo Perissé  
ORCID: https://orcid.org/0009-0007-8671-9823

## Resultados canónicos

- Corpus: 1.438 registros.
- Auditoría asistida: 1.867/1.980 = 94,29%; ponderada 94,41%; IC95% 92,70%-95,98%.
- Sensibilidad sin vacío-vacío: 1.572/1.685 = 93,29%.
- Control independiente no prellenado: baseline vs A = 594/660 = 90,00%; baseline vs B = 594/660 = 90,00%.
- Acuerdo interrevisor: 1.075/1.080 = 99,54%; cuatro desacuerdos en nombre y uno en domicilio.
- IDEM: 397/398 correctamente resueltos.

Los desacuerdos humanos se conservan como tales; no se fusionan A y B en una referencia única. Los datos individuales, direcciones exactas, coordenadas, imágenes y discrepancias fila por fila permanecen restringidos.

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

El verificador reproduce ambas selecciones y las compara con compromisos SHA-256 públicos del marco ordenado y de las dos membresías. Los compromisos certifican el conjunto completo, pero no revelan qué registros fueron seleccionados. La rama `main` fue contrastada el 3 de septiembre de 2026 contra el baseline y la planilla cerrada: 180/180 y 60/60 identificadores coincidieron con las selecciones reproducidas, el control fue un subconjunto de la auditoría y cada año aportó 30 y 10 registros respectivamente. Esta coincidencia se refiere exclusivamente a la pertenencia muestral; la doble revisión de los 60 registros presentó cinco desacuerdos, conservados sin adjudicación.

## Evaluación del tamiz automático de consistencia

El cruce a nivel de registro entre las banderas previas a la corrección y la auditoría asistida de 180 casos produjo 2 verdaderos positivos, 3 falsos positivos, 47 falsos negativos y 128 verdaderos negativos. La sensibilidad fue 4,08%, la especificidad 97,71%, el valor predictivo positivo 40,00% y el valor predictivo negativo 73,14%. Las estimaciones descriptivas ponderadas por la composición anual fueron 3,95%, 98,21%, 47,75% y 71,14%, respectivamente.

Las reglas funcionan como un tamiz selectivo de anomalías formalizadas, no como un detector general de discrepancias ni como sustituto de la lectura humana. Solo cinco registros muestreados tenían bandera automática, por lo que el valor predictivo positivo debe interpretarse con cautela.

La salida agregada está en `outputs/qa_screening_summary.csv`. Una auditoría autorizada puede regenerarla sin exponer identificadores:

```bash
python paper3_metodos/reproducibility/evaluate_qa_screening.py \
  /ruta/base_restringida_prevalidacion_v1.csv \
  /ruta/discrepancias_validacion_independiente_final.csv \
  /tmp/qa_screening_summary.csv
```

## Sensibilidad a las reglas de equivalencia

La concordancia principal se evaluó además con seis comparadores anidados y deterministas. El criterio resuelto y tipado pero estricto en grafía produjo 1.841/1.980 = 92,98% (93,05% ponderado); el comparador principal completo reprodujo 1.867/1.980 = 94,29% (94,41% ponderado). La diferencia total fue de 26 coincidencias, equivalentes a 1,31 puntos porcentuales: 11 provinieron de la normalización formal, 13 del diccionario cerrado de nacionalidades y 2 de la canonización del curso.

Las reglas completas están versionadas en `reproducibility/equivalence_rules_v1.json`. Las resoluciones de IDEM, las fechas resueltas, la equivalencia numérica de edad y el tratamiento de faltantes permanecieron invariantes porque forman parte del contrato histórico evaluado. Una auditoría autorizada puede reproducir solo salidas agregadas:

```bash
python paper3_metodos/reproducibility/evaluate_equivalence_sensitivity.py \
  /ruta/base_restringida_prevalidacion_v1.csv \
  /ruta/plantillas_validacion_manual_cerrada_v1.xlsm \
  /tmp/equivalence_sensitivity_summary.csv \
  /tmp/equivalence_sensitivity_by_field.csv
```

Las salidas públicas agregadas se encuentran en `outputs/equivalence_sensitivity_summary.csv` y `outputs/equivalence_sensitivity_by_field.csv`. El diccionario de nacionalidades es cerrado y específico de este corpus; no constituye una ontología universal ni debe trasladarse a otros períodos o instituciones sin nueva justificación documental.

## Alcance de la apertura

La publicación permite recomputar las métricas agregadas y auditar el diseño muestral. La reproducción exacta de la pertenencia requiere acceso autorizado al marco y a las planillas cerradas; no se publican registros, localizadores ni identificadores fila por fila. Esta distinción evita presentar la reproducibilidad computacional pública como si equivaliera a acceso abierto a documentación personal histórica.

## DOI

DOI conceptual: https://doi.org/10.5281/zenodo.22134990

Los DOI específicos de cada versión se encuentran en el historial del registro conceptual de Zenodo.

## Historial

Ver `CHANGELOG.md`.
