# Claim Convergence

Discovery finds the claims of a system. Note decomposition makes them individually addressable. Claim convergence makes them true.

A lattice contains candidate claims, but they carry contradictions, imprecisions, and unstated assumptions. Claims that were independently reasonable turn out to conflict when forced to coexist in a single formal system. Edge cases that narrative reasoning glossed over become unavoidable when every claim must be proven exhaustively. Claim convergence is where this resolution happens.

## Where claim convergence begins

Discovery produces claims independently. Each claim is reasonable in isolation. But claims must work together as a system, and that's where contradictions appear. Two claims may each be correct on their own but impose conflicting constraints on a shared concept. A definition that works for simple cases may fail when an edge case exercises it under conditions another claim guarantees. Informal reasoning tolerates vagueness in precisely the places where the interesting constraints live.

These contradictions are the raw material. By demanding precision — exact preconditions, exhaustive case coverage, explicit dependencies — claim convergence resolves them and surfaces structure that was hidden in the vagueness.

Note decomposition delivers per-claim files whose structural form satisfies the [Claim File Contract](design-notes/claim-file-contract.md) — one body per file, references resolve, metadata agrees with content. The semantic content is deliberately incomplete: type classifications are best-effort, dependencies may be imprecise, proofs may have gaps. Claim convergence tightens all of it. But it operates on structurally valid state from the start — the [Validation Principle](principles/validation.md) guarantees this.

## Reasoning, not polish

Claim convergence is not cleanup. It is discovery under a precision constraint. Discovery reasons at note scale — a 5000-word document with 40 claims, broad context, the full generative substrate active. Claim convergence reasons at claim scale — one claim, its specific dependencies, nothing else. The narrow focus surfaces findings that are invisible at note scale.

A reviewer reading one claim with its cited foundations sees "you used cardinality without a cardinality axiom in scope." That finding is invisible in a 40-claim document where the reviewer is tracking everything at once. Scope narrowing — the representation change from one file to many — is itself epistemically productive. The split doesn't just organize content for verification. It creates the conditions under which per-claim scrutiny can happen at all.

The empirical evidence supports this. Across hundreds of review cycles, the majority of findings are substantive — missing axioms, broken precondition chains, ungrounded operators, false claims corrected. New axioms surface that the discovery pass missed. These are reasoning contributions, not tightening. The substantive yield continues into later cycles, not just cycles one and two.

From the Xanadu domain: ASN-0034's GlobalUniqueness theorem illustrates this. Discovery stated the claim simply: no two distinct allocations produce the same address. The convergence process demanded an exhaustive proof and revealed that a 40-year-old addressing scheme achieves coordination-free uniqueness through structural length separation — a claim its designer never articulated. The proof also showed that the allocator discipline constraint is necessary: without it, uniqueness fails. Later, review at wider scope found a counterexample that mechanical verification (Dafny), bounded model checking (Alloy), and 30+ single-scope review cycles all missed — the allocator axiom permitted duplicate child-spawning. The fix cascaded through the lattice and 4 dependent claims re-verified automatically.

From the materials domain: ASN-0002's review cycle caught a genuine physics insight — a central potential U(r) depending only on centre-of-mass separation cannot couple to internal degrees of freedom, leaving β>1 internal-translational exchange without a per-encounter mechanism. The reviewer derived this from the note's own stated premises. That is reasoning produced by the precision demand, not by discovery's generative process.

## The quality boundary

Three principles govern whether the [claim convergence protocol](protocols/claim-convergence-protocol.md) converges or spirals. See the [principles README](principles/README.md) for the full account.

**[Coupling](principles/coupling.md)** monitors content balance. Per-claim files hold at roughly 70/30 prose-to-formal. Divergence signals sprawl — prose growing without corresponding formal content, or formal contracts absorbing essay content.

**[Validation](principles/validation.md)** enforces structural integrity. A [validate-before-review](patterns/validate-before-review.md) pass runs before each review cycle: the mechanical validator checks the [Claim File Contract](design-notes/claim-file-contract.md), and per-invariant fix recipes resolve any violations. The reviewer then sees structurally sound state. Three-quarters of typical non-convergence findings are structural violations a validator catches in one pass — duplicate declarations, dangling references, metadata disagreement, dependency cycles. Getting these out of the reviewer's path is what makes semantic review possible.

**[Voice](principles/voice.md)** shapes what the reviser writes. The same Dijkstra voice that governed discovery governs claim convergence — prose with embedded formalism, every statement justified in the sentence that introduces it, named invariants, frame conditions, no big blocks of notation without reasoning. The voice was the starting condition in discovery and it works here for the same reason: positive style structure leaves no slot for non-reasoning prose. Enumerated prohibition lists ("delete > restructure > add") were tried and failed — they produced over-deletion of load-bearing content and still missed drift vectors. The voice discipline replaced them.

## Finding classification

The reviewer classifies each finding as `comment.revise` or `comment.observe`. Correctness issues — broken precondition chains, missing axioms, ungrounded operators, hand-waved proofs, missing edge cases — are `comment.revise` and require resolution. Tightening observations — loose phrasing, minor style, alternative framings — are `comment.observe` and do not trigger revision.

OBSERVE is the off-ramp for the [production drive](design-notes/production-drive.md). Without it, every observation becomes a mandatory revision and the protocol over-revises. With it, the convergence predicate tracks only REVISE comments. Convergence means every `comment.revise` has a `resolution` — not zero findings of any kind. The first is reachable because correctness issues are exhaustible. The second is unreachable because no prose is perfect under infinite scrutiny.

## Reasoning that improves itself

Discovery connects — it finds claims, links them, grows the lattice outward. Claim convergence constructs — it builds from the bottom up, each piece locked into place before the next goes on. Each claim converged adds a piece to the structure, and that piece constrains what the remaining pieces can be. A tightened precondition in one cycle enables the next cycle's reviewer to see implications the previous version didn't have. A resolved contradiction between two claims reveals a relationship that only becomes visible once both are precise. The degrees of freedom shrink. The system takes shape.

Each cycle builds on the previous. A reviewer tightens a contract. The next reviewer sees that the tightened contract now implies something new. A reviewer at wider scope sees a relationship between two claims that only became visible because both were strengthened in the previous cycle. The reasoning compounds — each claim converged makes the next one more precise, because the contracts it produces become the premises its dependents reason from.

Each contradiction resolved tightens the specification and often reveals a deeper principle that unifies what seemed like separate concerns. The resolution process is where domain-specific reasoning dissolves into general mathematics. In the Xanadu domain, the content architecture's two-stream separation became an instance of correspondence decomposition; tumbler arithmetic became sequence arithmetic over ordered finite sequences. The domain terms fell away and the mathematics stood on its own. The lattice organized the work. Claim convergence revealed that the work was more general than the domain that motivated it.

## Convergence radiates through the lattice

![Convergence radiation](diagrams/claim-convergence-radiation.svg)

Converging a foundation note's claims changes everything above it. When a foundation's claims gain precise contracts — exact preconditions, exact postconditions, exact constraints — the discovery notes that depend on it see those contracts. Their reasoning becomes more rigorous because their premises are more rigorous. Claims that were invisible under informal foundations become visible under formal ones.

This is more than quality improvement. Discovery notes find new things after their foundations converge. In the Xanadu domain, a discovery note derived a new claim from freshly converged foundation contracts. The evidence channel verified whether the claim held empirically against the implementation. It did. A claim that didn't exist before convergence, validated against evidence that had existed for 40 years without anyone having formalized the relationship.

Claim convergence doesn't just verify what discovery found. It creates the conditions for discovery to find more.