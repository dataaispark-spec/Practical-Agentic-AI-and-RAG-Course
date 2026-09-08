from app.loop_engine import LoopState, ProductionLoop, Phase

def test_loop_verifies_and_stops():
    def decide(s): return {'type':'tool','tool':'lookup','args':{'x':21}} if not s.observations else {'type':'final'}
    loop=ProductionLoop(decide, {'lookup':lambda x:x*2}, lambda s: bool(s.observations), max_steps=8)
    state=loop.run(LoopState('answer'))
    assert state.verified and state.reason=='verified'

def test_loop_has_hard_budget():
    loop=ProductionLoop(lambda s:{'type':'tool','tool':'lookup','args':{'x':1}}, {'lookup':lambda x:x}, lambda s:False, max_steps=3)
    state=loop.run(LoopState('never'))
    assert state.reason in {'step_budget','no_progress','recovery_budget'}
