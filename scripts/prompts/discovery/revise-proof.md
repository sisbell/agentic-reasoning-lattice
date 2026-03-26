# Proof Revision

You are fixing a specific proof in an ASN reasoning document.

## ASN File

The ASN is at `{{asn_path}}`. Read it, fix the issue, write it back.

## Property

**Label**: {{label}}

## Issue

{{finding}}

## Rules

1. Fix the proof to address the issue above.

2. Ensure the property section ends with a `*Formal Contract:*` section.
   If it is not already present, add it after the proof. If it exists
   but needs updating after the fix, update it. Only include applicable
   fields. Example:

   ```
   *Formal Contract:*
   - *Preconditions:* w > 0, actionPoint(w) ≤ #a
   - *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w
   ```

   Fields:
   - *Preconditions:* — what must hold before
   - *Postconditions:* — what is guaranteed after
   - *Invariant:* — what holds across all state transitions
   - *Frame:* — what is preserved / not changed

   Skip for definitions (`**Definition (Name).**` headers).

3. If the proof needs a property that doesn't exist anywhere in the ASN
   or its foundations, add the new property:
   - Add a row to the property table
   - Write its derivation section with header and proof
   - Add a formal contract section to the new property

4. Do not change anything beyond the specific property being fixed and
   any new properties needed. Do not modify narrative prose.
