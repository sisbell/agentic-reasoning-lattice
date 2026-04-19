# Design Notes

Notes on the system's architecture and operation that aren't patterns. Patterns document observed emergent behavior with a specific solution/forces/structure form (see [patterns/](../patterns/)). Design notes document deliberate architectural choices, aggregate observations about how the system behaves, or cross-cutting principles that don't fit the pattern template.

## Notes

- [Review V-Cycle](review-v-cycle.md) — multi-scale review architecture. Local, regional, and global review cycles each handle the error class they're efficient at, with upward-then-downward passes through the scales.
- [Domain Language Emergence](domain-language-emergence.md) — how vocabulary produced by [prose coinage](../patterns/prose-coinage.md) is structured into layers (theory-channel / invented / formalization-level) and narrowed as it moves through the pipeline.
- [Self-Healing](self-healing.md) — map of where the system could detect and respond to disequilibrium patterns from its own operation. Three tiers: already automated, detection ready / action pending, and further-out candidates.
