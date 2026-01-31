from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Task
from app.services.ai_service import analyze_task


async def create_task(session: AsyncSession, text: str) -> Task:
    analysis = analyze_task(text)

    task = Task(
        original_text=text,
        title=analysis.title,
        priority=analysis.priority,
        category=analysis.category,
        estimated_minutes=analysis.estimated_minutes,
        subtasks="; ".join(analysis.subtasks),
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def update_task(session: AsyncSession, task: Task, text: str) -> Task:
    analysis = analyze_task(text)

    task.original_text = text
    task.title = analysis.title
    task.priority = analysis.priority
    task.category = analysis.category
    task.estimated_minutes = analysis.estimated_minutes
    task.subtasks = "; ".join(analysis.subtasks)

    await session.commit()
    return task
