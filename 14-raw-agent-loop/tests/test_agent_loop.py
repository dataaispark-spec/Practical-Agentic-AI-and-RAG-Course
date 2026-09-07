from app.agent_loop import AgentLoop, AgentState, Decision, DecisionType

def test_tool_then_final():
    def decide(s):
        return Decision(DecisionType.FINAL) if s.tool_results else Decision(DecisionType.TOOL, tool='lookup', args={'x':2})
    state=AgentLoop(decide, {'lookup':lambda x:x*2}, max_steps=5).run(AgentState('calculate'))
    assert state.tool_results == [4]
    assert state.termination_reason == 'verified_final'

def test_step_budget():
    def decide(s): return Decision(DecisionType.REFLECT, reason='again')
    state=AgentLoop(decide, {}, max_steps=3).run(AgentState('loop'))
    assert state.termination_reason in {'step_budget','repeated_state','reflection_budget'}

def test_invalid_tool():
    def decide(s): return Decision(DecisionType.TOOL, tool='missing')
    state=AgentLoop(decide, {}, max_steps=2).run(AgentState('x'))
    assert state.termination_reason == 'invalid_tool'
