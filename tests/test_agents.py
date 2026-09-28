from app.main import execute

def test_agent_plan_requires_human_approval():
    result = execute('add rate limiting')
    assert result['status'] == 'planned'
    assert result['human_approval_required'] is True
    assert len(result['plan']) == 3
