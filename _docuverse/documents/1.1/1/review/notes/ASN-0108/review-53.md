# Review of ASN-0108

I checked the load-bearing proofs first — the W2 weakest-precondition derivation (identity vs offset cursor, including the strict nesting membership-identity ⟹ frozen-prefix ⟹ genuine wp and the past-the-end corner), the W4 variable-schedule partition, the W5 cursor-advance induction for no-re-delivery, the W6a F-LAMBDA/F-V bridge, and the W9b per-link multiplicity charge with its W9c/W9d necessity/non-necessity boundary. These are sound, and the boundary walks (m=0, exact multiple, N>m, orphaned cursor) are correctly handled. My findings are about premise attribution and the meta-prose the `review-mode.anti-bloat` classifier flags — recurrences of one fact across separated paragraphs.

## REVISE

### Issue 1: Key permanence is attributed to the wrong premises (S0/LP11, not L12)
**ASN-0108, "two identity readings" / Gregory's-reading bullet, and the permanence paragraph**: "orders each link by the **least I-address that slice covers**, read from the endset alone (L12) over *permanent* I-addresses (S0)" and "This key is **permanent**: an I-address is never reassigned, and content is never moved or removed from the Istream (S0), so the key's value is immutable under rearrangement (… never content identity — LP11) and survives orphaning…"

**Problem**: The key is the T1-least element of `coverage(designated slice)`, and coverage "is a purely combinatorial property of the endset's span representation — it does not consult any state component" (ASN-0098; ASN-0043 `coverage` def). So the key is a pure function of the endset, which is immutable by L12 — and therefore immutable under *every* transition, full stop. The cited premises are about *content* and *position* permanence (S0: content never moves; LP11: reorder moves V-positions only), neither of which the key reads. The derivation names premises it does not use and misattributes the source of permanence — the very "name what you actually use" failure a rigor review must catch, and a defensive over-citation. (W8 itself gets this right: there it correctly leans on "the endset … persists by L12/LP13.")

**Required**: Derive the key's permanence from L12 alone (endset immutability, key blind to content existence and position). Drop the `(S0)` in the definition and the S0/LP11 chain in the permanence paragraph, or demote them to a remark that the *content denoted* is also stable — distinct from why the *key* is.

### Issue 2: W9's local-fact paragraph re-narrates W8's computability-failure mechanism verbatim-in-substance
**ASN-0108, W8 statement vs W9 "The local fact (cardinality)"**: W8 — "the **content-position key** alone … `κ(c)` becomes uncomputable when the V→I mapping it was drawn from is gone; the successor set then collapses and the call returns the empty window — *indistinguishable from genuine exhaustion* (W9)." W9 — "when the cursor's matched content is orphaned under the *content-position* key, `κ(c)` becomes *uncomputable* … `After(c, Σ)` loses its referent, and the call returns an empty window *indistinguishable from genuine exhaustion* — signalling cursor-invalidation, not exhaustion."

**Problem**: These two passages state the same mechanism (position key → orphaning → `κ(c)` uncomputable → empty window indistinguishable from exhaustion) in different words — anti-bloat pattern "two paragraphs say the same thing." The W8 *concrete walk* restating it is fine (examples are allowed); the second *statement* in W9 is the redundancy.

**Required**: In W9's local-fact paragraph, cite W8 for the computability failure rather than re-deriving the collapse; keep only W9's distinct content (computability secures the *cardinality* fact, no cut-point consulted).

### Issue 3: The resurrection/permanent-key fact and the clause-1-at-every-cursor condition are each stated twice across W5/W9/W9b with mutual deferral
**ASN-0108, W5 vs W9b, and W9 vs W9b**:
- W5 — "a delivered link that orphans and then resurrects is outside its scope … clause 1's both-states classification cannot bar it — and is kept from re-delivery only under a *permanent* key, which returns it at a key below the advancing cursor (W9b)."
- W9b — "A resurrected link is not excluded by clause 1, since W5 quantifies only over links matching in *both* states … resurrection-ahead is *counted* by (ii) rather than forbidden by (i)," and "Under *either permanent key* … on resurrecting it returns at its permanent key … which lies below the advancing cursor."
- W9 — "secured by clause 1 … at every visited cursor — W5's discipline, which also supplies W9b's termination condition (i)"; W9b (i) — "W5's clause 1, applied not once but at every cursor the pass visits (W9's global guarantee)."

**Problem**: The resurrection-outside-clause-1 fact (and "permanent key returns it below the advancing cursor") is given fully in both W5 and W9b, with W5 forward-deferring to W9b for the same point it already states — matching "multiple paragraphs defer to the same downstream location" and "say the same thing twice." Separately, W9's global guarantee and W9b's condition (i) define the identical condition (clause 1 at every visited cursor) and cross-reference each other circularly.

**Required**: State the resurrection/permanent-key fact once — W9b is the natural home given the charge accounting — and have W5 cite it without restating. State "clause 1 at every visited cursor" once (W9b (i)) and let W9's global guarantee reference it, dropping the back-reference loop.

### Issue 4: The key introduction carries design-rationale forward-citing W5/W8 for a parameter that is explicitly not a claim
**ASN-0108, Gregory's-reading bullet**: "udanax-green instead keys on whichever slot the link *matched* … We fix the slice *a priori*, keeping the key a function of that immutable value — and with it the permanence and state-stability (W5, W8) that the matched-slot key forfeits."

**Problem**: This sits in the *introduction* of a key the note states is "a design parameter, not a claim," yet justifies the a-priori-slice choice against a rejected matched-slot variant by forward-referencing W5/W8 — design-rationale and downstream-consumer enumeration in a definition slot. (The factual description of what udanax-green's spanfilade does is legitimate implementation evidence; the *justificatory* clause is the accretion.)

**Required**: Reduce to the structural fact — the slice is fixed a priori, so the key is a function of the immutable link value — and let W5/W8 do the property-sorting where those claims are stated, rather than previewing the verdict here.

## OUT_OF_SCOPE

The note defers count-only retrieval, full-set retrieval (ASN-0099), MAKELINK, FOLLOWLINK, and BEBE correctly, and routes the genuinely-open items (multi-document non-monotone ordering, born-ghost delivery, cross-state completeness invariant, uncomputable-cursor protocol, delivery-vs-count correspondence) to Open Questions rather than under-specifying them in-note. No missing-coverage findings.

VERDICT: REVISE
