# Review of ASN-0126

## REVISE

### Issue 1: Register-vs-check distinction stated three times
**ASN-0126, intro / Registry permanence (closing) / Registry entries**: intro — "registering a type means adding an entry to that catalog — an act fixed at substrate construction... whereas checking a type against the catalog (conformance) is what happens at every emit"; Registry permanence closing — "Every registration is therefore an entry present in Σ_init.registry — a construction-time act — and no entry is added at runtime; what runs at emit is the conformance check"; and again in the final Registry-permanence paragraph.
**Problem**: The same distinction is restated nearly verbatim in three sections. Two paragraphs in the same document saying the same thing in different words is the flagged redundancy pattern.
**Required**: State the register/check distinction once (it belongs in Registry permanence, where P1 makes it load-bearing) and delete the intro and Registry-entries restatements.

### Issue 2: Use-site inventories in structural slots
**ASN-0126, Single-source / Three shapes**: "classifiers attach to a single address, citations fan out from a single source, supersession chains anchor on a single predecessor, holdings are owned by a single agent. The single-source commitment captures every observed pattern"; and "The Unary shape covers classifiers, lifecycle markers, presence assertions. The Binary shape covers supersession, parent-child... The Multi shape covers citations, fan-outs..."
**Problem**: These are use-site inventories — corpus catalogs that do not advance the structural claim (|F|=1; three G-disciplines). The table already states what each shape expresses; the prose repeats it as a list of external usages.
**Required**: Delete the inventory sentences. The shape definitions and the table carry the content; the catalog of who-uses-what is not part of the structural commitment.

### Issue 3: Document-ordering justification
**ASN-0126, The idem flag**: "The flag belongs at the framework level rather than in the successor because the structural commitment... is consulted by apps independently of how the operational semantics resolve."
**Problem**: This justifies *where* the flag is documented, not what it asserts. Prose justifying document placement is noise the reader must skip.
**Required**: Delete. The flag's structural presence and state-independence (P3) are the content; the placement rationale is meta.

### Issue 4: Removed-draft narration
**ASN-0126, Registration entries**: "An earlier draft recorded per-slot residence domains (t_F, t_G ∈ {A_doc, A_rel, A}) and had Sh-conf enforce them. We have removed that: those domains are state-indexed... so enforcing them would make Sh-conf state-dependent..."
**Problem**: This is a prior finding's content relocated rather than removed — it narrates a rejected design. The positive claim (registry records shape and idem only; targets unconstrained by residence) is already stated in the preceding sentence and in Shape-conformance/P5.
**Required**: Delete the removed-draft paragraph. If the rationale for *not* enforcing residence is needed, it already lives in Shape-conformance ("Were it to... destroying state-independence").

### Issue 5: Scattered deferrals to the same downstream location
**ASN-0126, multiple sections**: "(Open questions #4)" in Single-source; "deferred to the successor note (Open questions #1)" in The idem flag; plus the lower-bound deferral "deferred to the operational layer" in Three shapes, and further "see X below" pointers in The shape-gated emit.
**Problem**: Multiple paragraphs in different sections defer to the same downstream location (the successor note / Open questions). This is forward-reference accretion that compounds across cycles.
**Required**: Consolidate deferrals into the Open questions list. Inline forward pointers should be removed; the section already exists to hold them.

### Issue 6: Duplicate derivation of the coverage-unsatisfiability fact
**ASN-0126, Shape-conformance**: "In fact that measure would be outright unsatisfiable for a prefix-coverage span: coverage is taken over all of T, and a unit-depth span has coverage... infinite." Then immediately: "That infinitude is not a fact we re-derive here: by T0(b)... every tumbler admits unboundedly many proper extensions... and so lies in {t : a ≼ t}."
**Problem**: The unsatisfiability of `|coverage(F)| = 1` is argued twice — once informally, then re-derived from T0(b)/T1. Two paragraphs, same conclusion.
**Required**: Keep the T0(b)/T1 derivation (it is the rigorous one) and fold the informal statement into it; drop the duplicate "outright unsatisfiable" lead-in.

### Issue 7: Design judgments presented as established results
**ASN-0126, Three shapes / Single-source**: "no recurring lattice pattern needs a G-discipline outside {empty, singleton, unrestricted-finite}, nor a multi-span F"; "The single-source commitment captures every observed pattern."
**Problem**: These are empirical claims about an external corpus, not theorems derivable within the ASN. They are framed as settled ("captures every observed pattern") while being unfalsifiable here. Standard 6 wants claims shown, not asserted; a claim about "every observed pattern" cannot be discharged inside the note.
**Required**: Mark these explicitly as design judgments (scope notes), not properties, or remove them. The structural commitment (|F|=1, three G-disciplines) stands on its own without the exhaustiveness assertion.

## OUT_OF_SCOPE

### Topic 1: Idem semantics at emit
**Why out of scope**: This note commits only to the flag's structural presence and state-independence (P3). The flag's effect on emit/nullify/re-emit is correctly deferred (Open questions #1) — new operational territory, not an error here.

### Topic 2: Multi-source / higher-arity extension
**Why out of scope**: The |F|>1 and N>3 cases are explicitly routed to the ungated link store / a supplemental note. Adding them is new territory, not a gap in this framework.

VERDICT: REVISE
