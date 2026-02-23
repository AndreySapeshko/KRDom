from backend.domain.ar.validators.validate_concept import validate_concept


def test_missing_required_window_detected(concept_missing_window, brief_with_required_window):
    issues = validate_concept(brief_with_required_window, concept_missing_window)

    assert len(issues.issues) > 0

    messages = [i.message for i in issues.issues]
    assert any("WIN1" in msg for msg in messages)
