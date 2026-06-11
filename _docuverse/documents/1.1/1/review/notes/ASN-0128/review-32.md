# Review of ASN-0128

## REVISE

### Issue 1: Wrapper wp equivalence stated without its state domain — falsified by the note's own counterexample
**ASN-0128, Standard registrations / DR (DisciplineRestoration — proof and wrapper wp)**: "`wp(Nullify_Binary(Σ, d_retr, a), {t : a ≼ t} ∩ A_rel^{Σ'} = {a}) ≡ P0 ∧ P-reg ∧ P-tgt`"

**Problem**: The displayed equivalence carries no domain qualifier, and as stated over the ambient reachable domain it is false — by a counterexample the note itself constructs three paragraphs later. The unit-depth ghost-target bypass tuple (from-fill `(d_retr, δ(1, #d_retr))`, to-span at a chain address ahead of the frontier) yields a reachable, non-surface-disciplined state at which a later `Nullify_Binary(Σ, d_retr, a)` with `a = a_emit(Σ, d_retr)` satisfies P0 ∧ P-reg ∧ P-tgt (self-emit disjunct), is admitted, I0-matches the bypass tuple, takes no step, and the postcondition fails: `{t : a ≼ t} ∩ A_rel^{Σ'} = ∅ ≠ {a}`. So sufficiency fails off the discipline — specifically at the hit branch, whose Residence bullet is the one place the proof consumes "Fix a surface-disciplined derivation" — while necessity, as the proof's own per-precondition argument shows, holds at every reachable state. The surrounding prose ("the wp the vacuity buys the wrapper") gestures at the scope, but the display itself is the formal claim, and the note's other wp displays are careful here: ASN-0086's wp Case 1 names its ambient domain explicitly, and I6 separates the unrestricted wp from its disciplined-domain reduction as two labeled claims. The same scoping looseness recurs in S3's from-fill paragraph: "every retraction is wrapper-routed, so the convention — F answers *who retracts*, G carries *what is retracted* — holds totally." "Totally" is true only at states surface-disciplined derivations reach; raw R-class `K.λ_sh` deposits remain `→_sh`-reachable, and such a tuple's from-span need not name its emitter's document.

**Required**: Qualify the displayed equivalence with its domain — "at every state a surface-disciplined derivation reaches (SD)" — and state the split explicitly: necessity holds at every reachable state; sufficiency's hit branch requires the discipline (the miss branch does not, ASN-0126's contract being discipline-independent). Rescope S3's "holds totally" to the same domain.

### Issue 2: DR statement/proof split has accreted placement meta-prose and a restatement
**ASN-0128, Idem operational semantics / DR (statement)**: "The proof, and the wrapper wp the vacuity restores, sit with the retraction policy that enforces the discipline (Standard registrations); the statement sits here, beside SD, because the contracts below consume it."
**ASN-0128, Standard registrations / DR (proof)**: "The statement stands beside SD (Idem operational semantics): along surface-disciplined derivations, C3 holds at every gate-clearing emit, so a tuple is born nullified only through C2's self-nullification."

**Problem**: The first quotation is prose justifying document ordering — "the statement sits here … because the contracts below consume it" advances no reasoning; the forward pointer alone does the work. The second quotation then restates DR's content (already given verbatim in the statement block) together with a second placement remark ("stands beside SD"). This is the anti-bloat pattern twice over: ordering justification, and two paragraphs in different sections saying the same thing in different words. A reader following the proof must skip past both before the proof begins.

**Required**: End the DR statement with a bare pointer ("Proof and wrapper wp: Standard registrations."). Open the proof block with the proof — at most "DR's statement (Idem operational semantics):" as a back-reference — deleting the restatement and both placement remarks.

### Issue 3: R-VAL and R-C1 state the same claim in two sections
**ASN-0128, R-VAL**: "The shipped representatives are registry entries, so the same sweep already decides the standard-registration designation — no further tests (R-C1, Standard registrations)."
**ASN-0128, R-C1**: "This is not a check beyond R-VAL's: the shipped representatives are registry entries, so C0's pairwise key-uniqueness sweep — already counted in R-VAL's `O(|registry|²)` tests — includes the three shipped pairs, and R-C1 names that instance."

**Problem**: The same observation — the designation non-collision check is an instance of C0's key-uniqueness sweep, costing nothing extra — is carried in full in both sections. This reads as residue of folding R-C1 into R-VAL: content relocated rather than removed. The R-VAL sentence is additionally a use-site remark pointing forward to a definition the reader has not met, in a paragraph whose job is the validation procedure, not the standard registrations.

**Required**: Carry the observation once, in R-C1, where the designated classes are introduced; delete R-VAL's forward sentence (or reduce it to the bare cross-reference "(R-C1)" attached to the key-uniqueness clause).

## OUT_OF_SCOPE

### Topic 1: Rejection-cause signaling at the operation surface
The exposed `Emit_K` and `Nullify_Binary` are partial — rejection is "no step, no address" — but the note fixes no way for a caller to distinguish a gate failure from an invalid home from a P-tgt failure. An error taxonomy or result type is interface machinery this note's contracts do not need; it belongs to a successor specifying the caller protocol.
**Why out of scope**: The note's wp analysis is complete under the attainability convention without it; distinguishing rejection causes adds surface, not semantics, and nothing in I6 or S3 depends on the distinction being observable.

### Topic 2: The serializing authority behind I4
I4 places concurrency "ahead of the substrate relation" and posits "a serializing authority orders the two calls" — but what that authority is, and what ordering or atomicity guarantees it owes (e.g., for `retract_stale`'s non-atomic batch interleaving with concurrent emits), is unspecified.
**Why out of scope**: `→_sh` inherits ASN-0086's sequential model by construction; a concurrency model is new state-machine territory, not an error in this note's sequential contracts, which are stated correctly modulo the interleaving they explicitly permit.

VERDICT: REVISE
