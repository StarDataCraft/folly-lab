# The Folly Manifesto

Folly is a practice of shipping one tiny, understandable interaction at a time.
Each Folly should reveal itself within ten seconds, work without a network, and
remain small enough to test, repair, and preserve.

The workflow is the artifact:

> IDEA → BUILD → TEST → REPAIR → PULL REQUEST → DEPLOY

We value finished over elaborate, deterministic over mysterious, and one safe
step over an endless loop.
