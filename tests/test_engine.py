from flowpilot.engine import run_workflow
from flowpilot.models import Step, Workflow


def test_runs_all_steps(capsys):
    workflow = Workflow("test", (
        Step("one", "print", {"message": "first"}),
        Step("two", "print", {"message": "second"}),
    ))
    result = run_workflow(workflow)
    assert result.success is True
    assert len(result.steps) == 2
    assert "first" in capsys.readouterr().out


def test_unknown_task_fails_workflow():
    workflow = Workflow("test", (Step("bad", "missing", {}),))
    result = run_workflow(workflow)
    assert result.success is False
    assert result.steps[0].success is False
    assert "Unknown task type" in result.steps[0].error


def test_retries_failed_task(monkeypatch):
    from flowpilot import engine

    calls = {"count": 0}

    def flaky_task(task_type, config):
        calls["count"] += 1
        if calls["count"] < 3:
            raise RuntimeError("temporary issue")

    monkeypatch.setattr(engine, "run_task", flaky_task)
    workflow = Workflow("retry", (Step("flaky", "fake", {}, retries=2),))
    result = run_workflow(workflow)
    assert result.success is True
    assert result.steps[0].attempts == 3
