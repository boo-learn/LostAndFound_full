import schemas
import models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.LostItem)
async def create_lost_item(item: schemas.LostItemCreate, db: AsyncSession = Depends(get_db)):
    db_item = models.LostItem(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.get("/", response_model=list[schemas.LostItem])
async def read_lost_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.LostItem))
    items = result.scalars().all()
    return items


@router.get("/{item_id}", response_model=schemas.LostItem)
async def read_lost_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await db.get(models.LostItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/search", response_model=list[schemas.LostItem])
async def search_lost_items(query: str, db: AsyncSession = Depends(get_db)):
    """
    Вернет список потерянных предметов, у которых имя, описание или местоположение содержат слово query.
    """
    results = await db.execute(
        select(models.LostItem).where(
            or_(
                models.LostItem.name.ilike(f"%{query}%"),
                models.LostItem.description.ilike(f"%{query}%"),
                models.LostItem.location.ilike(f"%{query}%"),
            )
        )
    )
    items = results.scalars().all()
    return items


@router.put("/{item_id}", response_model=schemas.LostItem)
async def update_lost_item(item_id: int, item: schemas.LostItemUpdate, db: AsyncSession = Depends(get_db)):
    db_item = await db.get(models.LostItem, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in item.model_dump(exclude_none=True).items():
        setattr(db_item, field, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.delete("/{item_id}")
async def delete_lost_item(item_id: int, db: AsyncSession = Depends(get_db)):
    db_item = await db.get(models.LostItem, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(db_item)
    await db.commit()
    return {"message": "Item deleted"}
