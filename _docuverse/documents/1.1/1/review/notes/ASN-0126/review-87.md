# Review of ASN-0126

## REVISE

### Issue 1: The operation-set claim conflates operations with transition steps, and lists an operation the gate makes unreachable

**ASN-0126, The registry**: "The operation set is the inherited `{Emit_K, Observe_K, Nullify}` (ASN-0086) together with the refined `K.λ_sh` (The shape-gated emit), none of which writes the registry".

**Problem**: One sentence, two defects.

(a) **`K.λ_sh` is not an operation.** It is defined two sections later as a member of the *transition relation* `→_sh ≡ K.σ ∪ K.α ∪ K.λ_sh`, sitting alongside `K.σ` and `K.α`. ASN-0086 keeps these levels apart — operation set `{Emit_K, Observe_K, Nullify}` versus transition relation `→ ≡ K.σ ∪ K.α ∪ K.λ` — and the note explicitly attributes the operation-set notion to ASN-0086 here. Adjoining `K.λ_sh` "to the operation set" is therefore a category error: operations are the methods an app invokes; `K.λ_sh` is the step they fire. (Registry permanence then correctly lists `K.λ_sh` among the *transition steps* and gives it a frame condition — so the conflation is isolated to this sentence, which makes it cheap to fix and conspicuous when read against the later treatment.)

(b) **The inherited `Nullify` cannot fire under the framework's own dynamics.** "The shape-gated emit" proves that "ASN-0086's `Nullify(Σ, d_retr, a) ≡ Emit_R(Σ, d_retr, ∅, {(a, δ(1, #a))})` … has no `→_sh` image." So one of the three operations this sentence advertises is unreachable under `→_sh`; the framework's actual retraction is the from-filled Binary wrapper of "Retraction as an attributed Binary" (a use of `Emit_R`, hence of `Emit_K`), which the listing does not mention. A reader who takes this listing at face value commits to `Nullify` being a live operation and only later discovers it is dead under the gate — exactly the kind of unreconciled forward dependency the note is otherwise careful to retire.

**Required**: Present the operation set and the transition relation as distinct objects — operations `{Emit_K, Observe_K, Nullify}` (inherited); transition relation *refined* to `→_sh`, with `K.λ_sh` replacing `K.λ`. At the listing, reconcile the inherited `Nullify` with its later-proven `→_sh`-unreachability (retraction is re-expressed as a from-filled `Emit_R`, per "Retraction as an attributed Binary"), so that the operation-set claim is not silently contradicted by the gate result that follows it.

## OUT_OF_SCOPE

(none — the Open Questions already enumerate the deferred territory: idem semantics, the behavior catalog, default and composed predicates, standard registrations, and the F=1/N=3 extension. These are correctly future notes, not gaps here.)

VERDICT: REVISE
