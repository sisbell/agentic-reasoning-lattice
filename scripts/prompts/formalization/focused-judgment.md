You are verifying domain extension claims in a formal specification. Each claim asserts that a property from one ASN can be extended or paralleled in another domain.

For each claim below, determine whether the extension validly transfers all prerequisites from the foundation property to the local property.

## Claims ({{count}})

{{claims}}

## Task

For each claim, output one of:
- **VERIFIED**: The extension is sound — all prerequisites of the foundation property are satisfied in the new domain.
- **GAP**: The extension has a gap — identify the specific prerequisite that is not satisfied or not addressed.

Format your response as:

Claim 1: VERIFIED — [brief explanation]
Claim 2: GAP — [specific missing prerequisite or unsound step]
...

Be precise. A claim is GAP only if a concrete prerequisite is missing or a logical step is unsound. Stylistic differences or alternative proof strategies are not gaps.
