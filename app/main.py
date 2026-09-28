from fastapi import FastAPI
from pydantic import BaseModel
from typing import TypedDict

app = FastAPI(title='Multi-Agent Coding Assistant')
class Task(BaseModel): request: str

class AgentState(TypedDict):
	request: str
	plan: list[str]
	status: str

def execute(request: str) -> dict:
	from langgraph.graph import END, START, StateGraph
	def planner(state): return {'plan': ['planner: clarify acceptance criteria', 'coder: propose implementation', 'tester: define verification cases']}
	def approval_gate(state): return {'status': 'awaiting_human_approval'}
	graph = StateGraph(AgentState)
	graph.add_node('planner', planner); graph.add_node('approval_gate', approval_gate)
	graph.add_edge(START, 'planner'); graph.add_edge('planner', 'approval_gate'); graph.add_edge('approval_gate', END)
	result = graph.compile().invoke({'request': request, 'plan': [], 'status': 'new'})
	return {**result, 'human_approval_required': True}

@app.get('/health')
def health(): return {'status': 'ok'}
@app.post('/tasks')
def create_task(task: Task): return execute(task.request)
