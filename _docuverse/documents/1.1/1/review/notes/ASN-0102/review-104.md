# Review of ASN-0102

I read the full note, checked each X-claim's derivation, traced the wp(S3★) argument, verified the tiling in X16, and worked through all five examples' arithmetic. The correctness core is solid: the store-frame claims (X1, X3), the no-overwrite/tiling argument (X7, X16), the merge/origin claims (X8, X11, X12), and the invariant discharge (X17) all hold, and the example suite genuinely exercises the boundaries (p=1, p=n_S+1, n_S=0, self-source, cross-origin, coalescing). My findings are confined to the anti-bloat surface explicitly in scope for this cycle.

## REVISE

### Issue 1: Composite-boundary framing stated twice, in different words
**ASN-0102, X17 (Range routing (RR) and the P4★/P4a/P7a preamble)**: RR opens "Read the standalone COPY as a composite with initial boundary `Σ_0 = Σ` and final boundary `Σ'`"; the later preamble repeats "Because a standalone COPY is itself a valid composite (read its pre-state as the composite's initial boundary `Σ_0 = Σ`, making the post-state `Σ'` a composite boundary)".
**Problem**: The same setup — treat COPY as a length-1 composite whose pre-/post-states are composite boundaries — is asserted in two separate paragraphs. This is the "two paragraphs say the same thing in different words" pattern; the reader must reconcile the duplicate before following either P4★ or P4a.
**Required**: State the composite-boundary reading once (e.g., at the head of the composite-boundary-properties block) and have RR reference it rather than re-derive it.

### Issue 2: Misdirected cross-reference "(as at X15)"
**ASN-0102, X17, RR**: "Read the standalone COPY as a composite ... `(as at X15)`."
**Problem**: X15 (Atomicity) establishes the opposite emphasis — COPY is a *single* elementary transition "not a composite of K.μ steps," with *no observable intermediate state*. It does not establish the "valid composite with boundaries `Σ_0`, `Σ'`" reading that RR needs; that justification actually lives in the P4★/P4a/P7a preamble (Issue 1). A reader following the pointer lands on a claim that does not license RR's framing.
**Required**: Repoint RR to the consolidated composite-boundary statement, or drop the parenthetical.

## OUT_OF_SCOPE

The four Open Questions (later displacement of copied content, transitive containment when a referencing document is itself a source, time-varying views, identity after the allocating document becomes unreachable) are correctly deferred — they concern future operations and reachability semantics, not COPY's own state transition.

VERDICT: REVISE
