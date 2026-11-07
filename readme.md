# Traktor Bridge 2.1.0

**Fork Maintainer**: ABUZUCOM
**Repository**: https://github.com/abuzucom/Traktor-Bridge

## Introduction

**Traktor to Pioneer CDJ hardware converter**

Convert Native Instruments Traktor playlists to Pioneer CDJ hardware and Rekordbox formats while preserving supported metadata including cue points, loops, BPM, musical keys, artwork, and Traktor Pro 4 beat-grid data. Native CDJ-2000NXS2 hardware export is supported.

Traktor Bridge 2.1.0 is an application for migrating Traktor collections to Pioneer hardware and Rekordbox software.

## Sources and Attribution

### Fork Maintainer
**ABUZUCOM**
* **GitHub**: [github.com/abuzucom](https://github.com/abuzucom)

### Original Upstream Project
Traktor Bridge by Benoit (BSM) Saint-Moulin: https://github.com/evmmc/Traktor-Bridge
See [NOTICE.md](NOTICE.md) for the upstream licensing status and attribution terms.

## Table of Contents

- [Quick Start](#quick-start)
- [Key Features](#key-features)
- [Visual System](#visual-system)
- [Export Formats](#export-formats)
- [Installation](#installation)
- [Usage](#usage)
- [Hardware Compatibility](#hardware-compatibility)
- [Supported Formats](#supported-formats)
- [Cue Point Translation](#cue-point-translation)
- [Technical Architecture](#technical-architecture)
- [Configuration Options](#configuration-options)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Troubleshooting](#troubleshooting)
- [Traktor Pro 4 Support](#traktor-pro-4-support)
- [Version 2.1.0 Changes](#version-210-changes)
- [Changelog](CHANGELOG.md)
- [Versioning](#versioning)
- [License & Usage](#license--usage)
- [Disclaimers & Warranty](#disclaimers--warranty)

---

![Traktor Bridge Interface](https://github.com/user-attachments/assets/ce3ff950-ebd8-4253-8eaa-ef45e089640a)

## Quick Start

1. **Download** Traktor Bridge 2.1.0
2. **Install dependencies**: `pip install -r requirements.lock`
3. **Run**: `python main.py`

## Key Features

- **Native CDJ hardware support** - Direct CDJ-2000NXS2 binary export with PDB DeviceSQL
- **ANLZ waveform generation** - Creates .DAT/.EXT files for CDJ display
- **Supported metadata preservation** - Artist, title, BPM, musical key, cue points, artwork, and supported Traktor Pro 4 fields
- **Multiple export formats** - CDJ hardware, Rekordbox software, XML, M3U playlists
- **Smart file management** - Automatic file location detection and path sanitization
- **Audio preview** - Built-in player with timeline visualization
- **Batch processing** - Convert multiple playlists simultaneously
- **Cross-platform** - Windows, macOS, Linux support

## Visual System

The interface uses the ABUZUCOM dark theme: Pitch `#0B0B0B`, Charcoal `#242424`, Paper `#EAE7E1`, Concrete `#A6A39D`, and Dull Silver `#74777A`. Display and editorial text use Libre Franklin. Utility text uses Cousine. The tokens live in `ui/brand.py`.

## Export Formats

### CDJ/USB
Native Pioneer CDJ hardware format with binary PDB DeviceSQL database. Creates complete folder structure with ANLZ waveforms for direct CDJ-2000NXS2 USB transfer.

### Rekordbox Database
SQLite/SQLCipher database compatible with Rekordbox software for import via preferences.

### Rekordbox XML
Standard XML format compatible with Rekordbox software import and other DJ applications.

### M3U Playlists
Universal playlist format compatible with most DJ software and media players.

## Installation

**Requirements**: Python 3.13 or newer

```bash
# Install the pinned dependency set
pip install -r requirements.lock
```

## Usage

### GUI Mode
```bash
python main.py
```

1. Select Traktor NML file (usually in `Documents/Native Instruments/Traktor Pro 3/collection.nml`)
2. Optional: Set music root folder for relocated files
3. Choose playlists/folders to convert
4. Select export format (CDJ/USB recommended for hardware)
5. Configure CDJ model and options
6. Convert to destination (USB drive for CDJs)

### CDJ Hardware Requirements

**USB Format**: FAT32 (MBR partition table)  
**File Limits**: ASCII-only filenames, 256 character path maximum  
**Capacity**: Maximum ~10,000 tracks supported by CDJ hardware  
**Structure**: Automatic `/PIONEER/USBANLZ/` folder creation

### Traktor Pro 4 Support

NML versions 19 and 20 are supported, including Traktor Pro 4 collections that use `VERSION="19+"` or `VERSION="20"`. The parser handles flexible beat-grid markers, cue colors, stem metadata, lock metadata, floating-point playtime, and dynamic smart-list/search expressions.

Dynamic smart-list expressions are preserved for inspection but are not evaluated by Traktor Bridge. Static playlist entries are the supported source for exports.

## Hardware Compatibility

**CDJ Players**: CDJ-2000NXS2 (primary), CDJ-2000, CDJ-3000  
**XDJ Players**: XDJ-1000MK2  
**Software**: Rekordbox 6/7, Serato DJ, VirtualDJ, djay Pro, subject to each product's import support

## Supported Formats

**Audio**: MP3, WAV, FLAC, AIFF, M4A, OGG  
**Artwork**: JPEG, PNG, GIF, WebP

## Cue Point Translation

| Traktor | Rekordbox/CDJ | Notes |
|---------|---------------|-------|
| Hot Cue | Hot Cue | Numbered 1-8 |
| Load Cue | Memory Cue | Navigation markers |
| Loop | Loop | Auto-repeat sections |
| Grid Marker | Beat Grid | BPM sync points |

## Technical Architecture

### Modular Export System
- **CDJ PDB Exporter** - Native binary DeviceSQL generation
- **ANLZ Generator** - Waveform files for CDJ display
- **Rekordbox Exporter** - SQLite/SQLCipher database creation
- **XML Exporter** - Standard Rekordbox XML format
- **M3U Exporter** - Universal playlist generation

### Performance Optimization
- **Smart caching** - 30K track limit with 100MB memory management
- **Background processing** - Non-blocking UI with progress tracking  
- **Resource management** - Automatic cleanup and memory optimization
- **Error recovery** - Comprehensive validation and fallback mechanisms

## Configuration Options

**Export Settings**: Format selection, key notation system, file copy options  
**CDJ Settings**: Target CDJ model, ANLZ generation, Rekordbox version  
**Application**: Startup behavior, performance tuning, logging level

## Keyboard Shortcuts

- **Ctrl+O** - Open NML file
- **Ctrl+R** - Reload collection
- **Ctrl+,** - Open preferences
- **F1** - Show usage guide
- **P** - Play/pause selected track

## Troubleshooting

**NML Parse Error**: Close Traktor before conversion  
**CDJ Not Recognizing USB**: Ensure FAT32 format and proper folder structure  
**Files Not Found**: Set music root folder for relocated files  
**Missing Dependencies**: Run `python -m pip install -r requirements.lock`. Some optional native packages may require platform build tools.
**Audio Issues**: Check system audio settings, restart application

## Version 2.1.0 Changes

- **Traktor Pro 4**: NML v20 metadata and playlist parsing, including flexible beat grids and stems
- **Security**: Hardened XML parsing and escaped rich-text log output
- **Reliability**: Explicit export failure reporting and missing-file validation
- **Dependencies**: Exact direct pins and a hashed transitive lockfile
- **Licensing**: MIT license and upstream attribution documented in `LICENSE` and `NOTICE.md`

See the complete [CHANGELOG](CHANGELOG.md).

## Versioning

Traktor Bridge follows [Semantic Versioning 2.0.0](https://semver.org/). The canonical application version is stored in `version.py` and is displayed by the GUI.

## License & Usage

**License**: MIT. The original upstream copyright and attribution are retained; ABUZUCOM holds copyright for fork changes.

See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md) for details.

## Disclaimers & Warranty

**Trademarks**: Pioneer DJ, Rekordbox, CDJ, XDJ are trademarks of Pioneer DJ Corporation. Native Instruments, Traktor are trademarks of Native Instruments GmbH. All trademarks are property of their respective owners.

**No Warranty**: Software provided "AS IS" without warranty of any kind, express or implied, including warranties of merchantability, fitness for purpose, and non-infringement. Author not liable for any damages arising from software use.

**No Affiliation**: Independent tool, not affiliated with, endorsed by, or sponsored by Pioneer DJ Corporation or Native Instruments GmbH. Provided for interoperability and educational purposes only.

**User Responsibility**: Users responsible for data backup before conversion and verifying hardware/software compatibility. Always test CDJ exports on target hardware before live performance use.

**Special thanks** to the Deep Symmetry community and all library maintainers who make tools like this possible.

---

Documentation version 2.1.0 - August 2026

**Maintained by ABUZUCOM**
