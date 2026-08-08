# Changelog

All notable changes to Traktor Bridge are documented here.

This project follows [Semantic Versioning 2.0.0](https://semver.org/):

- **MAJOR**: incompatible public API changes
- **MINOR**: backward-compatible functionality
- **PATCH**: backward-compatible fixes

## [Unreleased]

Changes planned for the next release will be listed here.

## [2.1.0] - 2026-08-08

### Added

- Traktor Pro 4/NML v20 parsing support, including flexible beat grids, cue colors, stem metadata, lock metadata, and floating-point playtime.
- Preservation of dynamic smart-list and search expressions during parsing.
- Traktor Pro 4 parser regression test coverage.
- Hashed dependency lockfile in `requirements.lock`.
- `converter_config.example.json` for first-run configuration.

### Changed

- Adopted SemVer with the canonical application version in `version.py`.
- Applied the ABUZUCOM dark visual system with Libre Franklin and Cousine typography.
- Removed improvised emoji and color treatments from the interface.
- Updated ABUZUCOM branding, repository links, licensing, attribution, and documentation.
- Exporters now report failed operations instead of silently returning success.

### Fixed

- Escaped log messages before rendering them as rich text.
- Improved handling of missing source files and failed export writes.

### Security

- Hardened NML XML parsing against external entities, DTDs, network access, and oversized XML trees.
- Added `.gitignore` coverage for local configuration, logs, caches, virtual environments, and generated exports.

### Documentation

- Documented the current Python 3.13+ setup, cross-platform usage, supported NML versions, and known T4 limitations.

[Unreleased]: https://github.com/abuzucom/Traktor-Bridge/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/abuzucom/Traktor-Bridge/releases/tag/v2.1.0
