# Review of ASN-0082

## REVISE

### Issue 1: σ(v) well-formedness is established three separate times

**ASN-0082, Post-Contraction Shift**: The claim "σ(v) = vpos(1, ord(v) ⊖ w_ord) = [1, v₂ − c] is well-defined and satisfies S8a" is fully derived in three distinct places:

1. The **D-SHIFT** "The shift is well-defined" paragraph ("ord(v) ⊖ w_ord is well-defined ... clause (iii) gives that it is Pos ... satisfies S8a by vpos's S8a-closure postcondition").
2. The **S8a-post** lemma, Q₃ case ("σ(v) = [S, vₘ − c] with S ≥ 1 ... vₘ − c ≥ p₂ ≥ 1 ... full S8a").
3. The standalone subsection **"S8a-post for the shifted position"** (re-derives `v₂ − c > 0` and `ord(v) ≥ w_ord` via OrdinalExceedsDisplacement).

**Problem**: All three discharge the same two obligations (strict positivity of the shifted ordinal; well-definedness of the subtraction). The third subsection adds nothing the S8a-post lemma's Q₃ case does not already cover — it is the relocated-finding/duplication pattern the anti-bloat mode targets.
**Required**: Keep one locus (the S8a-post lemma is the natural home). Have D-SHIFT and the assignment site cite it rather than re-derive. Delete the "S8a-post for the shifted position" subsection.

### Issue 2: D-SEP(a) re-proves OrdinalExceedsDisplacement(i) nearly verbatim

**ASN-0082, D-SEP proof of (a)** vs **OrdinalExceedsDisplacement proof of (i)**: Both establish `ord(r) ⊖ w_ord = ord(p)` by reducing to `(ord(p) ⊕ w_ord) ⊖ w_ord = ord(p)` and discharging TA4 with the identical precondition list ("Pos(w_ord) ...; k = actionPoint(w_ord) = 1 = #ord(p); #w_ord = 1 = k; the zero-prefix quantifier 1 ≤ i < 1 vacuous").

**Problem**: OrdinalExceedsDisplacement(i) already proves `ord(r) ⊖ w_ord = ord(p)` as a load-bearing intermediate. D-SEP(a) repeats the same TA4 application word-for-word. Two paragraphs saying the same thing.
**Required**: D-SEP(a) should cite OrdinalExceedsDisplacement(i) for the identity, or vice versa. Do not discharge TA4 twice.

### Issue 3: NAT-comm introduced as a local axiom

**ASN-0082, "The Ordinal Shift"/Statement Registry**: "NAT-comm | local axiom | ℕ addition is commutative: m + n = n + m for all m, n ∈ ℕ".

**Problem**: ASN-0034 deliberately factors ℕ facts into the NAT-* family (NAT-addcompat, NAT-closure, NAT-discrete, NAT-order, NAT-wellorder) precisely "so each proof cites only what it actually uses" (T0). Commutativity of ℕ addition is a foundation-tier fact of exactly that family, here axiomatized ad hoc inside an operations ASN. It is load-bearing in I3-S (`n + ℓₘ = ℓₘ + n`) and D-S, so it is not incidental. Self-containment is fine for *operation-local* definitions, but an unverified arithmetic axiom should not be minted here.
**Required**: Add ℕ commutativity to ASN-0034's NAT-* axioms and cite it, the way the registry already routes ℕ associativity through TA-assoc. Remove the local NAT-comm.

### Issue 4: meta-prose in structural slots

**ASN-0082, "Gap region"**: "After accounting for all eight clauses, the positions in the gap ... remain the only region not assigned a value ..." — the clause-counting framing is exhaustiveness meta-prose; the load-bearing content is only that I3-CS excludes the gap.

**ASN-0082, insertion "Scope."**: two consecutive paragraphs both assert "the shift relocates content at/beyond p forward" and "modifies M(d) only, not C." The second paragraph repeats the first except for introducing `S = p₁` and `n ≥ 1`.

**Problem**: Both are noise the reader must skip past — the duplicated scope statement and the "all eight clauses" tally do not advance the argument.
**Required**: Collapse the two Scope paragraphs into one; drop the clause-count framing in the Gap region paragraph and state directly that I3-CS excludes [p, shift(p, n)).

## OUT_OF_SCOPE

### Topic 1: depth > 1 contraction
The contraction is restricted to #p = 2 by the depth scoping axiom, and the Open Questions correctly flag the TA4 zero-prefix collision at deeper ordinals. Generalizing D-SEP/D-DP to depth > 1 is future territory, not a defect here.

VERDICT: REVISE
