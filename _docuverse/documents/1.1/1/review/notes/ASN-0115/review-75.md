# Review of ASN-0115

## REVISE

### Issue 1: UnitSpec (a) leaves the V-spec definition's `zeros(d) = 2` conjunct undischarged
**ASN-0115, §"What a spec-set is, and what delivery is" (UnitSpec lemma, part (a))**: "unit(d, v) is a V-spec in the sense above: its start has the required V-position shape, and its span is well-formed (T12), level-uniform, and ordinal-level. … and `d ∈ dom(Σ.M)` by hypothesis."

**Problem**: The V-spec definition imposes two conditions on the named document: it is "a tumbler with `zeros(d) = 2` (ASN-0045) that is present in the arrangement family, `d ∈ dom(Σ.M)`." UnitSpec's hypothesis supplies only `d ∈ dom(Σ.M)`, and the proof of (a) discharges the start shape, the span conditions, and the membership conjunct — but never establishes `zeros(d) = 2`. The fact is true and one step away: M0 (DocumentTumblerWellFormed, ASN-0093) gives `T4-valid(d) ∧ zeros(d) = 2` for every `d ∈ dom(M)`, and the ASN's standing reachability precondition puts every consulted state in M0's range. But the proof does not say so, and the gap propagates: every worked instance in the ASN (R8, R9, R10, R11) obtains its specs through UnitSpec, so each inherits an unverified conjunct of V-spec-hood. By the ASN's own citation discipline — which elsewhere discharges far smaller steps explicitly (e.g., `item` totality from S3★-aux, the equal-length prefix-equality step from Prefix + T3) — this conjunct must be named and closed, not left to the reader.

**Required**: Either add the one-line discharge to UnitSpec (a) — `zeros(d) = 2` by M0 (ASN-0093), since `d ∈ dom(Σ.M)` at the reachable state `Σ` — or restate the V-spec definition so that `zeros(d) = 2` is explicitly marked as the M0-derived consequence of `d ∈ dom(Σ.M)` at reachable states rather than an independent conjunct; either change closes the gap for all four worked instances at once.

## OUT_OF_SCOPE

### Topic 1: Delivery semantics for a span straddling the subspace boundary
The ASN deliberately excludes boundary-crossing spans via the ordinal-level discipline, proves the exclusion sound (Confinement lemma), exhibits a concrete straddling counterexample (`s = [1,5]`, `ℓ = [2,0]`), and records the relaxed-span question in Open Questions.
**Why out of scope**: the ordinal-level restriction is a scoping decision with a proof, not a gap; a delivery semantics for straddling spans is new territory for a future ASN.

### Topic 2: Reading the structure of a delivered link reference
R10 delivers `⟨ref, a⟩` and explicitly stops at the address — "*not* the link's endset structure, which is the concern of operations that read a link by address."
**Why out of scope**: per the scope list, that is READLINK territory (ASN-0111), and the ASN correctly defers rather than defining claims for it.

Anti-bloat scan (classifier active): no findings rise to the flag threshold. The force-empty rationale for the `act` override carries a real proof (the deep-case emptiness argument), the UnitSpec motivation states a substantive fact (naming a position does not determine a span), and the few intra-document forward pointers in the nominal-extent paragraph resolve to a section that actually carries the deferred analysis — I verified both directions of the `|act| = ℓ_{#ℓ}` biconditional against the R6 frontier case split, including the non-canonical-start and `V_S(d) = ∅` corners, and they hold. No relocated-finding residue, no duplicated normative prose, no consumer inventories.

VERDICT: REVISE
