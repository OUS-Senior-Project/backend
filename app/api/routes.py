from fastapi import APIRouter, HTTPException

from app.models.item import Item

router = APIRouter()

# In-memory "database"
items_db = []


@router.get("/items", response_model=list[Item])
def get_items():
    return items_db


@router.post("/items", response_model=Item)
def create_item(item: Item):
    # Prevent duplicate IDs
    for existing in items_db:
        if existing.id == item.id:
            raise HTTPException(status_code=400, detail="Item ID already exists")

    items_db.append(item)
    return item


@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            items_db.remove(item)
            return {"message": "Item deleted"}

    raise HTTPException(status_code=404, detail="Item not found")
