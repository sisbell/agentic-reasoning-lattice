# Review of ASN-0123

I checked the proofs at the level of detail the topic demands. The substantive core holds: VN-B1's induction over K.δ (the four arriving cases — Node/k=2 excluded, k=1 pinned to c₁, k=0 pinned to the frontier) is exhaustive and correct; SA's antichain argument (counting d₀'s two zeros plus the separator inside b's document prefix) is sound; V8's coverer-set equality and V9's reconstruction of O5(ii) as a *theorem* (the `[pfx(π), 0]` sub-prefix forcing `zeros ≥ 2` against O1a) are both airtight, and the latter is correctly load-bearing for severance. V-WF discharges every step precondition and both couplings across both branches, including the n=0 degeneracy. The two worked instances verify V2/V13/V9w/V10 against concrete addresses, the wp-style necessity analysis is present (G2, V10), and there are no cross-ASN references outside the foundation set. No correctness, edge-case, or completeness defect surfaced.

What remains is the residue the `review-mode.anti-bloat` classifier targets: a property stated in full at multiple sites, and a proof aside that justifies ordering by forward reference.

## REVISE

### Issue 1: Registry-purity asserted in full at three sites
**ASN-0123, `nextv` definition / G1 / V5(b)**:
- `nextv` def: "`nextv` is *registry-pure*: its arguments are the set of allocated identities and the source's address, and nothing else — the content store, arrangements, link store, and provenance are not consulted."
- G1: "The frontier is a function of the registry alone."
- V5(b): "the allocator is *registry-pure*: `(A Σ₁, Σ₂ : … : nextv(Σ₁.E, d) = nextv(Σ₂.E, d))` — `C`, `M`, `L`, `R` are not arguments".

**Problem**: V5(b) is the formal claim (the congruence statement is its load-bearing content). The `nextv`-definition annotation states the same property informally and re-enumerates the four uninvolved stores; V5(b) then re-enumerates `C, M, L, R` a second time. G1 echoes it a third. This is exactly the "definition's introduction enumerates downstream consumers / two paragraphs say the same thing in different words" compounding the mode flags — three full assertions of one property where one numbered claim plus pointers would do.

**Required**: Keep V5(b) as the formal home. Reduce the `nextv`-definition annotation to the bare property line (drop the store re-enumeration, which V5(b) carries) and let G1's "function of the registry alone" stand as the only informal echo, or have it point at V5(b). The store-list should appear once.

### Issue 2: VN-B1 closing remark is a forward-referencing ordering justification
**ASN-0123, after the VN-B1 proof**: "Note what the proof did *not* assume: VD (below). Contiguity of the namespace is forced by K.δ's freshness and operand constraints alone, whatever composite fires the step — VD governs what the arrivals *mean*, not where they land."

**Problem**: The "Note what the proof did *not* assume: VD (below)" framing is a non-circularity/ordering justification — the proof visibly never invokes VD, so the disclaimer's only function is to preempt a circularity worry against a downstream claim. That matches the named pattern "prose justifies document ordering / forward reference." The closing clause ("VD governs what the arrivals mean, not where they land") is a legitimate statement of what VD does and supports V5(a)'s allocation-order-vs-fork-order distinction; the defensive front half does not.

**Required**: Drop the "what the proof did not assume (below)" framing. If the robustness point ("whatever composite fires the step") is needed for V5(a), state it there as content rather than here as a disclaimer.

## OUT_OF_SCOPE

The out-of-scope topics (document creation, version comparison, edit/link/delivery/replication operations) are correctly excluded — no claim drifts into them, and the Open Questions enumerate the genuine future work (the VD-enforcement invariant, cross-owner derivation directionality, concurrent-fork serialization, location-fixed windowing). I have nothing to add here.

VERDICT: REVISE
