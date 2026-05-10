"""Trigger-agent-scope-alignment check.

Every registered trigger's `scope_query` must yield addresses that
the runtime's mutex layer can resolve to the agent's declared scope
classifier. The runtime's `Agent.__call__` walks
`resolve_to_scope(addr, declared_scope)`; if that returns None, the
fire is refused mid-flight. This doctor check runs the same
resolution on a sample address from each trigger and surfaces the
misalignment up front.

Today's example: `claims_statements_refresh` uses `per_asn_note` as
its scope_query (yielding note addresses), but its agent
`claims-statements-refresh` declares scope=claim. The mutex layer
can't resolve a note to a single claim; fires error out.
"""

from __future__ import annotations

import re
from typing import Iterable, Optional

from lib.backend.addressing import Address
from lib.predicates.agents import agent_scope_for, resolve_to_scope
from lib.protocols.febe.protocol import Session
from lib.runner import Scope, Trigger
from lib.shared.paths import agent_doc_path

from . import Issue, Severity


CHECK_NAME = "trigger-agent-scope-alignment"
CHECK_DESCRIPTION = (
    "Every trigger's scope_query must yield addresses compatible with "
    "its agent's declared scope classifier. Otherwise the runtime's "
    "mutex layer refuses to fire when the runner walks the trigger."
)


def _sample_asn_label(session: Session) -> Optional[str]:
    """First registered, non-retired note's ASN label (e.g., 'ASN-0034').

    Falls back to None when no note is registered; CLI-mode-only
    scope_queries can't be verified in that case.
    """
    from lib.predicates import is_retired
    label_re = re.compile(r"(ASN|MAT)-\d{4}")
    for link in session.active_links("note"):
        if not link.to_set:
            continue
        addr = link.to_set[0]
        if is_retired(session, addr):
            continue
        path = session.get_path_for_addr(addr) or ""
        m = label_re.search(path)
        if m:
            return m.group(0)
    return None


def _sample_address(
    session: Session, trigger: Trigger, asn_label: Optional[str],
) -> Optional[Address]:
    """Take the first address the trigger's scope_query yields.

    Tries daemon mode first (Scope()); if empty, retries CLI mode
    with a known ASN label. Returns None when neither mode produces
    an address (trigger has no in-scope docs to sample).
    """
    for scope in (Scope(), Scope(asn_label=asn_label) if asn_label else None):
        if scope is None:
            continue
        try:
            for addr in trigger.scope_query(session, scope):
                return addr
        except Exception:
            continue
    return None


def check_trigger_agent_scope_alignment(
    session: Session,
) -> Iterable[Issue]:
    """Yield Issues for triggers whose scope_query yields addresses
    incompatible with the agent's declared scope."""
    from lib import triggers as triggers_module

    asn_label = _sample_asn_label(session)
    triggers = [
        v for v in vars(triggers_module).values()
        if isinstance(v, Trigger)
    ]
    triggers.sort(key=lambda t: t.name)

    for trigger in triggers:
        agent = trigger.agent
        agent_path = str(agent_doc_path(agent.role))
        agent_addr = session.get_addr_for_path(agent_path)
        if agent_addr is None:
            yield Issue(
                severity=Severity.WARNING,
                check=CHECK_NAME,
                message=(
                    f"trigger={trigger.name}  agent doc not registered: "
                    f"{agent_path}"
                ),
            )
            continue

        declared = agent_scope_for(session, agent_addr)
        if declared is None:
            yield Issue(
                severity=Severity.WARNING,
                check=CHECK_NAME,
                message=(
                    f"trigger={trigger.name}  agent={agent.role} has no "
                    f"agent.scope.<type> classifier"
                ),
            )
            continue

        sample = _sample_address(session, trigger, asn_label)
        if sample is None:
            continue

        resolved = resolve_to_scope(session, sample, declared)
        if resolved is None:
            yield Issue(
                severity=Severity.ERROR,
                check=CHECK_NAME,
                message=(
                    f"trigger={trigger.name}  yields {sample} but agent "
                    f"declared scope={declared!r}; resolve_to_scope "
                    f"returned None"
                ),
            )
