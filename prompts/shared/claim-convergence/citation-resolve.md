You are typing each claim-label reference in a claim's prose into one of:

- **`depends`** — the claim's axiom or proof *consumes* a symbol, axiom, or operator the referenced claim supplies; the claim's correctness rests on it.
- **`forward`** — the claim names the referenced claim as a downstream concept (a refinement, elaboration, or navigation pointer); the claim stands without it.

# Examples

**Depends — the claim's reasoning rests on the cited claim:**

- The claim's axiom contains a quantifier `n ∈ S` where the set `S` is posited by a referenced claim. → `depends` on that claim (it supplies `S`).
- The claim's proof step invokes "by the strict total order" and the strict total order is supplied by a referenced claim. → `depends`.
- The claim's bound uses an operator like `|·|` defined elsewhere; that elsewhere-claim supplies the operator. → `depends`.

**Forward — the claim names the referenced claim as downstream:**

- The claim's body says *"the per-k assignments are defined in `<X>` at each k"* — `<X>` builds on this claim. → `forward` to `<X>`.
- A parenthetical says *"(generalized in `<Y>`)"*. `<Y>` extends this claim. → `forward` to `<Y>`.
- *"see `<Z>` for the refinement"* — `<Z>` is a refinement of this claim. → `forward` to `<Z>`.

The test: does the claim's *correctness* rest on the referenced body? If yes → `depends`. If the claim only names the referenced claim as scaffolding for the reader → `forward`.

# The claim

{{claim_md_content}}

# Where to find other claim bodies

Same-ASN claims live in `{{claim_dir}}` as `<label>.md`.

Cross-ASN claims live one level up: `{{claims_root}}/<asn-label>/<label>.md`.

Use the Read tool on any path when you need a claim's body — to write an accurate bullet, or to verify a token in the prose is a real label.

# Currently classified

The substrate records these as already classified for this claim. Skip them unless their direction is now wrong, or they no longer appear in the prose (file a retraction).

`*Depends:*`:

{{existing_depends}}

`*Forward References:*`:

{{existing_forwards}}

# Output

```
CLASSIFICATIONS:
- label: <label>
  direction: depends
  bullet: "- <label> (<NAME>) — supplies <what> used in <where in this claim>"

- label: <label>
  direction: forward
  bullet: "- <label> (<NAME>) — refines/elaborates/navigates <description>"

RETRACTIONS:
- label: <label>
  direction: depends | forward
  reason: "<why no longer valid>"
```

For each label in the prose not in the currently-classified lists, output a CLASSIFICATION.

For each currently-classified label no longer in the prose (or whose direction is wrong), output a RETRACTION — plus a CLASSIFICATION if the direction changed.

If both lists are empty, output two empty headers.

Match the bullet style of the claim's existing `*Depends:*` entries — same voice, same shape.
