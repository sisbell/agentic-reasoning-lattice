# Review of ASN-0077

## REVISE

### Issue 1: Non-foundation cross-ASN reference to ASN-0093
**ASN-0077, "Where origin already lives" section, O0(b) derivation closure-step parenthetical**: "the foundation-attested lemma that abstracts uniformly over K.σ from ASN-0093 and K.δ-IsDocument from ASN-0047"
**Problem**: ASN-0093 is not in the foundation list (foundations are 0034, 0036, 0040, 0047, 0053, 0058, 0098). Standard 7 requires flagging direct references to non-foundation ASNs. Although foundation ASN-0098's LP8 itself names K.σ (ASN-0093), the ASN under review should not propagate the non-foundation citation by number.
**Required**: Drop the "ASN-0093" mention. Acceptable phrasings: "covered by LP8 itself", or "the document-registration transitions LP8 abstracts over (K.σ, K.δ-IsDocument)". This preserves the technical content without naming a non-foundation ASN.

## OUT_OF_SCOPE

The ASN's own Open Questions section already routes the natural future-ASN topics:
- I-span lift behavior on cross-subspace inputs (link addresses currently silently dropped)
- Transitive provenance / intermediate-chain exposure
- Native-vs-transcluded distinction as a separate operation
- Historical containment (from Σ.R) as a complementary operation distinct from current-arrangement origin

No additional out-of-scope topics surfaced during review.

VERDICT: REVISE
