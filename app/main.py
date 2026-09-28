from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='Multi-Agent Coding Assistant')
class Task(BaseModel): request: str

def plan(request: str) -> list[str]: return ['planner: clarify acceptance criteria', 'coder: propose implementation', 'tester: define verification cases']
def execute(request: str) -> dict: return {'plan': plan(request), 'status': 'planned', 'human_approval_required': True}

@app.get('/health')
def health(): return {'status': 'ok'}
@app.post('/tasks')
def create_task(task: Task): return execute(task.request)
