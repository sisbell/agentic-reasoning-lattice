# Review of ASN-0036

## REVISE

### Issue 1: S2 introduced purely as a citable restatement of the type declaration

**ASN-0036, S2 (Arrangement functionality)**: "The single-valuedness already carried by the `Σ.M(d) : T ⇀ T` partial-function declaration, named here for citation in the S8 proof — each V-position maps to exactly one I-address"

**Problem**: The prose admits S2 adds no content — single-valuedness is definitionally carried by `⇀`. The clause "named here for citation in the S8 proof" is a use-site justification (the flagged anti-bloat pattern: a property's introduction enumerating its downstream consumer rather than advancing meaning). Naming the consumer is bookkeeping, not reasoning.

**Required**: State S2 as what it says ("each V-position maps to exactly one I-address, by the `⇀` declaration") and drop the "named here for citation in the S8 proof" clause. The S8 proof can cite S2 without S2 announcing that it will be cited.

### Issue 2: S8a is a duplicate of the domain-restriction axiom, flagged as such in its own prose

**ASN-0036, S8a**: "The domain-restriction axiom on `Σ.M(d)`, restated per-component for citation — `zeros(v) = 0` holds exactly when every component is positive (T0)"

**Problem**: S8a is by its own admission a per-component restatement of the already-stated `dom(Σ.M(d)) ⊆ {t : zeros(t) = 0 ∧ #t ≥ 2}` axiom — two statements of the same fact in different words (flagged pattern: "two paragraphs in the same document say the same thing"). "restated per-component for citation" is the same use-site meta-prose as Issue 1.

**Required**: Either fold the per-component form into the domain-restriction axiom as its postcondition, or keep S8a but strike "restated per-component for citation" and the redundant restatement framing. State the equivalence to `zeros(v)=0` once.

### Issue 3: S8 Case j = m re-derives a foundation result inline that its own Depends already packages

**ASN-0036, S8 proof, within-subspace lemma, Case j = m**: "NAT-discrete and NAT-order (ASN-0034) together promote the strict inequality `v_m < t_m` to `v_m + 1 ≤ t_m`: the contrary assumption `¬(v_m + 1 ≤ t_m)` gives `t_m < v_m + 1` by NAT-order trichotomy … whence NAT-discrete … forces `t_m = v_m`, contradicting `v_m < t_m` …"

**Problem**: The S8 Depends list already names this exact step as a packaged consequence ("NAT-discrete — the strict-to-`+1` promotion `m < n ⟹ m + 1 ≤ n`"). Deriving the promotion in full inline AND listing it as a single named dependency is duplication. The full contrapositive expansion is noise the reader must work around to follow the contradiction.

**Required**: Collapse to one. Cite the promotion `v_m < t_m ⟹ v_m + 1 ≤ t_m` as the named NAT-discrete step, or stop listing it as a packaged dependency — not both.

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG/D-MIN/S2 under INSERT/DELETE/COPY/REARRANGE

**Why out of scope**: The ASN's scope statement explicitly defers operation frame/postconditions to future ASNs, and the Open Questions correctly route the contiguity-preservation obligation there. Not an error in this ASN.

### Topic 2: Canonical choice of V-position depth `m`, subspace-alignment enforcement, and `Val` type structure

**Why out of scope**: These are surfaced as Open Questions, not asserted claims. They are genuinely new territory (allocation conventions, value-domain typing) belonging to operation-layer and content-model ASNs.

VERDICT: REVISE
