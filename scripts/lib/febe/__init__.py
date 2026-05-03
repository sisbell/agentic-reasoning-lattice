"""FEBE — Front-End Back-End protocol bindings.

Translates between front-end command codes (Nelson's Udanax 88.1
protocol — CREATEDOCUMENT=11, CREATEVERSION=13, MAKELINK=27,
FINDLINKSFROMTOTHREE=30, RETRIEVEENDSETS=28, …) and the substrate
backend's primitive operations.

Reference: worktrees/40-f1/udanax-test-harness/febe/client.py — the
test-harness's wire-protocol client (XuSession). This package is the
in-process Python equivalent: same command surface, same operation
names, but no wire encoding yet (deferred until cross-process is
needed).
"""
