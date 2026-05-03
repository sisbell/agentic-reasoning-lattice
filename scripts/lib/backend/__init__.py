"""Substrate backend.

Models tumbler addressing (ASN-0034 T4, T10a), the link store
(ASN-0043), and version semantics (ASN-0009). Exposes the substrate
primitives — address allocation, MAKELINK, FINDLINKS, doc and version
creation, link versioning. The FEBE wire protocol is *not* part of
this package; front-end clients reach the backend through the `febe`
package, which dispatches FEBE commands to backend methods.
"""
