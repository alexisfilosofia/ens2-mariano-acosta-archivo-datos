# Privacy audit for `v1.2-paper3`

Date: 2026-09-01

## Scope

The audit scanned the repository's 24 text-based files after applying the v1.2 patch and before tagging `v1.2-paper3`.

## Automated Checks

The scan checked for email addresses, Google Drive/Docs URLs, local filesystem paths, credential markers, coordinate-like pairs, restricted-file markers and row-level discrepancy references.

Result: 4 coordinate-like alerts, all in public map files:

- `assets/mapas/mapa-calor-publico.html`
- `assets/mapas/mapa-domicilios-publico.html`

Manual review confirms that these coordinates are public aggregate grid cells, the map center and the institutional marker for ENS N.º 2 "Mariano Acosta"; they are not individual student coordinates or exact domiciles.

## Sensitive-Term Review

Terms related to students, tutors, addresses, coordinates, photographs, restricted validation sheets and row-level discrepancies appear only in privacy statements, methodological exclusions, aggregate field descriptions or public aggregate-map metadata.

Allowed proper names present in the public materials are Alexis Marcelo Perissé as author, Mariano Acosta as the institutional name and Armenia Euredjian as the archive name.

## Public-Release Decision

Result: 0 privacy findings across 24 text-based files. No student/tutor names, row-level addresses, individual coordinates, archival images, restricted validation sheets, Drive IDs, local user paths, credentials or row-level discrepancies are included. The SHA-256 manifest is regenerated immediately before tagging `v1.2-paper3`.
