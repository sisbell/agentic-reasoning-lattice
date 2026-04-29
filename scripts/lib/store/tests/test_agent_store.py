"""Unit tests for AgentStore + default_store / agent_context.

Per docs/modules/agent-module.md:
- Wrapping a Store with AgentStore at orchestrator startup means every
  make_link from that point on is paired with a `manages` link from the
  agent doc to the new link.
- Attribution skips `agent` and `manages` types themselves.
- `default_store()` reads XANADU_AGENT_DOC and wraps automatically so
  subprocesses (convergence-resolution.py, convergence-cite.py, ...) attribute operations to the
  invoking orchestrator's agent.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from lib.store.agent_store import AgentStore
from lib.store.queries import active_links
from lib.store.store import (
    AGENT_DOC_ENV_VAR, Store, agent_context, default_store,
)


AGENT_DOC = "_docuverse/documents/agent/cone-review.md"
CLAIM_PATH = "claim-convergence/ASN-0001/T0.md"


class AgentStoreBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.inner = Store(
            log_path=self.root / "_store" / "links.jsonl",
            index_path=self.root / "_store" / "index.db",
        )
        self.addCleanup(self.inner.close)


class AgentStoreConstructionTests(AgentStoreBase):
    def test_construction_emits_agent_classifier(self):
        AgentStore(self.inner, AGENT_DOC)
        active = active_links(self.inner, "agent", to_set=[AGENT_DOC])
        self.assertEqual(len(active), 1)

    def test_construction_idempotent(self):
        a = AgentStore(self.inner, AGENT_DOC)
        b = AgentStore(self.inner, AGENT_DOC)
        active = active_links(self.inner, "agent", to_set=[AGENT_DOC])
        self.assertEqual(len(active), 1)
        self.assertIs(a._store, b._store)


class AgentStoreMakeLinkTests(AgentStoreBase):
    def setUp(self):
        super().setUp()
        self.agent_store = AgentStore(self.inner, AGENT_DOC)

    def test_make_link_emits_underlying_link(self):
        link_id = self.agent_store.make_link(
            from_set=[], to_set=[CLAIM_PATH], type_set=["claim"],
        )
        rec = self.inner.get(link_id)
        self.assertEqual(rec["type_set"], ["claim"])

    def test_make_link_emits_manages_for_attributed_types(self):
        link_id = self.agent_store.make_link(
            from_set=[], to_set=[CLAIM_PATH], type_set=["claim"],
        )
        active = active_links(
            self.inner, "manages",
            from_set=[AGENT_DOC], to_set=[link_id],
        )
        self.assertEqual(len(active), 1)

    def test_make_link_attributes_subtypes(self):
        finding_path = "_workspace/findings/claims/ASN-0001/review-1/0.md"
        link_id = self.agent_store.make_link(
            from_set=[finding_path], to_set=[CLAIM_PATH],
            type_set=["comment.revise"],
        )
        active = active_links(
            self.inner, "manages",
            from_set=[AGENT_DOC], to_set=[link_id],
        )
        self.assertEqual(len(active), 1)

    def test_agent_type_is_not_attributed(self):
        other_agent = "_docuverse/documents/agent/full-review.md"
        link_id = self.agent_store.make_link(
            from_set=[], to_set=[other_agent], type_set=["agent"],
        )
        active = active_links(
            self.inner, "manages",
            from_set=[AGENT_DOC], to_set=[link_id],
        )
        self.assertEqual(active, [])

    def test_manages_type_is_not_attributed(self):
        target_id = self.inner.make_link(
            from_set=[], to_set=[CLAIM_PATH], type_set=["claim"],
        )
        manages_id = self.agent_store.make_link(
            from_set=[AGENT_DOC], to_set=[target_id],
            type_set=["manages"],
        )
        active = active_links(
            self.inner, "manages",
            from_set=[AGENT_DOC], to_set=[manages_id],
        )
        self.assertEqual(active, [])


class AgentStoreProxyTests(AgentStoreBase):
    """AgentStore should proxy non-write methods transparently."""

    def setUp(self):
        super().setUp()
        self.agent_store = AgentStore(self.inner, AGENT_DOC)

    def test_get_proxies(self):
        link_id = self.agent_store.make_link(
            from_set=[], to_set=[CLAIM_PATH], type_set=["claim"],
        )
        rec = self.agent_store.get(link_id)
        self.assertEqual(rec["id"], link_id)

    def test_find_links_proxies(self):
        self.agent_store.make_link(
            from_set=[], to_set=[CLAIM_PATH], type_set=["claim"],
        )
        results = self.agent_store.find_links(type_set=["claim"])
        self.assertEqual(len(results), 1)


class _EnvIsolatedTests(unittest.TestCase):
    """Base for tests that read or set XANADU_AGENT_DOC. mock.patch.dict
    snapshots os.environ on entry and fully restores it on cleanup.
    """

    def setUp(self):
        patcher = mock.patch.dict(os.environ, {}, clear=False)
        patcher.start()
        self.addCleanup(patcher.stop)
        os.environ.pop(AGENT_DOC_ENV_VAR, None)


class DefaultStoreTests(_EnvIsolatedTests):
    def setUp(self):
        super().setUp()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.log = self.root / "_store" / "links.jsonl"
        self.idx = self.root / "_store" / "index.db"

    def test_no_env_var_returns_plain_store(self):
        store = default_store(log_path=self.log, index_path=self.idx)
        self.addCleanup(store.close)
        self.assertIsInstance(store, Store)
        self.assertNotIsInstance(store, AgentStore)

    def test_env_var_set_returns_agent_store(self):
        os.environ[AGENT_DOC_ENV_VAR] = AGENT_DOC
        store = default_store(log_path=self.log, index_path=self.idx)
        self.addCleanup(store.close)
        self.assertIsInstance(store, AgentStore)
        self.assertEqual(store.agent_doc, AGENT_DOC)


class AgentContextTests(_EnvIsolatedTests):
    def test_sets_and_restores_when_unset(self):
        self.assertNotIn(AGENT_DOC_ENV_VAR, os.environ)
        with agent_context(AGENT_DOC):
            self.assertEqual(os.environ[AGENT_DOC_ENV_VAR], AGENT_DOC)
        self.assertNotIn(AGENT_DOC_ENV_VAR, os.environ)

    def test_nested_contexts_restore_outer(self):
        outer = "_docuverse/documents/agent/full-review.md"
        inner = AGENT_DOC
        with agent_context(outer):
            self.assertEqual(os.environ[AGENT_DOC_ENV_VAR], outer)
            with agent_context(inner):
                self.assertEqual(os.environ[AGENT_DOC_ENV_VAR], inner)
            self.assertEqual(os.environ[AGENT_DOC_ENV_VAR], outer)
        self.assertNotIn(AGENT_DOC_ENV_VAR, os.environ)


if __name__ == "__main__":
    unittest.main()
