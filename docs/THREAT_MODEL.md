# STRIDE threat model (draft — replace assumptions with your own review)

## Scope and trust boundaries
- Client sends untrusted JSON via HTTP to `/api/validate`.
- Flask application validates shape, content length and type.
- API returns validation metadata only; there is no database, login or cloud deployment.
- Trust boundary: untrusted client -> web server / Flask process.

| STRIDE | Example threat | Current mitigation | Remaining risk / next step |
|---|---|---|---|
| Spoofing | Client claims another identity | No identity claims or user accounts | Add authenticated identity before user-specific features |
| Tampering | Malicious request data | JSON type and length validation | Add schema-based validation for future fields |
| Repudiation | Actions not attributable | No security audit trail | Add privacy-aware structured audit logs when needed |
| Information disclosure | Error messages reveal details | Generic errors, no secrets in repository | TLS termination needed before any remote exposure |
| Denial of service | Huge request body | 16 KiB request limit | Rate limiting, reverse proxy, resource quotas |
| Elevation of privilege | Compromised app runs as root | Non-root Docker user | Container runtime confinement and further isolation |

## Explicit limitations
- This is a local learning project, not a production-ready API.
- Security headers are present, but HTTPS and authentication are not configured.
- The scanner policies catch classes of issues, not every vulnerability.
