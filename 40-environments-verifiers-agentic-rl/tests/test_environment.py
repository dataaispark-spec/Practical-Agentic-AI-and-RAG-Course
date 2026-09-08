from app.environment import Environment

def test_verifier_controls_reward():
    env=Environment(lambda s,a:s+a, lambda a,o:o==3)
    e=env.step(1,2); assert e.verified and e.reward==1.0
    e=env.step(1,1); assert not e.verified and e.reward==0.0
