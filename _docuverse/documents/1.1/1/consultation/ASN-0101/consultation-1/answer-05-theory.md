## Question 5 [theory]

> Was middle-span DELETE intended as a single primitive operation distinct from the suffix-truncation K.μ⁻, or as a composite built from existing transition kinds?

Nelson specifies DELETE as a single primitive in FEBE, not as a composite. The notation `K.μ⁻` is from your formal specification, not from Literary Machines.

## What Nelson Specified

Nelson's FEBE protocol lists DELETEVSPAN as one of the 17 base commands:

> "DELETEVSPAN: This removes the given span from the given document." (4/66)

The command takes a span — and per the [spans](spans.md) concept, a span is just two tumbler addresses delimiting a contiguous range. Nelson makes no distinction between "suffix" spans (those ending at document end) and "middle" spans (those bounded on both sides by surviving content). The same primitive handles all cases.

## No Compositional Treatment

Nelson does not decompose DELETE into smaller operations. The FEBE protocol is described as a flat set of semantic commands, with editing primitives explicitly called "comparatively simple":

> "FEBE includes instructions for insertion in a document, deletion from a document, and rearrangements of unlimited size. These are comparatively simple." (4/61)

The complexity Nelson flags is in *link and connectivity* commands (4/61), not in editing primitives.

## Uniform Semantic Meaning

Nelson's [delete-semantics](delete-semantics.md) treatment reinforces this. DELETE always means the same thing regardless of span position:

- **Vstream:** content becomes "not currently addressable" in that document
- **Istream:** bytes remain forever
- The diagram on 4/9 shows "DELETED BYTES" as one document state, uniformly defined

There is no architectural reason in Nelson's model to distinguish middle-span DELETE from suffix-truncation — both are V-stream removals over a span, leaving I-stream content untouched.

## Bottom Line on Intent

Nelson's design intent: **DELETE is one primitive over arbitrary spans.** If your formal spec treats `K.μ⁻` (suffix-truncation) and middle-span deletion as separate transition kinds, that's an implementation-level decomposition you've introduced — possibly for proof tractability or to model V-stream gap-closing behavior — not something Nelson distinguished.

NEED_RAW: 4/65-4/67 if you want to verify there is no second DELETE variant in the command catalog beyond what's quoted above, and 4/9 for the deleted-bytes state diagram.
