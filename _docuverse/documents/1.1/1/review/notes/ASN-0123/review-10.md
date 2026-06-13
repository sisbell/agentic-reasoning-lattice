# Review of ASN-0123

This is an unusually careful note. The derivation-from-guarantees structure (G1–G3) is the right way to motivate an operation, the severance theorem (V9a) is a genuine result cleanly proved, VN-B1 correctly re-proves rather than imports ASN-0040's B1, SA is sound, and the boundary cases (empty source `n = 0`, first vs. subsequent fork, iterated forks, sharing where `|A| < n`) are all handled. The invariant-preservation delegation to `ExtendedReachableStateInvariants` via V-WF is the correct discharge pattern. Two issues remain, one load-bearing.

## REVISE

### Issue 1: the cross-owner branch's realizability rests on `pfx(π) ∈ E`, which PS does not deliver

**ASN-0123, V9 / V-WF (cross-owner) / Identity clause**: "π's account `pfx(π) ∈ E` (PS) carries a document sub-allocator, so π mints v there as a single K.δ in its own domain (V-WF)" — and the Identity clause: "π already holds a document-creation namespace (its account, `pfx(π) ∈ E`, with its document sub-allocator)."

**Problem**: PS's stated derivation runs in one direction only. From clauses (i)–(iii) it derives *coverage* — "every `e ∈ E` extends `n₀` ... `ω : E → Π` is total and single-valued" — i.e. every entity is covered by a principal. It does **not** derive the converse, that a principal's prefix is itself a member of `E`. The cross-owner branch needs exactly the converse: to mint `v` as a single K.δ, K.δ case (ii) requires the operand in `E` — `pfx(π)` (account-level, `zeros = 1`) for a `k = 2` descent, or an existing π-document for `k = 0`. Only then is the step enabled and `allocated_by(π, v)` realizable, and `allocated_by(π, v)` is precisely what V9 consumes to invoke O5. The gap is sharpened by the ASN's own registry identification, which is explicitly scoped: "E plays the registry role of ASN-0040's B **for document-level addresses**." The account-level prefix `pfx(π)` (`zeros = 1`) falls outside that identification, so even granting `pfx(π) ∈ Σ.B` from ASN-0042's PrefixBaptismCoupling, the stated B=E bridge does not carry it into `E`. Hence "`pfx(π) ∈ E` (PS)" is unsupported. This is load-bearing: without it, V-WF's "single K.δ" claim and V9's `allocated_by(π, v)` are ungrounded for the cross-owner branch. (The owned branch is unaffected — its operand is `d_src` or `c_m`, both provably in `E`.)

**Required**: Either (a) add a clause to PS coupling principal delegation to entity baptism in `E` and extending the B=E identification through account/node level, so that `pfx(π) ∈ E` holds for every `π ∈ Π`; or (b) state `pfx(π) ∈ E` (and π's possession of a document sub-allocator entity in `E`) as an explicit precondition of the cross-owner branch, and correct V9's citation from "(PS)" to that precondition. The O5 *conclusions* about `v` are fine — `v` is document-level and within the stated identification — so the fix is confined to operand availability.

### Issue 2: V7's downward navigation claims to enumerate "the versions of d" but excludes cross-owner versions

**ASN-0123, V7 (NavigationAsymmetry)**: "Downward — the versions of d are the registry query `E ∩ S(d, 1) = {c₁, …, c_hwm}` ... the full descendant set `{e ∈ E : d ≺ e}` is T1-contiguous (T5), a single range scan."

**Problem**: By the ASN's own `derives` relation, a cross-owner `VERSION(π, d)` produces a version `v` with `derives(v, d)` — V9 makes such `v` a first-class version of `d`. But V9's severance theorem gives `¬(d ≼ v)`, so cross-owner versions lie in neither `S(d, 1)` nor `{e : d ≺ e}`. The registry query therefore enumerates only the *owned, address-encoded* versions, not "the versions of d." The unqualified phrasing overstates what the navigation recovers, in tension with the ASN's otherwise scrupulous owned/cross-owner distinction.

**Required**: Scope the claim to "the owned (address-discoverable) versions of d," and note that cross-owner versions are not downward-navigable by address — the direct consequence of severance, already flagged in Open Question 2.

## OUT_OF_SCOPE

None. The ASN confines itself to the fork, touches adjacent operations only at frame/coupling boundaries as it declares, and routes genuine future territory (concurrency serialization, withdrawal/supersession, location-fixed windowing, direction recovery from symmetric provenance) to the Open Questions rather than claiming it.

VERDICT: REVISE
