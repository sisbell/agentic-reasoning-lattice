# Review of ASN-0047

## REVISE

### Issue 1: Circular discharge of S8-fin under K.μ~

**ASN-0047, *Extended reachable-state invariants*, verification matrix (S8a/S8-depth/S8-fin row and D-SEQ★ row, K.μ~ column)**: "S8-fin derived from K.μ~-FIX (`dom(M'(d)) = dom(M(d))`, so finiteness inherits from the pre-state)."

**Problem**: The discharge is circular as written. K.μ~-FIX's own proof (in *Decomposition of K.μ~*) reads: "D-SEQ★ at the pre- and post-states gives `V_S(d) = {...}` and `V_S(d') = {...}`; since π is a bijection ... `n'_S = n_S` and `V_S(d') = V_S(d)`." So K.μ~-FIX consumes D-SEQ★(Σ'). But D-SEQ★(Σ') is derived from "D-CTG★ + D-MIN★ + S8-depth + S8-fin + S8a," and its own derivation explicitly invokes S8-fin ("By S8-fin, let `v_max = max(V_S(d))`"). Chain: D-SEQ★(Σ') ← S8-fin(Σ') ← K.μ~-FIX ← D-SEQ★(Σ'). S8-fin(Σ') is discharged from a result that presupposes it.

**Required**: Break the circle by discharging S8-fin(Σ') independently of K.μ~-FIX. The K.μ⁻ + K.μ⁺ decomposition supplies this directly: K.μ⁻ restricts dom(M(d)) (a subset of a finite set is finite) and K.μ⁺ adds finitely many positions (finite + finite = finite), so S8-fin(Σ') holds by elementary preservation through the two atomic steps without appeal to K.μ~-FIX. Cite that route in both matrix cells.

### Issue 2: Citation-convention meta-prose inside FrontierEquivalence premise (i)

**ASN-0047, *FrontierEquivalence*, "Three load-bearing premises," premise (i)**: "T10a's *direct* per-`(t, k')` uniqueness axiom is stated for child-spawning `k' ∈ {1, 2}` only and does not cover the `k = 0` sibling-increment regime; the at-most-once property for `(t, 0)` is the derived consequence cited here under the named handle 'T10a chain-advancement uniqueness at `(t, 0)`,' with the derivation chain TA5(c) + P1 + precondition supplying the substantive content."

**Problem**: The substantive derivation (TA5(c) + P1 + precondition) is already stated in the preceding sentence. The quoted tail only explains why a *name* is introduced and which axiom does *not* apply — citation-convention bookkeeping that the reader must skip past to reach the proof. This is the "new prose around an axiom/lemma explains why it is needed rather than what it says" pattern.

**Required**: Delete the naming/non-applicability commentary; keep the one-sentence derivation. If the named handle is needed for downstream citation, introduce it in a single clause without re-litigating which T10a clause does or does not cover `k = 0`.

### Issue 3: Document-ordering justification in elementary definitions

**ASN-0047, *Elementary transitions*, K.μ⁺ precondition**: "the per-subspace strengthening to D-CTG★/D-MIN★ is introduced later and adopted at the K.μ⁺ amendment, not at this elementary-definition site."

**Problem**: This sentence advances no claim about K.μ⁺; it justifies where in the document a strengthening appears. The same defensive ordering-prose recurs (e.g., J1 "given once, in its operative content-subspace form, at *Scoped coupling constraints* below"; P4 "proved in *Content-scoped containment and provenance* below"; J1★ "This is the single site of the coupling's wp derivation"). The repeated "introduced later / given once / the single site" phrasing is meta-prose about non-duplication rather than content.

**Required**: Replace with a bare forward pointer where one is genuinely needed (e.g., "D-CTG★/D-MIN★ — see *Amendments*"), and drop the standalone sentences whose only function is to assert that material lives elsewhere.

### Issue 4: Duplicated K.δ-ID derivations

**ASN-0047, *Elementary transitions* (K.δ structural-identities catalogue) and *Properties Introduced* → "Derived structural identities" table**: The four identities K.δ-ID.zeros-0/1, K.δ-ID.zeros-2, K.δ-ID.parent-0/1, K.δ-ID.parent-2 are stated with full "Derivation:" text inline at the K.δ definition and then restated with a near-verbatim "Derivation" column in the table.

**Problem**: Two locations carry the same statement and the same derivation in different words — the "two paragraphs say the same thing" pattern. A future revision touching one site will drift from the other.

**Required**: Keep the derivations at one site (the inline K.δ catalogue is the natural home) and reduce the table to label + statement + a pointer, or vice versa — but not both with derivations.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking

The ASN notes a forked document's link subspace starts empty and that a link-inheritance mechanism "would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope." This is correctly deferred — a future operations ASN, not a defect here.

### Topic 2: Interior link withdrawal / tombstoning

D-CTG★/D-MIN★ admit only suffix truncation, so interior link withdrawal requires a mechanism outside K.μ⁻'s contract. The ASN catalogues this in Open Questions; it is new territory, not an error in the present model.

VERDICT: REVISE
