# Security finding and remediation record

Complete this after running the unsafe-change pull-request exercise.

| Field | Notes |
|---|---|
| Finding ID | DEVSECOPS-001 |
| Vulnerability | Unsafe shell execution (`shell=True`) |
| Severity | High (educational example; contextual severity depends on data flow) |
| Detection mechanism | Custom Semgrep SAST rule |
| Evidence | Link to failing GitHub Actions run (add actual URL) |
| Root cause | Shell invocation in application source |
| Remediation | Remove shell execution / use safe alternatives |
| Verification | Link to passing CI run (add actual URL) |
| Limitations | Static matching is not comprehensive taint analysis |
