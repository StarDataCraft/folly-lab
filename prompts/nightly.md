# Nightly Folly Run

Create exactly one small Folly and then stop.

1. Generate exactly two candidate ideas.
2. Select exactly one of those ideas.
3. Preserve the previous working version.
4. Change no more than five files where practical.
5. Add no new dependency.
6. Run targeted tests before the full test suite.
7. Perform no more than two repair cycles.
8. If tests still fail, preserve the repository, record the failure in
   `FOLLY_FAILURES.md`, and stop safely.
9. Create a pull request only after all tests pass.
10. Write exactly one report under `reports/`.
11. Stop after completing one Folly.

Safety constraints:

- Stop immediately on usage-limit warnings.
- Never purchase credits.
- Never use an API key.
- Never change account permissions.
- Never use an unlimited loop.
- Do not add secrets, external APIs, databases, authentication, payments,
  analytics, copyrighted assets, image generation, or new infrastructure.
- Keep GitHub Actions limited to tests and Python compilation checks.
