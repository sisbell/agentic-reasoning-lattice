# Discovery

A human poses a question. Discovery investigates it through two independent agent channels separated by a vocabulary firewall, producing a reasoning lattice of verified claims.

## The campaign

A campaign begins with a question — broad enough to be interesting, specific enough to be tractable. "What governs the stability of this class of materials?" "What are the key guarantees of this addressing scheme?" The question is the entry point. Everything that follows grows from it.

The question is decomposed into channel-appropriate sub-questions before any consultation begins. Theory channel questions are framed for hypothesis space — what does established knowledge predict? Data channel questions are framed for evidence space — what do the raw measurements show? Neither channel sees the other's sub-questions.

The theory channel consults established domain knowledge — literature, models, known principles. The data channel analyzes raw evidence — measurements, source code, experimental outputs. A vocabulary firewall prevents each from using the other's terms. The data channel reasons from evidence alone. It cannot retrieve known solutions from theoretical vocabulary — it can only report patterns it observes. This forces hypothesis space exploration rather than retrieval.

A synthesis step integrates both channels into a structured reasoning document (ASN) with dependency-mapped claims. Where the channels agree, principles are validated. Where they disagree, new hypotheses emerge. The disagreements are where discovery happens.

A campaign ends when the questions it spawned have been investigated, the resulting ASNs have entered blueprinting, and the verified nodes are in the lattice. One campaign may produce multiple ASNs — each sub-question that warrants its own investigation becomes its own node.

## Growing the lattice

![Growing the lattice](diagrams/growing-the-lattice.svg)

The first ASN from a campaign is usually too broad. That's expected. Agents identify natural boundaries — clusters of properties that reason about the same concept independently of other clusters — and split into focused ASNs, each covering one topic. Discovery runs on each independently.

As discovery proceeds on separate ASNs, patterns emerge. Two ASNs independently derive the same property — both need the same comparison operation, both define the same foundational concept. When this happens, one ASN's properties may be natural foundations for the other. If so, it becomes a dependency — the dependent ASN assumes those properties rather than re-deriving them. If neither is a natural home for the shared concept, there's a missing foundation layer. Extract it into a new ASN that both depend on. This is the meet operation — the extracted foundation is the greatest common element below both dependent ASNs.

Each ASN goes through [review/revise cycles](patterns/review-revise-iteration.md). During review, out-of-scope findings get flagged — questions that no existing ASN can answer, properties that belong elsewhere, concepts that need their own investigation. These are candidates for new inquiries, attaching to the lattice as new nodes. This is [scope promotion](patterns/scope-promotion.md) — the system discovers the questions it should be asking, not just answers to questions posed. Each new ASN created above existing ones is a join — a node that builds on multiple foundations.

The lattice grows through this process. Foundation ASNs emerge at the bottom — discovered by noticing what keeps being re-derived across multiple ASNs. The lattice deepens as shared concepts are extracted into new foundation layers. New domain vocabulary emerges because the mathematics requires it, not prescribed in advance.

## Entering blueprinting

At some point the lattice has enough structure to see which ASNs everything else rests on. These foundations need to be put on rigorous standing — formal contracts, mechanical verification, the full weight of the V-cycle. [Blueprinting](blueprinting.md) is that transition. It can only happen bottom-up: a foundation must be solid before anything built on it can be trusted.

An ASN is ready to enter blueprinting when three conditions hold:

**It must be a foundation in the lattice.** You cannot blueprint an ASN if it depends on another ASN that hasn't been blueprinted and formalized yet. Work bottom-up — foundations first, then the ASNs that build on them.

**Discovery cycles are producing diminishing returns.** When review/revise cycles start wordsmithing — rephrasing for clarity, minor notational adjustments, few or no substantive findings — the reasoning has stabilized. If each cycle is making structural changes, the ASN isn't ready.

**No other ASN in discovery owns properties that belong here.** Before promoting to blueprinting, scan the other ASNs still in discovery. If any of them independently derived properties that naturally belong in this ASN, absorb them first.

## Origin

This methodology was developed to formalize the Xanadu hypertext system — deriving formal properties from Ted Nelson's design intent (*Literary Machines*) and Roger Gregory's 1988 implementation (udanax-green) under enforced vocabulary separation. The campaign model, vocabulary firewall, and lattice growth operations emerged from that work. The methodology is the generalization. Xanadu is the origin.