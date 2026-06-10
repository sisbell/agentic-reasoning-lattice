# Review of ASN-0115

I checked the definitions (`act`, `item`, `deliver`/R0), the Confinement lemma, and each of R1–R11 against the cited substrate. The core resolution-then-dereference semantics are correct, and the hard boundary work is genuinely done: R6's gap analysis (terminal-overrun vs. interior-hole, scoped to the bindable slice), R7's comparability-is-required argument, R8's link-vacuity via CL-OWN + CL-UNIQ, and R11's single-live-condition wp all hold up. The Confinement lemma and all five worked instances check out arithmetically. Two issues remain.

## REVISE

### Issue 1: R9's provenance clause contradicts the content/link payload asymmetry the ASN itself establishes

**ASN-0115, R9 (CoherentMultiOriginAssembly)**: "The *resolution* is provenance-traceable: each active position `v` resolves to `a = Σ.M(d)(v)`, and that address determines a home document, so **no fragment's provenance is collapsed by co-assembly**."

**Problem**: R9 asserts provenance non-collapse uniformly across fragments, but the ASN's own claims establish that the *delivered object* exposes provenance only for one item kind:
- Content items carry `⟨content, Σ.C(a)⟩` — the value, not `a` (R1). From the delivered stream, `origin(a)` is **not** recoverable. Provenance *is* collapsed in the output for content.
- Link items carry `⟨ref, a⟩` — the address (R10). From the output, `home(a)` *is* recoverable.

So provenance traceability from the delivered object is true for links and false for content — exactly the kind/payload asymmetry R1 and R10 make explicit — yet R9 treats all fragments uniformly. R9 then rescues the headline by scoping to "traceability of the *resolution*, not inline provenance of the delivered stream … (the delivered content item carries `Σ.C(a)`, not `a`, by R1)." But the resolution mapping is an internal artifact of computing `deliver`; it is not observable in `deliver(R, Σ)`'s output, and "resolution determines a home document" is automatically true of *any* faithful realization (because `origin`/`home` are functions of the resolved address — R4 already pins per-document resolution). Stripped of the non-observable clause, R9 adds no checkable obligation beyond R4 + R5. A reader must reconcile R9's "not collapsed" headline against R1 to discover it means almost the opposite for content fragments.

**Required**: Either (a) restate R9's provenance clause to expose the asymmetry — link items carry `a`, so `home(a)` is output-recoverable, while content items carry only `Σ.C(a)`, so `origin(a)` is not (deferring inline content-provenance to the existing Open Question); or (b) demote the "resolution is provenance-traceable / no fragment's provenance is collapsed" sentence to an explicitly expository remark, leaving R9's invariant content as exactly R4 + R5 (per-document resolution + sequence ordering), since the traceability clause names nothing a realization could fail.

### Issue 2: the subspace-straddling exclusion is stated three times (anti-bloat)

**ASN-0115, §"What a spec-set is"**: "A single boundary-crossing span is therefore outside this ASN's scope; designating both subspaces together is achieved by *composing* per-subspace ordinal spans into the spec-set, not by one straddling span." (with the `s=[1,5]`, `ℓ=[2,0]` counterexample)

**ASN-0115, §"subspace crossing"**: "(A *single* span's denotation cannot itself straddle the boundary: the V-spec definition restricts `σ` to ordinal-level spans, for which the Confinement lemma keeps every `t ∈ ⟦σ⟧` on the start's first component, so a text-rooted span cannot reach link positions.)"

**ASN-0115, Open Questions**: "What must delivery guarantee when a single span's denotation straddles the subspace boundary…"

**Problem**: The same point — an ordinal-level span cannot straddle, so single-span crossing is out of scope and crossing is achieved by composing per-subspace specs — is made twice in the body and once as an Open Question. The §"subspace crossing" parenthetical is fully subsumed by the §"What a spec-set is" statement plus the already-stated Confinement lemma; it advances no reasoning the reader does not already have. The same body-prose-plus-Open-Question doubling recurs for transmission-channel faithfulness (R2's "frame limit" prose ↔ Open Question 4) and inline content provenance (R9's deferral ↔ Open Question 1).

**Required**: Delete the §"subspace crossing" parenthetical (it restates the earlier statement plus Confinement). State each scoping concern — straddling, channel faithfulness, inline provenance — once, letting the Open Questions carry the forward-looking framing rather than re-arguing the exclusion inline at the carrier claim.

## OUT_OF_SCOPE

None. The ASN stays within content delivery by spec-set; it correctly defers endset-reading (R10: "the link's endset structure … is the concern of operations that read a link by address (out of scope here)") and references RETRIEVEDOCVSPAN / FINDDOCSCONTAINING only as motivating contrast, not as claims.

VERDICT: REVISE
