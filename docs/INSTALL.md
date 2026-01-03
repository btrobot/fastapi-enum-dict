# FastAPI Enum-Dict - Installation Guide

## Quick Start (5 minutes)

### 1. Install the package

```bash
cd E:\mnvr\apps\backend\fastapi-enum-dict
pip install -e .
```

### 2. Initialize in your FastAPI project

```bash
cd your-fastapi-project
enum-dict init
```

This will create:
- `app/api/` - Enum and Dict API routes
- `app/models/` - Database models
- `app/schemas/` - Pydantic schemas
- `app/core/` - Enum/Dict managers
- `app/data/` - Enum definitions and labels
- `migrations/` - Database initialization script
- `.enum-dict.yaml` - Configuration file

### 3. Integrate with your FastAPI app

Edit `app/main.py`:

```python
from fastapi import FastAPI
from app.api import enums, dicts

app = FastAPI()

# Register routers
app.include_router(enums.router, prefix="/api/enums", tags=["Enum"])
app.include_router(dicts.router, prefix="/api/dicts", tags=["Dict"])
```

### 4. Create your first Enum

```bash
enum-dict create OrderStatus Pending Paid Shipped Completed Cancelled
```

### 5. Start your FastAPI app

```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` to see the auto-generated API!

---

## CLI Commands

### Initialize
```bash
enum-dict init [OPTIONS]

Options:
  --base-dir TEXT   Base directory (default: app)
  --db-url TEXT     Database URL (default: sqlite:///./app.db)
  --force          Overwrite existing files
```

### Create Enum
```bash
enum-dict create <NAME> <VALUE1> <VALUE2> ...

Examples:
  enum-dict create OrderStatus Pending Paid Shipped
  enum-dict create UserRole Admin User Guest
  enum-dict create Gender Male Female Other
```

### List All
```bash
enum-dict list [OPTIONS]

Options:
  --search TEXT     Search keyword
  --type TEXT       Filter by type (enum/dict)

Examples:
  enum-dict list
  enum-dict list --search Status
  enum-dict list --type enum
```

### Show Details
```bash
enum-dict show <NAME>

Examples:
  enum-dict show OrderStatus
  enum-dict show UserRole
```

### Update (Framework)
```bash
enum-dict update <NAME> <OPERATION> [OPTIONS]

Examples:
  enum-dict update OrderStatus add Refunded
  enum-dict update OrderStatus remove 2
  enum-dict update OrderStatus rename Paid to PaymentReceived
```

### Delete (Framework)
```bash
enum-dict delete <NAME> [--force]

Examples:
  enum-dict delete OrderStatus
  enum-dict delete OrderStatus --force
```

---

## Usage in Code

### Using Enums

```python
# Import generated enum
from app.data.enums import Orderstatus
from app.data.enum_labels import get_enum_label, ENUM_METADATA

# Use in model
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    status = Column(Integer)  # Store as integer
    
# Use in code
order = Order(status=Orderstatus.PENDING)

# Get label
label = get_enum_label("Orderstatus", order.status)
# Returns: "Pending"

# Get metadata
meta = ENUM_METADATA["Orderstatus"]
# {
#   "description": "OrderStatus",
#   "type": "enum",
#   "values": [...]
# }
```

### Using API

```python
# In your route
from app.api import enums

@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    order = db.query(Order).filter_by(id=order_id).first()
    
    return {
        "id": order.id,
        "status": order.status,
        "status_label": get_enum_label("Orderstatus", order.status)
    }
```

---

## Database Integration (Dict)

### Initialize Database

```bash
python migrations/init_dict_tables.py
```

This creates:
- `dict_types` table
- `dict_data` table

### Create Dict

```bash
enum-dict create Department --type dict RD QA OPS PM
```

### Use Dict in Code

```python
from app.core.dict_manager import DictManager
from app.models.database import get_db

db = next(get_db())
manager = DictManager(db)

# Create
manager.create("department", "部门", ["研发部", "测试部"])

# List
dicts = manager.list()

# Get
dept = manager.show("department")
```

---

## Configuration

### .enum-dict.yaml

```yaml
base_dir: app
db_url: sqlite:///./app.db
```

You can customize:
- `base_dir`: Where to generate files
- `db_url`: Database connection string

---

## Troubleshooting

### Import Error
```
ModuleNotFoundError: No module named 'app'
```

**Solution**: Make sure you're in the project root directory.

### Template Error
```
jinja2.exceptions.TemplateSyntaxError
```

**Solution**: Reinstall the package:
```bash
cd fastapi-enum-dict
pip install -e . --force-reinstall
```

### Database Error
```
No such table: dict_types
```

**Solution**: Run the migration:
```bash
python migrations/init_dict_tables.py
```

---

## Uninstall

```bash
pip uninstall fastapi-enum-dict
```

To remove generated files:
```bash
rm -rf app/api app/models app/schemas app/core app/data migrations .enum-dict.yaml
```

---

## Next Steps

1. ✅ Install and initialize
2. ✅ Create your first Enum
3. ✅ Explore the generated API
4. ⏳ Read the full documentation
5. ⏳ Customize for your project

**Happy coding!** 🚀
