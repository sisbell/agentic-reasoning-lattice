# Review of ASN-0115

## REVISE

### Issue 1: `act` and `deliver` are undefined when the named document is unallocated

**ASN-0115, "What a spec-set is"**: "`act(ρ, Σ) = dom(Σ.M(d)) ∩ ⟦σ⟧`"

**Problem**: The V-spec definition requires only that `d` be "a tumbler with `zeros(d) = 2`" whose span start is "a V-position of `d`." It never requires `d ∈ dom(Σ.M)`. But `dom(Σ.M(d))` presupposes the arrangement of `d` exists; for an unallocated document the arrangement is undefined, so `act`, `item`, `deliver₁`, and `deliver` (R0) are undefined on such inputs. The companion operation in the substrate, `project` (ASN-0098), explicitly carries the precondition "defined when `d ∈ dom(Σ.M)`." R6's note that "failure of an open-document precondition is a different matter" gestures at this but no precondition is ever stated.

**Required**: State `d ∈ dom(Σ.M)` as a precondition of a V-spec (or of R0), so the delivery object is well-defined over its declared domain. Distinguish this precondition from R6's unbound-position case, which is about absence of binding within an *existing* arrangement.

### Issue 2: R9 claims inline origin-traceability that R1 and the Open Questions contradict

**ASN-0115, R9**: "Each delivered content item retains a resolvable origin: the address it was drawn from determines `origin(a)` … so a fragment's provenance is never erased by its placement in the assembled stream."

**Problem**: R1 fixes that a content item carries `Σ.C(a)` — "the value, not the address `a`." If the address is not in the delivered item, then `origin(a)` is *not* recoverable from the delivered material; it is recoverable only from the resolution mapping, which is internal to the operation, not part of `deliver(R, Σ)`. R9 conflates "every item was drawn from an address with a definite origin" (true, the resolution is well-defined) with "the delivered item retains a resolvable origin" (the inline-provenance question). The first Open Question explicitly defers exactly this: "must a delivered fragment carry, within the delivered material itself, enough to ascertain its origin, or may origin be recoverable only by a separate query?" R9 silently answers a question the ASN declares open.

**Required**: Restate R9 so traceability is a property of the *resolution* (each active position has a determinate `origin(Σ.M(d)(v))`), not of the delivered stream — or, if R9 is meant to assert inline provenance, remove the contradicting Open Question and reconcile with R1.

### Issue 3: R10's lead-in asserts single-span subspace straddling that the claim and Open Questions defer

**ASN-0115, R10 lead-in**: "A span whose V-range straddles the boundary — or a spec-set with specs in both subspaces — gathers positions of both kinds."

**Problem**: The formal R10 claim commits only to "A spec-set spanning both subspaces … yields a heterogeneous delivery"; it does not establish that a *single* span can straddle. The final Open Question treats single-span straddling as unresolved: "What must delivery guarantee when a single span's denotation straddles the subspace boundary…?" So the prose presents as established fact something the claim does not cover and the Open Questions explicitly leave open. (For the ordinal/deepest-action-point spans this ASN emphasizes, a text-rooted span cannot even reach link positions: `s⊕ℓ` agrees with `s` on position 1 = `s_C`, so every `t < s⊕ℓ` has first component `s_C`, excluding `s_L` positions — making the lead-in's straddle case at best a non-ordinal corner the ASN does not analyze.)

**Required**: Confine the lead-in to the spec-set-with-mixed-specs case that R10 actually proves, and let single-span straddling remain solely an Open Question — or analyze it and promote it to a claim.

### Issue 4: R8(ii) "by reference" collides with R1's value-vs-reference item kinds

**ASN-0115, R8(ii)**: "the operation delivers them by reference to the shared address `a`"

**Problem**: R1 and the `item` definition reserve a *reference* payload (`⟨ref, a⟩`) for link positions, with content positions delivering a *value* (`⟨content, Σ.C(a)⟩`). R8(iii) confirms content delivery yields the value "once per V-position" — i.e. `Σ.C(a)` is delivered twice, not a single shared reference. R8(ii)'s "delivers them by reference to the shared address" therefore overloads "reference": it means *internal resolution dereferences the same address*, not that the payload is a reference. As written it reads as contradicting R1.

**Required**: Reword R8(ii) to say the two items are *resolved through* the one shared address `a` (identity-preserving co-resolution), reserving "reference" for the link-item payload kind.

## OUT_OF_SCOPE

(none — the deferred topics in the Open Questions are appropriately scoped; the issues above are about claims that contradict those deferrals, not about missing coverage.)

VERDICT: REVISE
