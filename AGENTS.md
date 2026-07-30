# Folly Repository Rules

Build one tiny, testable Folly at a time. Preserve the previous working version
and prefer the smallest practical change.

For every nightly run:

1. Create exactly one Folly.
2. Generate exactly two candidate ideas, then select one.
3. Change no more than five files where practical.
4. Add no new dependency.
5. Run the targeted tests before the full suite.
6. Perform no more than two repair cycles.
7. Create a pull request only after all tests pass.
8. Write exactly one report under `reports/`.
9. Stop after one Folly.

Safety rules:

- Work on a branch and never overwrite the last working version.
- GitHub Actions may run tests and compilation checks only.
- Never add secrets, API keys, external APIs, databases, authentication,
  payments, analytics, copyrighted assets, or new infrastructure.
- Stop on any usage-limit warning.
- Never purchase credits.
- Never use an API key.
- Never change account permissions.
- Never use an unlimited loop.
- If two repair cycles do not produce passing tests, preserve the repository,
  record the failure in `FOLLY_FAILURES.md`, and stop safely.
