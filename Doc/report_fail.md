# Test Report (FAILED/SKIPPED)

**Generated**: 2026-04-11 17:38:18

## Summary
- **Total Tests**: 1
- **Passed**: 0
- **Failed**: 1
- **Skipped**: 0
- **Total Duration**: 2.69s

## Test Results

---

### Feature: Générer le site statique
- **File**: `generation.feature`




#### [FAIL] Scenario: créer le fichier html de l'accueil
- **Status**: FAILED
- **Duration**: 0.01s


**Steps:**

1. [PASS] **Given** la page d'accueil est en configuration (0.00s)

2. [FAIL] **When** je souhaite créer le fichier html de la page d'accueil (0.00s) — `generation.feature:126`

3. [FAIL] **Then** le fichier créé s'appelle index.html (0.00s) — `generation.feature:127`
- **Failure Location**: `/home/user/Documents/marss/Tests/Steps/generation.py:615`

- **Error**:
```
fixturefunc = <function creer_accueil_html at 0x7df791744540>, request = <FixtureRequest for <Function test_creer_page_index>>
kwargs = {'echanges': {}}

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
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

echanges = {}

    @when("je souhaite créer le fichier html de la page d'accueil")
    def creer_accueil_html(echanges):
        """
        forcer le nom de la page
        """
        html = """
        <html>
        <head><title>accueil'</title></head>
        <body>accueil</body>
        </html>
        """
>       fichier = echanges['conf']['outputPath'] + 'index.html'
                  ^^^^^^^^^^^^^^^^
E       KeyError: 'conf'

Tests/Steps/generation.py:615: KeyError
```

