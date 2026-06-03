# Review of ASN-0071

The proofs here are genuinely thorough — PC, PC-RANGE, and F-DEEP each carry their case splits explicitly, the totality and componentwise arguments are non-circular, and the five worked queries verify the key postconditions against concrete states. The numerics all check out (`v_A ⊕ δ(1,2) = [s_C,2]`, the cross-depth subtree capture, the F-DEEP exclusion). I found no rigor gap. The residual problems are the forward-reference accretion this note is flagged for.

## REVISE

### Issue 1: Query section pre-states and defers the empty-source result
**ASN-0071, *The query***: "Dropping clause (i) is deliberate: a vspec naming a source whose content subspace is empty is admissible, and *Resolution* below handles it as the empty-source case (`iaddrs_one(d_s, σ)(Σ) = ∅`) rather than rejecting it as ill-formed."
**Problem**: This is the named accretion pattern in three forms at once — a defensive justification ("is deliberate"... "rather than rejecting"), a forward pointer to a downstream location ("*Resolution* below handles it"), and a pre-statement of the downstream result (`= ∅`). A reader following the vspec definition must skip this design-defense to reach the actual PC derivation. The mechanics belong in *Resolution*.
**Required**: In *The query*, state only that a vspec may name a source with empty content subspace (admissibility). Remove the justification, the forward pointer, and the pre-stated `iaddrs_one = ∅`.

### Issue 2: The empty-source resolution is stated in three places
**ASN-0071, *The query* / *Resolution* / F-DEEP row**: the fact `V_{s_C}(d_s) = ∅ ⟹ iaddrs_one(d_s, σ)(Σ) = ∅` appears in the *The query* parenthetical (Issue 1), again in *Resolution* ("the intersection is empty and `iaddrs_one(d_s, σ)(Σ) = ∅` trivially"), and again as the "companion empty-source case" in the F-DEEP claim row.
**Problem**: Two paragraphs (plus a table row) saying the same thing in different words. The Resolution derivation is the load-bearing one.
**Required**: Keep the empty-source case only where it is derived (in *Resolution*, where F-DEEP is established). Drop the duplicate statements.

### Issue 3: Repetitive sibling-creation narration in the worked scenario
**ASN-0071, *A worked scenario*, steps 6, 9, 12, 14**: each repeats verbatim the form "`parent(d_X) = parent(...) = acct ∈ E` (K.δ-ID.parent-0) discharges P8; `zeros(d_X) = 2`, so `Document(d_X)`."
**Problem**: Four near-identical discharge recitations. The first establishes the sibling-creation pattern; the rest are boilerplate the reader must scan past.
**Required**: Narrate the sibling-creation discharge once, then reference it ("by the same discharge as step 6") for the later siblings.

## OUT_OF_SCOPE

### Topic 1: Required guarantee linking current-state result to historical `R`
**Why out of scope**: Open Question 1 asks what relationship `find` must guarantee against the permanent provenance relation `R`. The Currency section correctly states present behavior (find ignores `R`); specifying a *required* reconciliation guarantee is new territory for a future ASN.

### Topic 2: Rejection policy for unresolvable vspec positions
**Why out of scope**: Open Question 2. F-FILT fixes current silent-filter behavior; a policy mandating rejection under some conditions is a future specification choice, not an error here.

VERDICT: REVISE
