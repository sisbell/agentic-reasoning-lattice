# Review of ASN-0042

## REVISE

### Issue 1: Repeated "load-bearing" reachability justifications across sections
**ASN-0042, O3 / O4 / O8 / ω_Σ definition**: O3 — "The reachability hypothesis `Σ reachable from Σ₀` is load-bearing, not decorative: it is the premise the proof consumes to exclude the bootstrap origin of `π'`"; O4 Preconditions — "The reachability premise is load-bearing: the induction over the transition sequence ... requires a finite witnessing path ... Without reachability, no base case anchors the coverage claim"; plus two further "is load-bearing" notes on the `ω_Σ` domain restriction.
**Problem**: The same defensive point ("this precondition is not decorative, here is why we need it") is restated in four places. Under the anti-bloat classifier this is defensive justification that explains *why the precondition is needed* rather than advancing the proof, and it is duplicated. The companion boilerplate "by iterated application of O12 along the witnessing sequence gives `Π₀ ⊆ Π_Σ`" is likewise re-derived verbatim in O3, O8 (Step 1), and OwnershipDomainPermanence (Step 1).
**Required**: State the reachability/O12-iteration step once (a one-line named lemma, e.g. "BootstrapContainment: `Σ` reachable ⟹ `Π₀ ⊆ Π_Σ`"), cite it, and delete the "load-bearing, not decorative" editorializing.

### Issue 2: O9 worked example imagines a case the precondition already excludes
**ASN-0042, Worked Example (O9 across nodes), `π_N` bullet**: "So `owns(π_N, a₅)` is false. O9 is vacuously satisfied. We further note that even if one tried to force `N(pfx(π_N)) = [1] ≼ N(a₅) = [2]`, the relation fails: `1 ≠ 2`."
**Problem**: O9's antecedent is `owns(π, a)`. Once `owns(π_N, a₅)` is shown false the obligation is discharged. The "even if one tried to force" sentence reasons about a consequent that the excluded precondition makes irrelevant — reviewer-drift prose imagining a case the carrier already rules out.
**Required**: Stop at "O9 is vacuously satisfied." Delete the counterfactual sentence.

### Issue 3: Ownership-transfer open question duplicated in three locations
**ASN-0042, OwnershipDomainPermanence section / Structural Provenance section / Open Questions**: OwnershipDomainPermanence — "This raises a tension that Nelson himself acknowledges ... We take the conservative reading ... and we record transfer as an open question." Structural Provenance — "Even if ownership were to transfer (contrary to O3 ...) the address would still record the original principal's identity ... Under a hypothetical transfer regime, they would diverge." Open Questions — "If ownership transfer is permitted, what invariants must it preserve ...".
**Problem**: The same out-of-scope speculation (transfer is unspecified; provenance vs. authority would diverge) is developed three times. Two of the three are essay content deferring to the same downstream Open Question.
**Required**: Keep the Open Questions entry; reduce the two body passages to a single sentence pointing at it, or remove them.

### Issue 4: "Mutual exclusivity of namespace vs principal baptism" restated redundantly
**ASN-0042, O15 condition (vii) gloss / O7(c) / Worked Example (Sub-account namespaces)**: condition (vii) — "a prefix consumed as a namespace address ... can never be re-purposed as a new principal's prefix"; O7(c) — "namespace baptism and principal baptism are mutually exclusive futures for the same prefix"; Worked Example — "By the mutual exclusivity of namespace and principal baptism for a given prefix (established in O7(c)) ...".
**Problem**: One fact (freshness gate (vii) + O18 make namespace and principal baptism exclusive) is asserted three times in three sections.
**Required**: Establish it once (it is a direct corollary of (vii) and O18 — make it a named derived fact) and cite it from O7(c) and the example.

### Issue 5: Mislabeled forward pointer in OwnershipDomainPermanence
**ASN-0042, OwnershipDomainPermanence, after the single-transition proof**: "Multi-step closure ... follows by repeated application of the single-transition result and is discussed informally below."
**Problem**: What appears below is not an informal discussion but a fully formal **Corollary (OwnershipDomainPermanence★)** with an induction. The forward pointer mischaracterizes its target — the kind of document-ordering meta-prose the anti-bloat pass targets.
**Required**: Replace with a direct reference: "extended to `→⁺` in Corollary OwnershipDomainPermanence★ below."

## OUT_OF_SCOPE

### Topic 1: Authentication / session-to-prefix binding mechanism
**Why out of scope**: The "Principal Identity and the Trust Boundary" section explicitly defers concrete authentication (certificates, keys, tokens) and correctly frames `session.account = pfx(π)` as an exogenous axiom. This is consistent with the declared scope exclusion; no revision needed, and the section properly refrains from specifying a mechanism.

### Topic 2: B1 contiguity preservation under ownership-driven delegation baptisms
**Why out of scope**: Whether delegation baptisms (which enter `pfx(π')` into `Σ.B` at sibling-stream positions) respect ASN-0040's B1 contiguity invariant is a baptism-mechanism question. ASN-0042 legitimately imports B1 as a foundation fact; the obligation belongs to ASN-0040, not here.

VERDICT: REVISE
