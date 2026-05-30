# Review of ASN-0043

## REVISE

### Issue 1: L11a summary table contradicts the body derivation
**ASN-0043, Properties Introduced table (L11a row) vs. "Link Distinctness and Permanence" body**: The table says L11a's proof proceeds by a two-case split — "chain-prefix-preservation excludes the cross-home case ... and T10a's per-(t, k') discipline excludes the same-home case (two distinct chains terminating identically force back-coincidence)."
**Problem**: The body derivation explicitly disavows any case split: "Instantiating GlobalUniqueness at the link-address events therefore yields `a₁ ≠ a₂` for distinct events directly, with no separate case split on `home(a₁)` versus `home(a₂)` — GlobalUniqueness already covers both configurations." The two descriptions of the same proof are mutually exclusive. This is reviser drift — the table retains a superseded two-case account.
**Required**: Reconcile. If the body's "instantiate GlobalUniqueness, no case split" is the intended proof, rewrite the table row to match (drop the cross-home/same-home language).

### Issue 2: Worked-example length leaks into the general L9 lemma
**ASN-0043, L9 proof, "T12 well-formedness of `(g, δ(1, #g))`"**: "By the construction of `g` above, `#g = #d' + 3 = 5 + 3 = 8 ≥ 1`".
**Problem**: L9 is quantified over *any* conforming `Σ`, and `d'` is selected as "any `d ∈ dom(Σ.M)`" — an arbitrary document-level tumbler. Its length is not 5. The "= 5 + 3 = 8" imports the concrete worked-example value into a general lemma proof. The conclusion (T12 holds, needing only `#g ≥ 1` with action point `k = #g ≤ #g`) survives, but the asserted equality is false for general `d'`.
**Required**: State `#g = #d' + 3 ≥ #d' + 1 ≥ 1` (or note `#d' ≥ 5` for document-level tumblers, giving `#g ≥ 8`), without fixing `#d' = 5`.

### Issue 3: S7c cited but absent from the ASN-0036 foundation
**ASN-0043, multiple sites**: "for content addresses, S7b (ASN-0036) and S7c supply T4-validity, `zeros = 3`, and `#E ≥ 2 > 1`"; "This parallels S7c (ElementFieldDepth, ASN-0036)"; worked example "*S7c (ContentElementFieldDepth, ASN-0036).*"
**Problem**: The ASN-0036 foundation provided here defines S7, S7a, S7b, S7d — but no S7c. S7c is a load-bearing citation for `#E(a) ≥ 2` on content addresses, yet it is not among the verified foundation claims. As written this is a dangling reference (foundation exception covers only claims that actually exist in the foundation).
**Required**: Either confirm S7c exists in ASN-0036 and correct the foundation, or weaken the dependence — `subspace_I(b) = E(b)₁` needs only `#E ≥ 1`, which S7b's `zeros(b) = 3` plus T4's field-segment constraint already delivers; drop the `#E ≥ 2` appeals to S7c where only `#E ≥ 1` is used.

### Issue 4: Axiom-justification essay prose around L1c
**ASN-0043, L1c, paragraphs "*Why `k₁ = 2` is the only `kᵢ = 2` step…*" and "*Why `k₁ = 2`, not `k₁ = 1`.*"**
**Problem**: The formal clause already binds `k₁ = 2` as a conjunct. These two paragraphs argue *why the axiom is structured this way* (k₁=1 is "structurally unreachable," subsequent kⱼ=2 is foreclosed) rather than stating what the axiom says — exactly the "new prose around an axiom explains why the axiom is needed rather than what it says" pattern. The structural facts they establish (third zero at position `#s+1`, `s = h(a)`) are already captured by the `s = h(a)` postcondition.
**Required**: Collapse both paragraphs into at most a one-line note that the single `k₁ = 2` step seats the field-separating zero, discharged by the `s = h(a)` postcondition. Remove the design-rationale argumentation.

### Issue 5: Repeated T4-validity derivation boilerplate
**ASN-0043, Notational convention / L0a / L1a / "Home and Ownership" / LinkHome / home(a) table**: the parenthetical "(derived via T10a.4 — T4PreservationUnderDiscipline, ASN-0034 — from the allocator chain)" recurs verbatim at ~six sites, and the "Home and Ownership" opening re-walks the full T4-validity-of-link-addresses derivation that L1c already establishes as a postcondition.
**Problem**: Use-site repetition of one derivation. The derivation should appear once (at L1c, where the postcondition is established) and be cited by name elsewhere. The "Home and Ownership" re-derivation duplicates the LinkHome definition's justification and L1c's postcondition.
**Required**: State the T4-validity derivation once at L1c; replace the other occurrences with a bare cite ("by L1c's T4-validity postcondition"). Delete the re-derivation paragraph in "Home and Ownership."

### Issue 6: Scope-lift point repeated across five sections
**ASN-0043, L0a / L9 precondition discussion / L14 / L14a / Open Questions**: the claim "a future ASN-0036 revision that fixes a content-subspace constant would lift L0a's scope from the `s_C`-resident slice to all of `dom(Σ.C)`" is stated five times in near-identical words (L0a final sentence; L9 "would be vacated by a future ASN-0036 revision…"; L14 "any future ASN-0036 revision absorbing a content-subspace constant would fix universally"; L14a "outside the `s_C`-resident regime…"; Open Questions bullet 1).
**Problem**: "Multiple paragraphs in different sections say the same thing." The forward-looking scope essay belongs in one place.
**Required**: State the scope-lift caveat once (Open Questions is the natural home) and remove the repetitions from L0a, L9, L14, L14a, retaining only the bare scoped-disjointness fact at each.

### Issue 7: Self-described bookkeeping inventory in the L9 proof
**ASN-0043, L9 proof, "*Theorems, lemmas, and meta-claims.*"**: "We list them at the end of this proof for the reader's bookkeeping but do not re-establish them per-state," enumerating L2, L4, L7, L8, L9, L10, L11b, L12a, L12b, L13.
**Problem**: A use-site inventory of which invariants are *not* checked, admittedly for "bookkeeping." It advances no reasoning — the conformance proof needs only the state-local checks, which are already listed above it.
**Required**: Delete the inventory, or reduce to a single sentence ("non-state-local invariants — theorems, definitions, and meta-lemmas — require no per-state re-verification").

## OUT_OF_SCOPE

### Topic 1: Discoverability/removal mechanism for superseded links
**Why out of scope**: L12 correctly notes that the mechanism by which a replaced link "ceases to be discoverable" is an operations question (REMOVELINK / arrangement-layer visibility), which the Scope section excludes. The ASN handles this correctly by deferring; no action needed.

META: (none — the ASN defines state, invariants, and a worked verification at the right abstraction level; it is bloated and carries a few defects, not off-track.)

VERDICT: REVISE
