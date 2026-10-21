# Model serving incident — synthetic Practice fixture

> This is a **fictional training observation**, not a real production incident or an executed probe. No root cause is provided. Do not invent additional logs, actual deployments, or runtime results.

## Known service topology

Business client → platform API gateway → model route / backend discovery → Qwen inference service → GPU.

## Already observed (fictional)

- Business reports model alias `qwen-main` stopped responding successfully today; yesterday it worked. Incident window: 2026-10-20 09:12 to 09:25 (example local time).
- A failed request to the platform gateway returned HTTP 503 with gateway detail `no healthy upstream for model=qwen-main`. Request ID: `example-req-01`.
- A second client using the same gateway and model alias also returned HTTP 503 around the same window. No guarantee is made about *all* clients.
- Another model alias `embeddings-main` returned HTTP 200 through the same gateway during the window.
- An authorized one-off direct call to a known Qwen inference instance returned HTTP 200 at 09:24, with a valid minimal inference response. This does **not** prove all backends, route registrations, or subsequent calls remain healthy.

## Still unknown

The gateway's actual service discovery snapshots, route tables, backend readiness/health status and event timeline, recent configuration changes, and whether the issue is intermittent.

## Practice objective

First formulate the *diagnostic problem* supported by these observations, then choose the highest-value next check. State what contrasting observations would imply, without assuming a particular cause or claiming a real production repair.
