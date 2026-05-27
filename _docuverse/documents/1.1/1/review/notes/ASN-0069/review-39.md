# Review of ASN-0069

## REVISE

(no issues identified)

## OUT_OF_SCOPE

### Topic 1: Concurrency semantics for parallel fork attempts
**Why out of scope**: SequentialTransitionAxiom resolves this at the foundation level; deeper concurrency primitives are an open question per the ASN's own list.

### Topic 2: Snapshot vs. living fork distinction
**Why out of scope**: This ASN commits to snapshot semantics (literal V-position inheritance via V4); living-fork variants are explicitly listed as future work.

### Topic 3: Fork discoverability from source's vantage
**Why out of scope**: The ASN's open questions correctly flag this as a future enumeration mechanism, not a property of the fork operation itself.

### Topic 4: Fork operations on transcludent sources
**Why out of scope**: Identified in the ASN's open questions; not properly addressable until transclusion semantics are formalized.

---

After exhaustive review, I find this ASN unusually rigorous. Every derivation cited was checked:

- **V1, V2** — both inductions on `A_v(d_src)`'s emission count are well-structured, with explicit base/step cases. The nested induction in V2 (length identity) is properly distinguished from the outer induction (prefix relation).
- **V3, V3a** — direct from frame composition + S7.
- **V4, V4b** — design commitments are explicitly labeled as such, with the alternative (rebased V-positions + correspondence tables) noted.
- **V5, V5a** — V5a's two-clause structure (per-transition and per-sequence) is correctly proved by induction; Corollary 2 is the right form for V10(b).
- **V6, V6a** — V6's contradiction via CL-OWN is sound; V6a's three clauses (link store preservation, source projection invariance, fork-projection-as-restriction) are derived through proper case analysis with both ⊆ and ⊇ directions shown for clause (iii).
- **V7** — empty-source case explicitly framed as a J4 extension, with K.δ-alone composite verified separately against ValidComposite★.
- **V8, V8a, V8b, V8c** — V8b's enumeration covers all elementary transitions in ASN-0047's vocabulary; non-monotonicity is correctly characterized.
- **V9, V9a** — J1★/J1'★ consumption is correctly bounded by V6's link-subspace emptiness.
- **V10, V11, V11a** — V11's premise scoping is genuinely subtle but handled with explicit Anchoring at Σ paragraph and per-stage discharge. V11a's transitivity is established by unfolding Prefix; the recovery procedure is rigorous.
- **V12** — V12(d)'s range equality derivation correctly uses V4b's exact equality (not just V4's containment) to feed P4★.
- **Composite verification** — Walks through both K.δ sub-cases (first/subsequent fork) with full discharge of outer, uniform, and per-sub-case preconditions; T10a's at-most-once-per-(t, k') constraint and T10a.6/T10a.7 are correctly invoked for freshness; J0/J1★/J1'★ couplings discharged with correct scope.
- **Worked example** — Verifies V0–V12 against specific scenarios (populated, empty, link-only, sibling forks, chain forks), with explicit computation of trailing-component values for V10(a).
- **Dependency audit** — Comprehensive; correctly flags ASN-0040 for removal.

No proofs handwave critical cases. No invariant conjuncts are skipped. No cross-ASN references to non-foundation ASNs. The design commitments (V4, V4b) are explicitly distinguished from derived consequences, with the alternative-ASN reading discussed. Boundary cases (empty source, link-only source, fork chains, sibling forks) are all addressed. Foundation invariant preservation is delegated correctly to ValidComposite★'s preservation theorem.

VERDICT: CONVERGED
