# Review of ASN-0115

I worked through the definitions and every proof. The construction is sound: the Confinement lemma is correctly proved via T5 and correctly scoped (`m ≥ 2` from the V-position start constraint); the `act` override and its deep/shallow case split are right; R6's terminal-overrun argument, R7's active-set-agreement argument (including the load-bearing comparability requirement, which is genuinely necessary — divergent branches can allocate the same address with different values), and R8's content/link case split all check out. The worked instances verify against the claims. Two issues remain.

## REVISE

### Issue 1: R11's "weakest precondition" postcondition is not pinned down, so the stated condition is not actually the weakest

**ASN-0115, R11 (wp paragraph)**: "The weakest precondition for delivery to include the value at `a` is therefore a *single* live condition: (i) the consulted arrangement binds some *active* content position to `a` — a `v ∈ act(ρ, Σ)` with `subspace(v) = s_C` and `Σ.M(d)(v) = a`."

**Problem**: This ASN draws the value/address distinction sharply and repeatedly — R1 ("not a description of where that value is stored"), and especially R8 ("byte-indistinguishable from the delivery of two coincidentally-equal contents at distinct addresses (S4)... discloses nothing about the shared origin"). Under the literal reading of the stated postcondition — *the value `Σ.C(a)` appears in the output* — condition (i) is sufficient but **not necessary**: S4 (OriginBasedIdentity) permits a distinct `a' ≠ a` with `Σ.C(a') = Σ.C(a)`, and an active position resolving to `a'` puts the value `Σ.C(a)` in the output while (i) is false. So (i) is *not* the weakest precondition for value-appearance. The claim is correct only under the reading "delivery includes an item *resolved from* `a`" — which the phrase "include the value at `a`" does not state. A spec that insists elsewhere you cannot recover the source address from a delivered value cannot then phrase a *weakest-precondition* claim as "include the value at `a`" as though that pins the address.

**Required**: Pin the wp's postcondition to "delivery includes an item *resolved from* `a`" (i.e. sourced from address `a`); then (i) is genuinely necessary-and-sufficient. Alternatively, if the intended postcondition really is value-appearance, downgrade "weakest precondition" to "a sufficient precondition" and note that S4 blocks necessity. As written, the wording is in tension with R1/R8.

### Issue 2 (anti-bloat): proof-commentary asides that restate the claim's own scoping or comment on difficulty

**ASN-0115, R6 (proof body)**: "...so a named position of depth `> m_S` is simply absent from `dom(Σ.M(d))` and dropped from `act` — **no claim about its T1-position relative to the active range is needed or made**." This trailing clause restates, inside the proof, the scope disclaimer the R6 box already carries ("The no-interior-hole guarantee is a claim about the bindable slice, not about every named tumbler in the interval"). The substantive step — deeper named positions are unbound by S8-depth, hence dropped — stands without the disclaimer; the disclaimer is duplicative meta-prose.

**ASN-0115, R7 (proof opening)**: "We first show the active sets agree... **— non-trivial because `act`'s depth-compatibility branch reads the whole subspace state of `dⱼ`, not just the restriction to `⟦σⱼ⟧` the hypothesis equates**." This comments on the proof's difficulty rather than advancing it.

**Problem**: Per this note's anti-bloat mandate, these are sentences the precise reader skips past — they describe what the proof does or does not assert rather than asserting it. They compound across cycles.

**Required**: Drop the "no claim about its T1-position..." clause (the box disclaimer already scopes the guarantee) and the "— non-trivial because..." aside (let the subsequent derivation carry the weight). Where a positive distinction is genuinely useful, e.g. R6's "We pin the shape of that slice by the Confinement lemma, *not* by D-SEQ★...", keep the lemma application but state it positively ("By Confinement, every depth-`m_S` member of `⟦σ⟧` agrees with `s` on positions `1..m_S−1`") without the defensive "*not* by D-SEQ★" framing.

## OUT_OF_SCOPE

### Topic 1: boundary-crossing (subspace-straddling) spans
The ordinal-level requirement on every V-spec excludes a single span whose denotation crosses from `s_C` into `s_L` (the `s = [1,5], ℓ = [2,0]` example is correct). The ASN's Open Questions already defer this, and the deferral is correct — designating both subspaces is achieved by composing per-subspace ordinal specs, not by one straddling span.

### Topic 2: inline provenance and channel faithfulness
R2's frame limit (faithfulness of denotation, not of any transmission medium) and R9's kind-asymmetry (content origin recoverable only through the resolution mapping, not the output) raise the question of whether delivered material should carry inline provenance. Correctly left to a future ASN; not an error here.

VERDICT: REVISE
