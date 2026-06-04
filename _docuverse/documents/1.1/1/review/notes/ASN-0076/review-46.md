# Review of ASN-0076

## REVISE

### Issue 1: E11 depends on E10 but is stated before it
**ASN-0076, E11 (proof)**: "The **frame pullback**: by E10, `Σ'.M(d) = Σ.M(d)` for every `d ∈ E_doc`, so `ran(Σ'.M(d)) = ran(Σ.M(d))`"

**Problem**: E11 is placed between E7 and E8 in the document, yet its proof is load-bearing on E10 ("No Implicit Notification"), which appears two sections *later*. The pullback in E11 cannot be discharged until E10's frame property `Σ'.M(d) = Σ.M(d)` is established. This is a forward reference in the exact shape the note's anti-bloat classifier targets — the reader must skip ahead to E10 to validate E11's central step. The claim numbering (E0–E11 with E11 inserted mid-flow) compounds the non-monotonic dependency order.

**Required**: Present E10 (or at least its frame conclusion) before E11, so E11's pullback cites an already-established result. Either move the E8/E9/E10 block ahead of E11, or inline the one-line frame fact E11 needs with its proper justification at the point of use.

### Issue 2: E2 carries defensive prose justifying machinery the proof does not use
**ASN-0076, E2 (proof)**: "Freshness against the link store is strictly weaker than L11a's allocation-event distinctness and is already on hand from E0, so neither SequentialTransitionAxiom's event-ordering apparatus nor a separate L1c-conformance certification of `ℓ_old` is needed."

**Problem**: This sentence (and the opening "no appeal to L11a is required") advances no part of the E2 argument. It explains what the proof does *not* invoke and why — defensive meta-commentary about proof economy that reads as residue from a prior review cycle. The actual proof (member/non-member of `dom(Σ.L)`) stands on its own; the disclaimer is noise the precise reader must skip past.

**Required**: Delete the meta-commentary about L11a / SequentialTransitionAxiom / L1c not being needed. State the member/non-member argument directly and stop.

### Issue 3: E11's `ℓ_new`-branch vacuity is asserted with an informal "unspawned frontier" notion, not derived
**ASN-0076, E11 (collapse paragraph)**: "while as an as-yet-unspawned allocator frontier `ℓ_new` seeds no descendant allocator and so has no extension in `dom(Σ.L)` either."

**Problem**: The conclusion `{t : ℓ_new ≼ t} ∩ ran(Σ.M(d)) = ∅` is correct, but the `dom(Σ.L)` half rests on an uncited intuition ("seeds no descendant allocator"). The subspace argument handles `dom(Σ.C)`, but for `dom(Σ.L)` the note offers only the informal frontier claim. A clean derivation is available from the foundation: every link in `dom(Σ.L)` is an `A_L`-emission with `#E = 2` (SubAllocatorBundle), so no link properly extends another within the element field; equivalently `dom(Σ.C) ∪ dom(Σ.L) ⊆ F` (LP-Sub, ASN-0098), and no `F`-candidate properly extends `ℓ_new` given its zero structure. The review standard forbids deriving a load-bearing exclusion from a one-phrase appeal to an undefined notion.

**Required**: Replace "as-yet-unspawned allocator frontier… seeds no descendant allocator" with an explicit derivation — either the `#E = 2`-uniformity of link addresses (SubAllocatorBundle) or the LP-Sub / `F`-structure argument — showing no element of `dom(Σ.L)` properly extends `ℓ_new`.

## OUT_OF_SCOPE

### Topic 1: Supersession-chain invariants, cycle-freedom, and "current successor" computation
**Why out of scope**: The Open Questions correctly defer chain semantics, retraction meaning, and authoritative-successor resolution to future ASNs. EDITLINK introduces the primitive and its single-edit guarantees; the relation-level theory is new territory, not a gap in this note.

### Topic 2: Authorization of `d_new` (who may publish a supersession)
**Why out of scope**: E6's application-layer note defers executor/capability questions to a future authorization ASN. The link model has no executor field, so this is genuinely absent from the current state vocabulary rather than an error here.

VERDICT: REVISE
