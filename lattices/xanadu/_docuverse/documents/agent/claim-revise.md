# Claim Revise

Closes one open `comment.revise` on a claim. The third stage of the review → findings → revise chain: the upstream claim-findings producer emits `comment.revise` links per finding; this agent fires once per unresolved comment and closes it via `resolution.py`.

## Scope

One unresolved `comment.revise` link per fire. The trigger walks comments whose target claim is derived from the requested ASN's source note (CLI mode) or every active `comment.revise` (daemon mode). Per-comment granularity matches the substrate predicate: the comment is the predicate, not the claim. Two unresolved comments on the same claim mean two fires of this agent, sequentially, each addressing one finding against the claim's current state.

## Process

Each fire:

1. Walk the comment_addr to find the finding doc (`from_set`) and the target claim (`to_set`).
2. Read the finding doc body; extract the title from its first heading line.
3. Resolve the claim path → derive `asn_num`.
4. Dispatch the per-finding worker `revise(asn_num, title, finding_text, comment_id, claim_path)`. The worker builds a prompt from the revise template + finding text, invokes Claude with Edit/Write/Read/Bash tools, and the in-process Claude session edits the claim and runs `resolution.py accept` (with edit) or `resolution.py reject` (with rationale).
5. Return `AgentResult` reflecting whether the comment closed.

The substrate writes (the `resolution.<kind>` link, the file edit, the optional rationale doc on reject) are emitted by the in-process Claude session through the `resolution.py` CLI, not by the agent shell. The shell's job is to walk substrate, populate args, and dispatch.

## Trigger

- Predicate-fired by the runner: `has_resolution(comment_addr)` is the skip signal. After the agent fires and closes the comment, the predicate flips True and the runner moves on.
- Per-comment fires give the runner natural granularity over the closure work — one fire = one finding closed. Cross-claim coordination, batching, and the review/revise alternation are all handled by the runner walking predicates, not by an agent-internal loop.

## Inputs

- The finding doc body (the prose the reviewer wrote about this issue)
- The target claim's path and `asn_num` (resolved from substrate)
- The comment's address (passed through to the Claude session via `PROTOCOL_COMMENT_ID` so it can call `resolution.py` to close)

## Outputs

- One `resolution.edit` (with edits to the claim's `.md`) or `resolution.reject` (with a rationale doc) per fire, depending on whether Claude judged the finding worth addressing.
- The substrate writes are emitted by the in-process Claude session through `scripts/agent_tools/resolution.py`.

## Tools

- Edit, Write, Read, Glob, Grep, Bash — same toolset as the per-finding worker function uses today.

## Convergence

This agent is a refiner: it closes substrate predicates (open `comment.revise` links) by emitting resolution links, without granting new substrate identity. Quiescence on a claim is the state where every `comment.revise` targeting it has a resolution. The runner walks the trigger until that state is reached across the ASN's claim cluster, alternating with claim-findings (when new reviews emit new comments) until the entire chain converges.
