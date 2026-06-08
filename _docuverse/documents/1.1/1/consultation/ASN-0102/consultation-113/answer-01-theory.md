## Question 1 [theory]

> Was the COPY operation intended to be semantically atomic (an indivisible placement), or merely to produce a correct end-state by whatever means, such that a contract-then-restore realization would equally satisfy the design?

## Short answer

Nelson never frames operations as "atomic" or "indivisible." He specifies COPY by its **end-state** — but the end-state he specifies is not just "the right bytes appear at the right V-position." It is a specific *structural* result: the placed material **shares I-addresses with the source** (transclusion). So "produce a correct end-state by whatever means" is the closer reading of Nelson's intent — *provided* the means actually reproduce that structural end-state. A contract-then-restore realization satisfies the design **only if** it preserves shared identity; if it re-allocates fresh I-addresses, it produces a duplicate, not a COPY, and fails the design regardless of how the visible text looks.

## Why end-state, not atomicity

Nelson designs the *virtuality* (the seeming) first and pushes mechanism downward:

> "The starting point in designing a computer system must be the creation of the conceptual and psychological environment--the seeming of the system--what I and my associates call the virtuality. You begin by designing a conceptual structure and how it should feel, then work back into the mechanics." (1/3, from `purpose`)

The COPY command itself is stated purely as a placement result, with no atomicity claim:

> "The material determined by `<spec set>` is copied to the document determined by `<doc id>` at the address determined by `<doc vsa>`." (4/67, from `operations`)

This is consistent with the broader posture that what the system "does--and thus is--is defined by the commands to which it responds" (4/61) — i.e., defined by observable effect, not by an internal procedure.

## But the end-state is constrained — it must be transclusion

The decisive point is *what* counts as a correct COPY end-state. COPY is transclusion, and transclusion is reference, not duplication:

> "Someone else may create a document which quotes it as much as desired. This mechanism we call the quote-window or quote-link. Through a 'window' in the new document we see a portion of the old." (2/32, from `transclusion`)

> "No copying operations are required among the documents throughout the system... We solve this problem simply by windowing to a changing document." (2/36, from `transclusion`)

And identity is by **creation**, not by value — which is exactly what shared I-addresses encode:

> Content identity is based on creation, not value. Two documents with identical text created independently have DIFFERENT I-addresses. Transcluded content SHARES the same I-address. (`sporgl-provenance`, paraphrasing 4/10-4/11)

The `i-space-v-space` mapping for COPY confirms the operative invariant: COPY "Creates Vstream mapping to existing Istream (transclusion)." The correct end-state is a new V→I mapping pointing at the *source's existing* I-addresses, not new ones.

## What this means for contract-then-restore

A "contract-then-restore" realization is design-equivalent **iff** the restore step rebinds the original I-addresses. Concretely:

- If "restore" re-establishes the same V→I bindings (same source I-addresses), the transclusion relationship is intact, provenance is preserved, links to those bytes survive, and `FINDDOCSCONTAINING` will still report the source. The design is satisfied — Nelson's effect-based specification doesn't care that you took a detour.
- If "restore" allocates **fresh** I-addresses (the way INSERT does), you have manufactured a value-identical duplicate, not a COPY. This silently breaks the guarantees COPY exists to provide: shared identity, origin traceability ("you can at once ascertain the home document of any specific word or character," 2/40, from `transclusion`/`origin-traceability`), and the live-vs-dead distinction ("Any detached copy someone keeps is frozen and dead," 2/48).

This is precisely the failure mode flagged in your own project notes for ASN-0101 (DEL-then-INSERT does not recover pre-state because INSERT allocates fresh I-addresses). The same hazard applies to any contract-then-restore *realization of COPY*: it is correct only if "restore" is identity-preserving, not allocation-fresh.

## Bottom line

COPY was not designed to be *procedurally* atomic — Nelson specifies by effect and leaves mechanism to the implementor. But its end-state is not merely "the right text at the right place"; it is the transclusion relation of **shared I-addresses with preserved provenance**. A contract-then-restore realization equally satisfies the design exactly to the extent that it reconstructs that shared-identity binding. The invariant that must hold is *shared identity*, not *indivisibility* of the operation.

---

One caveat on sourcing: "semantically atomic," "contract-then-restore," and the explicit equivalence framing are your analytical terms, not Nelson's — he never discusses operation atomicity or alternative realizations directly. My answer derives the design intent from his transclusion/identity guarantees and his virtuality-first methodology. If you want me to check whether 4/66–4/67 contains any wording about operation indivisibility or ordering constraints beyond the single COPY sentence quoted above: NEED_RAW: 4/66-4/67.
