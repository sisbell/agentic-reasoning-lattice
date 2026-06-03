# Review of ASN-0071

## REVISE

### Issue 1: Duplicate explanation of silent position-filtering in *Resolution*
**ASN-0071, *Resolution***: Two consecutive paragraphs make the same point. The resolve-equivalence paragraph's first relaxation axis already states: "`⟦σ⟧` may contain positions outside `dom(M(d_s))` … vspec silently drops the missing positions (F-FILT)." The following standalone paragraph then re-derives the identical mechanic: "A vspec may name positions not currently in `dom(Σ.M(d_s))`. The definition handles this silently: the intersection `⟦σ⟧ ∩ dom(Σ.M(d_s))` drops unresolvable positions…"
**Problem**: The mechanical content (intersection drops out-of-domain positions → F-FILT) is stated twice in different words. Only the "charitable reading" framing is new; the rest is restatement the reader must skip past.
**Required**: Fold the charitable-reading sentence into the first axis's discussion and delete the redundant standalone paragraph, or vice versa. State the silent-drop / F-FILT mechanic once.

### Issue 2: "What this verifies" bullets verify nothing in the constructed state and duplicate later sections
**ASN-0071, *A worked scenario* → "What this verifies"**: "*F-CUR* — state dependence: a later K.μ⁻ removing `v_B` would drop `d_B` from `find(Q)`, even as `(a₁, d_B) ∈ R` persists (P2)." and "*Home/transcluding recovery* — `origin(a₁) = d_A` …"
**Problem**: Both bullets sit under a header claiming the scenario *verifies* them, but neither is exercised by the trace. The F-CUR bullet invokes a K.μ⁻ transition the scenario never performs — it imagines a state outside the construction — and it duplicates the *Currency: state dependence* section, which already makes the identical current-vs-`R` point with K.μ⁻ and P2. The home/transcluding bullet previews machinery fully developed in *Discovery through sharing*. These are forward-previews, not verifications.
**Required**: Either drop the bullets (the downstream sections carry the content), or, if a concrete demonstration of F-CUR is wanted, actually execute the K.μ⁻ step in the trace and show `d_B` leaving the result set. Do not label hypothetical/forward-pointed prose as "verified."

### Issue 3: Use-site aside in the F-CONTENT derivation
**ASN-0071, *The operation*, F-CONTENT paragraph**: "by S3★, a content-subspace V-position routes into `dom(Σ.C)` and a link-subspace V-position into `dom(Σ.L)` (and by CL-OWN, ASN-0047, the latter are exactly `d`'s own links)."
**Problem**: The CL-OWN parenthetical does not advance the F-CONTENT argument, which needs only that link-subspace images land in `dom(Σ.L)`, disjoint from `dom(Σ.C)` (L14). Whether those links are `d`'s own is irrelevant to "matches occur only via shared content." It is noise inside an otherwise tight derivation.
**Required**: Delete the CL-OWN parenthetical.

## OUT_OF_SCOPE

### Topic 1: Invariant linking `find` results across an arrangement-contracting transition
**Why out of scope**: The relationship between `find(Q)(Σ)` immediately before and after a K.μ⁻ is correctly deferred to an Open Question. It is new territory (transition semantics for the query), not a defect in this state/operation specification.

### Topic 2: Provenance-relation (`R`-based) historical containment query
**Why out of scope**: The note correctly distinguishes current containment from `R`-based ever-containment and leaves the latter operation to a future ASN. Not an error here.

VERDICT: REVISE
