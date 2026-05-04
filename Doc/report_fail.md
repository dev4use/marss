# Test Report (FAILED/SKIPPED)

**Generated**: 2026-05-04 14:28:50

## Summary
- **Total Tests**: 1
- **Passed**: 0
- **Failed**: 1
- **Skipped**: 0
- **Total Duration**: 2.93s

## Test Results

---

### Feature: Générer le site statique
- **File**: `generation.feature`




#### [FAIL] Scenario: afficher les liens des posts précédent et suivant
- **Status**: FAILED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** ma liste comporte 3 posts (0.00s)

2. [PASS] **When** j'affiche le post milieu (0.00s)

3. [FAIL] **Then** j'ai ce résultat <a href="premier.html">premier</a> < ... > <a href="dernier.html">dernier</a> (0.01s) — `generation.feature:115`
- **Failure Location**: `/home/user/Documents/marss/Tests/Steps/generation.py:681`

- **Error**:
```
fixturefunc = <function affichage_liens_suivant_precedent at 0x7e30e5af54e0>
request = <FixtureRequest for <Function test_afficher_liens_precedent_suivant[3-milieu-<a href="premier.html">premier</a> < ... > <a href="dernier.html">dernier</a>]>>
kwargs = {'affichage': '<a href="premier.html">premier</a> < ... > <a href="dernier.html">dernier</a>', 'echanges': {'data': [{... 'url': 'dernier.html'}], 'html': '< <a href="premier.html">premier</a> | ... | <a href="dernier.html">dernier</a> >'}}

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
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

echanges = {'data': [{'label': 'premier', 'url': 'premier.html'}, {'label': 'milieu', 'url': 'milieu.html'}, {'label': 'dernier', 'url': 'dernier.html'}], 'html': '< <a href="premier.html">premier</a> | ... | <a href="dernier.html">dernier</a> >'}
affichage = '<a href="premier.html">premier</a> < ... > <a href="dernier.html">dernier</a>'

    @then(parsers.parse("j'ai ce résultat {affichage}"))
    def affichage_liens_suivant_precedent(echanges, affichage):
>       assert  echanges["html"] ==  affichage
E       assert '< <a href="premier.html">premier</a> | ... | <a href="dernier.html">dernier</a> >' == '<a href="premier.html">premier</a> < ... > <a href="dernier.html">dernier</a>'
E         
E         [0m[91m- <a href="premier.html">premier</a> < ... > <a href="dernier.html">dernier</a>[39;49;00m[90m[39;49;00m
E         ?                                    ^     ^[90m[39;49;00m
E         [92m+ < <a href="premier.html">premier</a> | ... | <a href="dernier.html">dernier</a> >[39;49;00m[90m[39;49;00m
E         ? ++                                   ^     ^                                   ++[90m[39;49;00m

Tests/Steps/generation.py:681: AssertionError
```

