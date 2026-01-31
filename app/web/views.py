from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_session
from app.db.models import Task
from app.services.task_service import create_task, update_task

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def list_tasks(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(Task).order_by(Task.created_at.desc()))
    tasks = result.scalars().all()

    return templates.TemplateResponse(
        "tasks.html",
        {"request": request, "tasks": tasks},
    )


@router.get("/tasks/new")
async def new_task_form(request: Request):
    return templates.TemplateResponse(
        "create_task.html",
        {"request": request},
    )


@router.post("/tasks/new")
async def create_task_web(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    form = await request.form()
    text = form.get("original_text")

    if not text:
        raise HTTPException(status_code=400, detail="Task text is required")

    await create_task(session, text)

    return RedirectResponse("/", status_code=303)


@router.get("/tasks/{task_id}")
async def task_detail(
    task_id: int,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    subtasks = []
    if task.subtasks:
        subtasks = [s.strip() for s in task.subtasks.split(";") if s.strip()]

    return templates.TemplateResponse(
        "task_detail.html",
        {
            "request": request,
            "task": task,
            "subtasks": subtasks,
        },
    )

@router.get("/tasks/{task_id}/edit")
async def edit_task_form(
    task_id: int,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return templates.TemplateResponse(
        "edit_task.html",
        {"request": request, "task": task},
    )


@router.post("/tasks/{task_id}/edit")
async def edit_task_submit(
    task_id: int,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    form = await request.form()
    new_text = form.get("original_text")

    if not new_text:
        raise HTTPException(status_code=400, detail="Task text is required")

    await update_task(session, task, new_text)

    return RedirectResponse(f"/tasks/{task.id}", status_code=303)

@router.post("/tasks/{task_id}/delete")
async def delete_task_web(
    task_id: int,
    session: AsyncSession = Depends(get_session),
):
    task = await session.get(Task, task_id)
    if task:
        await session.delete(task)
        await session.commit()

    return RedirectResponse("/", status_code=303)
