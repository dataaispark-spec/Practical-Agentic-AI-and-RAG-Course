from app.skill_registry import Skill, SkillRegistry

def test_candidate_requires_gate():
    r=SkillRegistry(); r.register(Skill('debug','1',.8))
    try: r.promote('debug','1'); assert False
    except ValueError: pass

def test_high_confidence_promotes():
    r=SkillRegistry(); r.register(Skill('debug','1',.95)); assert r.promote('debug','1').status=='trusted'
