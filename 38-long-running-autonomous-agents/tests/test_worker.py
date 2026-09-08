from app.worker import DurableJob, DurableWorker, Status

def test_resume_does_not_duplicate_effects():
    calls=[]; w=DurableWorker(lambda k:calls.append(k) or k); j=DurableJob('j','goal')
    w.run(j,3); j.status=Status.CREATED; w.run(j,3)
    assert calls==['j:0','j:1','j:2'] and j.status is Status.COMPLETED
