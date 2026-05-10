# Review of ASN-0042

## REVISE

### Issue 1: O6 proof — biconditional asserted without showing the reverse direction
**ASN-0042, Structural Provenance**: "Hence pfx(π) ≼ acct(a), and pfx(π) ≼ a iff pfx(π) ≼ b whenever acct(a) = acct(b). The set of covering principals — and thus the longest match — is identical."
**Problem**: The proof establishes the forward direction: pfx(π) ≼ a ⟹ pfx(π) ≼ acct(a) (the prefix's components are confined to node/user fields, which acct captures). It then asserts the biconditional pfx(π) ≼ a ⟺ pfx(π) ≼ acct(a) in a single "and," without showing the reverse. The reverse direction — pfx(π) ≼ acct(a) ⟹ pfx(π) ≼ a — requires a property that is never stated: **acct(a) ≼ a** (the account field is a prefix of the address). This follows from acct being defined as a truncation of leading fields, but the property is used without being named. The proof then silently applies prefix transitivity (pfx(π) ≼ acct(a) ≼ a) to close the reverse direction.

The chain the proof needs is: pfx(π) ≼ a ⟺ pfx(π) ≼ acct(a) (by the node/user confinement argument and acct ≼ identity), then acct(a) = acct(b) gives pfx(π) ≼ acct(b) ⟺ pfx(π) ≼ b. The forward half is shown; the reverse half and the connecting step are asserted.

**Required**: (i) State acct(a) ≼ a as a named property or lemma — it follows directly from the definition (acct extracts the leading N.0.U portion), but it is load-bearing for the proof and should be explicit. (ii) Show the reverse direction: pfx(π) ≼ acct(a) implies pfx(π) ≼ a by transitivity of ≼ through acct(a) ≼ a. (iii) State the biconditional as a conclusion, not an assertion.

### Issue 2: O2 well-definedness — existence of maximum in covering set
**ASN-0042, The Exclusivity Invariant**: "Therefore the set of covering prefixes is totally ordered by ≼, and the longest prefix is unique"
**Problem**: A totally ordered set has a maximum only if it is finite (or satisfies a compactness condition). The proof establishes total ordering of the covering prefixes but does not establish that a maximum exists. The covering set is finite — any prefix p ≼ a is uniquely determined by its length (p = [a₁, …, a_{#p}]), there are at most #a possible lengths, and by O1b each prefix is held by at most one principal — but this finiteness argument is not stated. "The longest prefix" presumes existence.
**Required**: One sentence establishing finiteness: each prefix of a is determined by its length (#a possible values), so the covering set has at most #a elements, and its maximum under ≼ exists.

### Issue 3: O10 — property statement makes unformalizable claim
**ASN-0042, The Fork as Ownership Boundary**: "the system provides an alternative: π may create a new address a' within dom(π) that structurally relates to a"
**Problem**: The phrase "structurally relates to a" is not captured by any of the formal conditions (a)–(c). Condition (a) says ω(a') = π. Condition (b) says pfx(π) ≼ acct(a'). Condition (c) says a is unchanged. None specify a relationship between a and a'. The ASN itself acknowledges this two paragraphs later: "a relationship that belongs to the content model, not the ownership model." The property statement should match what the formal conditions establish, not claim something the content model will (separately) provide.
**Required**: Remove "that structurally relates to a" from the property statement, or replace it with language matching the formal content — e.g., "π may create a new address a' within dom(π)" — and note that the content-level relationship between a and a' is established by the content model, not the ownership model.

## OUT_OF_SCOPE

### Topic 1: Interaction between ownership and the version DAG
**Why out of scope**: The ASN establishes ownership over addresses but does not address how ownership interacts with version creation, forking within a document's version history, or the version DAG's structural constraints. This is new territory requiring the document/version model, not an error in the ownership specification.

### Topic 2: Cross-node identity federation
**Why out of scope**: O9 establishes node-locality and O11 treats identity as axiomatic. The question of how a human establishes correlated principals on multiple nodes, and what invariants such federation must satisfy, is explicitly noted in the ASN's open questions and belongs in a future specification.

VERDICT: REVISE
