# Cone Review — ASN-0034/TA3 (cycle 3)

*2026-04-18 15:52*

### TA3 uses NAT-order transitivity but does not enumerate it among the four NAT-order roles
**Foundation**: N/A — cross-cutting citation discipline established by T1 Depends (enumerating eight transitivity sites), TumblerSub Depends (enumerating one strict-chain composition transitivity site), and TA2 Depends (which restricts to trichotomy and defining-clause uses), where every NAT-order transitivity use is separately enumerated.

**ASN**: TA3 Depends lists exactly four NAT-order roles: "*Length-pair trichotomy dispatch at `(#a, #w)`*", "*Length-pair trichotomy dispatch at `(#b, #w)`*", "*Result-length trichotomy dispatch at `(L_{a,w}, L_{b,w})`*", and "*Defining-clause conversion at component pairs*". The proof invokes transitivity of `<`/`≤` on ℕ at several sites outside these four roles:
- Sub-case A2 derivation of `L_{a,w} ≤ L_{b,w}`: "combined with the case hypothesis `#a < #b`, this places `(#b, #w)` in sub-case (γ) `#w < #b` (since `#w ≤ #a < #b`)" — chains `#w ≤ #a` with `#a < #b` to get `#w < #b`.
- Case B, B1→B2 bridge: "the pre-`dₐ` agreement between `a` and `b` forces `dₐ ≤ j`; combined with Case B's `j ≤ #a ∧ j ≤ #b`, this gives `dₐ ≤ #a ∧ dₐ ≤ #b`" — chains `dₐ ≤ j` with `j ≤ #a` (resp. `j ≤ #b`).
- Sub-case A2 tail-position hypothesis: "`(b ⊖ w)ᵢ = bᵢ` if `i ≤ #b` (copied from the minuend since `i > d = dₐ ≤ #a < i`)" — chains `d ≤ #a` with `#a < i` to conclude `d < i`.

**Issue**: Each of these is a NAT-order transitivity invocation at a distinct ℕ-triple, not a trichotomy dispatch and not a `≤ ⟺ < ∨ =` defining-clause conversion. T1 and TumblerSub both enumerate transitivity as a separate role in their NAT-order Depends (T1 lists eight transitivity sites explicitly), so the per-clause accounting convention is active in this ASN. TA3 collapses these uses into prose without a Depends entry, leaving the transitivity clause of NAT-order's Axiom uncited at the sites that consume it.

**What needs resolving**: TA3's NAT-order Depends must either enumerate the transitivity sites as a fifth role (matching the per-role, per-pair accounting T1 and TumblerSub apply), or reformulate the proof so that every `≤`/`<` chain reduces to a trichotomy dispatch or defining-clause conversion already listed in the four existing roles.
