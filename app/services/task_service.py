from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Task
from app.services.ai_service import analyze_task

def fallback_analysis(text: str):
    return {
        "title": text[:60] + ("..." if len(text) > 60 else ""),
        "priority": "Medium",
        "category": "Other",
        "estimated_minutes": 30,
        "subtasks": ["This subtask was created due to an error. Try again later."],
    }

async def create_task(session: AsyncSession, text: str) -> Task:
    try:
        analysis = analyze_task(text)
        data = analysis.model_dump()
    except Exception as e:
        print(f"[AI FALLBACK] {e}")
        data = fallback_analysis(text)

    task = Task(
        original_text=text,
        title=data["title"],
        priority=data["priority"],
        category=data["category"],
        estimated_minutes=data["estimated_minutes"],
        subtasks="; ".join(data["subtasks"]),
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def update_task(session: AsyncSession, task: Task, text: str) -> Task:
    try:
        analysis = analyze_task(text)
        data = analysis.model_dump()
    except Exception as e:
        print(f"[AI FALLBACK] {e}")
        data = fallback_analysis(text)

    task.original_text = text
    task.title = data["title"]
    task.priority = data["priority"]
    task.category = data["category"]
    task.estimated_minutes = data["estimated_minutes"]
    task.subtasks = "; ".join(data["subtasks"])

    await session.commit()
    return task
