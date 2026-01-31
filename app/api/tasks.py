from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Task
from app.db.session import get_session
from app.schemas.task import TaskCreate, TaskRead
from app.services.task_service import create_task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead)
async def create_task_api(
    data: TaskCreate,
    session: AsyncSession = Depends(get_session),
):
    return await create_task(session, data.original_text)


@router.get("/", response_model=list[TaskRead])
async def list_tasks(
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(Task))
    return result.scalars().all()


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()
    return {"status": "deleted"}
