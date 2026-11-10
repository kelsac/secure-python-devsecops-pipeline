# Secure Python API — DevSecOps Portfolio

A small application designed to demonstrate **automated security controls in CI**, secure defaults, threat modelling and an evidence-backed remediation workflow.

## Architecture
```text
Client -> Flask API -> input validation -> JSON response
                      |
                      +-- pytest tests
GitHub PR -> Tests + Semgrep SAST + Trivy dependency scan + Docker image scan
```

## Local setup (Python 3.11+)
```bash
python -m venv .venv
# Activate .venv (Windows PowerShell): .\\.venv\\Scripts\\Activate.ps1
# Activate .venv (Linux/macOS): source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m app.main
```
Test in a second terminal:
```bash
curl http://127.0.0.1:5000/health
curl -X POST http://127.0.0.1:5000/api/validate -H 'Content-Type: application/json' -d '{"message":"hello"}'
```

## Container
```bash
docker build -t secure-api .
docker run --rm -p 127.0.0.1:8080:8080 secure-api
```
Visit http://127.0.0.1:8080/health.

## Pipeline
`.github/workflows/security.yml` runs tests, Semgrep rules, Trivy filesystem/dependency scan and Docker image scan on PRs and main pushes.

**Security engineering note:** CI failures are quality gates only when GitHub branch protection *requires* successful status checks. Configure Settings -> Branches -> Add branch protection rule -> main -> Require status checks to pass. Require all four jobs. Also require a pull request, if available.

## Evidence and findings
- See `docs/THREAT_MODEL.md` for STRIDE and trust boundaries.
- See `docs/FINDINGS.md` for the finding/remediation template.
- Add links to an actual failing PR, a passing PR and scanned workflows after you run them.
- Document false positives, scan failures and exceptions; never claim "no vulnerabilities" simply because scans pass.

## Hardening backlog
- Pin GitHub Actions to reviewed full commit SHAs rather than mutable tags.
- Lock Python dependencies and add automated dependency update PRs.
- Add request rate limiting, HTTPS front end, authenticated user context and monitoring before production use.
- Add coverage metrics, SBOM, supply chain provenance and policy for suppressing accepted findings.

## Limits
Local teaching demonstration only. Does not deploy to Azure, does not authenticate users, and does not demonstrate production-grade cloud security.
