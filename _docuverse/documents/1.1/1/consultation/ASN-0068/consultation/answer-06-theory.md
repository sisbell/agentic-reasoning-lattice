## Question 6 [theory]

> Must the system be able to identify shared content between any two documents, regardless of when each was created?

# Yes — Shared Content Identification is a Core Requirement

The system must absolutely be able to identify shared content between any two documents at any time. This is foundational, not optional.

## The Mechanism: FINDDOCSCONTAINING

The protocol explicitly provides this operation:

> "This returns a list of all documents containing any portion of the material included by <vspec set>." `[LM 4/70]`

> "This returns a list of all documents containing any of the material specified by the span addresses, regardless of where the native copies are located." `[LM 4/63]`

The phrase "regardless of where the native copies are located" answers your question directly — geography of storage is irrelevant, and by extension, so is timing of creation.

## What Counts as "Shared" — A Critical Distinction

This is where my design intent must be precise: **shared content means shared Istream origin, not textual equivalence.**

Two documents share content when they reference the same bytes in Istream — i.e., one transcluded from the other, or both transcluded from a common source. Two documents that independently happen to contain identical text are NOT considered to share content. They have different I-addresses.

This distinction matters because the system distinguishes "quoted from the original" from "wrote the same words." Attribution requires this distinction.

## Why Creation Time is Irrelevant

Because I-addresses are permanent (`[LM 4/19]`: "any address... remains valid"), shared origin is detectable regardless of when either document was created:

- Document created in 1990 transcludes from document created in 1985 → shared I-addresses → detectable
- Document created in 2050 transcludes from document created in 1985 → shared I-addresses → detectable

The structural relationship is preserved by the addressing system itself, not by any time-dependent mechanism. As I noted: "Note that 'time' is not included in the tumbler. Time is kept track of separately." `[LM 4/18]`

## Two Forms of Shared-Content Detection

**1. Implicit (automatic, structural)** — Shared Istream origin. The system computes this from addresses alone. SHOWRELATIONOF2VERSIONS returns "a list of ordered pairs of the spans of the two spec-sets that correspond." `[LM 4/70]`

**2. Explicit (user-asserted)** — Counterpart links. For content that is equivalent but lacks shared Istream origin (e.g., translations, parallel formulations by different authors), users create counterpart links. `[LM 4/53]`

## Why This Must Be So

The purpose is intercomparison, which I consider essential:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." `[LM 2/20]`

Without the ability to find shared content across arbitrary documents, the docuverse degenerates into isolated files. The web of transclusion that makes Xanadu meaningful depends on this capability working at any scale, across any time span.
