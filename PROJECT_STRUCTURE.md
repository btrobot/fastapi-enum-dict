# Project Structure

FastAPI Enum-Dict follows GitHub best practices for Python projects.

```
fastapi-enum-dict/
├── .gitignore                      # Git ignore patterns
├── LICENSE                         # MIT License
├── README.md                       # Main documentation (Chinese)
├── CHANGELOG.md                    # Version history
├── CONTRIBUTING.md                 # Contribution guidelines
├── PROJECT_STRUCTURE.md            # This file
├── pyproject.toml                  # Package configuration
├── pytest.ini                      # Pytest configuration
├── requirements-test.txt           # Test dependencies
├── run_tests.py                    # Test runner script
│
├── fastapi_enum_dict/              # Main package
│   ├── __init__.py                 # Package initialization
│   ├── __main__.py                 # CLI entry point
│   │
│   ├── cli/                        # CLI implementation
│   │   ├── __init__.py             # CLI commands registration
│   │   ├── __main__.py             # CLI entry
│   │   ├── init_command.py         # init command
│   │   └── crud_commands.py        # CRUD commands
│   │
│   └── templates/                  # Jinja2 templates (21 files)
│       ├── core_*.py.j2            # Core module templates
│       ├── models_*.py.j2          # Database model templates
│       ├── api_*.py.j2             # API route templates
│       ├── schemas_*.py.j2         # Pydantic schema templates
│       ├── data_*.py.j2            # Data file templates
│       ├── jinja2_*.j2             # Code generation templates
│       └── migration_*.py.j2       # Database migration templates
│
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── test_simple.py              # Basic tests
│   └── test_detector.py            # Detector tests
│
├── docs/                           # Documentation
│   ├── INSTALL.md                  # Installation guide
│   ├── QUICK_START.md              # Quick start guide
│   ├── QUICK_REFERENCE.md          # Quick reference card
│   ├── TESTING_GUIDE.md            # Testing guide
│   ├── UNIT_TESTS_README.md        # Unit tests documentation
│   ├── TESTING_COMPLETE.md         # Testing completion report
│   ├── TEST_RESULTS.md             # Enum test results
│   ├── TEST_RESULTS_FINAL.md       # Final test results
│   ├── DICT_TEST_RESULTS.md        # Dict test results
│   ├── COMPLETE_TEST_SUMMARY.md    # Complete test summary
│   ├── BUG_FIX_REPORT.md           # Bug fix report
│   └── PROJECT_STATUS_FINAL.md     # Final project status
│
└── examples/                       # Usage examples
    ├── README.md                   # Examples documentation
    └── basic_usage.py              # Basic usage example

```

## Key Files

### Root Level

- **README.md** - Main project documentation with quick start guide
- **LICENSE** - MIT License
- **CHANGELOG.md** - Version history following Keep a Changelog format
- **CONTRIBUTING.md** - Guidelines for contributors
- **pyproject.toml** - Package metadata and dependencies (PEP 621)
- **.gitignore** - Git ignore patterns for Python projects

### Source Code

- **fastapi_enum_dict/** - Main package directory
  - CLI commands for init, create, list, show, update, delete
  - 21 Jinja2 templates for code generation
  - Type detection logic

### Tests

- **tests/** - Test suite with pytest
  - Unit tests (100% pass rate)
  - Test configuration in pytest.ini

### Documentation

- **docs/** - Comprehensive documentation
  - User guides (installation, quick start, reference)
  - Developer documentation (testing, project status)
  - Test reports and bug fix documentation

### Examples

- **examples/** - Usage examples
  - Basic usage with FastAPI
  - Enum and Dict integration examples

## File Naming Conventions

- Python files: `snake_case.py`
- Test files: `test_*.py`
- Documentation: `SCREAMING_SNAKE_CASE.md` for important docs, `Title_Case.md` for guides
- Templates: `module_name.py.j2`

## Excluded from Git

See `.gitignore` for complete list:
- `__pycache__/` - Python bytecode
- `*.egg-info/` - Package build artifacts
- `.pytest_cache/` - Pytest cache
- `*.pyc`, `*.pyo` - Compiled Python files
- Build and distribution directories
- Virtual environments
