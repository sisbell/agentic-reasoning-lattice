## Review Notes

I read through the ASN content — V-sub, S8-depth, S8-fin, NAT-induction, subspace, Σ.M(d), AX-1, and D-MIN — against the NAT-* and T-series foundation. The bulk of D-MIN's existence/uniqueness induction (the least-index principle P(N), the segment-identity split, the trichotomy-driven minimality argument, and the uniqueness argument via T1's incompatibility clauses) checks out: each step traces to a specific foundation clause, the base case and successor case are both discharged correctly, and the citation discipline (grounding constants like `1` and `0` directly rather than through a transitive route) is applied consistently. AX-1's absence from D-MIN's Depends list is not an error — it's used only in illustrative prose about the vacuous base-state case, not in the formal derivation, matching the same commentary-vs-Depends convention S8-depth uses to exclude OrdinalShift/OrdShiftHom.

One real gap surfaced in D-MIN's non-derivability argument.

### Non-derivability witness omits S8-depth from the tested constraint set
**Class**: REVISE
**Foundation**: S8-depth (FixedDepthVPositions)
**ASN**: D-MIN, body heading *"Non-derivability from the other constraints. D-MIN is logically independent of contiguity (D-CTG), positivity and depth (S8a), and finiteness (S8-fin)..."*; and Formal Contract Design Requirement bullet: *"it is not entailed by D-CTG, S8a, and S8-fin, witnessed by the contiguous, positive, finite, depth-2 set {[1, 5], [1, 6], [1, 7]}..."*
**Issue**: Both the enumeration heading and the Formal Contract's Design Requirement bullet attribute the witness's "depth" property to S8a, but S8a only constrains `zeros(t)=0 ∧ #t≥2` — positivity and a per-tumbler depth *floor* — not the uniform common-depth-across-positions property the witness actually relies on. The uniform depth is S8-depth's contribution, and the body correctly cites it two sentences later: *"every component is strictly positive at the common depth 2 (S8a, S8-depth)."* S8-depth is a distinct, independently-motivated axiom in this same ASN (with its own careful design-vs-evidence discussion), yet it is missing entirely from the formal "not entailed by X, Y, Z" list even though the witness set is constructed specifically to satisfy it (fixed depth 2 across all three positions) and would not be a valid counterexample without that property holding.
**What needs resolving**: Add S8-depth to both the Non-derivability heading's enumeration and the Formal Contract's Design Requirement bullet, and correct "positivity and depth (S8a)" to separate the two axioms by the properties they actually supply — positivity/depth-floor from S8a, uniform depth from S8-depth — consistent with how the body text three sentences later cites them.

### Notational drift: `M(d)` vs `Σ.M(d)` in S8-fin's intro prose
**Class**: OBSERVE
**Foundation**: Σ.M(d) (Arrangement)
**ASN**: S8-fin, intro paragraph: *"...most sharply S8, whose forward lockstep walk on `dom(M(d))` terminates only because the domain is finite... Every consumer (S8, D-SEQ, D-CTG-depth, D-MIN) reads S8-fin solely as the property that `dom(M(d))` is finite..."*
**Issue**: Every other use in this ASN, including S8-fin's own formal Axiom, writes `dom(Σ.M(d))`. These two instances drop the `Σ.` prefix. Meaning is unambiguous from context, so this doesn't affect soundness.
**What needs resolving**: N/A — cosmetic; align the two instances with `Σ.M(d)` if touching this paragraph for other reasons.

VERDICT: REVISE