# Review of ASN-0091

I checked the abstract Vstream-only class, the REARRANGE_K realisation (clause (i)–(v) + frame + reachability discharge), every RE-* derivation, the five worked examples, the multi-step ★ composition, and L-chain. The proofs are sound: RE-ran/RE-μ correctly split target (via RA-π injectivity on the finite dom, S8-fin) vs. non-target (via RA-frame); RE-disc rests correctly on RE-cov + RE-ran through LP12; the collapse branch, shared-image non-uniqueness, and fragmentation/coalescence/equality witnesses are each carried to concrete values. No correctness defect, no out-of-scope operation mechanics, and all cross-references are to foundation ASNs. The findings below are anti-bloat (the classifier this note carries).

## REVISE

### Issue 1: Comparative-to-foundation editorializing in the realisation section
**ASN-0091, "REARRANGE_K Realises the Abstract Class" → Pointwise-fixity frames**: "Two classes of V-position are not merely kept within their subspace but left wholly unpermuted (`π(v) = v`) — a stronger guarantee than K.μ~ clause (iv), which only requires subspace preservation."
**Problem**: The "stronger guarantee than clause (iv)" comparison is editorial. Clause (iv) is discharged on its own terms later in the same section; ranking RE-sub/RE-ext against it does not advance the discharge. The same comparative framing recurs in *Net-effect split* ("strictly weaker than ASN-0047's K.μ~ admissibility clause (ii)") — there the case split it sets up *is* load-bearing, but the "weaker/stronger than clause N" register is accreted meta-prose that should be cut where it is not carrying the argument.
**Required**: State the pointwise-fixity facts (`π(v) = v` and arrangement preservation) and their sources directly; drop the comparison to the foundation clause's weaker form.

### Issue 2: Exhaustive use-site inventory of binary transition invariants
**ASN-0091, "State-Component-Only Invariants"**: "This class comprises ASN-0036's S0 (ContentImmutability) and S1 (StoreMonotonicity) — both satisfied by `Σ'.C = Σ.C` … P0 by `Σ'.C = Σ.C`, P1 by `Σ'.E = Σ.E`, P2 by `Σ'.R = Σ.R`, and P3 … by all four together), L12 (LinkImmutability, by `Σ'.L = Σ.L`), and ASN-0093's C0 (ContentImmutability, by `Σ'.C = Σ.C`)."
**Problem**: This is a flat per-invariant inventory mapping each foundation binary invariant to the frame clause that discharges it — an exhaustiveness enumeration of exactly the kind that compounds across cycles. The discharge is uniform: every binary transition invariant of the foundations constrains only C, L, E, R, or dom(M), each fixed *with equality* by RA-frame. P3 is even re-derived after being named as the synthesis of P0∧P1∧P2∧L12.
**Required**: Replace the enumeration with the single principle ("every binary transition invariant constrains a component fixed by RA-frame, hence holds trivially"), citing the invariant set once rather than attributing each individually.

### Issue 3: "Why the precondition is needed" rationale prose
**ASN-0091, "Composite-Boundary Properties"**: "Interior composite states need not satisfy ASN-0047's three composite-boundary properties P4★ ∧ P4a ∧ P7a — ExtendedReachableStateInvariants establishes them only at composite boundaries, not at the interior states the REARRANGE domain otherwise admits — so the boundary claims require the pre-state to sit at a boundary."
**Problem**: Explains why RA-bndy exists rather than stating what it requires — the flagged "prose around a precondition explaining why it is needed" pattern. The load-bearing content is just: the boundary claims are scoped by RA-bndy; cite ExtendedReachableStateInvariants.
**Required**: State the RA-bndy scoping and the citation; trim the explanatory clause about interior states.

## OUT_OF_SCOPE

### Topic 1: Joint reconstitution of a same-source span split across two cuts
The body ("Cross-Document Transclusion Preserved") and the first Open Question both note that whether two fragments *jointly reconstitute* the original source span is not established. This is correctly deferred — it is new territory (a span-reassembly guarantee), not a defect in the per-byte origin-preservation this ASN proves.

VERDICT: REVISE
