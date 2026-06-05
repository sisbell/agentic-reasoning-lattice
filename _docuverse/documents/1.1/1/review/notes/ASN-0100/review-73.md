# Review of ASN-0100

This is a thorough, largely sound specification. The three-effect decomposition, the substrate composite realization, the invariant verification, the worked examples, and the two-case wp analysis are all present and mostly rigorous. My findings are concentrated in redundancy/scope, consistent with the anti-bloat classifier on this note. I found no correctness hole in the core proofs.

## REVISE

### Issue 1: The K.μ⁻-omission condition is restated in four places
**ASN-0100, multiple sections**: The condition "K.μ⁻ fires iff Right ≠ ∅; omitted in the append (`p_m = N+1`) and empty (`V_{s_C}(d) = ∅`) cases" is stated as (INS.μ⁻-fires) in the Substrate Decomposition (step 2), re-explained in the projection derivation ("When K.μ⁻ does not fire…"), re-explained again in §Position Constraints (the `j = N` and empty bullets: "K.μ⁻ is *omitted*"), and again in the empty-document worked example.
**Problem**: A reader following the composite structure rereads the same omission mechanics each time. The projection-derivation paragraph and the Position-Constraints bullets add nothing to (INS.μ⁻-fires) beyond restatement.
**Required**: State the omission condition once at (INS.μ⁻-fires) and have the later sections reference it rather than re-derive it.

### Issue 2: §Position Constraints duplicates composite mechanics already established
**ASN-0100, §Position Constraints**: The per-case bullets ("Left is empty (no `v < p`); the entire pre-state text subspace shifts by `n`. K.μ⁻ … shrinks `V_{s_C}(d)` to `∅`…"; "K.μ⁺ adds only the Insertion positions at the high end…") restate Effect Three and the Substrate Decomposition.
**Problem**: The genuinely new content of this section — the binary vs. ternary predicate distinction and the depth-parameter binding (`m := #p`, lower-bounded only by `#p ≥ 2`) — is buried among restated composite mechanics. The composite behavior per case is meta-prose here; it advances no claim not already carried by Effect Three, (INS.μ⁻-fires), and the worked examples.
**Required**: Keep the predicate/depth-parameter distinction; remove the per-case K.μ⁻/K.μ⁺ region descriptions that duplicate earlier sections.

### Issue 3: COPY mechanics described in an out-of-scope comparison
**ASN-0100, §INSERT vs. COPY**: "By contrast, COPY creates V→I mappings to *existing* I-addresses without allocating new content — the defining structural difference being that INSERT allocates fresh I-addresses while COPY does not."
**Problem**: COPY mechanics are explicitly out of scope. The substance needed to fix INSERT's identity character is INS.identity alone (each `a_k` fresh, `origin(a_k) = d`); the COPY description and the "two users insert 'the'" essay paragraph are contrastive motivation that describes an out-of-scope operation.
**Required**: Reduce to a one-line statement that INSERT allocates fresh addresses (INS.identity); drop the description of COPY's V→I mechanics.

## OUT_OF_SCOPE

### Topic 1: INS.identity.version (claim in the table)
**Why out of scope**: This claim is framed around version-chain independence (`d_v = inc(d_src, 1)`, "origin = d_v ≠ origin of d_v's source document"). Version creation is out of scope per the scope list. The in-scope content — INSERT on any document allocates with `origin =` that document — is already INS.identity; the version-relative framing adds only out-of-scope version semantics. Either drop INS.identity.version or fold its non-version content into INS.identity.

### Topic 2: Link-subspace insertion (correctly deferred)
**Why out of scope**: The ASN explicitly bounds itself to the content subspace and defers `K.μ⁺_L`/`K.λ` insertion to a future note. No action needed; noting that the deferral is appropriate.

VERDICT: REVISE
