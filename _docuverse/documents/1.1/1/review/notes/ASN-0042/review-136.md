# Review of ASN-0042

## REVISE

### Issue 1: Duplicated forward-deferral to the same downstream proof
**ASN-0042, "Ownership as a Structural Predicate" (O1b) and "The Account-Level Boundary"**:
- O1b: "It is proved by the shared induction in *State Axioms* (*Shared invariant induction*), jointly with O1a and T4-validity."
- Account-Level Boundary: "O1a, O1b (PrefixInjectivity), and T4-validity of prefixes are reachable-state invariants, proved in *State Axioms* under *Shared invariant induction*, where the joint conclusion for `ω` (O2) is stated."

**Problem**: Two paragraphs in different sections defer to the same downstream location (the *Shared invariant induction*) for the same three invariants. The second pointer carries no information the first does not, and the reader who has already seen the O1b deferral must re-read an equivalent restatement at the head of Account-Level Boundary. This is exactly the forward-reference accretion the anti-bloat classifier targets: a use-site/deferral note duplicated across sections.

**Required**: State the forward pointer to *Shared invariant induction* once (at the first claim that needs it) and delete the restatement. Each subsequent invariant can name *Shared invariant induction* in its own one-line status (as the summary table already does) without re-narrating that all three are jointly proved there.

### Issue 2: Use-site inventory and downstream-consumer enumeration in proof/summary slots
**ASN-0042, "State Axioms" (Shared invariant induction) and "Properties Introduced" (RegistryReachability row)**:
- Shared invariant induction closing line: "Together they ensure `ω` (O2) yields a unique principal at a valid hierarchy level with `fields(·)` well-defined (T4b UniqueParse)."
- RegistryReachability row: "discharges the `next`/`hwm`/B1/B6 preconditions wherever they are invoked".

**Problem**: Neither phrase advances the claim it sits on. The induction's conclusion is "every principal in every reachable state satisfies all three invariants"; the trailing sentence then enumerates a downstream consumer (`ω`) rather than completing the induction — meta-prose appended to a proof. The RegistryReachability "wherever they are invoked" is a use-site inventory standing in for the lemma's actual content (which is the registry-reachability invariant itself). Both are the "definition/lemma enumerates its consumers" pattern.

**Required**: End the *Shared invariant induction* at its actual conclusion (all three invariants hold) without the `ω`-consumer coda. Restate the RegistryReachability row in terms of what it guarantees (reachable registry ⇒ B₀-conformant), dropping "wherever they are invoked"; consumers cite it where they use it.

### Issue 3: Derived consequence embedded in the O17b axiom statement
**ASN-0042, O17b (BaptismalRegistryCoupling)**: "Composing this principal-introduction clause with the general baptism branch determines `pfx(π') = next(Σ.B, p, d)` for some B6-valid `(p, d)` — the next-reachable form."

**Problem**: O17b is labeled an axiom (coupling). This trailing sentence is not part of what the axiom *asserts*; it is a derivation ("composing ... determines ...") carried inside the axiom's prose. The same "next-reachable form" is then re-derived/re-cited at O7(c), O10, and the worked example, so the axiom slot is doing derivation work that belongs in a derived lemma. New prose around an axiom should say what the axiom states, not chain its consequences.

**Required**: Keep O17b to its two asserted clauses (general baptism branch; principal-introduction baptizes `pfx(π')`). Move the "`pfx(π') = next(Σ.B, p, d)`, next-reachable form" composition into a one-line derived corollary (or fold it into O18, which already handles the freshness half), and have O7(c)/O10 cite that corollary.

## OUT_OF_SCOPE

### Topic 1: Existence/density of admissible delegate prefixes
The O7(c) "may delegate" right and the question of whether an admissible fresh `p''` always exists is adequately witnessed by the worked-example "Unbounded recursion of delegation" construction; a general density guarantee (Open Question 4) is correctly deferred to a future ASN, not an error here.

VERDICT: REVISE
