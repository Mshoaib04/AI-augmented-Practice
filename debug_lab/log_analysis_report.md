# Sample application log analysis

Source: `app.log`, the supplied Demo 05 training fixture, not a production log.
All timestamps below are on 2026-09-10; the log does not specify a timezone.

## Chronological summary

The service starts normally at 02:14:01, creates an alert at 02:15:33
(HTTP 201), and explains alert 1 successfully at 02:17:02 (HTTP 200).
The first failure is at 02:22:18: explaining alert 2 returns HTTP 500,
followed by an `AttributeError` and a retry message.
An explanation for alert 3 succeeds at 02:31:47.

The same HTTP 500 and exception recur for alert 7 at 02:44:09.
At 02:58:22, database connection-pool capacity is reported at 82%.
Alert 9 is explained successfully at 03:05:41, followed by another
HTTP 500 for alert 11 at 03:12:56.
At 03:20:03, `GET /alerts/14` returns HTTP 404, `Alert not found`.
Alert 15 is explained successfully at 03:33:19.

Explaining alert 18 fails at 03:41:52 with the same exception.
Pool capacity reaches 91% at 03:50:07.
The fifth matching HTTP 500 occurs for alert 21 at 04:02:31.
Each HTTP 500 is followed by an INFO retry message one second later.
The final entry is a successful explanation of alert 23 at 04:15:44.

## Distinct ERROR patterns

| Error pattern | Count | First occurrence | Last occurrence | Method / endpoint / status |
|---|---|---|---|---|
| `AttributeError: 'NoneType' object has no attribute 'upper'` | 5 | 2026-09-10 02:22:18 | 2026-09-10 04:02:31 | POST `/alerts/{id}/explain`, HTTP 500 |
| `Alert not found` | 1 | 2026-09-10 03:20:03 | 2026-09-10 03:20:03 | GET `/alerts/14`, HTTP 404 |

Raw timestamps and endpoints supporting the five AttributeErrors:

| Timestamp | Endpoint |
|---|---|
| 2026-09-10 02:22:18 | `/alerts/2/explain` |
| 2026-09-10 02:44:09 | `/alerts/7/explain` |
| 2026-09-10 03:12:56 | `/alerts/11/explain` |
| 2026-09-10 03:41:52 | `/alerts/18/explain` |
| 2026-09-10 04:02:31 | `/alerts/21/explain` |

The exception lines have no timestamps of their own; each is associated
with its immediately preceding timestamped ERROR entry.
The 404 occurs only at 2026-09-10 03:20:03.

## WARN entries

| Timestamp | Message | Reported value |
|---|---|---|
| 2026-09-10 02:58:22 | Database connection pool capacity | 82% |
| 2026-09-10 03:50:07 | Database connection pool capacity | 91% |

Warnings and retry INFO messages are not counted as ERROR entries.

## Evidence and limitations

- Facts: six ERROR entries, five matching exception lines, one 404, two
  pool warnings, and five INFO retry messages appear in this sample.
- Retry messages do not prove retry success. Later successful requests
  use different alert IDs and cannot be treated as evidence of recovery
  for the failed requests.
- A call to `.upper()` on `None` is consistent with the exception.
  The log does not identify the variable, source line, or underlying defect.
- Increasing pool usage is a separate signal. The log does not prove it
  caused the HTTP 500 responses.
- Demo 06 deliberately introduces a different failure: referencing the
  undefined `resolved_by` variable raises `NameError`, not this sample's
  `AttributeError`. No production root cause is established here.

## Independent count verification

From `debug_lab`, run these macOS/Linux equivalents of the handout's
PowerShell checks:

```bash
grep -Fc "AttributeError: 'NoneType' object has no attribute 'upper'" app.log
grep -Fc "404 -- Alert not found" app.log
grep -c ' ERROR ' app.log
grep -c ' WARN ' app.log
grep -c 'INFO .*Retrying request' app.log
```

Expected results, respectively: `5`, `1`, `6`, `2`, `5`.
