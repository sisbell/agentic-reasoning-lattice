# Claim Signature Resolve

Producer that emits per-claim signature sidecars — the formal-symbol attestation that pairs with each claim's prose. Fires per claim with a stale or missing signature sidecar; gathers context (existing sidecar, transitive dependency signatures, notation primitives), runs the LLM helper to produce introduces/removes, emits the new sidecar via `emit_attribute`, persists a resolve-doc audit trail, commits.

## Scope

One claim per fire. The trigger walks each claim derived from the ASN's source note (CLI mode), or every active `claim`-classified address (daemon mode). Predicate `signature_is_fresh` is the chain-length comparison shared with `description_is_fresh` / `statements_is_fresh`: True (skip) iff the signature sidecar's supersession chain is at least as long as the claim's. Lower sidecar chain → at least one claim edit is unattested → fire.

## Process

Each fire:

1. Resolve the claim path → derive `asn_label`, `claim_label`, `asn_num`, `claim_dir`.
2. Read existing signature sidecar (file at `<claim_dir>/<claim_label>.signature.md`, may be empty).
3. Walk transitive `citation.depends` from the claim to collect upstream dependency signatures (same-ASN; one (label, signature_text) per upstream claim with a non-empty sidecar).
4. Read notation primitives from substrate (the protocol-level symbol vocabulary).
5. Dispatch `extract_signature_changes` LLM helper (Sonnet by default) with the assembled context. Returns `SignatureChanges(introduces, removes, raw_text, elapsed_seconds)`.
6. If both lists are empty: no-op return (sidecar already reflects truth — no write, no resolve doc, no commit). Predicate stays False until the next claim md edit advances the claim's chain past the sidecar's.
7. Otherwise: compute new sidecar bullets from `existing + introduces - removes`, emit the new sidecar via `emit_attribute(session, claim_rel, "signature", new_sidecar_text)` — this advances the signature link's sidecar version chain, flipping `signature_is_fresh` True.
8. Persist a resolve-doc audit trail to `_docuverse/documents/signature-resolve/<asn_label>/<claim_label>-<run_num>.md` (timestamp, model, raw LLM output).
9. Step commit.

## Trigger

Predicate-fired by the runner: `signature_is_fresh(claim_addr)` is the skip signal. The chain-length comparison gives staleness for free — every claim md edit advances the claim's chain via `register_version`, every signature emission advances the sidecar's chain via `emit_attribute`'s `register_version` path. No verb-flag classifiers.

## Inputs

- The claim's md content (read directly from disk)
- The claim's existing signature sidecar (read directly from disk; may be empty)
- Transitive same-ASN dependency signatures (substrate-walked via `citation.depends`)
- Notation primitives (substrate-read; protocol-level symbol vocabulary)

## Outputs

Per fire (only when introduces/removes is non-empty):
- Updated signature sidecar at `<claim_dir>/<claim_label>.signature.md`
- `signature` attribute link from claim md → sidecar (idempotent on existence; version chain advances on each emit)
- Resolve-doc audit at `_docuverse/documents/signature-resolve/<asn_label>/<claim_label>-<run_num>.md`
- One `signature-resolve(asn): <asn_label>/<claim_label> — N introduced, M removed` git commit

## Tools

None — the LLM helper invokes Sonnet directly via `invoke_claude` with no tool surface; the parsing of YAML response lives inside the helper. The agent shell does substrate writes (emit_attribute) and file I/O (resolve-doc persistence) directly, no Claude session for those.

## Convergence

This agent is a producer: it grants new substrate identity to a signature sidecar (or advances the existing sidecar's version chain). Refiners that depend on signature attestations (e.g., the structural-audit scout via the `declared-symbols-resolve` rule) read from the sidecar and trust its freshness via `signature_is_fresh`. Quiescence per-claim: signature sidecar's chain ≥ claim's chain. Quiescence across an ASN: every claim's predicate is True. The runner walks the trigger until that state is reached.

## What this isn't

- **Not the validator.** The structural validator (claim-validate.py, run by the `claim_structural_audit` scout) checks that declared symbols resolve to owners — it depends on signatures being populated. This agent is upstream: it makes signatures exist. Without it, declared-symbols-resolve has nothing to check against.
- **Not a refiner.** Doesn't close any predicate by emitting resolution links or editing claim content. It grants identity to a derived metadata sidecar.
