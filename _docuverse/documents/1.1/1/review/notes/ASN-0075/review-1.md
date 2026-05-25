# Review of ASN-0075

## REVISE

### Issue 1: D-EXH proof skips required chain through L14 and S3★
**ASN-0075, Three States of Content (D-EXH proof)**: "if `a ∈ ran(M(d))` and `subspace_I(a) = s_C`, then `(a, d) ∈ Contains_C(Σ) ⊆ R`"

**Problem**: `Contains_C(Σ)` requires a V-position with `subspace(v) = s_C`. The proof only has `a ∈ ran(M(d))`, which yields some `v` with `M(d)(v) = a` but not that `subspace(v) = s_C`. The link from `subspace_I(a) = s_C` to `subspace(v) = s_C` requires invoking L14 (a ∈ dom(C) ⟹ a ∉ dom(L)) and the contrapositive of S3★ (if subspace(v) = s_L then M(d)(v) ∈ dom(L), so M(d)(v) ∉ dom(C)).

**Required**: Make the chain explicit: (i) `subspace_I(a) = s_C` requires `a ∈ dom(C)` (subspace_I precondition); (ii) by L14, `a ∉ dom(L)`; (iii) by S3★, the V-position with M(d)(v) = a must satisfy subspace(v) = s_C; (iv) hence `(a, d) ∈ Contains_C ⊆ R` by P4★.

### Issue 2: D-ORD claims false uniqueness of vpos_B
**ASN-0075, Order Preservation**: "define `vpos_B(a)` as the unique (by S2) V-position satisfying `M(d_B)(vpos_B(a)) = a`"

**Problem**: S2 establishes V→I functionality (each V maps to at most one I), not I→V injectivity. S5 (UnrestrictedSharing) explicitly proves that within a single document, an I-address can be at arbitrarily many V-positions: "within a single document (multiplicity `N + 1` at `N + 1` distinct V-positions)." When content is transcluded multiple times in `d_B`, vpos_B(a) is not unique.

**Required**: Either replace with a deterministic choice such as `vpos_B(a) = min{v : M(d_B)(v) = a}` (well-defined by T1 totality and S8-fin), or acknowledge that the ordering is fixed only up to choice of representative.

### Issue 3: D-ACT cites M11-M12 for wrong decomposition
**ASN-0075, Actionability**: "by construction (and using the canonical-decomposition results of ASN-0058, M11–M12, applied to the witness's arrangement restricted to the deletion set), the deletion set decomposes uniquely into a finite collection of maximal witness runs."

**Problem**: ASN-0058's M11-M12 decompose V→I arrangements into mapping blocks `(v, a, n)`. A deletion witness run `(i_start, ℓ, origin)` is a maximal I-contiguous run of same-origin I-addresses — a property of an I-set alone, no V-structure. Two I-contiguous addresses in the deletion set can correspond to non-V-adjacent blocks in M(d_B), so the M11-M12 block decomposition gives a different (finer) grouping than the witness-run decomposition.

**Required**: Either provide a direct proof of unique decomposition (sort by T1, group by I-adjacency and same origin) or remove the M11-M12 citation.

### Issue 4: No concrete worked example
**ASN-0075, throughout**

**Problem**: The standards require verification of key postconditions against at least one specific scenario. The most natural scenario for SHOWDELETIONS is a fork: `d_B = inc(d_A, 1)` populated by transclusion, then divergent edits delete content from each side. The ASN never exhibits this, leaving its claims unverified against the canonical case.

**Required**: Add a concrete scenario — e.g., document `d_A` with arrangement `{v_1 ↦ a, v_2 ↦ b, v_3 ↦ c}`, fork to `d_B`, delete `b` from `d_A`, delete `c` from `d_B` — and trace through SHOWDELETIONS to verify D-EXH, D-IDENT, D-ORIG, and D-SYM.

### Issue 5: wp analysis trivial
**ASN-0075, SHOWDELETIONS Operation**: "Then `wp(SHOWDELETIONS(d_A, d_B), q) = (d_A ∈ E_doc ∧ d_B ∈ E_doc)`. The operation always terminates with `q` true when its precondition holds."

**Problem**: This wp is essentially a restatement of the precondition for an observational operation that always succeeds. The standards require non-trivial wp analysis. Substantive questions go unexplored: under what state conditions does the result identify content recoverable via D-IDENT? When does `DeletedFromAWithB ≠ ∅` hold? What precondition guarantees `DeletedFromAWithB ∪ DeletedFromBWithA` exhausts the symmetric difference of historical arrangements?

**Required**: Add at least one non-trivial wp computation — for instance, wp of "every deleted address has a witness in the partner document" or wp of "the output is non-empty implies shared provenance history."

### Issue 6: D-DISCR uses informal transition language
**ASN-0075, Why Provenance Is Load-Bearing (D-DISCR argument)**: "In the first, document `d` is created, content `a` is inserted into its arrangement, then `a` is removed."

**Problem**: For a load-bearing claim that justifies the existence of `R` in the state, the construction should name specific transitions from ASN-0047. The reader must reconstruct which of K.δ, K.α, K.μ⁺, K.μ⁻ are intended. Furthermore, the second scenario relies implicitly on the same `a`-value being allocatable in both histories, which by GlobalUniqueness requires identical allocator firings — this assumption goes unstated.

**Required**: Name the transitions explicitly: history 1 = K.δ(d) ; K.α(a, d) ; K.μ⁺(d, v ↦ a) ; K.μ⁻(d, ∅), and history 2 = K.δ(d) ; K.α(a, d) ; K.μ⁺(d', v' ↦ a). Confirm that `dom(C)` and `M(d)` agree across both final states.

### Issue 7: Open question on DELETED monotonicity is already established
**ASN-0075, Open Questions**: "What invariants must hold over the evolution of R to ensure that DELETED is monotone — once classified DELETED, always classified DELETED unless content is re-introduced into the document's arrangement?"

**Problem**: This is not open. P2 gives `R ⊆ R'` across transitions, so the R-part of DELETED is preserved. The other clause (`a ∉ ran(M(d))`) can only be falsified by K.μ⁺ adding `a` to M(d), which is exactly the "re-introduction" caveat the question allows. The foundation already supplies the answer.

**Required**: Remove this question or refine it to something genuinely open — for instance, whether reorderings (K.μ~) can affect DELETED classification, or whether the system can express "deleted with intent to permanently remove" as opposed to "transiently absent."

## OUT_OF_SCOPE

### Topic 1: Per-document link-subspace deletion analysis
**Why out of scope**: D-SUBSP correctly excludes cross-document link-subspace comparison via CL-OWN. A within-document notion of "link removed from arrangement" is a separate operation requiring its own specification of what `R`-analogue would be needed.

### Topic 2: Multi-document (N ≥ 3) SHOWDELETIONS
**Why out of scope**: The open question about N-document generalization names a future ASN, not a defect in this one.

### Topic 3: Restoration operation specification
**Why out of scope**: The composability discussion correctly notes restoration is possible but explicitly defers its specification.

### Topic 4: Authorization and access control for SHOWDELETIONS
**Why out of scope**: The ASN is about state observation; permission systems are a separate concern.

VERDICT: REVISE
