# Review of ASN-0043

## REVISE

### Issue 1: L9 formal statement is trivially satisfied and does not capture ghost-permission
**ASN-0043, L9 (TypeGhostPermission)**: "`... coverage({(s, ℓ)}) ⊄ dom(Σ'.C) ∪ dom(Σ'.L)`"
**Problem**: The witness type endset is the unit-depth span `(g, δ(1, #g))`, whose coverage is `{t : g ≼ t}` (by PrefixSpanCoverage) — an infinite prefix cone (T0(b)). Since `dom(Σ'.C) ∪ dom(Σ'.L)` is finite, the cone is *never* a subset of it, regardless of whether `g` is a ghost. The condition `coverage ⊄ domains` is therefore trivially true for **every** link, including one whose type endset points at live, stored content (the cone still escapes the finite domains via deeper extensions). The formal statement thus fails to express the substantive claim — that the *type address itself* need not be stored. The witness in fact proves the stronger, intended fact (`g ∉ dom(Σ'.C) ∪ dom(Σ'.L)`), so the statement is weaker than what is established and weaker than the prose ("references an address outside ... ghost").
**Required**: State the claim on the referenced type address directly — e.g., the span's start `g ∉ dom(Σ'.C) ∪ dom(Σ'.L)` (equivalently, that the canonical type address is unstored), rather than a subset condition on an infinite coverage cone.

### Issue 2: L1c chain prose restates clauses already in the formula
**ASN-0043, L1c, paragraph after the *Chain* formula**: "The seed `s` is constrained as a T4-valid tumbler with `zeros(s) = 2` ... the first step `k₁ = 2` lifts depth strictly above `#s` ... every subsequent intermediate state has length strictly greater than `#s`."
**Problem**: All three asserted facts (`T4-valid(s) ∧ zeros(s) = 2`, `k₁ = 2`, `#tᵢ > #s`) are already conjuncts of the Chain formula immediately above. The paragraph re-narrates the formula without advancing the argument — meta-prose the reader must skip to reach the actual postconditions.
**Required**: Delete the restatement; retain at most the one genuinely new gloss (the field-separating zero seated at position `#s + 1`), which is the only content not already in the formula and which CPP/the postcondition consumes.

### Issue 3: L9 witness defers its core construction downstream, forcing a forward jump
**ASN-0043, L9, *Choice of `a`* paragraph**: "The concrete construction of `a` and the freshness argument `a ∉ dom(Σ.L)` are case-split per `d'`'s prior link-allocation state and discharged in the L1c verification below ... exhibited there by direct chain-prefix and case-hypothesis reasoning."
**Problem**: The witness names the address `a` it depends on but explicitly defers both its construction and its freshness to a later "*Application to L9*" block, while simultaneously deferring producibility (for L1c) and disjointness (for L11a) to the same place. This is the multiple-paragraphs-defer-to-one-downstream-location pattern: the proof of L9 cannot be followed in place, and the reader must hold an unconstructed `a` across the FSP lemma before the construction appears.
**Required**: Construct `a` (the Case A / Case B split) at the point of first use, or invert the order so FSP and its application precede the L9 conclusion that depends on them. Collapse the triple forward-pointer into one.

### Issue 4: FSP application carries a use-site inventory of invariants
**ASN-0043, after FSP proof**: "The remaining items — non-state-local invariants: theorems, definitions, and meta-lemmas (L2, L4, L7, L8, L10, L13) — are proven once over all conforming states and require no per-state re-verification."
**Problem**: This is a catalog of which labels are handled where — proof-bookkeeping prose, not reasoning. It enumerates downstream items rather than advancing any claim. The same bookkeeping recurs in the worked example ("We record per step only the *substantive* new checks").
**Required**: Drop the inventory. If a reader needs to know an invariant is state-independent, that belongs to the invariant's own statement (its type column already marks META/LEMMA), not to a roster appended to FSP.

### Issue 5: Worked-example factoring paragraph is essay content about proof organization
**ASN-0043, Worked Example, *Each added link is a fresh sibling.*** : "... We record per step only the *substantive* new checks: the L11b non-injectivity witness (Step 1), the link-to-link reference L13 (Step 2) ..."
**Problem**: This paragraph describes how the subsequent four steps are organized and which checks are omitted, rather than performing verification. It re-discharges FSP's (h1)–(h3) hypotheses generically and then announces an editorial policy for the steps below — meta-prose in a verification slot.
**Required**: Replace with a single sentence ("Each of `a'`, `a₂`, `a₃`, `a₄` is the next `inc(·,0)` sibling of the previous link; FSP applies, so only the new check per step is shown below.") and let each step carry its own substantive check.

### Issue 6: Forward references to L3 in the type-accessor definition
**ASN-0043, *Named accessor* and *Convention — StandardTriple***: "Slot 3 is the type endset for every conforming link by L3 (below) ..."; the accessor `Σ.L(a).type ≡ Σ.L(a).e₃` is introduced before L3 is stated.
**Problem**: The abbreviation's well-definedness (`|Σ.L(a)| ≥ 3`) is justified by an invariant stated later, so the definition leans forward on a not-yet-given claim. Minor, but it is the forward-reference accretion this note is flagged for.
**Required**: Either move the `.type` abbreviation to immediately after L3, or note that the accessor is conditional and discharged by L3 without the parenthetical "(below)" cross-pointer.

## OUT_OF_SCOPE

### Topic 1: Lifting L0a/L14a from the `s_C`-resident slice to all of `dom(Σ.C)`
**Why out of scope**: This depends on ASN-0036 absorbing a global content-subspace constant, which is correctly recorded as the first Open Question. It is future foundation work, not an error here.

META: (none — the ASN defines state (Σ.L), invariants, and an abstract link structure that any implementation must satisfy; it has not drifted into implementation mechanics.)

VERDICT: REVISE
