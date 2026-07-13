import assert from "node:assert/strict";
import test from "node:test";

import { createLatestRequestGuard } from "../../apps/web/components/latestRequest.mjs";

test("only the latest citizen request may update state", () => {
  const guard = createLatestRequestGuard();
  const first = guard.begin();
  const second = guard.begin();
  assert.equal(guard.isCurrent(second), true);
  assert.equal(guard.isCurrent(first), false);
});

test("closing the detail panel invalidates an unfinished request", () => {
  const guard = createLatestRequestGuard();
  const request = guard.begin();
  guard.cancel();
  assert.equal(guard.isCurrent(request), false);
});
