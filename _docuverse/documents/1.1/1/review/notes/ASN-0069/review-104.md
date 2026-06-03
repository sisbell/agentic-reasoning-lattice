# Review of ASN-0069

## REVISE

### Issue 1: §"Composability: Fork of a Fork" opens with an informal 2-step trace that duplicates V11
**ASN-0069, §"Composability: Fork of a Fork"**: "Suppose `Σ →* Σ¹` forks `d_src` to `d¹_new`, then `Σ¹ →* Σ²` forks `d¹_new` to `d²_new`... By V1 at each fork... By V2 at each fork... By V4 at each fork... Composing: the I-addresses in `M²(d²_new)` are the same I-addresses as in `M(d_src)`..."

**Problem**: This informal trace is the `k = 2` instance of V11, which is then stated and proved generally by induction immediately below (base `k = 1` + inductive step). The Worked Example *also* contains a concrete chain instance ("Further forking — fork of a fork (V11 chain case)"). The fork-of-fork result is therefore presented three times: informal abstract trace, formal general induction, concrete worked instance. The middle layer (the informal trace) advances no reasoning that V11's statement and the worked instance don't already carry — this is the "two paragraphs saying the same thing in different words" pattern the anti-bloat pass targets. The trace is not cited by any downstream claim (everything cites V11/V11a).

**Required**: Delete the informal 2-step trace; let V11's statement + induction stand, with the Worked Example supplying the concrete illustration. If a lead-in is wanted, reduce it to one sentence stating that `d_new ∈ E_doc` is itself forkable.

### Issue 2: V5's first paragraph is rationale/essay, not derivation
**ASN-0069, §"Frame: Source Isolation"**: "V5 is foundational to the source-fork relationship. It establishes that the source owner's arrangement is unaffected by anyone else's forking activity. They cannot prevent forking (per Nelson's permissionless publishing contract, when applicable), but they incur no observable side effect."

**Problem**: This is "why the property matters" essay content occupying a structural slot — it explains the significance of V5 rather than advancing or applying it. The substantive content of the section is V5a (the general lemma), V5 (its instance), and the bidirectional-frame consequence at the section's end ("each is V5a instantiated at the other document"), all of which stand without this paragraph. The "permissionless publishing contract, when applicable" hedge is precisely the kind of unmoored gloss that compounds across cycles.

**Required**: Remove the paragraph (or fold its one load-bearing clause — that source isolation is symmetric — into the existing bidirectional-frame sentence, which already states it).

## OUT_OF_SCOPE

### Topic 1: ≼-transitivity is re-derived inline in V11a
**Why out of scope**: V11a derives transitivity of the prefix relation `≼` from scratch (unfolding Prefix + NAT-order) because the foundation Prefix contract (ASN-0034) exposes only the definition and the `p ≺ q ⟹ #p < #q` postcondition, not transitivity. The inline derivation is correct and, given the foundation's current surface, necessary. The cleaner fix — exposing ≼-transitivity as a foundation postcondition of Prefix so dependents cite rather than re-derive it — is a change to ASN-0034, not to this ASN. Flagging here only so the foundation gap is recorded.

VERDICT: REVISE
