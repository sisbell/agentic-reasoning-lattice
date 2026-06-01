# Review of ASN-0047

I worked through the state model, the seven elementary transitions plus K.μ~, the coupling constraints, the K.μ~ decomposition (including the admissibility-filter circularity question), the D-SEQ★ derivation, and the verification matrix against the worked examples. I did not find a substantive correctness gap — the boundary cases I probed (full-subspace clearance and depth re-pinning under K.μ⁻, first-content insertion, orphan links via bare K.λ, intra-document transclusion, record-then-strip composites excluded by J1'★, second-version fork via k=0 on A_v) are all handled, and the apparent circularity in establishing S3★(Σ') under K.μ~ is broken by the independently-verified `π_swap` witness. The findings below are confined to meta-prose / navigational accretion of the kind the anti-bloat classifier asks to surface at source.

## REVISE

### Issue 1: Design-uncertain deferral inside the L3 restatement duplicates an Open Question
**ASN-0047, §Link store and extended system state, L3 "Semantics of empty endsets at slots 1 and 2"**: "Whether to narrow K.λ with a stricter `e₁ ∪ e₂ ≠ ∅` precondition is recorded as *design-uncertain* and left to a future operations ASN."
**Problem**: This sentence is verbatim the Open Question "Should K.λ require `e₁ ∪ e₂ ≠ ∅` to exclude type-only links...". The deferral-to-future-ASN sits in a slot whose job is to restate an inherited invariant (L3) for narrative continuity; a reader following the L3 statement must skip past a future-work note that is already catalogued where future work belongs. This is the "multiple paragraphs deferring to the same downstream location" / open-question-in-a-structural-slot pattern.
**Required**: Keep the object-level fact (L3 admits `e₁ = ∅` and `e₂ = ∅`, only `e₃` is required non-empty) in the L3 restatement; delete the design-uncertain/deferral sentence here and rely on the existing Open Question entry.

### Issue 2: K.μ⁺ precondition states S2 preservation twice
**ASN-0047, §Elementary transitions, K.μ⁺ "Pairwise V-position distinctness on new mappings"**: the block first says the new positions "ensur[e] each new mapping adds a fresh V-position ... making `M'(d)` a partial function (S2) by construction," then restates "Functionality (S2) is preserved: `dom(M'(d)) ⊃ dom(M(d))` with value preservation at existing positions means new entries are assigned at positions outside `dom(M(d))`, so `M'(d)` remains a function..."
**Problem**: Two sentences in the same precondition block establish the same S2 claim in different words. The second is the verification-matrix S2/K.μ⁺ cell's argument restated inline. The reader parses the same disjointness-implies-single-valued argument twice.
**Required**: Keep one statement of S2 preservation (the pairwise-distinctness-of-new-positions form) and drop the second restatement; let the matrix cell carry the matrix-level summary.

### Issue 3: K.μ~ verification-matrix S3★ cell understates its own derivation, presenting apparent circularity
**ASN-0047, §Extended reachable-state invariants, verification matrix, S3★ row / K.μ~ cell**: "S3★(Σ') stipulated by admissibility filter (see *Decomposition of K.μ~*)".
**Problem**: Taken at the matrix (the navigational index a reader uses first), this cell reads as "S3★ at Σ' holds because we assume it" — and since Step (A) derives subspace preservation *from* S3★(Σ'), and Step (B.2)→(B.3) re-derive S3★(Σ') *using* subspace preservation, the cell invites a circularity reading. The body actually resolves this: B.3 establishes S3★ at Σ' from the decomposition mechanics (B.1 survivors + B.2 new content positions), and non-vacuity is secured by the directly-verified `π_swap` witness. But the matrix cell points only to "stipulated by admissibility filter," not to the B.1+B.2+B.3 discharge that makes the stipulation non-circular.
**Required**: Reword the cell to name the load-bearing discharge ("S3★(Σ') discharged by the K.μ⁻+K.μ⁺ decomposition: survivors via B.1, new content positions via B.2; non-vacuity by the π_swap witness") rather than "stipulated by admissibility filter," so the index does not present a circularity the body has already broken.

## OUT_OF_SCOPE

### Topic 1: NodeUniqueAllocation / node-allocation registry as an abstraction boundary
**Why out of scope**: Whether the external node-allocation registry is the right abstraction boundary for the docuverse layer (versus a registry-mechanism specification) is already an Open Question and concerns a future operations/protocol ASN, not a correctness defect here. The registry is introduced abstractly via axioms (NodeUniqueAllocation, NodeRegistryBootstrap), which keeps this ASN at the state/operation/invariant level rather than implementation mechanics — so it does not warrant META.

META: not applicable — the ASN remains squarely about state, transitions, and invariants stated abstractly enough to bind an alternative implementation.

VERDICT: REVISE
