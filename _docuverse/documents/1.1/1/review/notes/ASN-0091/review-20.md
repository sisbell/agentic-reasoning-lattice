# Review of ASN-0091

## REVISE

### Issue 1: Subspace preservation argument is one-sided
**ASN-0091, "REARRANGE as Vstream-Only Operation" section**: The text claims "RA-adm together with foundation S3★ + L14 already forces *subspace preservation* — no V-position may cross from one subspace to another under π" and proves:

> "An admissible bijection cannot carry a content-subspace V-position to a link-subspace V-position, since the post-state image would land in `dom(Σ'.C)` while S3★'s link-subspace clause demands a `dom(Σ'.L)` value, and these stores are disjoint by L14."

**Problem**: Only the content→link direction is argued. The conclusion "no V-position may cross from one subspace to another" requires both directions: content-subspace v cannot map to link-subspace AND link-subspace v cannot map to content-subspace. The symmetric direction (link→content) is left implicit, even though the same admissibility-clashing argument has to be re-instantiated (via RE-L and S3★'s content-subspace clause). This claim is the load-bearing step for showing RE-sub's pointwise-fixity strengthening is REARRANGE_K-specific (a key structural distinction in the ASN), so the proof should be complete.

**Required**: Add an explicit symmetric paragraph (or "by symmetric reasoning, applying RE-L in place of RE-C") covering the link→content case. The argument is analogous: v has subspace s_L; Σ.M(d)(v) ∈ dom(Σ.L) by S3★ at Σ; if π(v) has subspace s_C, then RA-π gives Σ'.M(d)(π(v)) ∈ dom(Σ.L) = dom(Σ'.L); S3★ at Σ' demands Σ'.M(d)(π(v)) ∈ dom(Σ'.C); L14 contradicts.

### Issue 2: "Governed by ASN-0098's LP-Comp" misstates LP-Comp's status
**ASN-0091, "Composition Across Multi-Step REARRANGE Sequences" section**: "the REARRANGE steps in such a mixed sequence are themselves governed by ASN-0098's LP-Comp (case-analysis over K.μ~) at the projection layer"

**Problem**: LP-Comp is explicitly marked as a NOTE in the shared vocabulary ("Documentation note, not a load-bearing lemma"). The actual lemma governing K.μ~ projection behavior is LP11 (ReorderingRebinding). The current phrasing reads as if LP-Comp is the load-bearing result, but LP-Comp only catalogs the case-split — LP11 is what discharges the K.μ~ case.

**Required**: Replace "governed by ASN-0098's LP-Comp (case-analysis over K.μ~) at the projection layer" with "governed by ASN-0098's LP11 (the K.μ~ case in LP-Comp's case-analysis) at the projection layer" (or similar phrasing that names LP11 as the substantive lemma and LP-Comp as the documentation device).

### Issue 3: ChainDisjointAdjacency lemma could appeal to a simpler argument
**ASN-0091, "Run Decomposition Is Not Invariant" section, inline ChainDisjointAdjacency lemma**: The proof argues structural equality of tumblers via T3 and component analysis.

**Problem**: A simpler argument is available and is implicit in the proof but not invoked: `x + 1 = inc(x, 0) ∈ dom(A_{s_X}(d_X))` by sub-allocator chain closure, and `y ∈ dom(A_{s_Y}(d_Y))`. By T10a's GlobalUniqueness / T10a.6 (DomainDisjointness), `dom(A_{s_X}(d_X)) ∩ dom(A_{s_Y}(d_Y)) = ∅` when the chains differ. Therefore `x + 1 ≠ y`. The current structural argument is correct but reproves a piece of T10a.6 inline. The lemma is correct; this is about presentation clarity for a load-bearing lemma used three times.

**Required**: Either (a) cite T10a.6 (DomainDisjointness) as the primary argument and keep the structural argument as elaboration, or (b) explicitly note why the structural argument is preferred (e.g., for self-containment of the lemma's reasoning).

### Issue 4: Empty case admitted at the abstract level but RE-frag/RE-coal/RE-eq witnesses assume non-empty
**ASN-0091, "REARRANGE as Vstream-Only Operation" section** admits the empty case (π is the empty bijection, RA-π vacuously satisfied). But the existential witnesses for RE-frag, RE-coal, RE-eq all use non-empty cases.

**Problem**: The three existential claims (RE-frag, RE-coal, RE-eq) are stated abstractly without restricting to the non-empty case. Strictly, "There exist rearrangements ... such that cardinality strictly increases" is satisfied by the non-empty witnesses provided. But the empty case has |runs(Σ.M(d))| = |runs(Σ'.M(d))| = 0, which trivially satisfies RE-eq. This is consistent — the witnesses suffice — but the relation between admitted empty case and the existential claims isn't explicit. Minor.

**Required**: Either note that the empty case is also a (degenerate) RE-eq witness, or note that RE-eq's witness is intentionally non-degenerate (the worked equality witness has |dom(M(d))| = 2, non-zero cardinality 2).

### Issue 5: Worked example 4's RE-eq equivalent goes unflagged
**ASN-0091, "Worked Example — Bijection Non-Uniqueness Under Shared I-Addresses"**: Pre-state has 3 maximal runs (all singletons), post-state has 3 maximal runs (all singletons). This is a concrete RE-eq witness in addition to its primary purpose (bijection non-uniqueness).

**Problem**: The worked example is not cross-referenced as a RE-eq witness, even though the equality witness in "Run Decomposition Is Not Invariant" uses a less rich state. Cross-referencing would strengthen the section by showing the equality case persists in the presence of shared I-addresses.

**Required**: Add a brief cross-reference note in either section linking the two as related RE-eq cases.

## OUT_OF_SCOPE

### Topic 1: REARRANGE operations on the link subspace
The ASN restricts REARRANGE_K (via CS3) to S = s_C. Operations rearranging the link subspace are noted in Open Question 2 as future work.

**Why out of scope**: A hypothetical REARRANGE_L operation would require additional invariant analysis (CL-OWN, CL-UNIQ behavior under permutation) and a separate cut-sequence apparatus. The current ASN's scope is REARRANGE on the content subspace.

### Topic 2: Bijection uniqueness criteria
The ASN notes π is non-unique under S5 sharing. The exact condition under which π IS unique (i.e., when ran(Σ.M(d)) has no repeated values) is left implicit.

**Why out of scope**: A formal "uniqueness iff no I-address sharing" theorem would be a separate result. The ASN demonstrates non-uniqueness concretely (worked example 4) and shows RE-proj's set image is invariant across witnesses — which is the substantive consequence.

### Topic 3: Bounds on run-decomposition cardinality change per invocation
Open Question 4 asks about upper bounds on fragmentation increase.

**Why out of scope**: A quantitative bound would require analysis of the cut structure's interaction with the pre-state run partition — a separate combinatorial result.

### Topic 4: Cross-document transclusion fragmentation guarantees
Open Question 1 addresses the case where a transcluded span fragments under REARRANGE.

**Why out of scope**: The current ASN establishes RE-trans (the transclusion relationship persists) and RE-frag (fragmentation possibility). What guarantees are owed to the source document when the transcluding view fragments is a separate question about cross-document semantics.

### Topic 5: REARRANGE_K well-definedness verification
The ASN relies on ASN-0084's R-PIV/R-SWP for well-definedness of REARRANGE_K rather than re-proving them.

**Why out of scope**: ASN-0084 is a foundation ASN; its results are available without restatement.

VERDICT: REVISE
