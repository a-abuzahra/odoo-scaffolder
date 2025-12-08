#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Odoo Module Scaffolder
A modern scaffolding tool for creating Odoo modules with best practices.
"""

import sys
import re
import shutil
import tty
import termios
import os


# Category to icon filename mapping
CATEGORY_ICONS = {
    "Accounting": "Accounting.png",
    "HR": "HR.png",
    "Base": "Base.png",
    "Inventory": "Inventory & Procurment.png",
    "Sales": "Sales.png",
    "PoS": "POS.png",
    "Manufacturing": "Manufacturing.png",
    "Services": "Services.png",
    "Website": "Website.png",
}


def get_icon_path(category):
    """Get the path to the bundled icon file for a category."""
    if category not in CATEGORY_ICONS:
        return None

    # Get the package directory
    package_dir = os.path.dirname(os.path.abspath(__file__))
    icon_filename = CATEGORY_ICONS[category]
    icon_path = os.path.join(package_dir, "icons", icon_filename)

    if os.path.exists(icon_path):
        return icon_path
    return None


def copy_icon(source, destination):
    """Copy an icon file from source to destination."""
    try:
        shutil.copy2(source, destination)
        return True
    except Exception as e:
        print(f"\033[33m⚠\033[0m  Warning: Could not copy icon: {str(e)}")
        return False


def get_terminal_width():
    """Get terminal width, default to 80 if unable to determine."""
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80


def getch():
    """Get a single character from user input."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def get_arrow_key():
    """Read arrow key input."""
    ch = getch()
    if ch == '\x1b':  # ESC
        ch = getch()
        if ch == '[':
            ch = getch()
            return ch
    elif ch == '\r' or ch == '\n':
        return 'enter'
    elif ch == '\x03':  # Ctrl+C
        raise KeyboardInterrupt
    return ch


def validate_module_name(name):
    """
    Validate module name according to Odoo conventions.
    Module names should be lowercase, with underscores separating words.
    """
    if not name:
        return False, "Module name cannot be empty"

    if not re.match(r'^[a-z][a-z0-9_]*$', name):
        return False, "Module name must start with a letter and contain only lowercase letters, numbers, and underscores"

    if name.startswith('_'):
        return False, "Module name cannot start with an underscore"

    return True, ""


def prompt_module_name():
    """Prompt user for the module name with Next.js style design."""
    # Cyan question mark with bold question
    sys.stdout.write("\033[36m?\033[0m What is your \033[1;36mmodule name\033[0m? ")

    # Gray placeholder
    placeholder = "my_module"
    sys.stdout.write(f"\033[90m{placeholder}\033[0m")
    sys.stdout.flush()

    # Move cursor back to start of placeholder
    sys.stdout.write("\b" * len(placeholder))
    sys.stdout.flush()

    while True:
        try:
            user_input = input().strip()

            if not user_input:
                # Error message with red X
                print("\033[31m✖ Module name is required\033[0m")
                print()
                # Re-prompt
                sys.stdout.write("\033[36m?\033[0m What is your \033[1;36mmodule name\033[0m? ")
                sys.stdout.write(f"\033[90m{placeholder}\033[0m")
                sys.stdout.flush()
                sys.stdout.write("\b" * len(placeholder))
                sys.stdout.flush()
                continue

            # Validate the module name
            is_valid, error_message = validate_module_name(user_input)

            if is_valid:
                # Move cursor up to replace the question line
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")  # Clear line
                # Print success with green checkmark
                print(f"\033[32m✔\033[0m \033[2mWhat is your module name?\033[0m \033[36m{user_input}\033[0m")
                return user_input
            else:
                # Error message
                print(f"\033[31m✖ {error_message}\033[0m")
                print()
                # Re-prompt
                sys.stdout.write("\033[36m?\033[0m What is your \033[1;36mmodule name\033[0m? ")
                sys.stdout.write(f"\033[90m{placeholder}\033[0m")
                sys.stdout.flush()
                sys.stdout.write("\b" * len(placeholder))
                sys.stdout.flush()

        except EOFError:
            print()
            raise KeyboardInterrupt


def prompt_horizontal_select(question, options, default_index=0):
    """Generic horizontal selection prompt."""
    selected = default_index

    # Print question
    print(f"\033[36m?\033[0m \033[1m{question}\033[0m")

    # Print all options horizontally
    sys.stdout.write("  ")
    for i, option in enumerate(options):
        if i == selected:
            sys.stdout.write(f"\033[36;4m{option}\033[0m")
        else:
            sys.stdout.write(option)
        if i < len(options) - 1:
            sys.stdout.write(" / ")
    sys.stdout.write("\n")
    sys.stdout.flush()

    # Listen for arrow keys
    while True:
        try:
            key = get_arrow_key()

            if key == 'C':  # Right arrow
                if selected < len(options) - 1:
                    selected += 1
            elif key == 'D':  # Left arrow
                if selected > 0:
                    selected -= 1
            elif key == 'enter':
                # Clear the options line
                sys.stdout.write("\033[F\033[K")
                # Clear the question line
                sys.stdout.write("\033[F\033[K")
                # Print success
                print(f"\033[32m✔\033[0m \033[2m{question}\033[0m \033[36m{options[selected]}\033[0m")
                return options[selected]
            else:
                continue

            # Redraw options
            sys.stdout.write("\033[F")  # Move up one line
            sys.stdout.write("\033[K")  # Clear line
            sys.stdout.write("  ")
            for i, option in enumerate(options):
                if i == selected:
                    sys.stdout.write(f"\033[36;4m{option}\033[0m")
                else:
                    sys.stdout.write(option)
                if i < len(options) - 1:
                    sys.stdout.write(" / ")
            sys.stdout.write("\n")
            sys.stdout.flush()

        except KeyboardInterrupt:
            # Clear the options
            sys.stdout.write("\033[F\033[K")
            sys.stdout.write("\033[F\033[K")  # Clear question line
            raise


def prompt_odoo_version():
    """Prompt user for Odoo version with horizontal selection."""
    return prompt_horizontal_select("Which \033[1;36mOdoo version\033[0m?", ["19.0", "18.0", "17.0"], default_index=0)


def prompt_yes_no(question, default=True):
    """Prompt user with Yes/No question."""
    options = ["Yes", "No"]
    default_index = 0 if default else 1
    result = prompt_horizontal_select(question, options, default_index=default_index)
    return result == "Yes"


def prompt_precommit():
    """Prompt user for pre-commit configuration with vertical selection."""
    options = [
        {
            "value": "yes",
            "label": "Yes",
            "description": "adds ruff, black, isort, pylint, and eslint (recommended)"
        },
        {
            "value": "no",
            "label": "No",
            "description": "manual formatting and linting"
        }
    ]
    selected = 0  # Default to Yes

    # Print question
    print("\033[36m?\033[0m Add \033[1;36mpre-commit hooks\033[0m?")

    # Print all options vertically
    for i, option in enumerate(options):
        if i == selected:
            print(f"  \033[36m❯ {option['label']}\033[0m \033[90m- {option['description']}\033[0m")
        else:
            print(f"    {option['label']}")

    # Listen for arrow keys
    while True:
        try:
            key = get_arrow_key()

            if key == 'B':  # Down arrow
                if selected < len(options) - 1:
                    selected += 1
            elif key == 'A':  # Up arrow
                if selected > 0:
                    selected -= 1
            elif key == 'enter':
                # Clear all option lines (1 line per option + question line)
                total_lines = len(options) + 1
                for _ in range(total_lines):
                    sys.stdout.write("\033[F\033[K")
                # Print success
                print(f"\033[32m✔\033[0m \033[2mAdd pre-commit hooks?\033[0m \033[36m{options[selected]['label']}\033[0m")
                return options[selected]['value'] == "yes"
            else:
                continue

            # Redraw options
            sys.stdout.write(f"\033[{len(options)}F")  # Move up to first option
            for i, option in enumerate(options):
                sys.stdout.write("\033[K")  # Clear line
                if i == selected:
                    print(f"  \033[36m❯ {option['label']}\033[0m \033[90m- {option['description']}\033[0m")
                else:
                    print(f"    {option['label']}")

        except KeyboardInterrupt:
            # Clear all lines
            total_lines = len(options) + 1
            for _ in range(total_lines):
                sys.stdout.write("\033[F\033[K")
            raise


def prompt_module_category():
    """Prompt user for module category."""
    categories = [
        "Accounting",
        "HR",
        "Base",
        "Inventory",
        "Sales",
        "PoS",
        "Manufacturing",
        "Services",
        "Website"
    ]
    return prompt_horizontal_select("Which \033[1;36mcategory\033[0m?", categories, default_index=0)


def format_module_title(module_name):
    """Convert module_name to title case (e.g., my_module -> My Module)."""
    return " ".join(word.capitalize() for word in module_name.split("_"))


def create_manifest(config):
    """Generate __manifest__.py content."""
    module_title = format_module_title(config['module_name'])
    version = config['odoo_version']
    category = f"PSAE/{config['category']}"

    manifest = f'''{{
    "name": "{module_title}",
    "summary": "",
    "description": """ """,
    "version": "{version}.1.0.0",
    "category": "{category}",
    "website": "https://www.odoo.com",
    "author": "Odoo PS",
    "license": "OEEL-1",
    "depends": ["base"],
    "data": [],'''

    if config.get('include_demo'):
        manifest += '\n    "demo": [],'

    if config.get('include_src'):
        manifest += '\n    "assets": {},'

    manifest += '\n    "task_ids": [],\n}'

    return manifest


def create_init_file(imports):
    """Create __init__.py content with given imports."""
    if not imports:
        return "# -*- coding: utf-8 -*-\n"
    return "# -*- coding: utf-8 -*-\n\n" + "\n".join(f"from . import {imp}" for imp in imports)


def scaffold_module(config):
    """Create the Odoo module structure based on configuration."""
    module_name = config['module_name']
    base_path = os.path.join(os.getcwd(), module_name)

    # Create base module directory
    os.makedirs(base_path, exist_ok=True)

    # Track subdirectories for root __init__.py
    root_imports = []

    # Always create models and views
    models_path = os.path.join(base_path, "models")
    os.makedirs(models_path, exist_ok=True)
    with open(os.path.join(models_path, "__init__.py"), "w") as f:
        f.write(create_init_file([]))
    root_imports.append("models")

    views_path = os.path.join(base_path, "views")
    os.makedirs(views_path, exist_ok=True)

    # Create data directory if needed
    if config.get('include_data'):
        data_path = os.path.join(base_path, "data")
        os.makedirs(data_path, exist_ok=True)

    # Create security directory if needed
    if config.get('include_security'):
        security_path = os.path.join(base_path, "security")
        os.makedirs(security_path, exist_ok=True)
        # Create empty ir.model.access.csv file
        with open(os.path.join(security_path, "ir.model.access.csv"), "w") as f:
            f.write("id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink\n")

    # Create controllers directory if needed
    if config.get('include_controllers'):
        controllers_path = os.path.join(base_path, "controllers")
        os.makedirs(controllers_path, exist_ok=True)
        with open(os.path.join(controllers_path, "__init__.py"), "w") as f:
            f.write(create_init_file([]))
        root_imports.append("controllers")

    # Create wizards directory if needed (let's add this as an option)
    # For now, we'll skip wizards unless explicitly requested

    # Create tests directory if needed
    if config.get('include_tests'):
        tests_path = os.path.join(base_path, "tests")
        os.makedirs(tests_path, exist_ok=True)
        with open(os.path.join(tests_path, "__init__.py"), "w") as f:
            f.write(create_init_file([]))

    # Create demo directory if needed
    if config.get('include_demo'):
        demo_path = os.path.join(base_path, "demo")
        os.makedirs(demo_path, exist_ok=True)

    # Create reports directory if needed
    if config.get('include_reports'):
        reports_path = os.path.join(base_path, "reports")
        os.makedirs(reports_path, exist_ok=True)
        with open(os.path.join(reports_path, "__init__.py"), "w") as f:
            f.write(create_init_file([]))
        root_imports.append("reports")

    # Create static/src directory if requested (for JS/CSS assets)
    if config.get('include_src'):
        static_src_path = os.path.join(base_path, "static", "src")
        os.makedirs(static_src_path, exist_ok=True)

    # Create icon if needed
    if config.get('include_icon'):
        static_desc_path = os.path.join(base_path, "static", "description")
        os.makedirs(static_desc_path, exist_ok=True)

        # Copy category-specific icon from bundled icons
        category = config.get('category')
        source_icon_path = get_icon_path(category)
        if source_icon_path:
            dest_icon_path = os.path.join(static_desc_path, "icon.png")
            copy_icon(source_icon_path, dest_icon_path)

    # Create root __init__.py
    with open(os.path.join(base_path, "__init__.py"), "w") as f:
        f.write(create_init_file(root_imports))

    # Create __manifest__.py
    with open(os.path.join(base_path, "__manifest__.py"), "w") as f:
        f.write(create_manifest(config))

    # Create pre-commit configuration if needed
    if config.get('add_precommit'):
        create_precommit_config(base_path)

    return base_path


def create_precommit_config(base_path):
    """Create .pre-commit-config.yaml file."""
    precommit_content = '''repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/psf/black
    rev: 24.2.0
    hooks:
      - id: black

  - repo: https://github.com/PyCQA/pylint
    rev: v3.0.3
    hooks:
      - id: pylint
        args: [--disable=all, --enable=unused-import]

  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v9.0.0
    hooks:
      - id: eslint
        files: \\.(js|jsx)$
        types: [file]
'''

    with open(os.path.join(base_path, ".pre-commit-config.yaml"), "w") as f:
        f.write(precommit_content)


def main():
    """Main scaffolder function."""
    try:
        print()  # Initial spacing

        # Collect all configuration
        config = {}

        # Prompt: Module name
        config['module_name'] = prompt_module_name()

        # Prompt: Use defaults?
        use_defaults = prompt_yes_no("Use \033[1;36mdefaults\033[0m?", default=True)

        # Always ask for version and category
        config['odoo_version'] = prompt_odoo_version()
        config['category'] = prompt_module_category()

        if use_defaults:
            # Apply default configuration
            config['include_demo'] = False
            config['include_tests'] = True
            config['include_security'] = True
            config['include_reports'] = False
            config['include_controllers'] = False
            config['include_data'] = False
            config['include_src'] = False
            config['include_icon'] = True
            config['add_precommit'] = True
        else:
            # Ask each question individually
            config['include_demo'] = prompt_yes_no("Include \033[1;36mdemo data\033[0m?", default=False)
            config['include_tests'] = prompt_yes_no("Include \033[1;36mtests\033[0m?", default=True)
            config['include_security'] = prompt_yes_no("Include \033[1;36msecurity files\033[0m?", default=True)
            config['include_reports'] = prompt_yes_no("Include \033[1;36mreports\033[0m?", default=False)
            config['include_controllers'] = prompt_yes_no("Include \033[1;36mcontrollers\033[0m?", default=False)
            config['include_data'] = prompt_yes_no("Include \033[1;36mdata directory\033[0m?", default=False)
            config['include_src'] = prompt_yes_no("Include \033[1;36mstatic/src directory\033[0m?", default=False)
            config['include_icon'] = prompt_yes_no("Include \033[1;36micon\033[0m?", default=True)
            config['add_precommit'] = prompt_precommit()

        print()  # Final spacing

        # Generate the module structure
        print("\033[36m⚙\033[0m  Creating module structure...")
        module_path = scaffold_module(config)
        print(f"\033[32m✔\033[0m  Module created successfully at: \033[36m{module_path}\033[0m")
        print()

    except KeyboardInterrupt:
        print("\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n\033[31m✖ Error:\033[0m {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
