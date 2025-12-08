# Quick Start Guide

## Installation

### Local Development
```bash
cd /home/ammar/odoo/script/odoo-scaffolder
pip install -e .
```

### From Source (for distribution)
```bash
pip install /path/to/odoo-scaffolder
```

## Usage

Simply run:
```bash
odoo-scaffolder
```

Or use Python directly:
```bash
python -m odoo_scaffolder
```

## Package Structure

```
odoo-scaffolder/
├── LICENSE                      # MIT License
├── MANIFEST.in                  # Package manifest for distribution
├── README.md                    # Full documentation
├── pyproject.toml               # Modern Python package configuration
└── odoo_scaffolder/             # Main package
    ├── __init__.py              # Package entry point
    ├── __main__.py              # CLI implementation
    └── icons/                   # Bundled category icons
        ├── Accounting.png
        ├── HR.png
        ├── Base.png
        ├── Inventory & Procurment.png
        ├── Sales.png
        ├── POS.png
        ├── Manufacturing.png
        ├── Services.png
        ├── Website.png
        └── README.md
```

## Publishing to PyPI

### Test on TestPyPI first
```bash
# Build the package
python -m build

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ odoo-scaffolder
```

### Publish to PyPI
```bash
# Build the package
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

## Development

### Running locally without installation
```bash
cd odoo-scaffolder
python -m odoo_scaffolder
```

### Testing imports
```bash
python -c "from odoo_scaffolder import main; print('Success!')"
```

### Verifying icon paths
```bash
python -c "from odoo_scaffolder.__main__ import get_icon_path; print(get_icon_path('Sales'))"
```

## GitHub Repository Setup

1. Create a new repository on GitHub
2. Repository already created at: https://github.com/a-abuzahra/odoo-scaffolder

## Notes

- Icons are bundled with the package (no internet required)
- Package is installed as `odoo-scaffolder` but imported as `odoo_scaffolder`
- Entry point is `odoo_scaffolder:main` which points to the main() function
- All icon files are included in the distribution via MANIFEST.in
