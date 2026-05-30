# Review of ASN-0042

## REVISE

### Issue 1: Downstream-consumer inventory in the cover-edge bridge

**ASN-0042, State Axioms — "Delegation edges are cover edges (bridge)"**: "The downstream consumer of the closure is **NestingByDelegation** below, which consumes `covers_Σ*` (the `R_Σ`-closure); O8 (IrrevocableDelegation) consumes no closure at all — its proof argues directly from the longest-match rule."

**Problem**: This is a use-site inventory in a definitional slot. It enumerates which later claims do and do not consume `covers_Σ*` and does not advance the bridge claim (that `delegated_Σ(π_d,π') ⟹ R_{Σ'}(π_d,π')`). The accompanying "justified by this correspondence rather than by the naming alone" is the same accretion pattern.

**Required**: Delete the downstream-consumer sentence and the naming-justification clause; the bridge claim and its one-line proof stand without them.

### Issue 2: Spurious, unestablished persistence argument in O8

**ASN-0042, O8 proof — "The delegate covers the address"**: "By B0★ (MultiStepIrrevocability) of ASN-0040 applied along the sub-trajectory `Σ_d^post →* Σ'`, `a` — being baptized — persists in the baptismal registry with unchanged components. Therefore `pfx_{Σ'}(π') ≼ a` holds in `Σ'`."

**Problem**: `pfx_{Σ'}(π') ≼ a` is immediate from the precondition `a ∈ odom(π') = {t : pfx(π') ≼ t}` — it needs no persistence argument. Worse, the B0★ invocation presupposes `a ∈ Σ_d^post.B`, which the precondition (`a ∈ odom(π') ∩ Σ'.B`) does not establish: `a` may be baptized partway along `Σ_d^post →* Σ'`. The sentence is both unnecessary and rests on an unproven premise — reviser drift.

**Required**: Replace with a one-line derivation of `pfx(π') ≼ a` from `a ∈ odom(π')` and O13 (prefix immutability). Drop the B0★ appeal here.

### Issue 3: Notation-justification meta-prose in the cover-relation definition

**ASN-0042, State Axioms — definition of `covers_Σ*`**: "This is the closure of the *structural cover* relation `R_Σ`, deliberately not written `(delegated_Σ)*`: `delegated_Σ` is the five-condition admission predicate (i)–(v), whereas `R_Σ` carries only the most-specific-cover geometry."

**Problem**: "deliberately not written" is defensive notation-justification. The genuine content (that `R_Σ` is the most-specific-cover relation, distinct from the admission predicate) belongs in `R_Σ`'s definition itself; the meta-commentary on what the closure is *not* named is noise.

**Required**: State `R_Σ` directly as the most-specific-cover relation and drop the contrastive framing.

### Issue 4: Implementation-provenance aside grafted onto the coupling axiom

**ASN-0042, O17b**: "(Implementation provenance: ASN-0040's `Bop` is the abstract image of udanax-green's single allocation point for registry writes.)"

**Problem**: This parenthetical explains why the coupling axiom is motivated by an implementation fact rather than stating what the axiom asserts — the "why the axiom is needed" accretion pattern, in implementation-mechanics form, in an axiom slot.

**Required**: Remove the parenthetical. If a Nelson/Gregory design line is wanted, keep it to the one-sentence motivation form used by the other axioms.

## OUT_OF_SCOPE

### Topic 1: Invariants of ownership transfer

The Open Questions raise transfer (divergence of provenance O6 from effective owner O2). The note correctly defers it; transfer is new territory, not an error here.

VERDICT: REVISE
