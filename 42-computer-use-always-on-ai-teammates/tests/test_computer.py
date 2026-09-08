from app.computer import ComputerPolicy, ComputerState, MockComputer

def test_unsafe_action_denied():
    c=MockComputer(ComputerPolicy({'click'},{'click'}))
    try: c.act(ComputerState(),'click'); assert False
    except PermissionError: pass

def test_approved_action_audited():
    s=ComputerState(); c=MockComputer(ComputerPolicy({'click'},{'click'})); c.act(s,'click',{'x':1},approved=True)
    assert s.history[-1]['action']=='click'
