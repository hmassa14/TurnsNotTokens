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
package org.apache.kafka.streams.processor.internals.metrics;

import org.apache.kafka.common.metrics.Sensor;
import org.apache.kafka.common.metrics.Sensor.RecordingLevel;

import java.util.Map;

import static org.apache.kafka.streams.processor.internals.metrics.StreamsMetricsImpl.AVG_LATENCY_DESCRIPTION;
import static org.apache.kafka.streams.processor.internals.metrics.StreamsMetricsImpl.GROUP_PREFIX;
import static org.apache.kafka.streams.processor.internals.metrics.StreamsMetricsImpl.GROUP_SUFFIX;
import static org.apache.kafka.streams.processor.internals.metrics.StreamsMetricsImpl.LATENCY_DESCRIPTION_SUFFIX;
import static org.apache.kafka.streams.processor.internals.metrics.StreamsMetricsImpl.MAX_LATENCY_DESCRIPTION;
import static org.apache.kafka.streams.processor.internals.metrics.StreamsMetricsImpl.TOTAL_DESCRIPTION;
import static org.apache.kafka.streams.processor.internals.metrics.StreamsMetricsImpl.addAvgAndMaxToSensor;
import static org.apache.kafka.streams.processor.internals.metrics.StreamsMetricsImpl.addInvocationRateAndCountToSensor;
import static org.apache.kafka.streams.processor.internals.metrics.StreamsMetricsImpl.addRateOfSumAndSumMetricsToSensor;

public class SinkNodeMetrics {
    private SinkNodeMetrics() {}

    private static final String SINK_NODE_LEVEL_GROUP = GROUP_PREFIX + "sink-node" + GROUP_SUFFIX;

    private static final String RATE_DESCRIPTION_PREFIX = "The average number of ";
    private static final String RATE_DESCRIPTION_SUFFIX = " per second";

    private static final String RECORDS_SENT = "records-sent";
    private static final String RECORDS_SENT_DESCRIPTION = "sent records";
    private static final String RECORDS_SENT_RATE_DESCRIPTION =
        RATE_DESCRIPTION_PREFIX + RECORDS_SENT_DESCRIPTION + RATE_DESCRIPTION_SUFFIX;
    private static final String RECORDS_SENT_TOTAL_DESCRIPTION = TOTAL_DESCRIPTION + RECORDS_SENT_DESCRIPTION;

    private static final String BYTES_SENT = "bytes-sent";
    private static final String BYTES_SENT_DESCRIPTION = "sent bytes";
    private static final String BYTES_SENT_RATE_DESCRIPTION =
        RATE_DESCRIPTION_PREFIX + BYTES_SENT_DESCRIPTION + RATE_DESCRIPTION_SUFFIX;
    private static final String BYTES_SENT_TOTAL_DESCRIPTION = TOTAL_DESCRIPTION + BYTES_SENT_DESCRIPTION;

    private static final String SEND_LATENCY = "send-latency";
    private static final String SEND_LATENCY_DESCRIPTION = "sending records";
    private static final String SEND_LATENCY_AVG_DESCRIPTION =
        AVG_LATENCY_DESCRIPTION + SEND_LATENCY_DESCRIPTION + LATENCY_DESCRIPTION_SUFFIX;
    private static final String SEND_LATENCY_MAX_DESCRIPTION =
        MAX_LATENCY_DESCRIPTION + SEND_LATENCY_DESCRIPTION + LATENCY_DESCRIPTION_SUFFIX;

    public static Sensor recordsSentSensor(final String threadId,
                                           final String taskId,
                                           final String processorNodeId,
                                           final StreamsMetricsImpl streamsMetrics) {
        final Sensor sensor = streamsMetrics.nodeLevelSensor(threadId, taskId, processorNodeId, RECORDS_SENT, RecordingLevel.DEBUG);
        final Map<String, String> tagMap = streamsMetrics.nodeLevelTagMap(threadId, taskId, processorNodeId);
        addInvocationRateAndCountToSensor(
            sensor,
            SINK_NODE_LEVEL_GROUP,
            tagMap,
            RECORDS_SENT,
            RECORDS_SENT_RATE_DESCRIPTION,
            RECORDS_SENT_TOTAL_DESCRIPTION
        );
        return sensor;
    }

    public static Sensor bytesSentSensor(final String threadId,
                                         final String taskId,
                                         final String processorNodeId,
                                         final StreamsMetricsImpl streamsMetrics) {
        final Sensor sensor = streamsMetrics.nodeLevelSensor(threadId, taskId, processorNodeId, BYTES_SENT, RecordingLevel.DEBUG);
        final Map<String, String> tagMap = streamsMetrics.nodeLevelTagMap(threadId, taskId, processorNodeId);
        addRateOfSumAndSumMetricsToSensor(
            sensor,
            SINK_NODE_LEVEL_GROUP,
            tagMap,
            BYTES_SENT,
            BYTES_SENT_RATE_DESCRIPTION,
            BYTES_SENT_TOTAL_DESCRIPTION
        );
        return sensor;
    }

    public static Sensor sendLatencySensor(final String threadId,
                                           final String taskId,
                                           final String processorNodeId,
                                           final StreamsMetricsImpl streamsMetrics) {
        final Sensor sensor = streamsMetrics.nodeLevelSensor(threadId, taskId, processorNodeId, SEND_LATENCY, RecordingLevel.DEBUG);
        final Map<String, String> tagMap = streamsMetrics.nodeLevelTagMap(threadId, taskId, processorNodeId);
        addAvgAndMaxToSensor(
            sensor,
            SINK_NODE_LEVEL_GROUP,
            tagMap,
            SEND_LATENCY,
            SEND_LATENCY_AVG_DESCRIPTION,
            SEND_LATENCY_MAX_DESCRIPTION
        );
        return sensor;
    }
}
