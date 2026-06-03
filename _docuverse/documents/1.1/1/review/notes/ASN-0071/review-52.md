# Review of ASN-0071

## REVISE

### Issue 1: Source self-inclusion is an unstated derived consequence
**ASN-0071, *The operation* / *Resolution***: `find(Q)(Σ) := { d ∈ Σ.E_doc : ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅ }`
**Problem**: A key sanity guarantee is provable but never stated: whenever `iaddrs_one(d_s, σ)(Σ) ≠ ∅`, the source document `d_s` is itself in the result. Proof: some `a = Σ.M(d_s)(v)` with `v ∈ ⟦σ⟧ ∩ dom(Σ.M(d_s))` gives `a ∈ ran(Σ.M(d_s)) ∩ iaddrs(Q)(Σ)`, and `d_s ∈ Σ.E_doc` by `wp-defined`. This is the formal bridge between the read-direction (what `d_s` contains) and the search-direction (who contains it) promised in the introduction — querying a document's own passage must return at least that document. The worked scenario silently exhibits it (`d_A ∈ find(Q)`) without naming it.
**Required**: State the consequence as a derived claim (`iaddrs_one(d_s, σ)(Σ) ≠ ∅ ⟹ d_s ∈ find(Q)(Σ)`) with its one-line derivation, or explicitly note its absence is intentional.

### Issue 2: Meta-prose in the finiteness proof
**ASN-0071, *Finiteness*, step (c)**: "finite ancestry is by definition of reachability, not a consequence of any single axiom."
**Problem**: This clause defends the epistemic status of the argument rather than advancing it. The load-bearing chain is: ExtendedReachableStateInvariants gives finite composite ancestry → each composite is a finite atomic sequence (ValidCompositeAmended) → finite concatenation of finite sequences is finite. The interjected aside is exactly the forward-reference/reviser-drift noise the precise reader must skip past.
**Required**: Delete the clause; keep the three-link chain.

### Issue 3: Visibility/access-control out-of-scope statement is deferred twice
**ASN-0071, intro ¶3** ("The visibility policy that would filter results by requester (LM 2/59) is a separate layer we leave out of scope") **and *What we do not specify* (iii)**.
**Problem**: The same exclusion is stated in two sections. The `What we do not specify` list is the structural home for scope exclusions; the intro restatement is redundant deferral to the same downstream point.
**Required**: State it once, in the scope section; the intro need not pre-announce it.

### Issue 4: PC-RANGE — a general claim derived inside the worked-scenario section
**ASN-0071, *A worked scenario* → "Cross-depth capture, in general"**: PC-RANGE is a general denotation characterization (`⟦σ⟧ ∩ dom(M(d_s)) = {...}` for arbitrary action-point width `ℓ_{#u}`), and it appears in the Claims table as an introduced claim.
**Problem**: A general lemma about what any vspec denotes against any arrangement is buried inside a concrete-example section, after the width-1 instance. Its derivation depends only on PC + T1 — it belongs alongside *Resolution* / *The query* where denotation is established, not as a generalization tacked onto one scenario. Placement, not existence.
**Required**: Relocate the PC-RANGE statement and derivation to the resolution/denotation development; the scenario may then cite it rather than introduce it.

## OUT_OF_SCOPE

### Topic 1: Relationship between current-containment result and the provenance relation R
**Why out of scope**: Correctly deferred to Open Questions; `find` reads only `E_doc` and `M`, and the `R`-coupling is genuinely new territory (currency vs. permanence), not a defect in this query spec.

### Topic 2: Rejecting vs. silently filtering unresolvable vspec positions (F-FILT policy)
**Why out of scope**: The filter semantics are specified and proven; whether the system should instead reject is a policy layer correctly listed in Open Questions.

VERDICT: REVISE
