# Review of ASN-0091

This note carries the `review-mode.anti-bloat` classifier. The underlying derivations (RE-C, RE-ran, RE-μ, RE-proj, the K.μ~ clause (i)–(v) discharge, the run-cardinality witnesses) are arithmetically sound and the cross-references are all to foundation ASNs. The findings below are accreted meta-prose and redundant exposition, which is what this cycle is tasked to surface.

## REVISE

### Issue 1: Ordering-justification prose in Pointwise-fixity frames
**ASN-0091, "REARRANGE_K Realises the Abstract Class"**: "These frames derive directly from R-PPERM/R-SPERM and R-FRAME-P/S(a), so they stand independent of the clause discharges below and are available to them."
**Problem**: The derivation of RE-sub/RE-ext from R-PPERM/R-SPERM and R-FRAME-P/S(a) is the content; the trailing clause "so they stand independent of the clause discharges below and are available to them" justifies *placement* (these frames were just relocated before the clause table). This is the flagged "prose justifies document ordering" pattern — it narrates argument structure rather than advancing the claim.
**Required**: Delete the "so they stand independent… available to them" justification. State the derivation; let the placement speak for itself.

### Issue 2: RE-eq witnessed three times with back-referencing commentary
**ASN-0091, "Worked Example — Bijection Non-Uniqueness"**: "Beyond exhibiting bijection non-uniqueness, this trace is also a richer RE-eq witness than the two-singleton case in 'Run Decomposition Is Not Invariant'… RE-eq thus does not require a sparse arrangement; it persists under S5/UnrestrictedSharing."
**Problem**: RE-eq already has a witness in "Run Decomposition Is Not Invariant" (the two-singleton cross-document arrangement), and the Net-Effect Collapse trace also exhibits cardinality preservation (3 runs at both states). This paragraph adds a *third* RE-eq witness and then editorializes about it relative to the first. The possibility claim is established once; the comparative commentary is accretion.
**Required**: Drop the RE-eq paragraph from the bijection trace (the trace's purpose is non-uniqueness, not run cardinality). Keep one RE-eq witness.

### Issue 3: Shared-image licence re-explained in three places
**ASN-0091, net-effect split prose / "Bijection Non-Uniqueness" setup / "Net-Effect Collapse" setup**: the rule "S2 imposes only functionality, S5 admits shared images, so a permutation within a shared-image block leaves M(d) pointwise unchanged" appears in the net-effect split paragraph and is re-narrated in the setup of both later traces.
**Problem**: Two paragraphs in different sections saying the same thing in different words is the flagged duplication pattern. The licence is a single fact; the traces should *use* it, not re-derive it.
**Required**: State the shared-image licence once (in the net-effect split), and have the bijection and collapse traces cite it rather than re-explain it.

### Issue 4: Each worked example narrates its novelty against its siblings
**ASN-0091, worked-example headers**: e.g. "The 4-cut swap differs from the 3-cut pivot in exactly one structural respect…", "The first two traces place c₀ = min(V_S(d))… This trace exhibits R-EXT firing on a non-empty… exterior", "The net-effect split… distinguishes one branch the preceding traces never instantiate."
**Problem**: Five traces, each opening with a contrast-framing sentence that inventories what prior traces did and did not cover. This is use-site/contrast meta-prose: the reader following a trace does not need it justified against the others. The examples themselves are legitimate (concrete examples are not meta-prose); the inter-trace bookkeeping is.
**Required**: Remove the comparative framing sentences. A one-line statement of what each trace demonstrates suffices; drop the running tally of sibling coverage.

## OUT_OF_SCOPE

(none — the Open Questions correctly defer link-subspace rearrangement semantics, fragment-reconstitution, and observational equivalence to future ASNs.)

VERDICT: REVISE
