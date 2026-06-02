# Review of ASN-0098

## REVISE

### Issue 1: The core observation is restated three times in different words

**ASN-0098, The Projection Operation / Frame Conditions / LP4**:
- Projection section: "Every guarantee in this ASN follows from one observation: of the two inputs, only the arrangement varies. The endset stands still ... Therefore every change in projection must be attributable to a change in Σ.M(d)."
- Frame Conditions intro: "A projection moves only if its inputs move. Since the endset (and therefore its coverage) is fixed by LP3, the projection through a document moves only if that document's arrangement is modified ..."
- LP4 proof: "The projection cannot displace without Σ.M(d) displacing."

**Problem**: The same idea — endset fixed, only `Σ.M(d)` varies — is asserted in three places. The Frame Conditions intro restatement adds nothing the projection-section statement and LP4 do not already carry. This is the "two paragraphs say the same thing in different words" pattern.

**Required**: State the observation once (the projection-section version is the natural home), and let LP4 carry the formal consequence. Drop the Frame Conditions intro restatement.

### Issue 2: Directionality essay inside LP2 drifts toward link-type semantics

**ASN-0098, LP2 (SlotInvariance)**: "The directionality of a standard triple (which end is 'from', which is 'to') is encoded in slot position alone, and slot position is immutable."

**Problem**: This is interpretive essay content about link directionality sitting in a proof whose actual content is structural slot-equality. It is also in mild tension with foundation L7 (DirectionalFlexibility, ASN-0043), which states directional significance is "determined by the link type, outside the link structure" — not "encoded in slot position alone." Link type semantics is out of scope; the directionality gloss should not be asserted here.

**Required**: Trim to the structural fact LP2 actually proves — slot position (which endset occupies which index) is preserved across transitions. Remove the directionality interpretation.

### Issue 3: The "Achievability" prose duplicates the worked numerical example's construction

**ASN-0098, Boundary and Width Behaviour** ("Achievability" paragraph + "Choose ℓ = δ(n, #s) with s ⊕ ℓ ≤ inc(t_m^X(d_0), 0) ...") and the subsequent "Worked numerical example."

**Problem**: The general achievability argument and the worked example present the same frontier construction (canonical displacement bounded at or before the chain's next emission). The worked example (with `δ(3, m)` vs `δ(4, m)`) is a legitimate concrete instance and should stay; the general prose preceding it restates the identical construction abstractly.

**Required**: Keep the worked example (concrete examples are wanted) and reduce the abstract "Achievability" paragraph to the one fact the example does not show — that the frontier bound `s ⊕ ℓ ≤ inc(t_m^X(d_0), 0)` is what discharges tightness against the chain's own future emissions.

### Issue 4: F-definition justifies its breadth by downstream rationale

**ASN-0098, Boundary and Width Behaviour**: "the union of all such chain elements across all T4-valid document tumblers — *including those not yet registered, since future document registrations can activate their chains* — and both subspaces ..."

**Problem**: The parenthetical explains *why* F ranges over unregistered documents (a forward appeal to LP19a's fresh-allocation reasoning) rather than stating the definition. This is forward-reference accretion in a definitional slot.

**Required**: State F as ranging over all T4-valid document tumblers; if the breadth needs motivating, attach it once at the point of use (LP19a), not inside the definition.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery, V-order reflection, link-to-link induced discovery
**Why out of scope**: These are listed in Open Questions and correctly deferred to future ASNs; the present ASN states no claims for them, so there is nothing to fix here.

VERDICT: REVISE
