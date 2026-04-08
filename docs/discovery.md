# Discovery

Discovery is about finding the formal structure of a system that exists but has never been formally specified. The goal is not to design — the system already exists — but to uncover the properties that make it work.

## Starting from nothing

Begin with a broad question: "What are the key guarantees of the system?" This draws in a wide range of concepts that the reasoning process works through — address permanence, content identity, hierarchical structure, link semantics. The result is a large initial ASN with many properties.

This first ASN is too big. That's expected. Read through it and look for natural boundaries — clusters of properties that reason about the same concept independently of other clusters. Tumbler arithmetic doesn't need to know about links. Content insertion doesn't need to know about version semantics.

Split the large ASN into two or more focused ASNs, each covering one topic. Run discovery on each one independently.

## Growing the lattice

As you run discovery on the separate ASNs, patterns emerge. Two ASNs independently derive the same property — both need tumbler comparison, both define what "prefix" means. When you see this, look at whether one ASN's properties are natural foundations for the other. If so, make it a dependency — the dependent ASN assumes those properties rather than re-deriving them. If neither is a natural home for the shared concept, there's a missing foundation layer. Extract it into a new ASN that both depend on.

Each ASN goes through review/revise cycles. During review, an ASN may reveal that it's really two independent arguments sharing a label namespace — the derivation threads never reference each other. Or review keeps finding properties that belong elsewhere, or the ASN is simply too large to hold in your head. These are signals to split. Meanwhile, reviewers flag things as out of scope that turn out to be genuine gaps — questions no existing ASN can answer. These become new ASNs.

The lattice grows through this process. An ASN depends on another when it uses that ASN's properties as premises. If you find circular dependencies — A needs B and B needs A — the boundary is wrong. Either one contains properties that belong in the other, or both depend on a missing foundation that should be extracted.

Foundation ASNs emerge at the bottom of the lattice. They weren't planned — they were discovered by noticing what kept being re-derived across multiple ASNs.

## Entering blueprinting

At some point the lattice has enough structure that you can see which ASNs everything else rests on. These foundations need to be put on rigorous standing — formal contracts, mechanical verification, the full weight of the downstream pipeline. [Blueprinting](blueprinting.md) is that transition. But it can only happen bottom-up: a foundation must be solid before anything built on it can be trusted.

An ASN is ready to enter blueprinting when three conditions hold:

**It must be a foundation in the lattice.** You cannot blueprint an ASN if it depends on another ASN that hasn't been blueprinted and formalized yet. Work bottom-up — foundations first, then the ASNs that build on them.

**Discovery cycles are producing diminishing returns.** When review/revise cycles start wordsmithing — rephrasing for clarity, minor notational adjustments, few or no REVISE findings — the reasoning has stabilized. If each cycle is making substantive structural changes, the ASN isn't ready.

**No other ASN in discovery owns properties that belong here.** Before promoting to blueprinting, scan the other ASNs still in discovery. If any of them independently derived properties that naturally belong in this ASN, absorb them first.
