# AI-assisted troubleshooting labs

These exercises implement the three handouts in
[Kaleakash/cicso_testing_repo](https://github.com/Kaleakash/cicso_testing_repo/tree/main/Assisted_Practice_Demo_Examples/3.AI-Assisted%20Troubleshooting/New):

- `GitHub_Copilot_Debugging_Lab_Ask_Edit_Agent.pdf` (Demo 04)
- `Demo_05_Log_Analysis_GitHub_Copilot_Updated.pdf`
- `Demo_06_Alert_Explain_Endpoint_GitHub_Copilot_Updated.pdf`

## Demo 04: runtime errors

`buggy_functions.py` keeps the handout's filename but contains the corrected
functions. The original implementation was exercised before applying fixes.

| Original failure | Cause | Targeted fix |
|---|---|---|
| `TypeError: can only concatenate str (not "int") to str` | Adding an integer count directly to a string | Use an f-string |
| `KeyError: 'network-team'` | Looking up an absent team with dictionary indexing | Use `dict.get()` with `"Unassigned"` |
| `ZeroDivisionError: division by zero` | Dividing by the length of an empty list | Return `0.0` for an empty list |

`get_alert_owner()` still requires `alert["owner"]`, as in the handout.
The fallback covers an owner absent from the team directory; it does not
silently accept a malformed alert without its required owner key.

From this directory:

```bash
python3 buggy_functions.py
python3 -m pytest test_fixed_functions.py -v
```

The script prints:

```text
There are 3 critical alerts active.
Unassigned
0.0
```

The suite includes the five handout tests plus four boundary cases:
zero alerts, an empty team directory, one response time, and all-zero
response times. Install `pytest` in your active virtual environment if needed.

## Demo 05: log analysis

`app.log` is the handout's complete synthetic sample, not a runtime log
from this checkout. `log_analysis_report.md` contains the chronological
summary, distinct error counts, raw timestamps, separate warnings,
limitations, and independent verification commands.

The sample has five AttributeErrors and one separate HTTP 404.
Neither retry success nor a causal link to database pool usage is proven.

## Demo 06: API reproduction and repair

The existing project is `../alert_explainer_api`; no duplicate API was created.

1. The original seven API tests passed.
2. Temporarily adding `resolved_by.upper()` to the explanation reproduced
   three failing API tests and a live HTTP 500.
3. The captured Uvicorn traceback ended with
   `NameError: name 'resolved_by' is not defined`.
4. The new acknowledgement regression test failed before the repair.
5. The repair defines a local `"Not yet acknowledged"` string and includes
   it in the explanation. Threshold and severity logic, schemas, routes,
   and the database model are unchanged.

The model has no `resolved_by` field, so Python cannot resolve that name.
This differs from calling `.upper()` on a defined variable whose value is
`None`, which would raise the AttributeError shown in Demo 05.

Run the API suite from its own directory:

```bash
cd ../alert_explainer_api
python3 -m pytest tests/test_alerts.py -v
```

Use the API README to install dependencies and start Uvicorn. Create an
alert with `POST /alerts/`, then use its returned ID for
`POST /alerts/{id}/explain`. The response should be HTTP 200 and contain
`Acknowledged by: Not yet acknowledged.`

The live reproduction uses an isolated temporary database, not the existing
`alerts.db`. Copilot editor modes and screenshots are UI demonstrations;
they are not programmatically verified by these CLI exercises.

## Recorded verification

The completed exercises were verified on 2026-11-18:

- All eight API tests and all nine Python-function tests passed.
- All nine severity/threshold combinations preserved their original
  recommendations and comparisons, with the acknowledgement appended.
- The repaired live endpoint returned HTTP 200 with the default message.
- All 25 sample-log lines matched the PDF; independent counts returned
  five AttributeErrors, one 404, six ERROR entries, two WARN entries,
  and five retry messages.

The API tests emitted an upstream Starlette/httpx deprecation warning.
Dependencies were installed in an isolated session environment; the checked-in
virtual environments and application database were not replaced.
