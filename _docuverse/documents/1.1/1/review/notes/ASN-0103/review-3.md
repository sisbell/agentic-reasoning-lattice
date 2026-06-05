# Review of ASN-0103

## REVISE

### Issue 1: Ownership conclusion rests on an unjustified registry extension

**ASN-0103, "Ownership and Immediate Referability" / CND.own**: "The account is a registry member by precondition — `A ∈ Σ.B` (CND.pre) — so `ω_Σ(A)` is defined; and the baptism of `d` adjoins it to the registry, `d ∈ Σ'.B` (registry coupling, O17b; ASN-0042) ..."

**Problem**: O17b does not establish `d ∈ Σ'.B`. Its statement is a closure/frame constraint — `Σ'.B = Σ.B ∨ (E p, d : B6(p,d) : Σ'.B = Σ.B ∪ {next(Σ.B, p, d)} ∧ ...)` — i.e. *at most one* baptism per transition. It permits the first disjunct `Σ'.B = Σ.B`, under which `d ∉ Σ'.B` and `ω_{Σ'}(d)` is undefined. The conclusion `d ∈ Σ'.B` requires independently showing that *this* transition is the baptizing disjunct **and** that `next(Σ.B, A, 2) = d`. The ASN never makes that identification. Compounding this, CREATENEWDOCUMENT is specified over ASN-0047's state `(C, L, E, M, R)`, which has no `B` component at all; the `K.δ` frame updates only `E` and `M`. The bridge from "`d` enters `E`" to "`d` enters the baptismal registry `B`" is asserted, not derived — and O17b is the wrong lemma for it (it constrains changes to `B`, it does not assert one occurred). Without `d ∈ Σ'.B`, the entire longest-prefix argument that follows (`ω_{Σ'}(d) = ω_Σ(A)`) is unsupported.

**Required**: Establish, via the baptism semantics (ASN-0040 `Bop`/`B0a`, or an explicit entity↔registry coupling that ties a `K.δ` document allocation to a registry extension), that the creation transition yields `Σ'.B = Σ.B ∪ {d}` with `d ∉ Σ.B`. Only then is `ω_{Σ'}(d)` defined and the account-tier (O1a) longest-prefix argument applicable. Cite the lemma that *forces* the extension, not O17b, which merely bounds it.

### Issue 2: Blanket invariant claim outruns what is verified

**ASN-0103, "Invariants Maintained"**: "All invariants hold at `Σ'`, and since the composite is a single atomic transition, they hold at every observable state. The operation is correct."

**Problem**: The binding correctness criterion is ASN-0047's `ExtendedReachableStateInvariants` theorem, whose conjunction includes D-CTG★, D-MIN★, D-SEQ★, S8★, S3★-aux, CL-OWN, CL-UNIQ, the link family (L0, L1, L1a, L1b, L1c, L3, L14, L-fin), C-fin, S7a, S7b, S7d, C1b, C1c, P7, plus composite-boundary properties P4★, P4a, P7a. The section verifies only a named subset (P0, P1, M0, S2, S3★, P6, P8, T8/GlobalUniqueness) and then asserts "all invariants hold." The unverified conjuncts are in fact all discharged — for `d` they are vacuous (empty arrangement: `V_S(d) = ∅`, no content/link V-positions) and for `d' ≠ d` they are frame-inherited (`C' = C`, `L' = L`, `R' = R`, `M'(d') = M(d')`) — but the proof does not say so. A blanket "all invariants hold" with a partial checklist is precisely the kind of unstated coverage the standard forbids.

**Required**: Either enumerate the remaining conjuncts and discharge them explicitly (one line each: "vacuous for the empty arrangement" / "frame-inherited"), or scope the claim to "the operative invariants" consistently and state that the balance hold vacuously/by frame, naming the vacuity premise (`dom(M'(d)) = ∅`, `C'=C ∧ L'=L ∧ R'=R`).

## OUT_OF_SCOPE

### Topic 1: Cross-model identification of ASN-0047's entity set with ASN-0042's baptismal registry

**Why out of scope**: A general account of how entity allocation in the transition model (`E`) couples to the principal/registry model (`B`, `Π`) is foundational infrastructure spanning ASN-0042/0047, not a CREATENEWDOCUMENT concern. (Note: Issue 1 is *not* this topic — Issue 1 is that *this ASN's* ownership claim depends on the coupling and must cite a lemma that actually delivers it. The general coupling axiom belongs elsewhere.)

VERDICT: REVISE
