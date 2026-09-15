/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements. See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.kafka.connect.transforms;

import org.apache.kafka.common.utils.internals.AppInfoParser;
import org.apache.kafka.connect.data.Schema;
import org.apache.kafka.connect.header.ConnectHeaders;
import org.apache.kafka.connect.source.SourceRecord;

import org.junit.jupiter.api.Test;

import java.util.Collections;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

public class FilterTest {

    private final Filter<SourceRecord> xform = new Filter<>();

    @Test
    public void filterDropsRecordWithHeaders() {
        xform.configure(Collections.emptyMap());
        ConnectHeaders headers = new ConnectHeaders();
        headers.addString("existing", "existing-value");

        SourceRecord original = sourceRecord(headers);
        SourceRecord xformed = xform.apply(original);
        assertNull(xformed);
    }

    @Test
    public void filterDropsRecordWithoutHeaders() {
        xform.configure(Collections.emptyMap());
        ConnectHeaders headers = new ConnectHeaders();

        SourceRecord original = sourceRecord(headers);
        SourceRecord xformed = xform.apply(original);
        assertNull(xformed);
    }

    private SourceRecord sourceRecord(ConnectHeaders headers) {
        Map<String, ?> sourcePartition = Map.of("foo", "bar");
        Map<String, ?> sourceOffset = Map.of("baz", "quxx");
        String topic = "topic";
        Integer partition = 0;
        Schema keySchema = null;
        Object key = "key";
        Schema valueSchema = null;
        Object value = "value";
        Long timestamp = 0L;

        return new SourceRecord(sourcePartition, sourceOffset, topic, partition,
                keySchema, key, valueSchema, value, timestamp, headers);
    }

    @Test
    public void testFilterVersionRetrievedFromAppInfoParser() {
        assertEquals(AppInfoParser.getVersion(), xform.version());
    }
}
