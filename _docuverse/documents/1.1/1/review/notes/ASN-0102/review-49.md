# Review of ASN-0102

## REVISE

### Issue 1: T7 misapplied to V-positions in X16

**ASN-0102, X16 (cross-subspace disjointness step)**: "The remaining post-state positions — the unmoved link-subspace entries (`subspace(u) = s_L`) — are disjoint from *every* `s_C`-position by subspace-identifier distinctness: any `s_L`-position and any `s_C`-position are element-level tumblers differing in their first component (`s_L ≠ s_C`), so T7 (SubspaceDisjointness, ASN-0034) gives them distinct addresses with no possibility of collision."

**Problem**: This invokes T7 on V-positions, but T7's precondition is `zeros(a) = zeros(b) = 3` (element-level I-addresses). V-positions satisfy `zeros(t) = 0` (S8a, ASN-0036) — they are explicitly zero-free, depth-≥2 tumblers, **not** element-level. Calling them "element-level tumblers" is false, and T7 does not apply to them. The conclusion (an `s_L` position and an `s_C` position are distinct) is true, but the cited justification is wrong.

**Required**: Derive the distinctness directly from T3 (CanonicalRepresentation) / T1: two depth-`m` V-positions differing at component 1 (`s_L ≠ s_C`) are distinct tumblers by component-wise inequality. Drop the T7 citation — it is for element-level I-addresses, not arrangement V-positions.

### Issue 2: standalone/embedded two-readings exposition is duplicated

**ASN-0102, Definition (after "We therefore read COPY's coupling discharge in two ways, both settled in X14.")** lays out "(i) *Standalone:* ... the couplings are read between `Σ` and `Σ'`. (ii) *Embedded:* ... the couplings are read between `Σ_0` and `Σ_n`, P4★ holds at the boundary `Σ_0`, and COPY's step-local discharge lifts ... by provenance permanence (P2) and store monotonicity."

**X14** then restates the identical distinction: "Let `B` denote the composite boundary that carries P4★: in the *standalone* reading `B = Σ` ...; in the *embedded* reading COPY carries `Σ_i → Σ_{i+1}` of a valid composite `Σ_0 →* Σ_n` ... and `B = Σ_0`. By the Amendment, P4★ ... holds at `B` ..."

**Problem**: The same two-readings machinery (standalone `B = Σ`, embedded `B = Σ_0`, lift via P2 + monotonicity) is stated in full in two places, with the Definition-section copy explicitly forward-pointing to where the work is actually done ("both settled in X14"). This is the "two paragraphs say the same thing" + "forward pointer to downstream location" pattern.

**Required**: State the discharge once, in X14 where the couplings are actually discharged. The Definition section needs only the operational facts (precondition read at COPY's immediate pre-state; COPY freely composable), not a duplicate of the boundary-reading argument.

### Issue 3: protocol-rationale bloat justifying free composability

**ASN-0102, Definition ("Amendment to `ValidComposite★`" and "What licenses free composition" paragraphs)**: e.g. "We do not restrict it to standalone use, because both authorities place COPY inside larger units of work."; "A standalone-only COPY would contradict the very call pattern the operation was built for"; "What licenses free composition is that COPY is *self-sufficient* in exactly the sense ASN-0047 attributes to `K.μ⁻` (J2) and `K.μ~` (J3) ..."

**Problem**: The object-level content is one sentence — COPY is added to `ValidComposite★`'s atomic vocabulary and is freely composable. The surrounding prose argues *why* the design choice is correct (defensive justification against a "standalone-only" alternative, appeals to docopy's call pattern, restatement of K.μ⁻/K.μ~ self-sufficiency). This is "new prose around an axiom explains why it is needed rather than what it says."

**Required**: Reduce to the structural statement (COPY is freely composable; it is self-sufficient w.r.t. J0/J1★/J1'★/P4★) and let X14 carry the discharge. Drop the contradiction-with-call-pattern argumentation.

### Issue 4: embedded J1'★ discharge is circular

**ASN-0102, X14 (J1'★ bullet, embedded branch (a))**: "In the embedded reading `a` is new to the range at `Σ_0`; COPY supplies a range witness at `Σ_{i+1}`, and since the composite is valid by hypothesis its closing witness at `Σ_n` is guaranteed — COPY's blanket record cannot be stranded without the composite itself failing J1'★, which validity excludes."

**Problem**: J1'★ at the boundary is part of what *defines* a valid composite. Discharging J1'★ for the embedded reading by assuming "the composite is valid by hypothesis" assumes the conclusion. A later step (e.g. a `K.μ⁻` removing exactly the copied content) can leave `(a, d) ∈ R_n ∖ R_0` with no range-new witness at `Σ_n` — precisely the J1'★ violation. The prose does not show COPY's contribution is consistent with validity; it asserts validity to conclude validity.

**Required**: Either show COPY's per-step witness survives to `Σ_n` under the relevant frame conditions, or state plainly that boundary J1'★ is a composite-level obligation COPY cannot discharge alone (so COPY discharges only its step-local range extension, and boundary J1'★ is checked by `ValidComposite★`). Do not claim to discharge it via "validity excludes."

## OUT_OF_SCOPE

The four Open Questions (later re-displacement and discoverability, transitive containment when a reference target is itself referenced, time-varying resolution, identity when the allocating document is unreachable) are correctly deferred to future ASNs.

VERDICT: REVISE
