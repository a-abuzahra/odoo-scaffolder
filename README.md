# Odoo Scaffolder

A modern, interactive scaffolding tool for creating Odoo modules with best practices. Inspired by Next.js's beautiful CLI interface.

## Features

- **Interactive CLI**: Beautiful terminal interface with arrow key navigation
- **Smart Defaults**: Quick setup with sensible defaults or customize everything
- **Best Practices**: Follows Odoo module structure conventions
- **Category Icons**: Automatically downloads category-specific icons
- **Pre-commit Support**: Optional pre-commit hooks with ruff, black, isort, pylint, and eslint
- **Flexible Structure**: Choose what to include (tests, security, controllers, etc.)

## Installation

### From PyPI (once published)

```bash
pip install odoo-scaffolder
```

### From Source

```bash
git clone https://github.com/a-abuzahra/odoo-scaffolder.git
cd odoo-scaffolder
pip install -e .
```

## Usage

Simply run the command and follow the interactive prompts:

```bash
odoo-scaffolder
```

### What You'll Be Asked

1. **Module Name**: The technical name for your module (e.g., `my_custom_module`)
2. **Use Defaults?**: Skip most questions with smart defaults
3. **Odoo Version**: Choose between 19.0, 18.0, or 17.0
4. **Category**: Select from Accounting, HR, Base, Inventory, Sales, PoS, Manufacturing, Services, or Website

If you choose not to use defaults, you'll also be asked about:
- Demo data
- Tests
- Security files
- Reports
- Controllers
- Data directory
- Static/src directory (for JS/CSS assets)
- Module icon
- Pre-commit hooks

## Module Structure

The scaffolder creates a standard Odoo module structure:

```
my_module/
├── __init__.py
├── __manifest__.py
├── models/
│   └── __init__.py
├── views/
├── security/                  # Optional
│   └── ir.model.access.csv
├── controllers/               # Optional
│   └── __init__.py
├── data/                      # Optional
├── demo/                      # Optional
├── tests/                     # Optional
│   └── __init__.py
├── reports/                   # Optional
│   └── __init__.py
├── static/
│   ├── description/          # Optional (with icon)
│   │   └── icon.png
│   └── src/                  # Optional (for JS/CSS)
└── .pre-commit-config.yaml   # Optional
```

## Icons

The scaffolder includes bundled category-specific icons that are automatically copied to your module when you choose to include an icon. Icons are stored in the `odoo_scaffolder/icons/` directory and are distributed with the package.

## Defaults

When using defaults, the following are included:
- ✅ Tests
- ✅ Security files
- ✅ Module icon
- ✅ Pre-commit hooks
- ❌ Demo data
- ❌ Reports
- ❌ Controllers
- ❌ Data directory
- ❌ Static/src directory

## Pre-commit Hooks

When enabled, the scaffolder creates a `.pre-commit-config.yaml` with:
- **ruff**: Fast Python linter
- **black**: Code formatter
- **isort**: Import sorter
- **pylint**: Code analyzer
- **eslint**: JavaScript linter

To use pre-commit hooks after scaffolding:

```bash
cd my_module
pip install pre-commit
pre-commit install
```

## Requirements

- Python 3.7+

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Odoo PS Team
