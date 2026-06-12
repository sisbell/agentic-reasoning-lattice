# Review of ASN-0120

## REVISE

### Issue 1: MLop's two branch predicates are independent, and the divergent boundary is never checked
**ASN-0120, MLop (and "A worked example")**: "`v_a = shift(max(V_{s_L}(d)), 1)` if `V_{s_L}(d) ≠ ∅`, and `v_a = [s_L, 1]` if `V_{s_L}(d) = ∅`" together with `a` "the fresh emission of `A_L(d)`".
**Problem**: The identity branch keys on the *store* (`K.λ`'s first/subsequent-emit predicate over `{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}`), while the seating branch keys on the *arrangement* (`V_{s_L}(d)`). These two predicates diverge in a reachable state the foundation explicitly contemplates: after a K.μ⁻ on the home with `n'_{s_L} = 0`, links remain homed in `dom(Σ.L)` (P3/L12) while `V_{s_L}(d) = ∅` and the link-subspace depth is re-pinned (ASN-0047, `m_L(d)` note). In that state MAKELINK takes the *subsequent*-emission branch for `a` (`a = inc(ℓ_prev, 0)`) and simultaneously the *first*-position branch for `v_a` (`v_a = [s_L, 1]`). I verified the contract is in fact sound there — `a` is fresh against the whole store, the seating discharge does not depend on the homed-set being empty, and D-MIN★/D-SEQ★ hold on the singleton — but the ASN never identifies the case. Worse, the worked example *derives* `V_{s_L}(C) = ∅` from "`C` homes no links," exhibiting exactly the homed-set ⟺ arrangement-emptiness inference that the contracted home falsifies in one direction. Boundary cases are mandatory; this is the one boundary where MLop's two branch selectors decouple.
**Required**: State explicitly that the `a`-branch and `v_a`-branch are selected by independent predicates (store-keyed vs. arrangement-keyed), name the contracted-home state where they diverge (homed links present, `V_{s_L}(d) = ∅`), and verify the mixed case — a short paragraph or an example variant suffices.

### Issue 2: Repeated forward deferrals to MLop carrying organizational meta-prose
**ASN-0120, residence section / resolution section / ML9**: "its two-branch determination — … — is stated once, with its rationale, in the operation contract (MLop below), and meets `K.μ⁺_L`'s required form by construction"; "the operation's enabling condition (`enabled`, MLop below)"; "stated once at MLop below; conjoining it parallels the `enabled(K.μ⁻[d,R])` conjunct of ASN-0098 LP12a".
**Problem**: Three separate sections defer to the same downstream location, and two of the three dress the pointer in meta-prose — "stated once, with its rationale" describes the document's organization rather than advancing any claim, and "parallels the `enabled(K.μ⁻[d,R])` conjunct of ASN-0098 LP12a" is a defensive precedent citation justifying the formula's shape rather than deriving it. This is the deferral-accretion pattern the anti-bloat classifier targets, and it compounds.
**Required**: Keep at most one bare forward reference to MLop ("(MLop)" suffices); delete "stated once, with its rationale" and the LP12a-parallel clause.

### Issue 3: The empty-resolution boundary is settled once and then re-argued twice
**ASN-0120, resolution section / ML5 paragraph / ML6 paragraph**: resolution section — "For the from and to slots the boundary is *admitted*: the operation's enabling condition (`enabled`, MLop below) constrains only the type slot's resolution…"; ML6 — "the contrast with the from/to slots is now sharp: L3 constrains only slot 3, which is why the empty-resolution boundary is admitted there and excluded here"; ML5 — "the empty-resolution boundary settled in the resolution section admits both degenerate forms."
**Problem**: The fact "L3/enabled constrain only slot 3, so empty resolution is admitted for from/to and rejected for type" is stated in full in the resolution section and then restated in different words in the ML6 paragraph; the ML5 paragraph adds a third pointer back to the settlement. Two paragraphs saying the same thing in different words is the exact accretion pattern to flag at source; the empty-endset boundary now has three prose sites plus two claim-table rows plus an Open Question.
**Required**: Settle the boundary once (the resolution section is the natural home), and let ML5/ML6 *use* the fact without re-deriving the contrast — the ML6 sentence quoted above can be deleted outright, since its necessity/sufficiency argument immediately precedes it.

## OUT_OF_SCOPE

### Topic 1: Direct I-address endset arguments (bypassing V-span resolution)
**Why out of scope**: The ASN correctly observes that ghost types (L9) and foreign endsets (full L4 generality) are unreachable through `ρ`-resolved V-specs and defers the I-address-direct argument shape. That is a distinct operation surface with its own well-formedness obligations — a future ASN, not a gap here.

### Topic 2: Re-seating a stored link whose arrangement entry was contracted away
**Why out of scope**: A link homed at `d` but absent from `V_{s_L}(d)` after contraction persists in the store (ML7) yet is not enumerable from `d`'s V-stream. Whether and how it can be re-seated is an arrangement-editing concern (EDITLINK territory), not part of MAKELINK's contract. (Issue 1 asks only that MAKELINK's own behavior *in* that state be acknowledged, not that re-seating be specified.)

VERDICT: REVISE
