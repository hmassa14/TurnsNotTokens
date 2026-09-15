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
import static org.apache.kafka.streams.processor.internals.metrics.StreamsMetricsImpl.LATENCY_DESCRIPTION_SUFFIX;
import static org.apache.kafka.streams.processor.internals.metrics.StreamsMetricsImpl.LATENCY_SUFFIX;
import static org.apache.kafka.streams.processor.internals.metrics.StreamsMetricsImpl.MAX_LATENCY_DESCRIPTION;
import static org.apache.kafka.streams.processor.internals.metrics.StreamsMetricsImpl.PROCESSOR_NODE_LEVEL_GROUP;
import static org.apache.kafka.streams.processor.internals.metrics.StreamsMetricsImpl.TOTAL_DESCRIPTION;
import static org.apache.kafka.streams.processor.internals.metrics.StreamsMetricsImpl.addAvgAndMaxToSensor;
import static org.apache.kafka.streams.processor.internals.metrics.StreamsMetricsImpl.addInvocationRateAndCountToSensor;
import static org.apache.kafka.streams.processor.internals.metrics.StreamsMetricsImpl.addRateOfSumAndSumMetricsToSensor;

public class SinkNodeMetrics {
    private SinkNodeMetrics() {}

    private static final String RATE_DESCRIPTION_PREFIX = "The average number of ";
    private static final String RATE_DESCRIPTION_SUFFIX = " per second";

    private static final String RECORDS_SENT = "records-sent";
    private static final String RECORDS_SENT_DESCRIPTION = "sent records";
    private static final String RECORDS_SENT_TOTAL_DESCRIPTION = TOTAL_DESCRIPTION + RECORDS_SENT_DESCRIPTION;
    private static final String RECORDS_SENT_RATE_DESCRIPTION =
        RATE_DESCRIPTION_PREFIX + RECORDS_SENT_DESCRIPTION + RATE_DESCRIPTION_SUFFIX;

    private static final String BYTES_SENT = "bytes-sent";
    private static final String BYTES_SENT_DESCRIPTION = "sent bytes";
    private static final String BYTES_SENT_TOTAL_DESCRIPTION = TOTAL_DESCRIPTION + BYTES_SENT_DESCRIPTION;
    private static final String BYTES_SENT_RATE_DESCRIPTION =
        RATE_DESCRIPTION_PREFIX + BYTES_SENT_DESCRIPTION + RATE_DESCRIPTION_SUFFIX;

    private static final String SEND_LATENCY = "send" + LATENCY_SUFFIX;
    private static final String SEND_DESCRIPTION = "calls to send";
    private static final String SEND_AVG_LATENCY_DESCRIPTION = AVG_LATENCY_DESCRIPTION + SEND_DESCRIPTION + LATENCY_DESCRIPTION_SUFFIX;
    private static final String SEND_MAX_LATENCY_DESCRIPTION = MAX_LATENCY_DESCRIPTION + SEND_DESCRIPTION + LATENCY_DESCRIPTION_SUFFIX;

    public static Sensor recordsSentSensor(final String threadId,
                                           final String taskId,
                                           final String processorNodeId,
                                           final StreamsMetricsImpl streamsMetrics) {
        return throughputSensor(
            threadId,
            taskId,
            processorNodeId,
            RECORDS_SENT,
            RECORDS_SENT_RATE_DESCRIPTION,
            RECORDS_SENT_TOTAL_DESCRIPTION,
            RecordingLevel.DEBUG,
            streamsMetrics
        );
    }

    public static Sensor bytesSentSensor(final String threadId,
                                         final String taskId,
                                         final String processorNodeId,
                                         final StreamsMetricsImpl streamsMetrics) {
        final Sensor sensor = streamsMetrics.nodeLevelSensor(threadId, taskId, processorNodeId, BYTES_SENT, RecordingLevel.DEBUG);
        final Map<String, String> tagMap = streamsMetrics.nodeLevelTagMap(threadId, taskId, processorNodeId);
        addRateOfSumAndSumMetricsToSensor(
            sensor,
            PROCESSOR_NODE_LEVEL_GROUP,
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
        final String sensorSuffix = processorNodeId + "-" + SEND_LATENCY;
        final Sensor sensor = streamsMetrics.nodeLevelSensor(threadId, taskId, processorNodeId, sensorSuffix, RecordingLevel.DEBUG);
        final Map<String, String> tagMap = streamsMetrics.nodeLevelTagMap(threadId, taskId, processorNodeId);
        addAvgAndMaxToSensor(
            sensor,
            PROCESSOR_NODE_LEVEL_GROUP,
            tagMap,
            SEND_LATENCY,
            SEND_AVG_LATENCY_DESCRIPTION,
            SEND_MAX_LATENCY_DESCRIPTION
        );
        return sensor;
    }

    private static Sensor throughputSensor(final String threadId,
                                           final String taskId,
                                           final String processorNodeId,
                                           final String operationName,
                                           final String descriptionOfRate,
                                           final String descriptionOfCount,
                                           final RecordingLevel recordingLevel,
                                           final StreamsMetricsImpl streamsMetrics,
                                           final Sensor... parentSensors) {
        // use operation name as sensor suffix and metric name prefix
        final Sensor sensor =
            streamsMetrics.nodeLevelSensor(threadId, taskId, processorNodeId, operationName, recordingLevel, parentSensors);
        final Map<String, String> tagMap = streamsMetrics.nodeLevelTagMap(threadId, taskId, processorNodeId);
        addInvocationRateAndCountToSensor(
            sensor,
            PROCESSOR_NODE_LEVEL_GROUP,
            tagMap,
            operationName,
            descriptionOfRate,
            descriptionOfCount
        );
        return sensor;
    }

}
