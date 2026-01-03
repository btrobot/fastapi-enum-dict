"""
FastAPI Enum-Dict Basic Usage Example

This example shows how to use the generated Enum and Dict in a FastAPI application.
"""
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

# Assuming you've run: enum-dict init --base-dir app
# And created some enums/dicts

app = FastAPI(title="Enum-Dict Example")


# Example 1: Using Enum
def example_enum():
    """Example of using generated Enum"""
    from app.data.enums import OrderStatus
    from app.data.enum_labels import get_enum_label
    
    # Use enum value
    status = OrderStatus.PAID
    
    # Get label
    label = get_enum_label("OrderStatus", status.value)
    
    return {
        "status_value": status.value,
        "status_name": status.name,
        "status_label": label
    }


# Example 2: Using Dict with Database
def example_dict(db: Session):
    """Example of using Dict from database"""
    from app.core.dict_manager import DictManager
    
    manager = DictManager(db)
    
    # List all dicts
    dicts = manager.list()
    
    # Show specific dict
    dept = manager.show("department")
    
    return {
        "all_dicts": dicts,
        "department_detail": dept
    }


# Example 3: API Endpoint with Enum
@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    """Get order with status"""
    from app.data.enums import OrderStatus
    from app.data.enum_labels import get_enum_label
    
    # Mock order data
    order = {
        "id": order_id,
        "status": OrderStatus.PAID.value,
    }
    
    # Add label
    order["status_label"] = get_enum_label("OrderStatus", order["status"])
    
    return order


# Example 4: API Endpoint with Dict
@app.get("/departments")
async def list_departments():
    """List all departments from dict"""
    from app.models.database import get_db
    from app.core.dict_manager import DictManager
    
    db = next(get_db())
    manager = DictManager(db)
    
    result = manager.show("department")
    
    return result.get("values", [])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
