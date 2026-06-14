I'll give the verdict-bearing findings first, then note what's solid.

## Revision list

**1. [DEFECT] — Approach 4 (all-wildcard fast path): the running-cardinality rule "up on ordinary creation, down on retraction" is wrong; it drops the retractor.** A retraction `K.λ` step does *two* things to the active view, not one: it **adds** the retractor itself — which is addressable unless it self-nullifies, and is counted under `q*` (the note's own worked example has `a_R ∈ addressable(Σ)` and `|addressable| = 4` *includes* it) — and it **removes** each previously-active target it nullifies. So a single-target retraction is `+1 − 1 = 0`, not `−1`; a builder maintaining `|addressable|` as the digest prescribes drifts low by one per retraction, and `q*` returns wrong numbers. This is precisely the ordinary-vs-retraction distinction the note spends CN-MONO and the dynamic worked example establishing and explicitly calls "load-bearing" — the digest flattens it in the one place it generates code. Fix: state the rule as *increment for every freshly created **addressable** link (ordinary or retraction); decrement for every link newly moved into `nullified` (a retraction's targets); a retraction step does both (`+1 − k`, net 0 in the common single-target case).* While here, soften "common": `q*` is the trivial boundary case (store-size), not a demonstrably frequent query.

**2. [SHARPENING] — Guarantees: surface CN-ZERO's "not found" leg.** The digest excludes the "nothing displayed" misreading via CN-LOC and nails the empty-request/empty-store split (its strongest move), but never states CN-ZERO's third leg: a zero is a *verdict over the whole addressable store*, not an exhaustion artifact — non-impedance (FL-JUNK) means junk volume cannot displace a match. It holds by construction in the full-scan baseline, but one line forbidding early-bail/heuristic narrowing that could miss a match amid junk would pin the guarantee for the indexed path too.

**3. [SHARPENING] — Implementation approaches: the Rust/`im` specificity presupposes a target the note doesn't establish.** The data-structure *families* (persistent set keyed by address; ordered map with range scans; tumbler-prefix trie) are at the right altitude; "the natural Rust analog…" and "`im`'s persistent set" (twice) pin a language and a named crate. Either state a "target is Rust" premise up front or speak in families. It doesn't mislead, but it's a notch below design altitude.

**4. [SHARPENING] — Open question 6 (federated count) is silent.** Staying single-store is correct (matches the note's single-`Σ` framing), and the digest rightly refuses to re-litigate the spec's open questions — but one line in *How it fits* or *Decisions* noting that federated counting across independently administered stores is a separate, open design (note OQ6) would close a loop a builder will reach for.

## What's solid

- The **locality/orphan trap** — that a content-pointing-only query channel collapses a deeply-orphaned request to the *empty-request* zero (≠ empty-store zero), and the remedy of an **address-direct query path** to honor CN-ORPHAN in practice — is the digest's best contribution: grounded in Q16 and the note's "request as given" remark, and exactly right.
- The **epoch-tagged cache** (OQ3) and **set-by-address dedup** (OQ4) are sound, correctly framed as hints-not-state, and answer the open questions structurally without overclaiming.
- The **forced/conventional tagging** is accurate throughout; nothing forced is actually conventional or vice versa.
- Every **Green source-level claim** is grounded in the evidence: full-enumeration cost (Q11), shared `sat` / spanfilade from/to/three sub-indices (Q12–14), the `onlinklist` off-by-one "counted twice" (Q13), the `TRUE||` dead-coded home filter (Q17), count disabled in multi-session (Q19). No fabricated Green claims.
- §7's recovery text is now clean and conventional (append-only log, replay-rebuilt hints) — the substrate-filename problem is gone, and nothing else depended on it.

VERDICT: REVISE
