# Review of ASN-0123

This is a strong, careful note. The derivation-from-guarantees structure (G1/G2/G3), the VN-B1 induction, the V9 severance theorem (with O5(ii) re-derived as a theorem rather than cited), and the two worked instances against implementation addresses all meet the bar. The proofs show their work; I found no checkmark-proofs or "by similarly" hand-waves in the load-bearing arguments. SA, the PS coverage derivation, V8, and the V9 case analysis each check out. One real well-definedness gap remains, plus one minor anti-bloat item.

## REVISE

### Issue 1: the cross-owner identity clause does not pin v; its determinism rests on an unproved document-namespace contiguity

**ASN-0123, The Operation — Identity clause, cross-owner branch**: "v := the document identity π allocates as a single document-level K.δ in its account's document sub-allocator A_doc(pfx(π)) = S(pfx(π), 2) (ASN-0047): allocated_by(π, v), with v ∈ S(pfx(π), 2)."

**Problem**: The owned branch fixes its output by an explicit frontier function, `v := nextv(E, d_src)`, whose well-definedness you discharge through VN-B1 (version-namespace contiguity). The cross-owner branch specifies v only by `{allocated_by(π,v) ∧ v ∈ S(pfx(π),2) ∧ fresh}`, which every fresh stream member satisfies. The qualifier "a single document-level K.δ" *does* narrow it — a single K.δ from an operand in E can reach only the next sibling `inc(c_m, 0)` or the base `inc(pfx(π), 2)` (a k=1 step lands outside `S(pfx(π),2)` by the penultimate-zero argument, and `inc(t,0)=c_j` needs `c_{j-1}∈E`, so no skip-ahead is reachable). But that forces v to *the frontier* only when the realized children `E ∩ S(pfx(π), 2)` are a contiguous prefix `{c₁,…,c_m}`; with a gap, both each gap-filler and the frontier are fresh single-K.δ targets. That contiguity is the document-namespace analog of VN-B1, and you neither state nor prove it. VN-B1 as written is restricted to version streams `S(d,1)` with a `zeros(d)=2` base and a k=1 base-spawn; it does not cover document streams `S(pfx(π),2)` with a `zeros(pfx(π))=1` base and a k=2 base-spawn. You explicitly argue (in VN-B1's introduction) that ASN-0040's B1 does not transfer to ASN-0047's K.δ vocabulary by citation — the identical non-transfer applies to document streams, so the contiguity must be proved, not assumed. V-WF is unaffected (realizability needs only existence), but the Effect is presented as a function of Σ ("the operation's value is the fresh identity") and in this branch it is not determined.

**Required**: Either **(a)** generalize VN-B1 to every B6-valid sibling stream — the induction carries over with the base-arrival case becoming the k=2 descent for document namespaces in place of the k=1 version step — then define the document-namespace frontier (e.g. `nextd(E, π) := next(E, pfx(π), 2)`, ASN-0040) and set `v := nextd(E, π)`, restoring parity with the owned branch and grounding V-WF's "k=2 for the first document / k=0 for a later one" split in the operation definition rather than in the proof; or **(b)** state explicitly that placement within π's document namespace is delegated to document creation (out of scope) and that the cross-owner branch requires only freshness, ownership, and the transcription, and reconcile the single-valued "v" in the Effect/Result clauses with that non-determinism.

### Issue 2 (minor, anti-bloat): nextv carries a forward-referenced restatement

**ASN-0123, State and Local Apparatus — nextv**: "… this is VN-B1, stated and proved next." and "nextv is registry-pure: its arguments are the set of allocated identities and the source's address, and nothing else (V5(b) states it formally as a congruence)."

**Problem**: nextv's well-definedness is established *before* VN-B1, the result it depends on, forcing the "stated and proved next" forward reference; and registry-purity is asserted informally at the definition site, then re-claimed formally at V5(b). The forward reference is an ordering artifact, and the informal sentence duplicates V5(b).

**Required**: Move VN-B1 (generalized per Issue 1) ahead of nextv so the definition cites an established result; drop the informal registry-purity sentence and let V5(b) carry it. (Note: fixing Issue 1 via path (a) reorders this region anyway.)

## OUT_OF_SCOPE

No improperly-included material found. The note confines itself to the fork and routes genuinely future questions — concurrent-fork serialization, derivation-direction recovery, link-subspace versioning, location-fixed windowing vs. isolation, withdrawal/supersession, provenance-after-contraction, and correspondence's minimal shared-identity — to its Open Questions rather than specifying them. That is correct scoping, not incompleteness in this ASN.

VERDICT: REVISE
