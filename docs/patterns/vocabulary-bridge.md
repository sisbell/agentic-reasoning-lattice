# Vocabulary Bridge

## Pattern

Discovery agents and formalization agents speak different languages about the same things. Discovery uses domain vocabulary — "document," "element," "content," "link" — because that's what the authorities (Nelson, Gregory) use. Formalization uses structural vocabulary — `zeros(t) = 2`, field levels, T4 field decomposition — because that's what the math requires.

Without a bridge, every formalized ASN independently translates domain terms to structural claims. The cone on ASN-0036 recreated D-DOC ("a document is a tumbler with zeros(d) = 2") because no shared translation existed. ASN-0040 would need the same translation for baptism. Every ASN above the algebra layer encounters the same gap.

A vocabulary bridge is a dedicated layer that maps domain concepts to structural claims once, so every ASN above it can use domain language grounded in formal structure.

## Forces

- **Discovery speaks domain language.** The two data authorities — Nelson's theory, Gregory's evidence — produce findings in domain vocabulary. "Documents," "elements," "content." That's how the domain experts think.
- **Formalization speaks structural language.** Proofs operate on tumblers, zero counts, field decompositions. "Document" has no formal meaning — `zeros(t) = 2` does.
- **The translation is repeated.** Every ASN that references "documents" must independently establish what that means formally. Each one rediscovers the same mapping.
- **Independent rediscovery is expensive.** The cone spent a cycle creating D-DOC for ASN-0036. ASN-0040 would spend another cycle creating the same definition. The lattice pays the cost every time.
- **The bridge is load-bearing.** ASN-0036's S7 proof could not be completed without formally establishing that documents are T10a allocation outputs. The domain concept wasn't optional — it was required for the proof.

## Structure

```
foundation layer    [tumbler algebra — structural language]
                         ↑
vocabulary bridge   [document = zeros(t)=2, element = zeros(t)=3, ...]
                         ↑
structure layer     [strand model — domain language grounded in bridge]
```

The bridge sits between the algebra (which knows only tumblers and operations) and the higher layers (which reason about documents, elements, content, links). It translates once. Everything above it inherits the translation.

## Two kinds of bridge

**Domain → structural**: maps a domain concept to its formal definition. "Document" → `zeros(t) = 2`. The concept exists in the authorities' vocabulary. The structural claim exists in the algebra. The bridge connects them.

**Alias resolution**: maps multiple domain terms to the same structural claim. Nelson calls it "node," Gregory calls it "server," T4 calls it "network field" — all mean the first tumbler field. The two data authorities produce different terms because they reason from different sources. Without resolution, every downstream ASN encounters the confusion independently and resolves it ad hoc.

Both kinds sit in the same bridge layer. Both arise because the authorities speak different languages about the same structure. The interesting claim: alias conflicts surface in different contexts. The "node" vs "network" mismatch appeared in S7's regional review — not in a vocabulary audit, but in a proof that needed to cite T4 precisely. The cone couldn't reconcile S7's "node" with T4's "network" and flagged it. Each context that encounters the alias discovers the inconsistency independently until the bridge resolves it once.

## Detection

You know you need a vocabulary bridge when:

- A cone creates a definition that maps a domain term to a structural claim
- The same mapping would be needed by multiple ASNs
- The domain term comes from the discovery authorities, not from the formalization

The cone creating D-DOC in ASN-0036 was the detection signal. The same definition already existed in ASN-0045's discovery. The formalization independently confirmed it was needed.

## Applications

### ASN-0045 — Entity definitions

ASN-0045 maps Xanadu domain concepts to T4 field structure:

- `E.document` — `ValidAddress(t) ∧ zeros(t) = 2`
- `E.element` — `ValidAddress(t) ∧ zeros(t) = 3`
- `E.user` — `ValidAddress(t) ∧ zeros(t) = 1`
- `E.node` — `ValidAddress(t) ∧ zeros(t) = 0`

Every ASN above ASN-0034 that mentions "document" or "element" depends on these definitions. ASN-0045 was initially considered "just T4 corollaries" — but the cone proved it's a load-bearing vocabulary bridge that the strand model (ASN-0036), baptism (ASN-0040), and every operation ASN needs.

## Leads to

[Reasoning lattice](reasoning-lattice.md) — the vocabulary bridge is a layer in the lattice. It emerges through extract/absorb when multiple ASNs independently rediscover the same domain-to-structure mapping.

[Scope promotion](scope-promotion.md) — the cone creating D-DOC in ASN-0036 is a scope promotion signal: the definition belongs in the bridge layer (ASN-0045), not in the consuming ASN.

## Origin

Discovered when the ASN-0036 regional sweep, running against the updated ASN-0034 foundation, created D-DOC to complete S7's proof. The definition matched ASN-0045's discovery output exactly — the formalization independently rediscovered what discovery had already found. ASN-0045's role as a vocabulary bridge between algebra and structure became clear: it wasn't corollaries, it was the translation layer that every higher ASN needs.
