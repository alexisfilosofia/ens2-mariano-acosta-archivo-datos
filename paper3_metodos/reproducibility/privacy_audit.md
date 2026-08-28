# Privacy audit for `v1.1-paper3`

Date: 2026-08-27

## Scope

Audited paths:

- `paper3_metodos/`
- `CITATION.cff`
- `LICENSE.md`
- root `README.md`
- `index.html`

This audit was refreshed after the final editorial cleanup of `main` following publication of `v1.1-paper3`. No row-level validation data were used.

## Automated checks

The audit scanned text-based release files for:

- email addresses;
- personal local paths, mounted-volume paths and cloud document URLs;
- credential markers and authentication string formats;
- latitude/longitude coordinate pairs;
- street-address-like patterns;
- private file ID hints.

Result: **0 findings** across 18 text-based files.

## Sensitive-term review

The release also searched for terms related to:

- names of students;
- names of parents or tutors;
- domiciles and addresses;
- coordinates;
- photographs;
- full validation sheets;
- row-level discrepancies;
- restricted bases;
- `IDEM` handling.

Result: terms related to people, addresses, coordinates, photographs and restricted validation appear only in privacy statements, methodological exclusions, or aggregate-field descriptions. No student names, parent/tutor names, individual addresses, individual coordinates, archival photographs, row-level discrepancies, complete validation tables, private file IDs, tokens or credentials were found.

Allowed proper names present in the release:

- Alexis Marcelo Perissé, as author;
- Mariano Acosta, as the institutional name;
- Armenia Euredjian, as the archive name.

## Public-release decision

The materials in `paper3_metodos/` and the updated public landing page are suitable for public release as aggregate methodological documentation and divulgation materials. Version `v1.1-paper3` remains the scientific release in force; restricted row-level data and archival images remain outside the repository.
