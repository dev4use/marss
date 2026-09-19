# Test Report (FAILED/SKIPPED)

**Generated**: 2026-05-13 16:18:47

## Summary
- **Total Tests**: 1
- **Passed**: 0
- **Failed**: 1
- **Skipped**: 0
- **Total Duration**: 0.35s

## Test Results

---

### Feature: Générer le site statique
- **File**: `generation.feature`




#### [FAIL] Scenario: gérer les cas anormaux d'extrait
- **Status**: FAILED
- **Duration**: 0.01s


**Steps:**

1. [PASS] **Given** mon post a un contenu avec balises (0.00s)

2. [FAIL] **When** je génère l'extrait du post (0.00s) — `generation.feature:157`

3. [FAIL] **Then** j'ai un résultat sans balises (0.00s) — `generation.feature:158`
- **Failure Location**: `/home/user/Documents/marss/Code/marss.py:291`

- **Error**:
```
fixturefunc = <function generer_extrait at 0x795e75838040>
request = <FixtureRequest for <Function test_extraits_posts_anormaux[un contenu avec balises-sans balises]>>
kwargs = {'echanges': {'contenu': '\n        # titre\n        contenu\n        ## titre 2 \n        '}}

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
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
Tests/Steps/generation.py:238: in generer_extrait
    echanges["resultat"] = extraitDeMarkdown(echanges["contenu"])
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

texte = '\n        # titre\n        contenu\n        ## titre 2 \n        '

    def extraitDeMarkdown(texte):
        """recuperation d'un extrait du chapo sous h1
    
        - prérequis : h1, h2, contenu sous h1
        - entrant : texte markdown
        - sortant : texte avec [...] si tronque, rien si pas de h2
        """
    
        res = texte.splitlines()
        # print("Tableau initial:", res)
        res = list(filter(None, res))
        # print("Tableau nettoye:", res)
        start = [i for i, s in enumerate(res) if s.startswith('# ')]
>       debut = int(start[0])
                    ^^^^^^^^
E       IndexError: list index out of range

Code/marss.py:291: IndexError
```

