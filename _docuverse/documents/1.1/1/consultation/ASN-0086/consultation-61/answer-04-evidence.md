## Question 4 [evidence]

> Does ASN-0043's L1c, as stated, already commit to a witness-only reading of its existential, or does its phrasing leave room for an operational re-execution requirement that L1cWitnessOnly would rule out?

## KB Synthesis

This question is not answerable from the KB as provided.

The KB contains extensive implementation findings relevant to the underlying semantic territory — particularly [INV-ITOV-FILTERING] (unreferenced I-addresses are silently filtered at query time, not at storage time), [EC-GHOST-LINK] (FOLLOWLINK succeeds with empty result when endset I-addresses have no current POOM mapping), and [PRE-FOLLOWLINK] (no liveness precondition on endset I-addresses) — all of which bear on witness-only vs. re-execution readings of existentials over POOM mappings.

But the KB does not include ASN-0043's L1c text. Without the actual phrasing of L1c, I cannot determine whether its existential is already scoped to a snapshot witness or whether its wording is compatible with an operational re-execution requirement that a separate L1cWitnessOnly clause would need to foreclose.

To answer the question, I would need either ASN-0043's L1c text or a summary of its wording.

---

## Code Exploration

The terms "L1c", "ASN-0043" (as a formal assertion), "L1cWitnessOnly", "witness-only", and "existential" do not appear anywhere in this test harness repository. I have searched all files including findings, knowledge-base, docs, and the backend source.

**The question cannot be answered from sources I can access.**

The notation "ASN-0043" (as a named formal assertion with labeled sublemmas like "L1c") and the "witness-only vs. operational re-execution" distinction are formal specification concepts — likely from a Dafny spec or formal axiom document in the parent `xanadu-spec` repository. That repository is outside my permitted working directory.

What **is** present in this harness regarding finding 0043:

Finding `0043-createnewversion-copies-text-not-links.md` and `knowledge-base/analyzed/0043.md` document the behavioral fact that `docreatenewversion` [`do1.c:264-303`] copies only the text subspace vspan (via `retrievedocumentpartofvspanpm` [`orglinks.c:155-162`] which reads `cdsp.dsas[V]` and `cwid.dsas[V]`) — no link subspace. The KB entry `INT-LINK-TRANSCLUSION` states that `find_links` works on versions via content-identity intersection, not POOM structure.

That claim **as stated in the KB** is behavioral, not existential in the formal-logic sense: it asserts a definite content-identity search, not a bare existence witness. But whether that corresponds to what "L1c" says, and whether L1c's phrasing leaves room for re-execution semantics, requires reading the actual formal spec file — which is not in this repository.

If you can share the formal spec containing L1c (paste it here, or make it accessible within this working directory), I can trace through the code and give you a precise answer tied to actual lines.
