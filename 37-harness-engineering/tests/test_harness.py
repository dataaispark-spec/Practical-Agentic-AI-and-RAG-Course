from app.harness import Harness, HarnessState

def test_harness_enforces_policy():
    h=Harness(lambda t,c:{'type':'tool','tool':'danger'}, {'danger':lambda:1}, lambda d:False)
    try: h.step(HarnessState('x')); assert False
    except PermissionError: pass

def test_harness_executes_allowed_tool():
    h=Harness(lambda t,c:{'type':'tool','tool':'lookup','args':{'x':2}}, {'lookup':lambda x:x*3}, lambda d:True)
    s=h.step(HarnessState('x'))
    assert s.context[-1]['result']==6 and s.tool_calls==1
