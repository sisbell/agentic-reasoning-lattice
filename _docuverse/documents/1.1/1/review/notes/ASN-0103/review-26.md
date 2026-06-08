# Review of ASN-0103

This note is mathematically careful — the `D_A = E ∩ S(A,2)` double-inclusion, the FirstForkRoot lemma, and the lexicographic dominance argument all hold up under scrutiny, and the worked example exercises the load-bearing length filter. My findings are about accreted prose, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Off-chain branch re-derives a distinctness already established by freshness

**ASN-0103, Effect One, "*Off-chain (v_{#A+1} ≠ 0).*"**: "hence `d < v` by T1 case (i) (ASN-0034), so `d ≠ v`. CND.monotone makes *no* dominance claim over such `v`: distinctness by divergence at `#A+1` already discharges freshness, the only property the operation needs from these entities."

**Problem**: Freshness was already discharged in the *Freshness* paragraph by `d ∈ S(A, 2) \ D_A = S(A, 2) \ E`, whence `d ∉ E` — and that conclusion covers *every* entity of `E`, off-chain documents included. The off-chain branch then re-establishes `d ≠ v` for exactly those entities, by a second route, and explicitly frames its purpose as discharging freshness. Since the claim states these entities are not dominated, the ordering relation `d < v` is also not load-bearing for anything downstream. The branch exists only to "complete" the `#A+1`-component split, handling a case CND.monotone's scope has already carved out — the imagined-case / redundant-derivation pattern. If off-chain document-level entities (`A ≼ v`, `Document(v)`, `v_{#A+1} ≠ 0`) are in fact unreachable under the account allocator (their parent is a sub-account `[A, x, …]`, not `A`), the branch imagines a case the discipline excludes; if they are reachable, freshness already covers them. Either way it adds no reasoning.

**Required**: Delete the off-chain branch and the corresponding `#A+1` split; restrict the dominance proof to on-chain versions (`v_{#A+1} = 0`), which is the only scope CND.monotone claims, and let the *Freshness* paragraph carry distinctness for all of `E`.

### Issue 2: Use-site justification and forward references in "A Note on Sub-Allocator Activation"

**ASN-0103, A Note on Sub-Allocator Activation**: "One consequence of Effect One is worth stating explicitly because it underwrites every later operation on `d`. ... The first INSERT into `d` will draw `[d.0.s_C.1]` from `A_C(d)`; the first MAKELINK will draw `[d.0.s_L.1]` from `A_L(d)`."

**Problem**: The effect itself (creation activates `A_C(d)`, `A_L(d)` without emission, per CND.subAlloc) is object-level and correctly derived from SubAllocatorBundle. But "worth stating explicitly because it underwrites every later operation on `d`" is a use-site justification, and the INSERT/MAKELINK sentences forward-reference out-of-scope operations to motivate the claim rather than advance it. This is forward-reference accretion around an otherwise sound effect.

**Required**: State the activation effect (anchors stand ready, not yet in `dom(C') ∪ dom(L')`) and drop the "underwrites every later operation" justification and the INSERT/MAKELINK draws.

### Issue 3: Duplicate deferral to the registry-carrying ASN

**ASN-0103, CND.own**: "we defer them to a registry-carrying ASN (see Open Questions)." and **Open Questions, final bullet**: "What coupling between the entity set and the baptismal registry must hold in every reachable state ... so that the effective-owner reading of ownership becomes derivable rather than asserted?"

**Problem**: Two locations defer the same effective-owner / registry-coupling question to the same downstream ASN — the "multiple paragraphs deferring to the same downstream location" pattern. The CND.own prose pointer and the Open Question are redundant.

**Required**: Keep the deferral in one place. The Open Question is the natural home; in CND.own, simply note that the effective-owner statement quantifies over the registry `B` absent from this state, without the cross-pointer.

### Issue 4: CND.A-act prose justifies why the assumption is needed rather than stating it

**ASN-0103, The Operation's Input**: "The foundations state SubAllocatorBundle only for the document tier, so `Activated(A_doc(A))` is not derivable from them; we take it as owed by out-of-scope account provisioning."

**Problem**: A standing assumption may note non-derivability briefly, but this is amplified — the table entry for CND.A-act repeats the rationale ("account-tier analogue of SubAllocatorBundle ... structural per Nelson's baptism/ghost-element intent") and appends a use-site inventory ("Discharges `Activated(A_doc(A))` for the ActivatedEmission check on `d`"). The assumption's *content* is one line; the surrounding why-it-is-needed and where-it-is-used prose exceeds it.

**Required**: State the assumption (`A ∈ E ∧ Account(A) ⟹ Activated(A_doc(A))`) once with a single non-derivability note. Drop the duplicated rationale in the claims table and the use-site inventory.

## OUT_OF_SCOPE

### Topic 1: Effective-owner and subdivision-authority grounding over the baptismal registry
**Why out of scope**: These require ASN-0042's registry `B`, which is not part of this state `(C, L, E, M, R)`. The note correctly limits itself to the structural ownership `pfx(π) ≼ d` and defers the rest. This is a future registry-carrying ASN, not an error here.

### Topic 2: Forking contrast prose (CREATENEWVERSION mechanics)
**Why out of scope**: The "What Distinguishes Creation From Forking" section describes forking's populated arrangement to frame the contrast. Forking is explicitly out of scope; the note defines no forking claims and the formal content for *this* operation remains `ran(M'(d)) = ∅`. The contrast is acceptable framing, not a claim to flag.

VERDICT: REVISE
