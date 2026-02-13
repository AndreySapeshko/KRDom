from backend.domain.ar.validators.validate_concept import validate_concept


def test_valid_concept_has_no_issues(valid_concept, empty_brief):

    issues = validate_concept(empty_brief, valid_concept)
    print(f"PRINT assert issues: {issues}")

    assert issues.issues == []
