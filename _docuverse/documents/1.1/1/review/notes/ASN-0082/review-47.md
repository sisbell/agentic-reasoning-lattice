# Review of ASN-0082

## REVISE

### Issue 1: I3-S(a) and D-S(a) end in ✓ but rest on an ℕ-arithmetic fact the foundation does not supply
**ASN-0082, Span Width Preservation (I3-S derivation of (a))**: "These denote the same natural number by commutativity of addition on ℕ ... Commutativity is not among the minimal NAT-* axioms ASN-0034 extracts ...; we flag the reliance explicitly rather than name an axiom the foundation does not supply."
**Problem**: The derivation reduces to `n + ℓₘ = ℓₘ + n` (and D-S(a) to the mixed identity `(s₂+c')−c = (s₂−c)+c'`). The foundation's ℕ axioms are NAT-addcompat, NAT-closure (only the *left* identity `0+n=n`), NAT-discrete, NAT-order, NAT-wellorder. These do not include the recursive definition of `+`, a right identity, or a right-successor law, so commutativity is **not derivable** from them. Self-flagging an undischarged step does not discharge it — the `✓` on I3-S(a)/D-S(a) is unwarranted. This is precisely a "proof by checkmark over a multi-step ℕ argument." There is no way around it: at position m both reaches require `(sₘ+n)+ℓₘ = (sₘ+ℓₘ)+n`, which needs both associativity and commutativity.
**Required**: Either (i) have the foundation supply commutativity/associativity of ℕ `+` (or the recursive definition that yields them) and cite it, or (ii) prove them locally from NAT-wellorder by induction, or (iii) restructure so the claim does not depend on reordering ℕ summands. Until then the `✓` must be downgraded to an explicit open obligation, not a completed derivation.

### Issue 2: D-CTG is restated with a dropped conjunct, strengthening the cited foundation invariant
**ASN-0082, Foundation Invariants (contraction citations)**: "D-CTG (VContiguity, text subspace only): `(A d, u, q : ... : (A v : subspace(v) = 1 ∧ #v = #u ∧ u < v < q : v ∈ V_1(d)))`"
**Problem**: The foundation D-CTG (ASN-0036) carries a `zeros(v) = 0` guard in the inner antecedent: `... subspace(v) = 1 ∧ #v = #u ∧ zeros(v) = 0 ∧ u < v < q ...`. Dropping it weakens the antecedent and therefore *strengthens* the claim — the restated version would assert membership of e.g. `[1,0]`-shaped interlopers that S8a excludes from V_1(d). An ASN must not silently restate a foundation invariant in a stronger form, even where the omission happens to be harmless in the one application (D-SEP(b), where `r=[1,p₂+c]` is zero-free).
**Required**: Quote D-CTG verbatim with the `zeros(v) = 0` conjunct, and let D-SEP(b) discharge `zeros(r)=0` explicitly where it applies D-CTG.

### Issue 3: D-SEQ-post relies on proof-internal "Step 1/2/3" of ASN-0036, not on its contract
**ASN-0082, D-SEQ-post**: "These four conditions reproduce the four preconditions cited in ASN-0036's D-SEQ derivation (Step 1 used S8a's componentwise positivity ...; Step 3 used contiguity (D-CTG) ...; Step 2 used D-MIN ...)."
**Problem**: The foundation D-SEQ contract exposes only its postcondition, not a numbered internal proof structure. Citing another ASN's proof steps breaks self-containment (rule 7). The good news is the subsequent "Replaying the derivation locally at depth m = 2 ..." is in fact a complete, self-contained argument; the Step-1/2/3 references are decorative and load nothing.
**Required**: Delete the appeal to ASN-0036's internal step numbering; keep the local replay, which stands on its own.

### Issue 4: The depth scoping axiom is justified twice in near-identical prose
**ASN-0082, Depth axiom paragraph vs. "Necessity from TA4" paragraph**: the depth-axiom paragraph already states "TA4's zero-prefix precondition collides with S8a's componentwise positivity at any depth > 2"; the immediately following "Necessity from TA4" paragraph restates "force, at depth > 2, a non-empty zero-prefix range on ord(p), colliding with S8a's componentwise positivity."
**Problem**: Two adjacent paragraphs make the same TA4/S8a-collision argument in different words — accreted "why the axiom is needed" prose flagged by the anti-bloat classifier. The reader must read the same justification twice to confirm it is the same.
**Required**: Collapse to a single statement of the TA4/S8a collision and its consequence (`#p = 2` forced); the Open Question already carries the "does it generalize" pointer, so the second paragraph is pure duplication.

### Issue 5: I3-V is explained three times in prose beyond its worked-example trace
**ASN-0082, I3-V**: the exclusion clause is expounded in (a) the inline "Reading I3-V's exclusion clause" box, (b) the post-clause prose "I3-V (the vacating clause) is a one-line corollary of I3-CS ...", and (c) the "Gap and vacated regions" paragraph.
**Problem**: Three separate prose expositions of the same exclusion mechanism (the sparse `{[1,1],[1,4]}` reasoning recurs across them). This is accretive repetition independent of the legitimate worked-example "I3-V trace."
**Required**: Keep one statement (the I3-CS corollary derivation is the tightest) plus the worked-example trace; remove the redundant expositions.

## OUT_OF_SCOPE

### Topic 1: Spans that straddle the contraction boundary
**Why out of scope**: D-S handles only spans with start (and hence reach) in the right region. A span crossing X (partially deleted) needs split/clip semantics — span-algebra interaction belonging to a future DELETE-on-spans ASN, not a defect here.

### Topic 2: Generalization of contraction past ordinal depth 1
**Why out of scope**: Already named in the Open Questions; the TA4/S8a obstruction is correctly identified as the blocker. New territory, not an error.

### Topic 3: Updating external references to a V-position after a shift
**Why out of scope**: Raised in Open Questions; requires an external-reference/citation model this ASN does not introduce.

VERDICT: REVISE
