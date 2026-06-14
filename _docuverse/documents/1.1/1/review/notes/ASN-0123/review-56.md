# Review of ASN-0123

I read the note as a derivation of CREATENEWVERSION from the guarantees it must keep, and checked each load-bearing proof against its cited foundations. The proofs that could plausibly have failed are the apparatus lemmas (SA, VN-B1) and the ownership theorems (V8, V9 severance), plus the operation's validity (V-WF) and the carry-through biconditional (V10). I worked each of these and they hold.

**Verification record (the claims I checked line-by-line):**

- **SA** — the antichain proof is sound. Two stored addresses `a = [d₀,0,s,k] ≺ b = [d',0,s',k']` force `#d' ≥ #d₀+1`; `b` inherits `a`'s separator zero at position `#d₀+1`, which lands inside `d'`, giving `d'` three zeros against `zeros(d') = 2`. The appeal to LP-Sub's `#E = 2` structural form is legitimate (substrate chains emit `#E = 2` exactly).
- **VN-B1** — the contiguity induction is exhaustive over K.δ. The case split (Node excluded by `zeros=2`; base-tier spawn `k=g` forces `j=1`; other inter-tier spawn `k=3−g` excluded by the penultimate-component mismatch; `k=0` sibling forces `t = c_{j−1}` and `j = m+1` via IH + freshness) covers `k ∈ {0,1,2}` for both `g=1` and `g=2`. The penultimate-component exclusions check out arithmetically. Proving the B1-analog directly over K.δ rather than citing ASN-0040 B1 is correct, since the transition systems differ.
- **V9 severance** — `¬(d_src ≼ v)` is genuinely a theorem. The structural O5(ii) discharge (length-`(#pfx(π)+1)` prefix `[pfx(π),0]` has `zeros = 2`, forcing any longer coverer to violate O1a) is sound, and the severance argument closes both branches (`d_src ≼ pfx(π)` → Z-mono contradiction; `pfx(π) ≼ d_src` → contradicts `ω(d_src)=π_o` maximality). This is the reviewer-protected content; it is correct and I did not trim it.
- **V8** — coverer-set equality (`coverers(v) = coverers(d_src)` via Z-mono + Covering-chain) correctly yields `ω'(v) = ω(d_src)`.
- **V-WF** — both ValidComposite★ clauses discharge. The cross-owner branch correctly resolves `nextd` to one document-tier K.δ in `A_doc(pfx(π)) = S(pfx(π),2)`, establishes `v ∈ E_doc` before the K.μ⁺ precondition is needed, and the J1★/J1'★ couplings are pinned exactly by the `R'` clause. The single-identity count holds because P-tier excludes the node-tier cross-owner case (which would require minting account+document).
- **V10** — the biconditional reduces correctly to LP12 at `d=v` (using `L'=L` and `ran(M'(v)) = A`); LP12's preconditions (`a ∈ dom(Σ'.L)`, `v ∈ dom(Σ'.M)`) are met.
- **V9w** — `(a, d_src) ∈ R` via P4★ requires `Σ` a composite boundary, which P-bdy supplies; `(a, v) ∈ R'` via V13. Both worked instances (owned and cross-owner) are arithmetically correct, including the `|A| = 2 < n = 3` shared-address case and the position-4 severance divergence.

**Boundary coverage:** empty source (`n=0`), shared content (`|A| < n`), cross-owner empty source (vacuous witness, state-indistinguishable from fresh doc), first vs. subsequent fork (`hwm = 0` vs. `≥ 1`), node-tier forker (excluded). All handled. Concrete examples are present and verified. No cross-ASN references outside the foundation set (all of 0034/0036/0040/0042/0043/0045/0047/0058/0093/0098 are foundations).

**Anti-bloat scan:** After the recent tightening (V0/V7/G2 prose, consultation-55), the meta-prose surface is small. I tested the suspicious passages against "would a precise reader skip this?": the atomicity remark (states the boundary-level guarantee and the real interior-state gap), the J4 relation remark (heads off "isn't this J4?"), V11's window paragraph (distinguishes required isolation from optional tracking-as-query), and the P-tier scope note (states the non-obvious "source read without permission" property) all advance the argument. The V0 "no third branch contributes to the count" sentence initially read as defensive exhaustiveness, but it is load-bearing — it ties the count to P-tier's domain restriction, justifying "exactly one identity." I found no paragraph imagining an excluded case, no relocated-finding content, no consumer-enumeration in definitions, and no same-thing-twice duplication that rises to a finding.

## REVISE

None. I have no correctness, missing-case, depth, or prose-clarity issue to raise. The non-trivial weakest-precondition content the rigor standard asks for (exact condition for post-fork link discoverability) is present as V10's biconditional; derived consequences are explored throughout (V12 from V0+V2, V9w from V13+P4★, the renumber-or-refuse dilemma in V6); the key postconditions are checked against the implementation's own addresses in two worked instances.

## OUT_OF_SCOPE

### Topic 1: The PS ownership-over-transition-model bridge
**Why out of scope**: Reading ASN-0042's `ω`/`pfx` over ASN-0047's states is a hybrid the foundations do not assemble, and the note correctly declares it as a standing assumption (PS), deriving the one consequence it needs (`ω` totality) rather than assuming it. Making this bridge a verified foundation is future work, not an error here.

### Topic 2: Serialization of concurrent forks
**Why out of scope**: The interior state (after K.δ, before K.μ⁺) is genuinely exposed, and the note flags this honestly as open question Q4. The whole-request serialization is realized architecturally in the implementation (single-threaded run-to-completion), which the note records as the foundation-unspecified guarantee.

### Topic 3: Versioning link-subspace material (links about links)
**Why out of scope**: V2b proves foreign-origin links cannot be seated in the version's link subspace, and V10 shows content anchoring is the complete cross-fork connectivity channel. Whether a separate non-fork mechanism should make link-subspace material itself versionable is correctly deferred (Q3).

VERDICT: CONVERGED
