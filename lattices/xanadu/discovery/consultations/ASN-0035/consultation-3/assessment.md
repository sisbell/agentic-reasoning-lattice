# Revision Categorization — ASN-0035 review-3

**Date:** 2026-03-14 15:55



## Issue 1: BAPTIZE operation signature omits `actor`
Category: INTERNAL
Reason: This is a notational well-formedness issue resolvable from the ASN's own content. The `authorized(actor, p)` predicate is already introduced as abstract and deferred to the account ontology — the fix is choosing between explicit parameterization or declaring an implicit-parameter convention, both derivable from the existing specification style.
