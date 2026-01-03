# Examples

This directory contains usage examples for FastAPI Enum-Dict.

## Files

- `basic_usage.py` - Basic usage examples showing how to use generated Enum and Dict in FastAPI

## How to Use

1. Initialize enum-dict in a FastAPI project:
```bash
cd your-fastapi-project
enum-dict init
```

2. Create some enums and dicts:
```bash
enum-dict create OrderStatus Pending Paid Shipped
enum-dict create Department --type dict RD QA OPS
```

3. Run the example (adapt paths as needed):
```bash
python examples/basic_usage.py
```

## More Examples

For more examples, see:
- [Quick Start Guide](../docs/QUICK_START.md)
- [Quick Reference](../docs/QUICK_REFERENCE.md)
