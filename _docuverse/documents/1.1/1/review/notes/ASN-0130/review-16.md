# Review of ASN-0130

## REVISE

### Issue 1: The wp formula for referenceability gates the already-registered branch under VALID

**ASN-0130, PR0 ("Success, precisely — the born-nullified boundary and the wp")**: 

> `wp(register_pred(d, A_def), POST-ref) ≡ VALID(Σ, A_def) ∧ (hit(Σ, a) ∨ (d ∈ dom(Σ.M) ∧ C3(Σ, d)))`

with the necessity step

> "Reading the branches: a `VALID`-failing call, and an admitted miss with `d ∉ dom(Σ.M)`, are rejections — wp false under I6's attainability convention."

**Problem**: `POST-ref ≡ (E (b, F', G') ∈ A_pdef^{Σ'} :: addrs(F') = {a})` is a **state predicate over Σ′**, not a predicate about the call's *returned address*. I6's attainability convention (`wp(g → S, R) ≡ g ∧ wp(S, R)`, false on `¬g`) governs postconditions of the form `POST(a★)` that mention what the operation produces; it does not govern a state predicate that a *pre-existing* tuple can already satisfy. A rejected `register_pred` call is a skip — PR0 says "no step, no tuple, no address," so `Σ' = Σ` — and a skip **preserves** any standing active registration.

Concrete counterexample, on a *registration-disciplined* derivation (so the scoping does not save the formula):
1. Register `r` (pdef deposit).
2. Register `a`, whose term references `r`; condition (iv) passes (`r` active). Now both active.
3. `Nullify_Binary` the `pdef` tuple at `r` — an `L_R`-growing step, not `L_pdef`-growing, hence disciplined. Per "Standard registrations," `r` leaves `A_pdef`; `a`'s tuple is untouched ("De-registration does not cascade"). Now `a` active, `r` inactive.
4. Call `register_pred(d, A_def)` for `a`'s run. `VALID` fails at **(iv)** (`r` not actively registered); the call is rejected, `Σ' = Σ`.

At Σ′ = Σ, `a`'s incumbent is still in `A_pdef`, so `POST-ref` holds — yet the formula evaluates `VALID ∧ (…) = false`. The formula is therefore not the weakest precondition; it is strictly too strong, excluding exactly the case `(a already actively registered) ∧ ¬VALID`. The flaw is general to any reference-bearing definition (and ASN-0130 is fundamentally about reference-bearing definitions); the reference-free `quiescent_v1/v2` of the worked example happen to be immune only because their `VALID` cannot fail on a hit.

**PR5a carries the identical defect** for `POST-cert`: a `Nullify_Binary` on `a`'s `pdef` tuple after certification leaves the `pd_stable` certificate active while CVALID condition (i) ("`a` actively registered") fails — a state the ASN *itself* flags in PR5a's closing parenthetical ("a later de-registration leaves the certificate active while the condition-(i) fact recedes into history"). Re-certification then rejects, but `POST-cert` holds, contradicting `CVALID ∧ (…)`.

**Required**: Lift the already-registered disjunct out from under `VALID`. The weakest precondition (for `A_def ≠ ∅`, `a = min(A_def)`) is

`wp ≡ (E (b, F', G') ∈ A_pdef^Σ :: addrs(F') = {a}) ∨ (VALID(Σ, A_def) ∧ d ∈ dom(Σ.M) ∧ C3(Σ, d))`

reducing to `(∃ active tuple denoting a) ∨ (VALID ∧ d ∈ dom(Σ.M))` on surface-disciplined derivations. The necessity sentence must subdivide the `VALID`-failing branch into "`a` already actively registered" (wp true) vs. not (wp false), rather than declaring `VALID`-failure uniformly wp-false. Apply the same correction to PR5a's `POST-cert` wp.

### Issue 2: PR-DISC carries a use-site inventory and a full seal preview that duplicates "Standard registrations"

**ASN-0130, PR-DISC**: 

> "This is the note's central scoping hypothesis: every claim below that consumes `sig`, validation permanence (PR1), or registration order (PR2) is stated on these derivations…"

and 

> "The entry-point seal (Standard registrations) makes the hypothesis a fact about the shipped surfaces rather than an assumption: the exposed `Emit_K` rejects every `pdef`- and `pd_stable`-class call, so `register_pred` and `certify_pd_stable` are the only routes into their slices…"

**Problem**: Two flagged anti-bloat patterns in one definition. (a) The scoping sentence is a *use-site inventory* — it enumerates downstream consumers ("every claim below that consumes `sig`, … (PR1), or … (PR2)") rather than advancing the definition. (b) The entry-point-seal sentence is a full preview of "Standard registrations," whose "Entry points — the seal" paragraph states the same fact again: "The seal is what makes the registration discipline (PR-DISC) a fact about the shipped surfaces rather than an assumption…". The two passages say the same thing in different words and defer to each other.

**Required**: PR-DISC needs only the definition of *registration-disciplined* plus a one-clause pointer that the seal (Standard registrations) discharges it. Drop the downstream-consumer enumeration; let the consuming claims cite PR-DISC where they consume it. State the seal once, in "Standard registrations."

### Issue 3: Defensive meta-prose around the encoding discipline

**ASN-0130, PR-ENC-uniq**: 

> "The argument consumes nothing but content: prefix-freeness quantifies over the encoding's parse-valid sequences, a set fixed by the discipline, so uniqueness — and with it everything identification and resolution consume — holds at every state, against every store."

**ASN-0130, PR-ENC**: 

> "the supply belongs to expansion (PR3), which needs a name source no author-written name can collide with."

**Problem**: The PR-ENC-uniq sentence is a defensive statement *about the argument* (what it "consumes," that it holds "at every state, against every store") plus a forward use-site claim ("with it everything identification and resolution consume") — the proof is complete in the preceding sentence. The PR-ENC clause justifies the reserved expansion-name supply by naming its downstream consumer (PR3) rather than stating the constraint. Both are meta-prose the precise reader skips past.

**Required**: Delete the PR-ENC-uniq robustness sentence (state-independence already follows from "properties of the value sequence alone"). In PR-ENC, keep the constraint ("no recorded parameter name and no body binder may inhabit the supply") and drop the PR3-consumer rationale.

## OUT_OF_SCOPE

### Topic 1: Signature compatibility across supersession
**Why out of scope**: PR4 versions definitions through the shipped `supersedes` relation with "no new machinery," but a consumer that follows `tip(a₁)` to a successor `a₂` and evaluates `a₂(args)` has no guarantee `sig(a₂)` is arity/sort-compatible with `sig(a₁)`. Constraining supersession successors to compatible signatures would be new machinery layered on `pdef`; it is a future certification/versioning ASN, not a defect here. (Adjacent to the note's own Open Question 3 on dangling references, but distinct.)

META: (none — the note specifies abstract state, operations, and invariants for a self-hosting definition layer, with the byte encoding deliberately left as a substrate parameter; it has not drifted into implementation mechanics.)

VERDICT: REVISE
