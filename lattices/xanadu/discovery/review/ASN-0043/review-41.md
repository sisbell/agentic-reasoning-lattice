# Review of ASN-0043

## REVISE

### Issue 1: L9 witness construction assumes content store finiteness without justification

**ASN-0043, L9 (TypeGhostPermission)**: "Choose a document prefix `d'` under which no address has been allocated — that is, no `b ∈ dom(Σ.C)` has `origin(b) = d'` and no `b ∈ dom(Σ.L)` has `home(b) = d'` (by L-fin, `dom(Σ.L)` is finite; by T0(a), node-field components are unbounded, so document prefixes exist beyond those occupied by any existing address)."

**Problem**: The parenthetical justification cites L-fin for link finiteness and T0(a) for unbounded prefixes, but the "no content under `d'`" requirement also needs `dom(Σ.C)` to occupy only finitely many document prefixes. ASN-0036 has no finiteness axiom for `dom(Σ.C)` — S8-fin constrains per-document arrangements, not the global content store. A conforming state satisfying S0–S3 could have an infinite `dom(Σ.C)` whose origins exhaust all document prefixes, making the fresh-prefix claim unjustified.

The requirement is also unnecessary. None of the L9 invariant verifications depend on `d'` being content-free: L0 holds by subspace separation (`s_L ≠ s_C`); L1a holds because `home(a) = d'` by construction; L11a holds because `a` is fresh in `dom(Σ.L)` (by L-fin), not because `d'` is globally fresh. The ghost address `g` is guaranteed outside `dom(Σ'.C) ∪ dom(Σ'.L)` by subspace separation alone (`s_X ≠ s_C, s_X ≠ s_L`), independent of prefix choice.

**Required**: Drop the "no `b ∈ dom(Σ.C)` has `origin(b) = d'`" constraint. Allocate `a` at any fresh address in any document's link subspace — freshness of the *address* is guaranteed by L-fin and T0(a) (infinitely many valid link addresses, finitely many occupied). The document prefix need not be globally fresh.

### Issue 2: L11b L1c verification references wrong allocation frontier

**ASN-0043, L11b (NonInjectivity)**: "L1c — `a'` is the next sibling of `a` via `inc(·, 0)`, conforming to T10a"

**Problem**: "The next sibling of `a` via `inc(·, 0)`" means `a' = inc(a, 0)`. But if other link addresses were allocated after `a` in the same allocator's sibling stream, `inc(a, 0)` is already in `dom(Σ.L)`. Consider a state `Σ` with links at `1.0.1.0.1.0.2.1` and `1.0.1.0.1.0.2.2`: if `a = 1.0.1.0.1.0.2.1`, then `inc(a, 0) = 1.0.1.0.1.0.2.2` is already occupied. This contradicts the freshness requirement `a' ∉ dom(Σ.L)`.

The proof body correctly says "allocate `a'` by forward allocation" (which means the allocator's next output from its current frontier), but the L1c verification line contradicts this by pinning `a'` to `inc(a, 0)` specifically.

**Required**: Replace "the next sibling of `a` via `inc(·, 0)`" with "the allocator's next sibling output via `inc(·, 0)` from its current frontier." The allocator that produced `a` has advanced to some frontier `a_{last} \geq a`; the next output is `inc(a_{last}, 0)$`, which is fresh by T9 (ForwardAllocation).

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage belongs in span algebra

PrefixSpanCoverage — "for any tumbler `x` with `#x ≥ 1`, `coverage({(x, δ(1, #x))}) = {t ∈ T : x ≼ t}`" — is a general property of spans and prefix containment. It has no dependency on link concepts; it follows entirely from T1, T12, OrdinalShift, and case analysis on tumbler depth. The result is used by L9, L10, and L13, but it is equally relevant to any future ASN that uses span queries over prefix-delimited subtrees.

**Why out of scope**: This is a tumbler/span algebra result, not a link ontology result. It should migrate to a span algebra or tumbler algebra foundation ASN so that future ASNs can cite it without depending on the link ontology.

VERDICT: REVISE
