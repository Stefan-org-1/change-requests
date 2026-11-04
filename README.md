# change-requests

Approved deploys. A change says which version of a repo may deploy to which environments, when, and who approved. The deploy gate lets a deploy through only if a change on `main` covers it and its approvers meet what `org-policy` requires for that environment.

These files mock the outcome of a change process, not the process. In practice a system such as Jira or ServiceNow runs the request, review and approval. The gate only needs the result: an approved change with its version, environments, window and approvers. This repo holds that result so the gate has something to read, and the gate trusts it as is.

## Request a change

Add `changes/<repo>/<name>.yaml`:

```yaml
repo: payments-web
version: 1.0.0                 # release tag, or a full commit SHA
environments: [prod]
window:
  start: 2026-11-02T09:00:00-05:00
  end: 2026-11-02T17:00:00-05:00
reason: Release on-call notes
emergency: false
requested_by: StefanPanait
approvers: [wendellliam]
```

- `window`: at most 14 days, or 24 hours for an emergency.
- `emergency: true`: may override rule sets marked `break_glass` in `org-policy`, with the approvals `org-policy` names for break-glass.
- `approvers`: edit to add or revoke an approval. The gate reads the current list on every check.

Who must approve is set in `org-policy`. The requester and the deployer never count as approvers.

The change can be used for any number of deploys inside its window.
