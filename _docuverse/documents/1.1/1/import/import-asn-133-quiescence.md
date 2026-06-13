---
create_note: 133
title: "Substrate Quiescence"
source_doc: "_workspace/asn-new-quiescence-draft.md"
depends: [86, 126, 128, 129, 130]
---

# Why I'm importing this doc

This is the capstone of the protocols stack (86 → 126 → 128 → 129 → 130 →
133). ASN-0129 supplies the predicate language a coordination system's
conditions are written in and the dynamics classes (PD0–PD2, ST/SF) that
say how a condition's truth moves; ASN-0130 makes those conditions
substrate artifacts. This note closes the arc: it defines what it is for
such a system to be *done* — quiescence — and proves termination as a
*conditional* theorem with every hypothesis named and placed.

The design discipline is to put each hypothesis where it belongs: what the
substrate guarantees unconditionally (Q0 recognizability — quiescence is a
PL term, decidable by any observer; Q1 absorption — a fixed point of
firing), what a rule author can make checkable at registration (extinction
via SF spelling — Q-EXT makes at-most-once firing a theorem from the
class, the Marker pattern's termination half as a registration-time lint),
and what remains assumption (H-FAIR fairness, H-W bounded work) named
rather than smuggled. H-W is proved *meta-level* — its statement quantifies
over reachability, a fixpoint PL deliberately cannot express (PC6a).

Two contributions beyond the conditional theorem. Q-FLIP corrects the
folklore "no retraction ⟹ triggers flip at most once" as unsound against
0128/0129's shipped default-view + BH4-footprint machinery, replacing it
with the per-spelling-class falsifier accounting 0129's FP enumerates. And
the RG rule model (domain in QD + Boolean PL trigger + emission contract,
bodies opaque) is deliberately self-contained — the agents layer is
*replaced, not promoted*: rather than forcing an agents ASN, the minimal
trigger/emission unit the quiescence theorems consume is internalized, with
the full agent semantics left to the protocol layer unless a forcing case
arrives.

The draft was authored against the final post-audit text of ASN-0129 and
ASN-0130, then citation-swept after 0130's anti-bloat audit closed: PR-DISC
scoping (fenced to pdef-triggers; inline-PL triggers carry no such
hypothesis), ever-registration survival of Q0 under de-registration, ST⁺
wording, and 0130's OQ3/OQ4 cross-references all reflected. An operator
adversarial read named the fire-level finiteness hypothesis (H-FIN) and the
universal-over-emission-choices reading of termination, and firmed the
ASN-0086 audit-slice citation into a core claim. The remaining proof-rigor
items it surfaced (Q5's W(σ) definition, Q6's fairness argument, the
stratification detail in the worked composition) are deliberately left for
the maiden review to deepen rather than pre-guessed.
