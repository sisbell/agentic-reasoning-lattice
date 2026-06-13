# Review of ASN-0125

This is a strong, largely sound note. The central reasoning — mutation is unimplementable (EL0), intent is invisible (EL1), so editing must be allocate-plus-assert with the assertion carried as a typed link-to-link tuple (EL2/EL3) — is rigorous, and the three-axis decomposition (EL9), the two-regime discovery split (EL11), and the set-valued currency query (EL14) are derived carefully and verified against the worked example. The math I could check holds. The findings below are refinements, not structural defects.

## REVISE

### Issue 1: EL6(v) asserts discipline preservation without the argument that EL-DM and EL12 rely on

**ASN-0125, EL6(v) (AssertionContract)**: "*(v) Discipline and permanence.* `Σ'` is edit-disciplined when `Σ` was; and at every `Σ' →* Σ''`, `e_b ∈ S^{Σ''}` with value fixed and `(y, x) ∈ succ_h(Σ'')` (EL5a)."

**Problem**: The permanence half cites EL5a; the discipline-preservation half has no derivation. Yet it is load-bearing: EL-DM's inductive step discharges the `assert_sup` case by citing it verbatim ("*`assert_sup`.* EL6(v): `Σ'` is edit-disciplined when `Σ` is."), and EL12's active-at-birth chaining for the second fork invocation depends on the intermediate state being disciplined. Meanwhile EL7(vi) proves the structurally identical — and strictly harder — `editlink` case in a full paragraph. A claim used as a lemma in two downstream proofs should be shown, especially when its sibling is shown.

**Required**: State the (short) argument: `assert_sup` emits one `[K_sup]` claim `(b, {(x,δ(1,#x))}, {(y,δ(1,#y))})` with `x ≠ y` (precondition) and `x, y ∈ dom(Σ.L) ⊆ dom(Σ'.L)`, conforming to Df-DISC(ii); it adds no `[R]` tuple, so clause (i) is untouched and no prior tuple's conformance is disturbed (L12) — hence `Σ'` is edit-disciplined.

### Issue 2: EL11(b) states a conditional equality unconditionally

**ASN-0125, EL11(b) (TwoRegimeDiscovery)**: "the claim sets `in(y, Σ) = {e ∈ Ŝ^Σ : old(e) = y}` and `out(x, Σ) = {e ∈ Ŝ^Σ : new(e) = x}` are computable from `Σ.L` alone — this is `Observe_{K_sup}` at pattern `Ĝ = {y}` (resp. `F̂ = {x}`), view `hist`, filtered by the decidable schema-conformance predicate"

**Problem**: `Observe_{K_sup}(Σ, ∅, {y}, hist)` returns `{(a,F,G) ∈ L_{K_sup}^Σ : {y} ⊆ coverage(G)}`; on schema-conforming claims `coverage(G) = {t : old(e) ≼ t}`, so the filtered result is `{e ∈ Ŝ^Σ : old(e) ≼ y}`. This equals `in(y, Σ) = {e : old(e) = y}` only via the antichain collapse `old(e) ≼ y ⟺ old(e) = y`, which holds (R0a) only when `y ∈ dom(Σ.L)`. For `y ∉ dom(Σ.L)`, a claim with `old(e) ≺ y` (some proper extension `y`) is returned by `Observe` but is not a member of `in(y, Σ)`, so the stated identity is false. The direct comprehension `in(y, Σ)` is computable for any `y`; it is the `Observe` *identification* that is conditional. (All actual uses — `in(a,·)`, `in(aᵢ,·)`, `in(ℓ₀,·)` — supply `y ∈ dom(Σ.L)`, so nothing downstream breaks; the equality claim is merely stated too strongly.)

**Required**: Qualify the identification with `y, x ∈ dom(Σ.L)` and note the antichain step that collapses `≼` to `=`, or drop the `Observe` identity and rest the computability claim on the direct comprehension.

### Issue 3: EL-DM's statement and its Df-DISC lead-in carry use-site inventory and meta-prose around a forward reference

**ASN-0125, EL-DM and the Df-DISC closing paragraph**: Df-DISC ends "we owe a demonstration that disciplined states are reachable and closed under editing, so that the 'at disciplined `Σ`' conditionals below range over something the system can actually produce. We assemble it into an inductive invariant of a named layer." EL-DM's statement then reads "so the conditional claims that follow (EL6(iii), EL7(iii), the EL7(iv) full frame, EL14's active-at-birth, and EL8's disciplined-state hypothesis) are evaluated over a reachable, non-vacuous domain, not an assumed one. (EL11's contextual half rests instead on per-claim schema-conformance, which EL4 supplies without a whole-state hypothesis; ... so it applies there too.)"

**Problem**: EL-DM's content is "every editing-layer-reachable state is edit-disciplined," plus its base/step proof. The parenthetical enumerating five downstream consumers — and the further parenthetical carving out where EL-DM is *not* needed — is a use-site inventory that does not advance the claim; the Df-DISC sentences ("we owe a demonstration… We assemble it…") are roadmap meta-prose. This is exactly the "definition's introduction enumerates downstream consumers" / meta-prose-around-forward-reference pattern the anti-bloat classifier flags.

**Required**: State EL-DM plainly with its proof. If non-vacuity must be noted, say it once and briefly; drop the five-site enumeration and the "we owe a demonstration" framing.

### Issue 4: The "menu was shorter than it looked" remark restates eliminations already established in EL2 and EL3

**ASN-0125, "two remarks" following EL3**: "The value space fails RQ1, RQ2, RQ4, and RQ7 … The address space fails RQ1 and RQ2 … fails RQ4 absolutely … and fails RQ6 …"

**Problem**: The value-as-slot carrier was already eliminated at EL2(b) and reused at EL3 ("a link *other than the successor* … since the successor's slots close at its birth (EL2(b))"); the address-nesting carrier was already eliminated at EL2(c); and EL3's claims-table row compresses both as "content-encoded, slot-at-birth, and address-form carriers each violate named RQs." The remark re-derives both in expanded RQ-by-RQ form — two passages saying the same thing. The remark's genuinely new content is the *collapse* observation ("'A separate supersession link' and 'a typed relation distinct from these' are the same architecture"); that part is non-redundant and worth keeping.

**Required**: Keep the architecture-collapse insight (and the Nelson framing on version numbers); replace the re-enumeration of value-space and address-space RQ violations with a back-reference to EL2(b)/(c) and EL3, so the elimination is stated in one place.

## OUT_OF_SCOPE

None. The eight Open Questions correctly defer future territory (cross-asserter retraction authority, meta-claims targeting claims, span-level endset correspondence, edit↔listing coupling, subtype-family observation closure), and no claim in the body strays into adjudication mechanics, link discovery, or the other scoped-out operations — EL14(d) explicitly leaves adjudication to the reader rather than defining a selector.

VERDICT: REVISE
