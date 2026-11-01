# change-requests

Approved deploys. A change says which version of a repo may deploy to which environments, and when. The deploy gate lets a deploy through only if a merged change covers it and the change's PR has the approvals that `org-config` requires for that environment.

## Request a change

Add `changes/<repo>/<name>.yaml` in a PR:

```yaml
repo: payments-web
version: eed2318...            # full commit SHA
environments: [prod]
window:
  start: 2026-11-02T09:00:00-05:00
  end: 2026-11-02T17:00:00-05:00
reason: Release on-call notes
emergency: false
```

- `window`: at most 14 days, or 24 hours for an emergency.
- `emergency: true`: may override rule sets marked `break_glass` in `org-config`, with the approvals `org-config` names for break-glass.

Reviewers come from `.github/CODEOWNERS`. Who must approve is set in `org-config`, not here. The PR author never counts as an approver. Approvals count only on the PR's latest commit.

The change can be used for any number of deploys inside its window.
