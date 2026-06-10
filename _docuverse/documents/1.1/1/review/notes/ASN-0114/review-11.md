# Review of ASN-0114

The reasoning here is sound: F2's two-step argument (non-empty by S2, single-span ruled out by S0 convexity) is airtight, F5 correctly composes L12 into LP13's closure rather than mis-citing L12 directly, the F7 empty-wp is a genuine non-trivial weakest-precondition (the `Σ.L(a).eᵢ = ∅` conjunct is state-dependent), and the worked instance checks out arithmetically (a₃ ⊕ δ(2,8) = a₅ by OrdinalShift; a₅ as the gap witness; LP-Fin Corollary giving {a₃,a₄,a₇,a₈}). Boundary coverage is complete (i=0, i=1, i=|L|, i>|L|, a∉dom(L), empty end). The findings below are precision and depth gaps, not logical errors.

## REVISE

### Issue 1: `coverage(·)` applied to span-sets is the foundation operator on the wrong type
**ASN-0114, "The substrate we build on" / "The selector and its domain" (F0, F1):** "We will write the result of FOLLOWLINK as a span-set and measure it by its coverage" and "the returned span-set R satisfies coverage(R) = coverage(Σ.L(a).eᵢ)."

**Problem**: The load-bearing contract equation `coverage(R) = coverage(Σ.L(a).eᵢ)` (carried through F0, F1, F5, F6, F7, the wps, and the worked instance) applies `coverage` to a span-set `R`. But `coverage` is defined in the foundations (ASN-0043, ASN-0098) only on `Endset = 𝒫_fin(Span)` — a *set* — whereas `R` is a *sequence* (ASN-0053). ASN-0053 already provides `⟦R⟧` for span-set denotation. The note thus uses one foundation's operator (endset `coverage`) where another foundation's notation (span-set `⟦·⟧`) is the typed fit, and never pins the meaning of `coverage(R)` formally — the phrase "measure it by its coverage" is the only gesture at it. Because the whole specification is stated through this equation, the notation it rests on should not be left as an unstated coercion from a sequence to its member-set.

**Required**: Either write `⟦R⟧` for the span-set side (per ASN-0053), giving `⟦R⟧ = coverage(Σ.L(a).eᵢ)`, or add a one-line bridge — `coverage(R) := ⟦R⟧` — and note the two coincide because both reduce to the union over the same spans (so sequence-vs-set and span order are immaterial). This also makes F3's "denotationally equal" land on the right symbol.

### Issue 2: F7 carves out slot 3 by convention without citing L3 or deriving the consequence
**ASN-0114, "The empty end versus the invalid selector" (F7):** "Slots `1` and `2` (and any slot beyond `3`) may legitimately be empty — a link may record no spans at a given end."

**Problem**: The parenthetical silently excludes slot 3 from the possibly-empty slots, but never says why at the point it matters. The reason is L3 (ASN-0043/0093: `Σ.L(a).e₃ ≠ ∅`), cited only back in the substrate section and not reconnected here. More to the point, the note proves F7 and has both S2 collapses in hand but never combines them with L3 to state the clean derived guarantee: by L3 plus the second S2 collapse, `coverage(Σ.L(a).e₃) ≠ ∅`, so `followlink(Σ, a, 3) ≠ ⟨⟩` for *every* valid link. The empty-success outcome — and therefore the entire empty-versus-invalid ambiguity F7 exists to guard against — is structurally confined to the non-type slots. This is exactly the kind of consequence (postcondition established, implication unexplored) the methodology asks to be made explicit; it is also why the worked instance can use `e₂ = ∅` but is forced to give `e₃` a non-empty value, a coupling the prose leaves implicit.

**Required**: At the slot-3 carve-out, cite L3 and state the consequence — the type selector never yields the empty-success `⟨⟩`, so the empty/invalid collision F7 forbids is reachable only at non-type slots.

### Issue 3: isolated methodology editorializing
**ASN-0114, "The pure-read frame" (F4):** "The frame is as much a part of the specification as the effect."

**Problem**: This sentence asserts the importance of frames rather than advancing the FOLLOWLINK argument; the reader skips it to reach the useful counterexample that follows. The intro's "But the discipline of specification forces precise questions" is borderline-similar framing. These are the only meta-prose instances I found — the note is otherwise disciplined: the implementation-evidence paragraphs are corroboration (methodology-encouraged), the "boundary we must respect" section is object-level scope delineation, and there is **no** forward-reference accretion (references run backward to foundations or defer genuinely-future topics to Open Questions). I flag the editorializing only because the anti-bloat classifier directs surfacing it at source.

**Required**: Delete or fold the standalone "as much a part of the specification" assertion into the counterexample sentence that already makes the point operationally.

## OUT_OF_SCOPE

### Topic 1: Resolution of the returned endset against a document's arrangement
**Why out of scope**: The note correctly fences this off in "A boundary we must respect," distinguishing the recorded end (FOLLOWLINK's concern) from its projection-and-filter into a live arrangement, and derives the right observation that shrinkage/per-document variation are properties of *resolution*, not of this operation. Correctly deferred, not an error.

### Topic 2: Normal form, multi-document coverage, serialization encoding
**Why out of scope**: The Open Questions enumerate these (span-set normal form under F3's representation freedom; reporting coverage spanning multiple documents; re-encoding the `⟨⟩`/`⊥` distinction across a wire boundary). These are future territory, properly parked.

META: not applicable — the note specifies an abstract read operation's domain, postcondition, frame, and derived guarantees that any implementation must satisfy, and stays on that abstraction; it has not drifted into implementation mechanics.

VERDICT: REVISE
