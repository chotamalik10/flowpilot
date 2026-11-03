import json

import pytest

from flowpilot.workflow import WorkflowValidationError, load_workflow


def test_load_valid_workflow(tmp_path):
    path = tmp_path / "workflow.json"
    path.write_text(json.dumps({
        "name": "sample",
        "steps": [{"name": "hello", "type": "print", "message": "hi"}],
    }), encoding="utf-8")
    workflow = load_workflow(path)
    assert workflow.name == "sample"
    assert workflow.steps[0].task_type == "print"
    assert workflow.steps[0].config["message"] == "hi"


def test_rejects_empty_steps(tmp_path):
    path = tmp_path / "workflow.json"
    path.write_text('{"name": "empty", "steps": []}', encoding="utf-8")
    with pytest.raises(WorkflowValidationError, match="non-empty"):
        load_workflow(path)


def test_rejects_duplicate_step_names(tmp_path):
    path = tmp_path / "workflow.json"
    path.write_text(json.dumps({
        "name": "duplicate",
        "steps": [
            {"name": "same", "type": "print", "message": "a"},
            {"name": "same", "type": "print", "message": "b"},
        ],
    }), encoding="utf-8")
    with pytest.raises(WorkflowValidationError, match="Duplicate"):
        load_workflow(path)
