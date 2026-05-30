# Review of ASN-0042

## REVISE

### Issue 1: O1a/O1b/T4 shared induction depends on axioms defined two sections later
**ASN-0042, *The Account-Level Boundary***: "O1a, O1b (PrefixInjectivity), and T4-validity of prefixes are all reachable-state invariants, established here by a single induction ... *Non-delegation step:* O15 admits no new principal and O13 (PrefixImmutability) fixes existing prefixes ... *O1a:* `π'` satisfies `zeros(pfx(π')) ≤ 1` by condition (iii). *T4:* Freshness-(v) supplies `T4(pfx(π'))` directly."
**Problem**: The induction cites O12, O13, O14 (by clause), O15's conditions (i)–(v), and Freshness-(v) — every one of which is defined in the later *State Axioms* section. A reader reaching this proof cannot verify it: the delegation predicate, the persistence/immutability axioms, and Freshness-(v) have not yet been stated. This is a genuine forward-dependency, not a stylistic one — the proof is unverifiable in linear reading order.
**Required**: Either relocate the shared induction to *State Axioms* (after O12–O18 and Freshness-(v)), or move the cited axioms earlier. The proof must follow the facts it consumes.

### Issue 2: Repeated forward deferrals to one downstream location
**ASN-0042, O1b**: "It is established by the shared induction in *The Account-Level Boundary*." (and the T4-validity invariant and the O1a intro each defer to the same induction)
**Problem**: Three separate statements in different positions point forward to a single proof site. This is the deferral-accretion pattern: the reader is bounced between sections to assemble one argument. Combined with Issue 1, the invariant `pfx`-machinery is scattered across three sections.
**Required**: Consolidate O1a, O1b, and the T4-prefix invariant with their shared induction in one place, stated after the axioms they depend on, so each is verifiable where it appears.

### Issue 3: O14 conjuncts cited by unlabeled ordinal position
**ASN-0042, O14 and its consumers**: "the coverage conjunct of O14's first clause", "O14's sixth clause", "O14's seventh clause", "third clause for O1a, fourth clause for O1b, fifth clause for T4", "O14(iii)", "O14(vi)", "O14(vii)".
**Problem**: O14 lists eight conjuncts as bare formula lines with no labels. At least six proofs and table rows reference them by counted ordinal ("seventh clause"). The reader must count unlabeled lines to resolve each citation, and any future insertion silently invalidates every downstream reference. Note also the first "clause" bundles two facts (`Π₀ ≠ ∅` *and* coverage), so "first clause" is already ambiguous.
**Required**: Label O14's conjuncts (O14.1–O14.8 or named tags) and cite by label throughout.

### Issue 4: Meta-prose around the cover-edge bridge and O7(c) condition taxonomy
**ASN-0042, *State Axioms* (bridge)**: "(Persistence of this edge into states beyond `Σ'` follows separately from O13 (PrefixImmutability), which fixes `pfx(π')` against later transitions.)" and **O7(c)**: "Condition (iii) ... genuinely constrains the target prefix `p''` ... Condition (iv) ... is, by contrast, discharged at `Σ'` independent of the choice of `p''` ... This recursive right is established only for the entry state `Σ'`..."
**Problem**: These passages classify which conditions matter and caveat the scope of the claim rather than advancing it; the bridge parenthetical is a deferral aside interrupting the derivation. This is the meta-prose the anti-bloat classifier targets — the precise reader must skip past condition-taxonomy commentary to reach the actual obligation on `p''` (conditions (iii) and (v)).
**Required**: State the binding obligations on `p''` directly (it must satisfy (iii) and (v); (i),(ii),(iv) are automatic at `Σ'`) and drop the per-condition justification narrative. Move the persistence parenthetical into the proof flow as a plain step or cut it.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer invariants
The Open Questions raise transfer (O3 currently forbids it). This is correctly deferred — the refinement-only regime is the system as specified.

### Topic 2: Realizing longest-match `ω` in an implementation
The final Open Question notes account-level containment decides only single-principal coverage. The implementation obligation for `ω` belongs to a future translation/implementation ASN, not here.

The mathematical content is sound: the covering-chain lemma, O2's four-step well-definedness, O3/O8 refinement and irrevocability, O10's Form-A/Form-B non-coverage analysis (both `zeros = 0` and `zeros = 1` branches), and the worked example all check out. The findings are organizational and anti-bloat, not correctness.

VERDICT: REVISE
