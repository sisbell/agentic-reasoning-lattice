# Review of ASN-0068

## REVISE

### Issue 1: Action-point necessity is asserted three times around CV-IN-N

**ASN-0068, The Input (CV-IN-N and surrounding prose)**:

- Framing sentence before CV-IN-N: "Level-uniformity (S6) requires only `#start(σ) = #width(σ)` and does not bound the action point of the width, so the precondition `actionPoint(width(σ)) = m_σ` is necessary."
- CV-IN-N itself: "*necessity of the action-point constraint*: Relaxing the precondition to `actionPoint(width(σ)) < m_σ` admits spans whose V-extent at depth `m_σ` is unbounded…"
- Paragraph after the justification: "The exact constraint `actionPoint(width(σ)) = m_σ` rules out this unbounded capture by forcing `reach(σ)` to agree with `start(σ)` at all positions `1 ≤ i < m_σ`…"

**Problem**: The pre-sentence asserts the necessity conclusion that CV-IN-N then states formally and proves — pure announcement of a claim that immediately follows. The first half of the post-paragraph ("rules out this unbounded capture by forcing `reach(σ)` to agree…") restates the justification's own conclusion. Three passages carry the same point. This is the forward-reference/duplication accretion the anti-bloat pass targets: the reader works past two framing restatements to reach the one claim.

**Required**: Delete the pre-sentence (CV-IN-N's title and statement already carry "necessity"). In the post-paragraph, keep only the genuinely new positive content ("The span's V-extent at depth `m_σ` therefore contains exactly `n_σ` consecutive depth-`m_σ` tumblers… independent of any arrangement") and drop the restatement of the `reach(σ)`-agreement mechanics already established in the justification.

### Issue 2: Design-rationale prose in the run-result definition

**ASN-0068, The Result**: "The result triple omits it to avoid duplicating state-derivable information: the V-position pair plus the width determines the run, and any caller that needs I-addresses can extract them from `M` on demand. This keeps the result type free of stored state — `Result` is a set of structural witnesses, not a snapshot of `M`."

**Problem**: The substantive fact — the shared I-address is derivable as `M(d_a)(v_a + k)` and is therefore omitted — is stated in the preceding sentence and is correct. The quoted tail is modeling rationale ("to avoid duplicating… on demand. This keeps the result type free of stored state…") explaining *why the representation was chosen* rather than advancing what the result is. This is the "explains why rather than what" pattern.

**Required**: Cut to the factual statement (I-address derivable from `M`, hence not stored in the triple). Drop the "to avoid duplicating… free of stored state" rationale.

## OUT_OF_SCOPE

### Topic 1: Concurrent-modification and replication invariants
The Open Questions raise behavior under mid-comparison arrangement modification, cross-replica determinism, and multi-document correspondence composition. These are correctly parked as future work — they require operations/protocols outside this read-only observer.

VERDICT: REVISE
