# Review of ASN-0117

I read the ASN on its own terms. The architecture is sound: DELETE is correctly framed as an arrangement-layer contraction with the content store in strict frame, derived by citation to the foundation contraction ASN-0082 (a foundation ASN, so the citations are permitted). The DEL-REMOVE count-contraction restatement correctly handles within-document sharing, the worked example exercises the real boundaries (suffix delete, full delete, sharing), and the wp analysis is genuinely non-trivial. Two issues remain.

## REVISE

### Issue 1: wp derivation's intermediate range identity drops the link-subspace images

**ASN-0117, "A weakest precondition" section**: "We read `ran(M'(d))` off the Effect... Hence... `ran(M'(d)) = M(d)(L) ∪ M(d)(R) = ran(M(d)) \ A_del^{excl}`".

**Problem**: `ran(M'(d))` is the full-document range, spanning *both* subspaces. DEL-FSUB preserves the link-subspace (`s_L`) positions verbatim, so their images sit in `ran(M'(d))` but are absent from `M(d)(L) ∪ M(d)(R)` (where `L, R ⊆ V_S(d) = V_{s_C}(d)` are text positions only). The intermediate identity `ran(M'(d)) = M(d)(L) ∪ M(d)(R)` is therefore false as a full-document statement. The *final* identity `ran(M(d)) \ A_del^{excl}` happens to be correct — because `A_del` consists of text content addresses (`subspace_I = s_C`), disjoint from the unchanged `s_L` images, so removing `A_del^{excl}` from the full prior range yields exactly the post-state full range. But the step that bridges them is wrong, and it matters here precisely because LP12 evaluates discoverability against the *full* `ran(M(d))` and a link's coverage may reference link-subspace addresses (L4(c) cross-subspace endsets).

**Required**: Either restrict the middle term to the text subspace explicitly (`{Σ.M(d)(v) : v ∈ project, subspace(v) = s_C}`) and carry the unchanged `s_L` images through, or write the identity as `ran(M'(d)) = (M(d)(L) ∪ M(d)(R)) ∪ ran(M(d)\!\restriction\!V_{s_L}(d))` so the derivation `= ran(M(d)) \ A_del^{excl}` is justified rather than asserted.

### Issue 2: P2's gap-closure clause is stated unconditionally but is undefined on the suffix-delete boundary

**ASN-0117, P2 (GapClosure)**: "...the gap closes exactly (`σ(q_{J+c}) = q_J`)."

**Problem**: When `J + c = N + 1` (suffix delete, the case the precondition explicitly admits), `R = ∅` and `q_{J+c} = q_{N+1}` is not an arranged position. There is no gap to close, yet P2 asserts the gap-closure clause unconditionally. ASN-0082's own D-SEP guards this: D-SEP(b) conditions the positional reading on `R ≠ ∅`, reserving only the pure arithmetic identity `ord(r) ⊖ w_ord = ord(p)` (D-SEP(a)) for the unguarded case. The worked example correctly notes "DEL-SHIFT vacuous" for the suffix case, but the P2 claim statement does not carry that condition.

**Required**: Condition the gap-closure clause of P2 on `R ≠ ∅` (matching D-SEP(b)), or relabel `σ(q_{J+c}) = q_J` as the pure arithmetic identity (D-SEP(a)) that holds whether or not `q_{J+c}` is arranged, so the prose "the gap closes" is not asserted where there is no gap.

## OUT_OF_SCOPE

### Topic 1: Provenance relation (R) under deletion
The ASN works in the `(C, M)` + frame-`L` state model and does not address the provenance relation `R` of ASN-0047's extended state. Since deletion shrinks `Contains_C(Σ)` while `R` only grows, P4★ is trivially preserved, but the interaction is genuinely a concern of the full transition model, not this operation's two-layer scope. The third open question ("invariant relating a content-based discovery index to the arrangement after a deletion") correctly defers this.

### Topic 2: Concurrent deletion without a serializing authority
The second open question raises coordination-free concurrent edits. This is new territory beyond a single-operation specification.

VERDICT: REVISE
