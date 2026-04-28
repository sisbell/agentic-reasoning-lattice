# Verify the Whole

## Pattern

After narrowing scope and hardening each piece independently, step back to the original width and check that the pieces cohere. The individual pieces may each be correct in isolation but inconsistent with each other — shared definitions used differently, dependency chains with gaps, scope claims that exceed what the proofs establish.

Verification at the whole is not the same as the original broad investigation. Discovery produces the work. Verification checks the hardened work. The content is different — it's been through [scope narrowing](scope-narrowing.md) and [review/revise iteration](review-revise-iteration.md). What you're checking is whether the narrowing preserved coherence.

## Forces

- **Narrowing creates seams.** Breaking a document into 29 claims creates 29 boundaries. Each boundary is a potential inconsistency — a definition used differently on either side, a dependency assumed but not declared, a notation that shifted meaning.
- **Local correctness does not imply global correctness.** Each claim's proof may be sound. Each contract may match its proof. But the claims together may be inconsistent — S8's proof uses D-CTG without declaring it, S5's narrative claims more than its proof establishes.
- **The whole reveals what the parts hide.** Cross-claim issues are invisible at narrow scope. They only become visible when you see multiple claims together — the shared definitions, the dependency chains, the implicit assumptions that cross boundaries.
- **Verification is cheaper than discovery.** The work is already hardened. You're not producing new content — you're checking consistency. The findings are specific: "S8 uses D-CTG but doesn't declare it" rather than "the arrangement model needs work."

## Structure

```
hardened pieces ──→ assemble at original width ──→ review for coherence
                                                      │
                                           findings ──→ fix ──→ re-verify
                                                      │
                                           none ──→ coherent
```

The verification uses the same [review/revise iteration](review-revise-iteration.md) pattern but at wider scope. The reviewer sees all the pieces together. The findings target the seams between pieces, not the pieces themselves.

## When it finds something

Verification findings fall into categories:

- **Undeclared dependencies** — a claim uses another without declaring the relationship
- **Contract mismatches** — a contract claims something the proof doesn't establish (or vice versa)
- **Scope mismatches** — narrative claims exceed what the formal proof covers
- **Shared definition drift** — the same term used with subtly different meanings across claims
- **Missing bridging claims** — two claims that should connect but nothing formally links them

Each finding goes back through scope narrowing — fix it at the narrowest scope that can see the problem.

## Applications

### In discovery

The synthesis agent reads all authority responses and assembles a note. Before it's done, it verifies the whole: do the theory findings and evidence findings cohere? Are there contradictions? The synthesis step IS the verification — it checks that the narrowed inquiries (scoped to each authority) produced a consistent whole.

**What it catches**: theory says "immutable content store" but evidence shows "editing commands modify content." The contradiction becomes a finding — S0 (content immutability) is about existing content, not about the content store as a whole. New content can be added; existing content cannot be changed. The whole-verification caught an apparent contradiction that neither authority would flag in isolation.

### In claim convergence

Comprehensive-scope review reads the entire assembled note and checks that the hardened claims cohere. Each claim was reviewed and revised at narrower scope. Comprehensive-scope review verifies at note scope.

**What it catches**: S8's proof uses D-CTG for contiguous range structure but never declares the dependency. At narrow scope, S8's proof looks fine — D-CTG is just something it references. At comprehensive scope, the missing dependency is visible because the reviewer can see both S8 and D-CTG and notice the undeclared relationship.

### In cone-scoped review

Cone-scoped review is verify-the-whole at cluster scope. The cluster's claims have been hardened individually. Cone-scoped review assembles them and checks coherence — but only within the cone, not the full note.

**What it catches**: S4's contract omits T3 as a precondition. At narrow scope, S4 looks fine. At S7's cone scope, the reviewer sees that S7 depends on S4 providing T3-based guarantees, but S4's contract doesn't promise them. The seam between S4 and S7 is only visible when both are in context.

### In extract/absorb

When a shared concept is extracted into a foundation layer, every consuming document now depends on the extracted version instead of its own copy. The extraction isn't just mechanical replacement — the consuming documents must be verified against the shared definition. Did the extraction change the meaning? Do the proofs still hold? Do the dependency chains still resolve?

**What it catches**: two notes defined "tumbler arithmetic" slightly differently. Extracting it into a shared foundation forces one definition. Verify the whole checks that both notes still cohere with the shared version — the one whose definition shifted may need proof adjustments.

### Between notes

When claim convergence on one note discovers something that affects another (a scope promotion finding), the lattice as a whole needs verification. Does the new node cohere with its neighbors? Do the dependency declarations match? This is verify-the-whole at lattice scope — the broadest verification in the system.

## Pair with scope narrowing

Scope narrowing and verify the whole always appear together. Every narrowing step needs a corresponding verification at the original width:

- Discovery narrows via scoped inquiry → synthesis verifies the whole consultation
- Claim derivation narrows into claims → the [claim convergence protocol](../protocols/claim-convergence-protocol.md) reviews at progressively wider scope, with comprehensive-scope review verifying the whole note
- Cone-scoped review narrows to a cluster → re-verifies the cluster's coherence
- Extract/absorb narrows a shared concept into one definition → verify consuming documents still cohere

Narrowing without verification produces pieces that don't fit. Verification without narrowing has nothing hardened to check. The pair is the fundamental rhythm of the system: narrow, harden, step back, check.

## Origin

Verify the whole was present before scope narrowing was named. Comprehensive-scope review existed from the first claim convergence runs — it was always clear that per-claim review couldn't catch everything. The pattern was recognized when the same structure appeared at every scale: synthesis in discovery (verify the consultation), comprehensive-scope review in claim convergence (verify the note), cone-scoped review (verify the cluster). The same check, at different widths, for the same reason — narrowing creates seams, verification finds them.