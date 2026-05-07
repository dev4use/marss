# Test Report (FAILED/SKIPPED)

**Generated**: 2026-05-07 17:39:13

## Summary
- **Total Tests**: 1
- **Passed**: 0
- **Failed**: 1
- **Skipped**: 0
- **Total Duration**: 2.92s

## Test Results

---

### Feature: Générer le site statique
- **File**: `generation.feature`




#### [FAIL] Scenario: afficher les liens des posts précédent et suivant
- **Status**: FAILED
- **Duration**: 0.01s


**Steps:**

1. [PASS] **Given** ma liste comporte 1 posts (0.00s)

2. [PASS] **When** j'affiche le post premier (0.00s)
- **Failure Location**: `/home/user/Documents/marss/.venv/lib/python3.12/site-packages/_pytest/python.py:166`

- **Error**:
```
E   pytest_bdd.exceptions.StepDefinitionNotFoundError: Step definition is not found: Then "j'ai ce résultat ". Line 115 in scenario "afficher les liens des posts précédent et suivant" in the feature "/home/user/Documents/marss/Tests/Features/generation.feature"
All traceback entries are hidden. Pass `--full-trace` to see hidden and internal frames.
```

