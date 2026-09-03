# Privacy audit for `v1.2-paper3` and the post-v1.2 sampling addendum

Initial audit date: 2026-09-01  
Sampling addendum audit date: 2026-09-03

## Scope

The initial audit scanned the repository's 24 text-based files after applying the v1.2 patch and before publishing `v1.2-paper3`. The addendum reviewed the 26 text-based files expected on `main` after adding the public sampling specification and verifier.

## Automated checks

The scan checked for email addresses, Google Drive/Docs URLs, local filesystem paths, credential markers, coordinate-like pairs, restricted-file markers, row-level discrepancy references and publication of sample membership identifiers.

The initial scan produced four coordinate-like alerts, all in public map files:

- `assets/mapas/mapa-calor-publico.html`
- `assets/mapas/mapa-domicilios-publico.html`

Manual review confirms that these coordinates are public aggregate grid cells, the map center and the institutional marker for ENS N.º 2 "Mariano Acosta"; they are not individual student coordinates or exact domiciles.

The sampling addendum adds three SHA-256 commitments: one for the ordered restricted frame and one for each complete membership set. These digests do not publish member identifiers or support testing the inclusion of a single record. The verifier reports only counts, nesting and pass/fail status.

## Sensitive-term review

Terms related to students, tutors, addresses, coordinates, photographs, restricted validation sheets and row-level discrepancies appear only in privacy statements, methodological exclusions, aggregate field descriptions, public aggregate-map metadata or generic command-line placeholders.

Allowed proper names present in the public materials are Alexis Marcelo Perissé as author, Mariano Acosta as the institutional name and Armenia Euredjian as the archive name.

## Public-release decision

Result: no privacy findings. No student/tutor names, row-level addresses, individual coordinates, archival images, restricted validation sheets, Drive IDs, local user paths, credentials, row-level discrepancies or membership lists are included. The baseline, closed workbook and the mapping between deterministic internal identifiers and documentary locations remain restricted.

The SHA-256 manifest is regenerated after the addendum files are finalized and before the next archived release.
