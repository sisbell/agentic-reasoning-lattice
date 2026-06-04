# Review of ASN-0101

I checked the operation specification (D0), the gap-closure argument (D1), the seven preservation claims (D2–D8), the projection characterisation (D9), the ValidComposite★ extension (D10), and the wp calculations (D11), plus the boundary-case enumeration and the three worked examples. The mathematical content is sound: the shift-inverse construction, the source-correspondence discharge of S3★/CL-OWN/CL-UNIQ across the `Q ∩ X` re-mapping, the three-group invariant partition, the honest treatment of multi-step J0 breakage, and the four wp derivations all check out, and the boundary enumeration is genuinely exhaustive. One finding remains, and it is an accretion finding rather than a correctness one.

## REVISE

### Issue 1: D10 "Vocabulary note" is accreted defensive meta-prose around K.σ
**ASN-0101, D10, "Vocabulary note"**: "ASN-0047's ValidComposite★ originally enumerates eight transitions ... K.σ ... is listed in the vocabulary above for substrate completeness — it was introduced by ASN-0093 after ASN-0047 was fixed, and downstream specifications that invoke 'ValidComposite★ chains' should range over the full substrate vocabulary — but its admission to ValidComposite★ is ASN-0093 substrate housekeeping, not ASN-0101's burden of proof. The remainder of this section concerns only DEL."

**Problem**: This paragraph advances no part of D10's claim. It explains *why* a list entry (K.σ) is present and whose burden it is — exactly the "new prose explaining why an entry is present rather than advancing meaning" and "a paragraph looks like a prior finding's content relocated rather than removed" patterns the anti-bloat classifier flags. The note reads as a response to the prior (declined) K.σ vocabulary-consistency findings: rather than simply letting the clean extended vocabulary `{..., K.ρ, K.σ, DEL}` stand, the reviser added a paragraph defending the discrepancy between the body's nine-entry foundation vocabulary and the note's own "eight transitions" count. The precise reader must skip it to reach D10's actual content (admission of DEL, conditions (1)–(2)).

**Required**: Delete the Vocabulary note. The extended vocabulary in D10's statement already lists `K.σ` and `DEL`; D10's claim is the admission of DEL, and the body already states DEL "extends the foundation's transition vocabulary." If a one-clause scoping reminder is genuinely needed, fold it into D10's statement (e.g., "DEL is the only addition; K.σ is inherited from ASN-0093"), not a standalone justificatory paragraph.

## OUT_OF_SCOPE

None. The ASN correctly confines itself to DELETE mechanics; the "Boundaries the abstract specification does not cross" section names INSERT/versioning/index concerns only to disclaim them, which is in-scope scoping rather than coverage of out-of-scope operations.

VERDICT: REVISE
