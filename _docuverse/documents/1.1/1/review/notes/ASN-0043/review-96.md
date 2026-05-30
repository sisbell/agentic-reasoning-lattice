# Review of ASN-0043

## REVISE

### Issue 1: FSP's producibility hypothesis is weaker than the L1c contract it claims to discharge

**ASN-0043, FreshSiblingConformance (FSP), hypothesis (h2) and the L1c bullet of its proof**: h2 reads "*Producibility:* `a` is the terminus of a T10a-conforming chain seeded at a T4-valid document-level tumbler `home(a) ∈ dom(Σ.M)`," and the proof discharges L1c with "*L1c.* `a` is the terminus of a T10a-conforming chain (h2)."

**Problem**: L1c's formal contract is *not* "some T10a chain from `home(a)` to `a`." It additionally requires `k₁ = 2` and `(A i : 1 ≤ i ≤ n : #tᵢ > #s)`. A generic T10a-conforming chain satisfies neither automatically: `inc(·, 0)` preserves length (TA5(c)), so a chain beginning with a document-level sibling step has `#t₁ = #s`, violating `#tᵢ > #s`, and has `k₁ = 0 ≠ 2`. The reason these clauses hold — that `home(a) =` seed forbids any document-level sibling step, forcing the first operative step to be the `k'=2` separator-seating descent (the only way to move `zeros` from 2 to 3) — is a real derivation that FSP omits entirely. As written, FSP discharges L1c's strong conjuncts from a hypothesis that does not entail them.

**Required**: Either strengthen h2 to require an L1c-form chain (`k₁ = 2`, `#tᵢ > #s` for all `i`), or add the one- to two-line argument that the seed-equals-home constraint forces both conjuncts.

### Issue 2: The "L3 non-emptiness binds slot 3 only" fact is restated three times

**ASN-0043, FSP proof (L3 bullet), L9 construction paragraph, and the L9 row of Properties Introduced**: FSP: "(the non-emptiness conjunct constrains slot 3 alone, so empty slots `4..N` are admissible)"; L9: "L3's slot-3 non-emptiness clause constrains slot 3 alone (slots `4..N` may be empty by the per-slot `eᵢ ∈ Endset` conjunct's admission of `∅`)"; table row: "(admissible by L3's slot-3-only non-emptiness conjunct)."

**Problem**: The same structural fact about L3 is asserted in three places in three phrasings — the "two paragraphs say the same thing in different words" anti-bloat pattern. A reader following the padding argument re-encounters the identical justification without new content.

**Required**: State the slot-3-only reading once (at L3 or at first use in FSP) and reference it; drop the restatements in L9's prose and the table row.

### Issue 3: L1b is asserted without grounding or derivation, yet is load-bearing

**ASN-0043, L1b — LinkElementFieldDepth**: "Every link address has element field depth at least 2: `(A a ∈ dom(Σ.L) :: #E(a) ≥ 2)`."

**Problem**: Unlike L0, L1, and L1a — each of which carries Nelson/Gregory grounding or an explicit derivation — L1b is a bare invariant with neither. It is not idle: L9 Case B and L11b both rely on `#E(a) ≥ 2` to conclude that `inc(·, 0)` advances the ordinal while *fixing* the subspace identifier (because the subspace identifier `E₁` is then not the terminal `sig` position). A load-bearing constraint stated with no rationale leaves the reader unable to judge why depth 2 (subspace identifier + within-subspace ordinal) rather than depth 1 is required.

**Required**: Ground or derive `#E(a) ≥ 2` — e.g., that a link address needs both a subspace identifier `s_L` and an ordinal within it, mirroring S8a's `#t ≥ 2` for V-positions.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace residence
The note scopes disjointness and non-transcludability (L0a, L14a) to the `s_C`-resident slice of content, and the first Open Question already names the global-constant strengthening. Extending disjointness to all of `dom(Σ.C)` belongs to a future content-side invariant, not this ASN.

VERDICT: REVISE
