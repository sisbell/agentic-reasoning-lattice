"""FEBE 88.1 protocol command codes.

Sourced from worktrees/40-f1/udanax-test-harness/febe/client.py
(XuSession.command(code, ...) calls). These constants pin the
numeric codes the wire protocol uses; the in-process Session
(scripts/lib/febe/session.py) currently dispatches by method name
rather than by code, but the codes are kept here so a future wire
implementation can reference them without spelunking through the
test-harness.

Only commands the in-process Session currently exposes are defined
below. Codes for operations not yet implemented (insert, delete,
pivot, vcopy, retrieve_*) are deferred until those operations are
needed — adding them would suggest support that doesn't yet exist.
"""

CREATEDOCUMENT = 11
CREATEVERSION = 13
MAKELINK = 27
FINDLINKSFROMTOTHREE = 30
