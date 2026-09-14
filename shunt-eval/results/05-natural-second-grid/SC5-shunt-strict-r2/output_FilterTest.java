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
import org.apache.kafka.connect.data.SchemaBuilder;
import org.apache.kafka.connect.data.Struct;
import org.apache.kafka.connect.source.SourceRecord;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;

public class FilterTest {

    private final Filter<SourceRecord> xform = new Filter<>();

    @AfterEach
    public void teardown() {
        xform.close();
    }

    @Test
    public void testConfigureDoesNotThrow() {
        assertDoesNotThrow(() -> xform.configure(Map.of()));
    }

    // Apply

    @Test
    public void testApplySchemaless() {
        SourceRecord transformed = xform.apply(createRecordSchemaless("value"));

        assertNull(transformed);
    }

    @Test
    public void testApplyWithSchema() {
        SourceRecord transformed = xform.apply(createRecordWithSchema(Schema.STRING_SCHEMA, "value"));

        assertNull(transformed);
    }

    @Test
    public void testApplyWithStruct() {
        Schema structSchema = SchemaBuilder.struct()
                .field("first", Schema.STRING_SCHEMA)
                .field("second", Schema.INT32_SCHEMA)
                .build();
        Struct original = new Struct(structSchema).put("first", "foo").put("second", 42);

        SourceRecord transformed = xform.apply(createRecordWithSchema(structSchema, original));

        assertNull(transformed);
    }

    @Test
    public void testApplyWithNullValue() {
        SourceRecord transformed = xform.apply(createRecordSchemaless(null));

        assertNull(transformed);
    }

    @Test
    public void testApplyOnKey() {
        SourceRecord transformed = xform.apply(new SourceRecord(null, null, "topic", 0, Schema.STRING_SCHEMA, "key", null, null));

        assertNull(transformed);
    }

    @Test
    public void testFilterVersionRetrievedFromAppInfoParser() {
        assertEquals(AppInfoParser.getVersion(), xform.version());
    }

    private SourceRecord createRecordWithSchema(Schema schema, Object value) {
        return new SourceRecord(null, null, "topic", 0, schema, value);
    }

    private SourceRecord createRecordSchemaless(Object value) {
        return createRecordWithSchema(null, value);
    }
}
