# Paper 3: materiales metodológicos reproducibles

Versión científica: `v1.2-paper3`

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

## Reproducibilidad

```bash
python -m pip install -r paper3_metodos/reproducibility/requirements.txt
jupyter nbconvert --to notebook --execute paper3_metodos/notebooks/paper3_reproducibility.ipynb --output /tmp/paper3_reproducibility_executed.ipynb
```

## DOI

DOI conceptual: https://doi.org/10.5281/zenodo.22134990

DOI de versión `v1.2-paper3`: https://doi.org/10.5281/zenodo.22240577

## Historial

Ver `CHANGELOG.md`.
