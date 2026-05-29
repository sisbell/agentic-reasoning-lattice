# Review of ASN-0036

The proof obligations in this note are, on the whole, discharged rigorously: S8's partition proof handles the empty case, the within-subspace incompatibility lemma covers both `j < m` and `j = m`, the cross-subspace argument routes through T5/T10 correctly, and D-CTG-depth/D-SEQ are fully case-split with no "by similar reasoning." I checked the boundary cases (empty arrangement, `m = 2` collapsing to the single `j = m` branch, half-open exclusion of the successor V-position) and they hold. The remaining findings are accretion, not unsound logic — which is what this cycle's `review-mode.anti-bloat` classifier targets.

## REVISE

### Issue 1: `V_1(d)` defined twice; text-subspace scoping stated three times

**ASN-0036, Arrangement contiguity / Valid insertion position**:
- D-CTG intro: "This statement is specific to the text subspace (S = 1)... The contiguity properties below are stated for the text subspace (S = 1)." — the same scoping asserted twice in one paragraph.
- Abbreviation paragraph: "...write `V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}`... The specialization to the text subspace is `V_1(d) = {v ∈ dom(M(d)) : subspace(v) = 1}`."
- Valid insertion position section: "Write `V_1(d) = {v ∈ dom(M(d)) : subspace(v) = 1}` for the text-subspace V-positions of document d."

**Problem**: `V_1(d)` is given its full set-builder definition twice, identically, in different sections; the text-subspace restriction is stated three times. This is the "two paragraphs say the same thing in different words" pattern. A reader following a claim in the insertion-position section must re-verify it is the same `V_1(d)` already fixed earlier.

**Required**: Define `V_1(d)` once (at the abbreviation paragraph), state the text-subspace restriction once, and have later sections refer to it without re-stating the definition.

### Issue 2: meta-prose gesturing at out-of-scope operations inside the D-CTG base-case verification

**ASN-0036, paragraph following D-SEQ**: "D-CTG is a design constraint on well-formed document states. It constrains which arrangement modifications constitute well-formed editing operations. We verify the base case: before any operations, `dom(M(d)) = ∅`..."

**Problem**: The middle sentence ("It constrains which arrangement modifications constitute well-formed editing operations") points forward at editing operations — explicitly deferred to the Open Questions and out of scope — and does not advance the base-case verification it is embedded in. It is meta-prose the reader steps over to reach the actual claim (`dom(M(d)) = ∅ ⟹` vacuous satisfaction).

**Required**: Drop the operations-gesturing sentence; the base-case verification stands on its own.

### Issue 3: S8a's prose double-states its own content

**ASN-0036, S8a**: "Over the ℕ-carrier (T0), the domain-restriction axiom's conjunct `zeros(v) = 0` is definitionally componentwise positivity — `zeros(v)` (T4) counts the components equal to `0`, so `zeros(v) = 0 ⟺ (A i : 1 ≤ i ≤ #v : vᵢ > 0)`."

**Problem**: The sentence asserts the equivalence in words ("is definitionally componentwise positivity"), then immediately restates the same equivalence in symbols. A named handle for "componentwise positivity" is defensible given its many citations, but the prose says the thing twice before the formal contract says it a third time.

**Required**: Keep the symbolic equivalence; delete the prose paraphrase that precedes it.

## OUT_OF_SCOPE

### Topic 1: preservation of D-CTG/D-MIN/S2 under editing operations
The note verifies the contiguity invariants on the base state and on the worked-example states, but their preservation under DELETE/INSERT/REARRANGE is correctly deferred (Open Questions Q6). This is operation-layer territory, not a gap in this ASN.

VERDICT: REVISE
