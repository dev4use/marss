# Test Report (FAILED/SKIPPED)

**Generated**: 2026-05-12 14:59:30

## Summary
- **Total Tests**: 1
- **Passed**: 0
- **Failed**: 1
- **Skipped**: 0
- **Total Duration**: 3.28s

## Test Results

---

### Feature: Générer le site statique
- **File**: `generation.feature`




#### [FAIL] Scenario: transformer le chemin image
- **Status**: FAILED
- **Duration**: 0.01s


**Steps:**

1. [PASS] **Given** j'ai des images en contenu md (0.00s)

2. [PASS] **When** je veux transformer ces chemins (0.00s)

3. [FAIL] **Then** je me retrouve avec des chemins modifiés (0.00s) — `generation.feature:91`
- **Failure Location**: `/home/user/Documents/marss/Tests/Steps/generation.py:221`

- **Error**:
```
fixturefunc = <function visualiser_chemins_transformes at 0x7cfd34507f60>, request = <FixtureRequest for <Function test_changer_chemin_image_md>>
kwargs = {'echanges': {'changer': {'contenu': '(../Media', 'site': '(Media'}, 'contenu': '\n    # ici\n\n    ![dette technique](../Media/dette-technique.png "dette technique")\n    '}}

    def call_fixture_func(
        fixturefunc: _FixtureFunc[FixtureValue], request: FixtureRequest, kwargs
    ) -> FixtureValue:
        if inspect.isgeneratorfunction(fixturefunc):
            fixturefunc = cast(Callable[..., Generator[FixtureValue]], fixturefunc)
            generator = fixturefunc(**kwargs)
            try:
                fixture_result = next(generator)
            except StopIteration:
                raise ValueError(f"{request.fixturename} did not yield a value") from None
            finalizer = functools.partial(_teardown_yield_fixture, fixturefunc, generator)
            request.addfinalizer(finalizer)
        else:
            fixturefunc = cast(Callable[..., FixtureValue], fixturefunc)
>           fixture_result = fixturefunc(**kwargs)
                             ^^^^^^^^^^^^^^^^^^^^^

.venv/lib/python3.12/site-packages/_pytest/fixtures.py:915: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

echanges = {'changer': {'contenu': '(../Media', 'site': '(Media'}, 'contenu': '\n    # ici\n\n    ![dette technique](../Media/dette-technique.png "dette technique")\n    '}

    @then("je me retrouve avec des chemins modifiés")
    def visualiser_chemins_transformes(echanges):
>       actual = remplacerPathMedia(echanges["contenu"], echanges["echanger"])
                                                         ^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'echanger'

Tests/Steps/generation.py:221: KeyError
```

