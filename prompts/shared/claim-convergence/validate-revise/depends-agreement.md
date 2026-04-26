# Validate-Revise — Depends Agreement

## Context

You are fixing a structural violation of invariant #5 from the Claim File Contract:

> **Depends agreement.** The yaml `depends:` list and the markdown Formal Contract Depends section name the same set of claims.

The yaml `depends` list is authoritative. The markdown Formal Contract Depends section must name the same set of claims — each entry uses the same label as yaml.

## Correct form

yaml:
```yaml
depends:
- T0
- NAT-order
- NAT-zero
```

markdown Formal Contract block:
```
*Formal Contract:*
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies the carrier ℕ and tumbler length.
  - NAT-order (NatStrictTotalOrder) — supplies strict total order < on ℕ.
  - NAT-zero (NatZeroMinimum) — supplies 0 ∈ ℕ as the minimum.
- *Postconditions:* ...
```

Each md depends entry: `  - <label> (<name>) — <brief description>`. The `<label>` is the first token after the bullet and MUST equal a yaml.label of an existing claim. Not a kind keyword ("Definition"), not a sub-reference ("T1(c)").

## File to fix

{file_path}

## Authoritative yamls (do not edit; use for labels and names)

The first yaml below is the companion yaml for the file being fixed. Its `depends` list is authoritative — the md Depends must match this set. The yamls after it are for each depended claim, giving the `name` field to use in md Depends entries.

{yaml_bundle}

## Findings in this file

{findings_list}

## Fix instructions

1. The authoritative yamls are shown above. Use their `label` and `name` fields **verbatim** — do not guess.
2. Find the markdown Formal Contract block (`*Formal Contract:*`). If present:
   - Find the `- *Depends:*` sub-section.
   - For each companion yaml depend not yet in the md Depends: **before adding a bullet, verify the dep is actually used in the proof**. Read the md body (Axiom, Proof, Derivation, Preconditions, Postconditions) and locate a specific proof step, cited lemma, or used symbol that the dep supplies. If found, add a bullet `  - <label> (<name>) — <brief description>`, using label and name from the depended yaml and a gloss that names the concrete usage. If you cannot identify a concrete usage in the proof, **DO NOT invent a gloss describing the dep as "consumer," "context," "backdrop," "companion," or any relationship other than what the proof actually uses** — the yaml entry is likely inverted (a downstream consumer erroneously listed as an input). In that case, leave the md unchanged and decline the fix for that dep; the validator will re-surface the finding on the next pass, where it can be judged as a yaml-correctness issue rather than a prose-sync issue.
   - For each md Depends entry whose first token is a type keyword (Definition, Axiom, Lemma, Theorem, Corollary, Design-requirement), rewrite the first token to the actual label from yaml. E.g., `- Definition (Span) — ...` becomes `- Span (Span) — ...` when yaml.label is Span and yaml.name is Span.
   - For md entries that use sub-reference notation (like `T1(c)`), if the companion yaml depends on the parent only (`T1`), rewrite the md entry's first token to the parent label. Preserve the sub-reference as descriptive prose in the description part (e.g., "transitivity clause T1(c)") if it's meaningful.
   - If an md entry references a label that's not in companion yaml's depends and is not a sub-reference of a yaml depend, it's extraneous — remove the entry.
3. If the markdown file has NO `*Depends:*` section at all (some files embed dependencies inline in the Axiom prose):
   - Do NOT restructure the file to add a structured Depends section. That's a larger design call.
   - Instead, leave such files unchanged and note it in your final summary. Their findings will be surfaced in the judgment-required pass.

## Alternative: retract instead of add

The finding `in store citations but not in md Depends: [...]` admits two interpretations:

- **The proof actually uses X but the md Depends list is missing the entry.** Resolution: add the bullet (rule 2 above).
- **The proof does not use X; the substrate citation is stale from a prior proof version.** Resolution: retract the substrate citation. Run:

      PROTOCOL_CLAIM_PATH=<file_path> python scripts/retract.py --to <label>

  This files a `retraction` link pointing at the stale citation's link id. The citation remains in the substrate (append-only) but no longer counts toward the dependency graph; the depends-agreement check will pass on the next validator pass.

**How to choose.** Read the md body (Axiom, Definition, Proof, Derivation, Preconditions, Postconditions) and grep for the dep's label or any of its declared symbols. If you find a use-site, add the bullet. If you cannot find any use-site after thorough inspection, retract — do not fabricate a gloss to pass the check, and do not "leave the md unchanged and decline the fix" (the previous default — retraction is now the principled fix).

The mirror direction (`in md Depends but not in store citations`) does not have a retract path. That finding means the md asserts a dep that was never properly emitted via `cite.py`. Resolution: emit the citation via `python scripts/cite.py --to <label>` and verify the md entry is correct.

## Do not

- Do not change the yaml file.
- Do not edit the proof, Axiom body, Preconditions, Postconditions, or other non-Depends content.
- Do not restructure a file that uses inline-in-Axiom depends form to use a separate block. Leave it for human decision.
- Do not commit.

## On apparent false positives

If a finding looks incorrect, it is almost always format drift (wrong first token, sub-reference notation, kind-word prefix). Apply the canonical form. The yaml label is the authoritative first token of every md depends entry.

## Tools

Read, Edit, Bash. Read the companion yaml and the depended-upon yamls for authoritative labels and names. Edit only the markdown Depends section. Use Bash to invoke `scripts/retract.py` or `scripts/cite.py` when the resolution is to update the substrate rather than the md.
