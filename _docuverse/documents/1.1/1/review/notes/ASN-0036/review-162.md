# Review of ASN-0036

I read the strand model end to end and checked each proof. The core proofs — S8's singleton partition (within-subspace incompatibility lemma plus the cross-subspace T5/T10 argument), D-CTG-depth's infinite-intermediate contradiction, and D-SEQ's four-step assembly — are sound, with boundaries (`m = 2` forcing `j = m`, empty `dom(M(d))`, the half-open upper bound) handled explicitly. The worked example exercises S0/S3/S5/S7/S8/D-SEQ across three states and adds two violation cases. Two issues remain, both narrow.

## REVISE

### Issue 1: `subspace` claims a dependency its definition does not have
**ASN-0036, Properties Introduced table**: "subspace(v) | ... | introduced; uses T0 (ASN-0034), S8a"
**Problem**: The `subspace` formal contract states `Preconditions: v ∈ T, #v ≥ 1` and `Definition: subspace(v) = v₁`, with no Depends clause. The projection `v₁` does not use S8a — S8a merely guarantees that V-positions *satisfy* the `#v ≥ 1` precondition at use sites, which is not the same as the definition depending on S8a. The table conflates "applicable to objects that satisfy S8a" with "derived using S8a." A reader tracing the dependency graph is misled into thinking `subspace` is downstream of S8a, when in fact S8a's own statement and proof presuppose `subspace` (S8a/S8-depth reference `subspace(u) = subspace(w)`), making the claimed dependency backwards.
**Required**: Drop S8a from the table entry for `subspace`. Keep T0 only if the intent is to source the ℕ-valued codomain of `v₁`; otherwise list it as a bare introduced projection matching its (empty-Depends) formal contract.

### Issue 2: orphaned defensive notation caveat around "consecutive V-positions"
**ASN-0036, end of the S8-depth section**: "consecutive positions differ only at the ordinal (last) component: position s.x is followed by s.(x+1), where +1 is NAT addition on the ordinal component — distinct from tumbler ordinal displacement, which we always write shift(v, k) (equivalently v ⊕ δ(k, m) per ASN-0034), never v + k."
**Problem**: The `s.(x+1)` / `+1` notation introduced here is never used in any subsequent formal statement — D-MIN, D-SEQ, the singleton interval, and ValidInsertionPosition all express increments exclusively via `shift`. The trailing clause ("distinct from ... which we always write shift(v, k) ..., never v + k") is a defensive notational disambiguation guarding against a confusion the rest of the note never invites, since it consistently uses `shift`. Under this note's anti-bloat classifier this is exactly the accreted meta-prose to surface: it does not advance any claim and the reader must skip it.
**Required**: Either cut the caveat and the unused `s.(x+1)` notation, defining "consecutive" directly as `v_{j+1} = shift(v_j, 1)` (the form actually used downstream), or delete the sentence entirely since D-SEQ already pins the structure.

## OUT_OF_SCOPE

### Topic 1: operation-layer preservation of D-CTG / D-MIN / S2
The note proves D-CTG/D-MIN/D-SEQ are well-formedness constraints on document *states* and verifies the empty base case, but does not prove that DELETE/INSERT/COPY/REARRANGE preserve them.
**Why out of scope**: Operation-specific frame and postconditions are explicitly excluded by the Scope section, and the obligation is already recorded as an Open Question. This is future-ASN territory, not a defect here.

### Topic 2: value-domain `Val` structure and the sharing inverse
S5 establishes unbounded sharing multiplicity but says nothing about computing which documents reference a given I-address, and `Val` is left opaque.
**Why out of scope**: Both are correctly posed as Open Questions; introducing them now would over-reach the state/invariant remit of the strand model.

VERDICT: REVISE
