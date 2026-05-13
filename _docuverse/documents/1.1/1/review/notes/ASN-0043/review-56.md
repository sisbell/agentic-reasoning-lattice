# Review of ASN-0043

## REVISE

### Issue 1: Cross-document distinctness misattributes `home(a) = d` to L1a's formal content
**ASN-0043, Home and Ownership**: "For links `a₁, a₂` allocated under distinct documents `d₁ ≠ d₂`, L1a gives `home(a₁) = d₁` and `home(a₂) = d₂`"

**Problem**: L1a's formal statement is `(A a ∈ dom(Σ.L) :: N(a).0.U(a).0.D(a) ∈ dom(Σ.M))` — it establishes only that the extracted document-level prefix is *some* allocated document, not that it equals the document under which `a` was allocated. The equality `home(a) = d` (creating document) is structural: it follows from the L1c chain's prefix-preservation property — `inc(·, k')` for `k' ∈ {0, 1, 2}` preserves positions 1..#d via TA5(b)/(c), so `a`'s first #d components match `d`. The proof prose conflates the informal "creating document" reading of L1a with the formal membership clause, then routes the entire cross-document argument through "L1a gives". The same misattribution appears in the surrounding prose ("By L1a, the document-level prefix of `a` identifies the document whose owner created the link"). L1a as stated cannot do this work alone.

**Required**: Choose one of: (a) strengthen L1a's formal statement to capture creating-document identification directly; (b) add a separate lemma deriving `home(a) = d` from the L1c chain's prefix-preservation property (citing TA5(b)/(c) and L1c chain step structure), and route the cross-document argument through that lemma; or (c) define "allocated under `d`" structurally as `home(a) = d`, reducing cross-document distinctness to a direct application of T3 on the premise. The proof must not depend on a derivation that L1a's formal content does not deliver.

### Issue 2: L11b verification cites T10a.4 for zero count preservation; T10a.4 establishes only T4-validity
**ASN-0043, L11b proof (Conformance of Σ'), L1/L1b bullet**: "`zeros(a') = 3` follows from T10a.4 plus the structural form of the allocator chain at element field depth ≥ 2"

**Problem**: T10a.4 (T4PreservationUnderDiscipline) establishes T4-validity, which yields only `zeros ≤ 3`, not the specific value `zeros = 3`. The correct citation for sibling zero count preservation is T10a.8 (UniformSiblingZeroCount): every `inc(·, 0)` sibling shares the base's zero count. Length preservation comes from T10a.1 (or TA5(c)) and element-field projection from T4b. "The structural form of the allocator chain" hand-waves over T10a.1 and T10a.8 without naming them. At Dijkstra's standard for citation, this is exactly the kind of "by similar reasoning" gloss that the review brief calls out: the citation does not establish what it claims, and a reader who does not already know T10a.8 cannot verify the step.

**Required**: Expand the citation chain: from `zeros(a) = 3` (L1 on Σ) and `#E(a) ≥ 2` (L1b on Σ), the sibling-advance construction gives `#a' = #a` (TA5(c)/T10a.1), `zeros(a') = zeros(a) = 3` (T10a.8), and T4-validity of `a'` (T10a.4) — from which `#E(a') ≥ 2` follows by T4b. Naming the specific T10a sub-claims discharges L1 and L1b for `a'` without the "structural form" gloss.

## OUT_OF_SCOPE

None substantive — the Scope section correctly excludes operations, search semantics, version creation, replication, and indexing implementation, and the Open Questions list legitimate future ASN topics.

VERDICT: REVISE
