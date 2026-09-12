# Task set with answer keys

Twelve tasks on Apache Kafka trunk at commit `0ffb4f5` (shallow clone). Every target file was checked with `wc -l` and `wc -c`. Every file sits in the band where the arms actually differ: over 350 lines so Spotify's hook fires, under 100 KB so stock Claude Code does not page or refuse it. Answer keys were derived mechanically with the commands shown, not by reading and guessing. Re-derive them if the pinned commit changes.

Categories map to the two workflows the experiment is about: **reading** (bulk-read questions, code-write from a reference) and **debugging** (precise edits that need exact line content, planted concurrency bugs that need reasoning).

| Id | Category | Target | Lines | Bytes |
|---|---|---|---|---|
| R1 | bulk-read | `server/src/main/java/org/apache/kafka/server/BrokerLifecycleManager.java` | 770 | 33,318 |
| R2 | bulk-read | `storage/src/main/java/org/apache/kafka/server/log/remote/storage/RemoteLogManagerConfig.java` | 616 | 36,909 |
| R3 | bulk-read, multi-file | `group-coordinator/.../GroupCoordinatorShard.java` + `GroupCoordinatorRecordHelpers.java` | 1,496 + 841 | 65,491 + 31,522 |
| R4 | bulk-read, source+test | `raft/.../internals/BatchAccumulator.java` + `BatchAccumulatorTest.java` | 646 + 764 | 22,924 + 26,662 |
| W1 | code-write | reference `connect/transforms/.../MaskField.java` | 225 | 9,346 |
| W2 | code-write | reference `streams/.../metrics/ProcessorNodeMetrics.java` | 213 | 11,302 |
| W3 | code-write | reference `storage/.../RemoteLogManagerConfig.java` | 616 | 36,909 |
| E1 | precise-edit | `core/src/main/java/kafka/server/share/SharePartitionManager.java` | 985 | 48,461 |
| E2 | precise-edit | `clients/src/main/java/org/apache/kafka/clients/NetworkClient.java` | 1,879 | 84,351 |
| E3 | precise-edit | `storage/src/main/java/org/apache/kafka/storage/internals/log/LocalLog.java` | 1,072 | 54,491 |
| D1 | planted-bug | `streams/.../processor/internals/StateDirectory.java` | 1,019 | 46,200 |
| D2 | planted-bug | `clients/.../producer/internals/RecordAccumulator.java` | 1,500 | 74,614 |

W1 and W2 use references under 350 lines on purpose: no Connect transform or Streams metrics registry is bigger, and the interesting question for code-write is whether the worker's output compiles, not whether the hook fires on the reference.

---

## R1. `broker-lifecycle-events`

**Prompt.** In `server/src/main/java/org/apache/kafka/server/BrokerLifecycleManager.java`, list every inner class that implements `EventQueue.Event`. For each one, state (a) which `BrokerState` value(s) it assigns to the `state` field, or "none" if it never assigns `state`, and (b) the name of the public method (or the event class) that enqueues it. Also state the initial value of `state`. Give the answer as a table with one row per event class.

**Answer key.** 12 event classes. Initial state `BrokerState.NOT_RUNNING` (line 131).

| Event class | `state =` | Enqueued by |
|---|---|---|
| ResendBrokerRegistrationEvent | none | `resendBrokerRegistration()` |
| BeginControlledShutdownEvent | PENDING_CONTROLLED_SHUTDOWN | `beginControlledShutdown()` |
| SetReadyToUnfenceEvent | none | `setReadyToUnfence()` |
| OfflineDirEvent | none | `propagateDirectoryFailure(...)` |
| OfflineDirBrokerFailureEvent | none | `propagateDirectoryFailure(...)` via scheduleDeferred |
| CordonedDirEvent | none | `propagateDirectoryCordoned(...)` |
| StartupEvent | STARTING | `start(...)` |
| BrokerRegistrationResponseEvent | none | registration response handler (prepend) |
| BrokerHeartbeatResponseEvent | RECOVERY, RUNNING | heartbeat response handler (prepend) |
| RegistrationTimeoutEvent | none | StartupEvent via scheduleDeferred |
| CommunicationEvent | none | `scheduleNextCommunication` via scheduleDeferred |
| ShutdownEvent | SHUTTING_DOWN | `eventQueue.beginShutdown` |

Derivation:

```
python3 - <<'EOF'
import re
L=open('server/src/main/java/org/apache/kafka/server/BrokerLifecycleManager.java').read().split('\n')
for i,l in enumerate(L):
    m=re.search(r'class (\w+) implements EventQueue\.Event',l)
    if not m: continue
    d=0;j=i;s=False
    while j<len(L):
        for c in L[j]:
            if c=='{': d+=1;s=True
            elif c=='}': d-=1
        if s and d==0: break
        j+=1
    print(m.group(1), re.findall(r'\bstate = BrokerState\.(\w+)','\n'.join(L[i:j+1])) or 'NONE')
EOF
grep -n "eventQueue\.\(append\|scheduleDeferred\|prepend\)" server/src/main/java/org/apache/kafka/server/BrokerLifecycleManager.java
```

**Grader** `key_list`. Score = 0.5 x recall over the 12 class names + 0.4 x recall over the 5 (class, state) pairs + 0.1 for NOT_RUNNING as initial state. Minus 0.05 per invented event class or state attributed to the wrong class. Enqueue column is not scored. Pass at score 0.9 or above.

---

## R2. `remote-log-config-keys`

**Prompt.** Read `storage/src/main/java/org/apache/kafka/server/log/remote/storage/RemoteLogManagerConfig.java`. List every configuration key (the actual string value, e.g. `remote.log.storage.system.enable`) that is registered with `.define(` inside `configDef()`, together with its `ConfigDef.Type` and its default value (resolve constants to literal values; write `null` if the default is the literal null). Do not include `*_PROP` constants that are declared in the file but are not passed to `.define(`; list those separately under a heading "declared but not defined".

**Answer key.** 29 defined keys.

| Key | Type | Default |
|---|---|---|
| remote.log.storage.system.enable | BOOLEAN | false |
| remote.log.storage.manager.impl.prefix | STRING | "rsm.config." |
| remote.log.metadata.manager.impl.prefix | STRING | "rlmm.config." |
| remote.log.storage.manager.class.name | STRING | null |
| remote.log.storage.manager.class.path | STRING | null |
| remote.log.metadata.manager.class.name | STRING | "org.apache.kafka.server.log.remote.metadata.storage.TopicBasedRemoteLogMetadataManager" |
| remote.log.metadata.manager.class.path | STRING | null |
| remote.log.metadata.manager.listener.name | STRING | null |
| remote.log.metadata.custom.metadata.max.bytes | INT | 128 |
| remote.log.index.file.cache.total.size.bytes | LONG | 1073741824 |
| remote.log.manager.thread.pool.size | INT | 2 |
| remote.log.manager.copier.thread.pool.size | INT | 10 |
| remote.log.manager.expiration.thread.pool.size | INT | 10 |
| remote.log.manager.follower.thread.pool.size | INT | 2 |
| remote.log.manager.task.interval.ms | LONG | 30000 |
| remote.log.reader.threads | INT | 10 |
| remote.log.reader.max.pending.tasks | INT | 100 |
| log.local.retention.ms | LONG | -2 |
| log.local.retention.bytes | LONG | -2 |
| log.remote.copy.lag.ms | LONG | 0 |
| log.remote.copy.lag.bytes | LONG | -1 |
| remote.log.manager.copy.max.bytes.per.second | LONG | Long.MAX_VALUE |
| remote.log.manager.copy.quota.window.num | INT | 11 |
| remote.log.manager.copy.quota.window.size.seconds | INT | 1 |
| remote.log.manager.fetch.max.bytes.per.second | LONG | Long.MAX_VALUE |
| remote.log.manager.fetch.quota.window.num | INT | 11 |
| remote.log.manager.fetch.quota.window.size.seconds | INT | 1 |
| remote.fetch.max.wait.ms | INT | 500 |
| remote.list.offsets.request.timeout.ms | LONG | 30000 |

Declared but not defined (4): `remote.log.index.file.cache.ttl.ms`, `remote.log.manager.task.retry.backoff.ms`, `remote.log.manager.task.retry.backoff.max.ms`, `remote.log.manager.task.retry.jitter`.

Derivation:

```
python3 - <<'EOF'
import re
src=open('storage/src/main/java/org/apache/kafka/server/log/remote/storage/RemoteLogManagerConfig.java').read()
consts={m.group(1):m.group(2).strip() for m in re.finditer(r'public static final \w+ (\w+) = (.+?);\n',src)}
i=0
while True:
    j=src.find('.define(',i)
    if j<0: break
    k=j+8;d=1
    while d:
        d+=(src[k]=='(')-(src[k]==')'); k+=1
    a=[x.strip() for x in re.split(r',(?![^()]*\))',src[j+8:k-1])]
    dflt=a[2] if not a[2].startswith('ConfigDef.Importance') else 'REQUIRED'
    print(consts.get(a[0],a[0]),a[1],consts.get(dflt,dflt)); i=k
EOF
F=storage/src/main/java/org/apache/kafka/server/log/remote/storage/RemoteLogManagerConfig.java
for p in $(grep -o "public static final String [A-Z_]*_PROP" $F | awk '{print $5}'); do grep -q "\.define($p" $F || echo "NOT DEFINED: $p"; done
```

**Grader** `key_list`. Match keys by case-insensitive exact dotted string. Score = 0.6 x recall over 29 keys + 0.3 x fraction of matched keys with a correct default (numeric equality; `1024*1024*1024L` accepted for 1073741824; `9223372036854775807` accepted for Long.MAX_VALUE) + 0.1 x recall over the 4 undefined keys. Minus 0.03 per invented key in the main list; the 4 undefined keys appearing in the main list count as invented. Pass at 0.9.

---

## R3. `group-coordinator-record-replay` (multi-file)

**Prompt.** Cross-reference `group-coordinator/src/main/java/org/apache/kafka/coordinator/group/GroupCoordinatorShard.java` and `group-coordinator/src/main/java/org/apache/kafka/coordinator/group/GroupCoordinatorRecordHelpers.java`. For every `case` label in the `switch` inside `GroupCoordinatorShard.replay(...)`, give: (1) the key class the record key is cast to, (2) which manager field (`groupMetadataManager` or `offsetMetadataManager`) the record is forwarded to, and (3) the names of all `public static CoordinatorRecord` helper methods in `GroupCoordinatorRecordHelpers` that build a record with that key class, or "none in this file" if no helper in that file builds one. One row per case label.

**Answer key.** 22 case labels, 30 helper methods.

| Case | Key class | Manager | Helpers |
|---|---|---|---|
| LEGACY_OFFSET_COMMIT | LegacyOffsetCommitKey | offsetMetadataManager | none |
| OFFSET_COMMIT | OffsetCommitKey | offsetMetadataManager | newOffsetCommitRecord, newOffsetCommitTombstoneRecord |
| GROUP_METADATA | GroupMetadataKey | groupMetadataManager | newGroupMetadataRecord, newGroupMetadataTombstoneRecord, newEmptyGroupMetadataRecord |
| CONSUMER_GROUP_METADATA | ConsumerGroupMetadataKey | groupMetadataManager | newConsumerGroupEpochRecord, newConsumerGroupEpochTombstoneRecord |
| CONSUMER_GROUP_PARTITION_METADATA | ConsumerGroupPartitionMetadataKey | groupMetadataManager | newConsumerGroupSubscriptionMetadataTombstoneRecord |
| CONSUMER_GROUP_MEMBER_METADATA | ConsumerGroupMemberMetadataKey | groupMetadataManager | newConsumerGroupMemberSubscriptionRecord, newConsumerGroupMemberSubscriptionTombstoneRecord |
| CONSUMER_GROUP_TARGET_ASSIGNMENT_METADATA | ConsumerGroupTargetAssignmentMetadataKey | groupMetadataManager | newConsumerGroupTargetAssignmentMetadataRecord, newConsumerGroupTargetAssignmentMetadataTombstoneRecord |
| CONSUMER_GROUP_TARGET_ASSIGNMENT_MEMBER | ConsumerGroupTargetAssignmentMemberKey | groupMetadataManager | newConsumerGroupTargetAssignmentRecord, newConsumerGroupTargetAssignmentTombstoneRecord |
| CONSUMER_GROUP_CURRENT_MEMBER_ASSIGNMENT | ConsumerGroupCurrentMemberAssignmentKey | groupMetadataManager | newConsumerGroupCurrentAssignmentRecord, newConsumerGroupCurrentAssignmentTombstoneRecord |
| SHARE_GROUP_MEMBER_METADATA | ShareGroupMemberMetadataKey | groupMetadataManager | newShareGroupMemberSubscriptionRecord, newShareGroupMemberSubscriptionTombstoneRecord |
| SHARE_GROUP_METADATA | ShareGroupMetadataKey | groupMetadataManager | newShareGroupEpochRecord, newShareGroupEpochTombstoneRecord |
| SHARE_GROUP_TARGET_ASSIGNMENT_METADATA | ShareGroupTargetAssignmentMetadataKey | groupMetadataManager | newShareGroupTargetAssignmentMetadataRecord, newShareGroupTargetAssignmentMetadataTombstoneRecord |
| SHARE_GROUP_TARGET_ASSIGNMENT_MEMBER | ShareGroupTargetAssignmentMemberKey | groupMetadataManager | newShareGroupTargetAssignmentRecord, newShareGroupTargetAssignmentTombstoneRecord |
| SHARE_GROUP_CURRENT_MEMBER_ASSIGNMENT | ShareGroupCurrentMemberAssignmentKey | groupMetadataManager | newShareGroupCurrentAssignmentRecord, newShareGroupCurrentAssignmentTombstoneRecord |
| SHARE_GROUP_STATE_PARTITION_METADATA | ShareGroupStatePartitionMetadataKey | groupMetadataManager | newShareGroupStatePartitionMetadataRecord, newShareGroupStatePartitionMetadataTombstoneRecord |
| CONSUMER_GROUP_REGULAR_EXPRESSION | ConsumerGroupRegularExpressionKey | groupMetadataManager | newConsumerGroupRegularExpressionRecord, newConsumerGroupRegularExpressionTombstone |
| STREAMS_GROUP_METADATA | StreamsGroupMetadataKey | groupMetadataManager | none |
| STREAMS_GROUP_MEMBER_METADATA | StreamsGroupMemberMetadataKey | groupMetadataManager | none |
| STREAMS_GROUP_TARGET_ASSIGNMENT_METADATA | StreamsGroupTargetAssignmentMetadataKey | groupMetadataManager | none |
| STREAMS_GROUP_TARGET_ASSIGNMENT_MEMBER | StreamsGroupTargetAssignmentMemberKey | groupMetadataManager | none |
| STREAMS_GROUP_CURRENT_MEMBER_ASSIGNMENT | StreamsGroupCurrentMemberAssignmentKey | groupMetadataManager | none |
| STREAMS_GROUP_TOPOLOGY | StreamsGroupTopologyKey | groupMetadataManager | none |

Note the odd name `newConsumerGroupRegularExpressionTombstone` with no "Record" suffix. A summary that normalizes names will get it wrong.

Derivation:

```
python3 - <<'EOF'
import re
L=open('group-coordinator/src/main/java/org/apache/kafka/coordinator/group/GroupCoordinatorShard.java').read().split('\n')
seg='\n'.join(L[1297:1520])
for m in re.finditer(r'case (\w+):\n(.*?)(?=\n\s+case \w+:|\n\s+default:|\n    \}\n)',seg,re.S):
    print(m.group(1), re.search(r'(\w+Manager)\.replay',m.group(2)).group(1), sorted(set(re.findall(r'\((\w+Key)\)',m.group(2)))))
s=open('group-coordinator/src/main/java/org/apache/kafka/coordinator/group/GroupCoordinatorRecordHelpers.java').read()
ms=list(re.finditer(r'public static CoordinatorRecord (\w+)\(',s))
for i,m in enumerate(ms):
    b=s[m.start():(ms[i+1].start() if i+1<len(ms) else len(s))]
    print(m.group(1), sorted(set(re.findall(r'new (\w+Key)\(',b))))
EOF
```

**Grader** `key_list`. Score = 0.4 x recall over 22 case labels with the correct manager + 0.5 x recall over the 30 helper names attributed to the correct case + 0.1 if all 7 "none" rows are marked as having no helper. Minus 0.03 per invented helper or helper on the wrong case. Pass at 0.9.

---

## R4. `batch-accumulator-test-coverage` (source + test)

**Prompt.** Read `raft/src/main/java/org/apache/kafka/raft/internals/BatchAccumulator.java` and `raft/src/test/java/org/apache/kafka/raft/internals/BatchAccumulatorTest.java`. List every public method declared directly on `BatchAccumulator` (exclude the constructor and methods of nested classes). For each, say whether `BatchAccumulatorTest` calls it at least once (yes/no), and for the ones it calls give the number of call sites. Finish with the list of public methods that the test never calls.

**Answer key.** 14 public methods. Never called (4): `appendVotersRecord`, `appendSnapshotHeaderRecord`, `appendSnapshotFooterRecord`, `epoch`.

| Method | Line | Called | Sites |
|---|---|---|---|
| append | 118 | yes | 28 |
| allowDrain | 217 | yes | 1 |
| appendControlMessages | 231 | yes | 4 |
| appendVotersRecord | 318 | no | 0 |
| appendLeaderChangeMessage | 341 | yes | 2 |
| appendSnapshotHeaderRecord | 364 | no | 0 |
| appendSnapshotFooterRecord | 386 | no | 0 |
| forceDrain | 401 | yes | 7 |
| needsDrain | 444 | yes | 15 |
| timeUntilDrain | 455 | yes | 12 |
| epoch | 471 | no | 0 |
| drain | 493 | yes | 11 |
| isEmpty | 535 | yes | 4 |
| close | 543 | yes | 4 |

Derivation:

```
grep -n "^    public " raft/src/main/java/org/apache/kafka/raft/internals/BatchAccumulator.java | grep "("
grep -o "acc\.\(allowDrain\|append\|appendControlMessages\|appendLeaderChangeMessage\|close\|drain\|forceDrain\|isEmpty\|needsDrain\|timeUntilDrain\|epoch\|appendVotersRecord\|appendSnapshotHeaderRecord\|appendSnapshotFooterRecord\)(" raft/src/test/java/org/apache/kafka/raft/internals/BatchAccumulatorTest.java | sort | uniq -c
```

**Grader** `key_list`. Score = 0.4 x recall over 14 names + 0.4 x recall over the 4 never-called methods flagged "no" + 0.2 x fraction of the 10 called methods flagged "yes". Call-site counts accepted within plus or minus 2, not scored. Minus 0.05 per invented public method (private methods and the constructor count as invented) and per called method flagged as uncalled. Pass at 0.9.

---

## W1. `connect-smt-truncate-field`

**Output file.** `connect/transforms/src/main/java/org/apache/kafka/connect/transforms/TruncateField.java`

**Prompt.** Write a new Kafka Connect Single Message Transform `TruncateField` at `connect/transforms/src/main/java/org/apache/kafka/connect/transforms/TruncateField.java`, following the structure and conventions of `connect/transforms/src/main/java/org/apache/kafka/connect/transforms/MaskField.java` exactly (same package, same license header, abstract generic base class with nested `Key` and `Value` subclasses, same helper utilities from `org.apache.kafka.connect.transforms.util`). Spec: (1) Config keys `fields` (LIST, no default, required, Importance.HIGH) and `max.length` (INT, default 255, `ConfigDef.Range.atLeast(1)`, Importance.HIGH). (2) In `configure`, read config through `SimpleConfig` and keep field names in a `Set<String>`. (3) `apply` dispatches to `applySchemaless` via `Requirements.requireMap` when `operatingSchema(record) == null`, else `applyWithSchema` via `Requirements.requireStruct`. (4) Only values that are `instanceof String` and longer than `max.length` are truncated with `String.substring(0, maxLength)`; everything else copies through unchanged; with a schema, the output `Struct` uses the input schema unchanged. (5) Provide `public static final class Key` and `Value` as MaskField does, plus `version()`, `config()` returning `CONFIG_DEF`, and an empty `close()`. Do not write tests and do not modify any existing file.

**Grader** `compile_and_checklist`. Module `:connect:transforms`. Required regexes: `public abstract class TruncateField<R extends ConnectRecord<R>> implements Transformation<R>`, `public static final class Key<R extends ConnectRecord<R>> extends TruncateField<R>`, same for `Value`, `public static final ConfigDef CONFIG_DEF`, literals `"fields"` and `"max.length"`, `atLeast\(1\)`, `configure\(Map<String, \?> props\)`, `public R apply\(R record\)`, `public ConfigDef config\(\)`, `public void close\(\)`, `public String version\(\)`, the three `protected abstract` hooks, `requireMap\(`, `requireStruct\(`. Required behavior: `\.substring\(0, ` and `instanceof String` both present.

---

## W2. `streams-sink-node-metrics`

**Output file.** `streams/src/main/java/org/apache/kafka/streams/processor/internals/metrics/SinkNodeMetrics.java`

**Prompt.** Create `streams/src/main/java/org/apache/kafka/streams/processor/internals/metrics/SinkNodeMetrics.java`, a new node-level metrics registry following the structure of `streams/src/main/java/org/apache/kafka/streams/processor/internals/metrics/ProcessorNodeMetrics.java` exactly (same package, license header, `final` class with private constructor, constants for metric names and descriptions, static sensor factories taking `threadId, taskId, processorNodeId, streamsMetrics`). Spec: (1) `recordsSentSensor(...)`: sensor `records-sent`, `RecordingLevel.DEBUG`, registered with `StreamsMetricsImpl.addInvocationRateAndCountToSensor` in `PROCESSOR_NODE_LEVEL_GROUP` with the node-level tag map (rate description "The average number of records sent per second", total "The total number of records sent"). (2) `bytesSentSensor(...)`: sensor `bytes-sent`, DEBUG, registered with `addRateOfSumAndSumMetricsToSensor`. (3) `sendLatencySensor(...)`: sensor `send-latency`, DEBUG, registered with `addAvgAndMaxToSensor` producing `send-latency-avg` and `send-latency-max`. (4) Build names and descriptions from `private static final String` constants, reusing `TOTAL_DESCRIPTION`, `RATE_DESCRIPTION_PREFIX`, `RATE_DESCRIPTION_SUFFIX`, `AVG_LATENCY_DESCRIPTION`, `MAX_LATENCY_DESCRIPTION`, `LATENCY_SUFFIX` from `StreamsMetricsImpl` where they fit. (5) Include a private `throughputSensor(...)` helper mirroring ProcessorNodeMetrics and use it for `recordsSentSensor`. Do not write tests and do not modify any existing file.

**Grader** `compile_and_checklist`. Module `:streams`. Required: `class SinkNodeMetrics`, `private SinkNodeMetrics\(\)`, the three public factories, `private static Sensor throughputSensor\(`, literals `"records-sent"`, `"bytes-sent"`, `"send-latency"`, `PROCESSOR_NODE_LEVEL_GROUP`, `nodeLevelSensor\(`, `nodeLevelTagMap\(`, `RecordingLevel.DEBUG`. Required behavior: `addInvocationRateAndCountToSensor\(`, `addRateOfSumAndSumMetricsToSensor\(`, and `addAvgAndMaxToSensor\(` each appear at least once.

---

## W3. `remote-log-deletion-config`

**Output file.** `storage/src/main/java/org/apache/kafka/server/log/remote/storage/RemoteLogDeletionConfig.java`

**Prompt.** Create `storage/src/main/java/org/apache/kafka/server/log/remote/storage/RemoteLogDeletionConfig.java`, a configuration class following the conventions of `storage/src/main/java/org/apache/kafka/server/log/remote/storage/RemoteLogManagerConfig.java` (same package and license header; `*_PROP`, `*_DOC` and `DEFAULT_*` public constants; a `public static ConfigDef configDef()` that chains `.define(...)`; a `private final AbstractConfig config` field set by `public RemoteLogDeletionConfig(AbstractConfig config)`; one public getter per key delegating to the wrapped config). Spec: (1) `remote.log.deletion.enable`, BOOLEAN, default false, MEDIUM, getter `isRemoteLogDeletionEnabled()`. (2) `remote.log.deletion.thread.pool.size`, INT, default 2, `atLeast(1)`, MEDIUM, getter `remoteLogDeletionThreadPoolSize()`. (3) `remote.log.deletion.batch.size`, INT, default 100, `atLeast(1)`, LOW, getter `remoteLogDeletionBatchSize()`. (4) `remote.log.deletion.retry.backoff.ms`, LONG, default 500L, `atLeast(0)`, LOW, getter `remoteLogDeletionRetryBackoffMs()`. (5) Every key has a non-empty `*_DOC` passed to `.define(...)`. Do not write tests and do not modify any existing file.

**Grader** `compile_and_checklist`. Module `:storage`. Required: class declaration, `public static ConfigDef configDef\(\)`, the constructor, `private final AbstractConfig config`, the four key literals, the four `_PROP` and four `_DOC` constants, `DEFAULT_` constants with `false`, `2`, `100`, `500L`, the four getters. Required behavior: exactly 4 `\.define\(`, at least 2 `atLeast\(1\)`, at least 1 `atLeast\(0`, and `config.getBoolean\(`, two `config.getInt\(`, one `config.getLong\(`.

---

## E1. `share-session-release-loglevel`

**Prompt.** In `core/src/main/java/kafka/server/share/SharePartitionManager.java`, inside the `releaseSession` method, the log statement with the message `"Share session error for {}: no such share session found"` is logged at `error` level. Change that one call to `warn`. The same message is also logged elsewhere in the file (in `newContext` and `acknowledgeSessionUpdate`); leave those untouched. Make no other changes.

**Trap.** The identical string appears four times: line 426 in `releaseSession` (target), 534 and 568 in `newContext`, 608 in `acknowledgeSessionUpdate` (at debug).

**Expected diff.**

```diff
@@ -423,7 +423,7 @@
         // Remove the share session from the cache.
         ShareSessionKey key = shareSessionKey(groupId, memberId);
         if (cache.remove(key) == null) {
-            log.error("Share session error for {}: no such share session found", key);
+            log.warn("Share session error for {}: no such share session found", key);
             return CompletableFuture.failedFuture(Errors.SHARE_SESSION_NOT_FOUND.exception());
```

**Grader** `exact_diff`. Decoy lines 534, 568, 608 must be unchanged. Any other changed line in the repo fails.

---

## E2. `networkclient-rebootstrap-rename`

**Prompt.** In `clients/src/main/java/org/apache/kafka/clients/NetworkClient.java`, the private method `handleRebootstrap` iterates `this.metadataUpdater.fetchNodes()` with a lambda parameter named `node` and a local `String nodeId`. Rename them to `nodeToClose` and `nodeToCloseId` respectively, so the method matches the naming already used in the rebootstrap branch of `handleApiVersionsResponse`. Only rename inside `handleRebootstrap`; do not touch `handleApiVersionsResponse` or any other method that uses a `nodeId` variable, and do not change the log message text.

**Trap.** `nodeId` is a local in a dozen other methods. Lines 1122 to 1127 in `handleApiVersionsResponse` already use the target names with an identical log line and must not be edited. The log string contains the word `node`, so a regex rename corrupts it.

**Expected diff.**

```diff
@@ -1231,12 +1231,12 @@
     private void handleRebootstrap(List<ClientResponse> responses, long now) {
         if (metadataRecoveryStrategy == MetadataRecoveryStrategy.REBOOTSTRAP && metadataUpdater.needsRebootstrap(now, rebootstrapTriggerMs)) {
-            this.metadataUpdater.fetchNodes().forEach(node -> {
-                String nodeId = node.idString();
-                this.selector.close(nodeId);
-                if (connectionStates.isConnecting(nodeId) || connectionStates.isConnected(nodeId)) {
-                    log.info("Disconnecting from node {} due to client rebootstrap.", nodeId);
-                    processDisconnection(responses, nodeId, now, ChannelState.LOCAL_CLOSE);
+            this.metadataUpdater.fetchNodes().forEach(nodeToClose -> {
+                String nodeToCloseId = nodeToClose.idString();
+                this.selector.close(nodeToCloseId);
+                if (connectionStates.isConnecting(nodeToCloseId) || connectionStates.isConnected(nodeToCloseId)) {
+                    log.info("Disconnecting from node {} due to client rebootstrap.", nodeToCloseId);
+                    processDisconnection(responses, nodeToCloseId, now, ChannelState.LOCAL_CLOSE);
                 }
             });
```

**Grader** `exact_diff`. Lines 1234 to 1239 only. The string `"Disconnecting from node {} due to client rebootstrap."` must appear exactly twice, unchanged.

---

## E3. `locallog-roll-kafka6388-loglevel`

**Prompt.** In `storage/src/main/java/org/apache/kafka/storage/internals/log/LocalLog.java`, the method `roll(Long expectedNextOffset)` logs `"Rolled new log segment at offset {} in {} ms."` at `info` level in two places. Change only the one in the branch that handles an already-existing, empty active segment with the same base offset (the branch guarded by `activeSegment.baseOffset() == newOffset && activeSegment.size() == 0`, with the KAFKA-6388 comment) from `logger.info` to `logger.warn`. Leave the `logger.info` on the normal roll path unchanged. Make no other edits.

**Trap.** Both occurrences are inside the same method (`roll`, lines 584 to 650). Target line 609, decoy line 645.

**Expected diff.**

```diff
@@ -606,7 +606,7 @@
                         updateLogEndOffset(nextOffsetMetadata.messageOffset);
-                        logger.info("Rolled new log segment at offset {} in {} ms.", newOffset, time.hiResClockMs() - start);
+                        logger.warn("Rolled new log segment at offset {} in {} ms.", newOffset, time.hiResClockMs() - start);
                         return newSegment;
```

**Grader** `exact_diff`. Line 609 only. Line 645 unchanged.

---

## D1. `statedirectory-lock-unsynchronized`

**Setup patch** (applied before the run; one word removed):

```diff
@@ -501,7 +501,7 @@
      * @return true if successful
      */
-    synchronized boolean lock(final TaskId taskId) {
+    boolean lock(final TaskId taskId) {
         if (!hasPersistentStores) {
             return true;
         }
```

**Prompt.** Review `streams/src/main/java/org/apache/kafka/streams/processor/internals/StateDirectory.java` for thread-safety problems. Name the method and the lines involved and explain the race.

**Why it is subtle.** `lockedTasksToOwner` is a `ConcurrentHashMap`, so the `get` at 509 and `put` at 523 look individually safe. `unlock`, `clean`, `cleanRemovedTasks`, `removeStartupState` and `cleanOutdatedDirsOnStartup` all stay `synchronized`. Only reading the body of `lock` shows the check-then-act lost its mutual exclusion.

**Expected answer.** Method `StateDirectory.lock(TaskId)`, lines 504 to 525 after the patch, the `get` at 509 followed by the `put` at 523. Two stream threads can both see `lockOwner == null`, both put themselves, both return true, and both believe they own the task's state directory.

**Grader** `bug_report`. Pass requires: names `lock`; cites a line within 10 of 504 to 525; describes two threads both acquiring the lock, or "get then put is not atomic", or "should be putIfAbsent", or "missing synchronized". False positives that do not count: `lockOwner(TaskId)` at 542, `close()` reading `isEmpty()` at 563, `getOrCreateDirectoryForTask` double-check at 396 to 420, `hasStartupTasks()` at 289, the private helpers only called under the monitor, and the `compareAndSet` uses.

---

## D2. `recordaccumulator-tryappend-outside-lock`

**Setup patch** (moves the existing-batch append out of the `synchronized (dq)` block; the variable is renamed to `tryResult` because a later block declares `appendResult` and the original name fails to compile):

```diff
@@ -326,12 +326,12 @@
                     // After taking the lock, validate that the partition hasn't changed and retry.
                     if (partitionChanged(topic, topicInfo, partitionInfo, dq, nowMs, cluster))
                         continue;
-
-                    RecordAppendResult appendResult = tryAppend(timestamp, key, value, headers, callbacks, dq, nowMs);
-                    if (appendResult.appended())
-                        return updatePartitionInfoOnAppend(appendResult, topicInfo, partitionInfo, dq, cluster);
                 }
 
+                RecordAppendResult tryResult = tryAppend(timestamp, key, value, headers, callbacks, dq, nowMs);
+                if (tryResult.appended())
+                    return updatePartitionInfoOnAppend(tryResult, topicInfo, partitionInfo, dq, cluster);
+
                 if (buffer == null) {
```

Both planted files were run through `javac -proc:none` and produce an error list identical to the unmodified originals (classpath-only errors), so neither patch introduces a compile error.

**Prompt.** Review `clients/src/main/java/org/apache/kafka/clients/producer/internals/RecordAccumulator.java` for thread-safety problems. Name the method and the lines involved and explain the race.

**Why it is subtle.** The `synchronized (dq)` block is still there and still guards `partitionChanged`; the second `synchronized (dq)` around `appendNewBatch` is intact; `tryAppend` carries no "must hold lock" comment. Only tracing what `tryAppend` does (`peekLast`, mutating the last batch's `MemoryRecordsBuilder`, `closeForRecordAppends`) against the sender thread's `synchronized (deque)` in `drainBatchesForOneNode` shows the loss of exclusion.

**Expected answer.** Method `append(...)`, lines 325 to 333 after the patch, the `tryAppend` call at 331 running after the block closes at 329. Another producer thread or the sender's drain can interleave with an append to the same batch.

**Grader** `bug_report`. Pass requires: names `append`; cites a line within 10 of 325 to 333; says `tryAppend` or "appending to the last batch" runs outside the deque lock and races another appender or the drain. False positives that do not count: `nextBatchExpiryTimeMs` non-volatile, `nodesDrainIndex` plain HashMap, `muted` HashSet, `computeIfAbsent` on `CopyOnWriteMap`, the `closed` volatile read in `tryAppend`, `batch.abort` after leaving the lock in `abortBatches`, the `AtomicInteger` counters.

---

---

## Prompt variants: named and natural

Every task runs in two variants with the same answer key. **Named** prompts, shown above in each task section, give the file path, which isolates the decision the hook intercepts once the file is known. **Natural** prompts are what a developer would type, with no path, so the session has to find the file first. That is where a search subagent would be used in stock Claude Code, and where the shunt arm has to locate the file before the hook can block it.

Because a natural run can land on the wrong file, every run is also checked for whether the target file was read, grepped, or delegated (from the transcript). A run that never touched the target is scored as a miss regardless of its answer text. Cost and request count are split at the first touch into a **finding phase** and an **answering phase**; the finding phase includes the first request's fixed system-prompt cache write, so compare it across arms, not against zero.

| Id | Natural prompt |
|---|---|
| R1 | How does the broker lifecycle manager in the Kafka server move between broker states? List every event class it handles, which BrokerState each one sets if any, and what enqueues it. What state does it start in? |
| R2 | What are all the broker configuration keys for Kafka's remote log manager (tiered storage), with the type and default of each? Also tell me whether any remote log manager config constants are declared in that config class but never actually registered with the ConfigDef. |
| R3 | When Kafka's group coordinator shard replays records from the log, which record types does it handle, which manager (group metadata or offset metadata) each one goes to, and which of the record helper methods build each record type? Note which record types have no helper. |
| R4 | Which public methods of the Raft BatchAccumulator class does its unit test never exercise? List all of its public methods and say whether each is called from the test. |
| W1 | Add a new Kafka Connect single message transform called TruncateField that truncates string fields to a maximum length. Follow the same pattern the existing MaskField transform uses, including Key and Value variants. Config: `fields` (list, required) and `max.length` (int, default 255, must be at least 1). Only string values longer than the limit get truncated; everything else passes through unchanged. Don't write tests or change existing files. |
| W2 | Add a SinkNodeMetrics registry to Kafka Streams next to the existing node-level metrics classes, following the conventions of the processor node metrics class. It needs three DEBUG-level node sensors: records-sent (invocation rate and count), bytes-sent (rate of sum and sum), and send-latency (avg and max). Don't write tests or change existing files. |
| W3 | Add a RemoteLogDeletionConfig class next to Kafka's remote log manager config, following that class's conventions (PROP/DOC/DEFAULT constants, a static configDef(), a wrapped AbstractConfig, one typed getter per key). Four settings: remote.log.deletion.enable (boolean, default false), remote.log.deletion.thread.pool.size (int, default 2, at least 1), remote.log.deletion.batch.size (int, default 100, at least 1), remote.log.deletion.retry.backoff.ms (long, default 500, at least 0). Each needs a doc string. Don't write tests or change existing files. |
| E1 | In the broker's share partition manager, when a share session is released but it isn't in the cache, we log "Share session error for {}: no such share session found" at error level. That case should be a warning. The same message is logged in a couple of other places; leave those exactly as they are. |
| E2 | In the Kafka client's NetworkClient, the rebootstrap handler loops over nodes using `node` and `nodeId` as names, while the rebootstrap branch of the API-versions response handler already uses `nodeToClose` and `nodeToCloseId`. Make the rebootstrap handler use the same names. Don't touch the API-versions handler, any other method that has a `nodeId`, or the log message text. |
| E3 | In the local log's segment roll logic there's a special case for rolling when the active segment already has the same base offset and is empty (the KAFKA-6388 case). The "Rolled new log segment" message in that branch should be logged at warn instead of info. The same message on the normal roll path should stay at info. Nothing else should change. |
| D1 | Can you review how Kafka Streams locks and unlocks task state directories for thread-safety problems? Name the method and lines involved and explain any race you find. |
| D2 | Can you review the Kafka producer's record accumulator, the part that appends records into batches per partition, for thread-safety problems? Name the method and lines involved and explain any race you find. |

## Self-test before the grid

Each grader runs once against the answer key text (must pass) and once against a deliberately wrong answer built from its own false-positive or decoy list (must fail). Results go in `tasks/<id>.selftest.json`. A grader that passes the wrong answer is a bug in the grader, not a finding.
