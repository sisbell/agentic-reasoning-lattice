# Review of ASN-0108

This is a strong, unusually thorough note — the wp analysis in W2 and the cumulative-inflow bound in W9b are exactly the kind of depth the standard demands, and the four termination walks correctly exercise the boundary regimes (m=0, exact multiple, non-divisible, N>m all check against W9a's `⌈m/N⌉ + [N∣m]` formula). The defects are concentrated in the stability/termination core (W5, W8, W9), where the note repeatedly conflates two distinct properties of the ordering key: *order-stability across states* and *computability of the cursor key on a held, orphaned address*. The recent revision regrounded one of these in W5 but did not propagate the regrounding.

## REVISE

### Issue 1: W5's iff is not tight — clause 1 permits resurrection re-delivery

**ASN-0108, W5**: "Resumption is *coherent* — it skips no link that was already an undelivered tail matcher when the cursor was set (a link matching in both the cursor-setting state and the resume state), and re-delivers none already seen — *if and only if* the key satisfies **clause 1 (cut-point preservation)** at every cursor the reader actually holds."

**Problem**: The skip half is explicitly scoped to links matching in both states, and is correctly equivalent to clause 1. The re-delivery half ("re-delivers none already seen") is *unscoped* and is **not** implied by clause 1. Clause 1 quantifies only over links matching in both states of a transition, so it never constrains a link's re-entry position after an orphan gap. A link delivered, then orphaned (leaving `Match`), then resurrected above a later cursor by the LP18 mechanism is re-delivered while clause 1 holds throughout. W9b itself states this outcome: "a delivered link orphaning and resurrecting: that link is simply consumed once per inflow event it accrues" — i.e. delivered again, under clause 1 (W9b's condition (i)). So the "⟸" direction (clause 1 ⟹ no re-delivery) fails for general clause-1 keys; the headline iff is false as written. The claim-table row for W5 inherits the same defect.

**Required**: Scope "re-delivers none already seen" to links matching across the cursor's transition (matching the skip clause's scoping), or restrict the iff to the key class for which it holds — an allocation-monotone/address key returns a resurrected link at its permanent low key, below the advancing cursor, so it is not re-delivered, and the iff is recoverable there. As stated, the universal "the key satisfies clause 1" overclaims.

### Issue 2: W8/W9 ground cursor-key survival in T8, contradicting W5's own (regrounded) orthogonality finding

**ASN-0108, W5**: "Allocation axioms enter only orthogonally — that the cursor `c` stays an allocated, uniquely-identifying address is T8 ... but none of these is what freezes the key."
**ASN-0108, W8**: "With an address-based key this is unconditional: the cursor's address — hence its key — is permanent (T8) regardless of whether the link still matches."
**ASN-0108, W9**: "an address-based key supplies for free (W8) since the permanent address remains a valid cut-point regardless of membership (T8)."

**Problem**: W5 correctly establishes that the address key's value-freezing is *definitional* — `κ` is the identity, a total state-independent function — and that T8/GlobalUniqueness are *orthogonal* to it. W8 and W9 then ground the cursor key's recoverability/permanence in **T8**, undoing the W5 regrounding. `After(c, Σ') = {a ∈ Match(Σ') : κ(c) <_K κ(a)}` requires only that the reader can evaluate `κ` on the held cursor; for `κ(a) = a` that is the identity applied to a value the reader already holds, requiring neither that `c` remain allocated (T8), nor that `c` be unique (GlobalUniqueness), nor that `c ∈ Match`. Relatedly, W8's "With a state-stable key (W5), κ(c) survives the disappearance of c" is not entailed: W5 defines state-stability only over surviving/matching links (both clauses quantify "for every `a` matching in both states" / "every pair `a, b` in the tail"), so it constrains nothing about an orphaned cursor's key. A content-position key whose values never move but whose content can be removed would be state-stable per W5 yet lose `κ(c)` on orphaning — so state-stability does not deliver cursor-survival; value-totality does.

**Required**: Re-attribute the cursor's survival-under-orphaning in W8/W9 to the definitional totality and state-independence of `κ` (as W5 now does), not to T8 or to state-stability. If T8 is cited at all, scope it to its actual role — persistence of the address *as an allocated entity*, distinct from computability of `κ` on a held value. This is the same point W5 already makes; the regrounding simply was not carried into W8/W9.

### Issue 3: W9's "single cursor's cut-point is all W9 needs" is neither necessary nor sufficient for what W9 asserts

**ASN-0108, W9**: "Recoverability of the single cursor's cut-point is all W9 needs; it is implied by state-stability in the sense of W5 (whose cut-point clause, specialised to `c`, gives exactly recoverability)... Formally, when `κ(c)` is recoverable, `|Window(q, c, N, Σ)| < N ⟹ After(next-cursor, Σ) = ∅`."

**Problem**: W9 equates "recoverable" with clause 1 specialised to the current cursor `c`. Single-cursor clause 1 is on both ends the wrong condition:

- *(too strong for the formal statement)* `|Window| < N ⟹ After(next-cursor) = ∅` is a pure cardinality fact: when `κ(c)` is merely **computable**, `After(c,Σ)` is well-defined, and `|Window| < N` forces `|After(c,Σ)| < N`, so `After` is exhausted and `After(next-cursor) = ∅`. No cut-point *preservation* is consulted. The W5 cut-point walk witnesses this — `κ(c)` computable, clause 1 fails (L₂ moves below `c`), yet at the terminal step `After(L_3) = ∅` holds. So clause 1 at `c` is strictly more than the formal statement requires; computability is the right proviso, and it is also what the cited W8 counterexample (content removed ⟹ `κ(c)` uncomputable) actually exhibits.

- *(too weak for the informal exhaustion reading)* "every matching link reachable past the cursor has been delivered" requires clause 1 at *every* cursor of the pass — exactly W9b's condition (i): "the cursor's cut-point is preserved at each successive cursor ... applied not once but at every cursor the pass visits." W9 directly contradicts W9b here. Chaining the W5 cut-point walk one window earlier (clause 1 at `c₁` fails, skipping `L_x`; clause 1 at `c₂` holds; window 2 short) yields `After(c₂) = ∅` with `L_x` matched but never delivered — a short window, current-cursor cut-point intact, yet a match skipped.

**Required**: Split the two claims. State the cardinality fact `After(next-cursor) = ∅` under the weakest proviso it needs — `κ(c)` computable — and align the W8 counterexample with that (it is a computability failure, not a cut-point-preservation failure). State the everything-delivered guarantee under clause 1 at *every* cursor (W9b's condition (i)), deleting "single cursor's cut-point is all W9 needs." Do not equate "recoverable" (computability) with "cut-point preserved" (clause 1) — they differ, and the note needs both notions named distinctly. Across Issues 2–3 this argues for one consolidated hierarchy of the key conditions (computable / cut-point-preserving = clause 1 / tail-order-preserving = clause 2 / state-stable / value-total), since the inconsistent use of "recoverable" and "state-stable" is what produces these conflations.

## OUT_OF_SCOPE

### Deferred topics are appropriately bounded
The satisfaction predicate and query construction (which region `W` and which type-filter a query `q` fixes) are correctly deferred to ASN-0127 / ASN-0086; `Match` is taken as given, which is the right move for a windowing note. The five Open Questions (multi-document global ordering, eventual delivery of non-allocation-monotone new links, the cross-state completeness invariant, orphan-vs-exhaustion disambiguation, and delivery-order-vs-count correspondence) are genuine future territory and are flagged as such — no new out-of-scope topic to add.

**Why out of scope**: These are downstream operations and refinements, not defects in this note's windowing guarantees.

### Anti-bloat pass
I ran the forward-reference/meta-prose pass. The note is dense, but most prose candidates fall in the prompt's protected categories — concrete walks (required by the depth standard), statements of what the operation does/does-not-do (W3, W10), and motivating analogies (W11). I did not find significant removable accretion of the flagged kinds (no axiom-rationale sub-paragraphs, no document-ordering justifications, no downstream-consumer inventories in definitions). The one genuine prose defect is the inconsistent stability terminology, which is substantive and is captured in Issues 2–3 rather than as a separate verbosity finding. One minor pattern worth noting at source: both W2 and W5 carve out the "new link landing below the cursor" case with forward pointers to W6 — acceptable as local scoping, but a candidate to state once if the regrounding above is done.

VERDICT: REVISE
