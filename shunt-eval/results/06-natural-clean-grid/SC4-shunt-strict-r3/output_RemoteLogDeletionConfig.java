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
package org.apache.kafka.server.log.remote.storage;

import org.apache.kafka.common.config.AbstractConfig;
import org.apache.kafka.common.config.ConfigDef;

import static org.apache.kafka.common.config.ConfigDef.Importance.MEDIUM;
import static org.apache.kafka.common.config.ConfigDef.Range.atLeast;
import static org.apache.kafka.common.config.ConfigDef.Type.BOOLEAN;
import static org.apache.kafka.common.config.ConfigDef.Type.INT;
import static org.apache.kafka.common.config.ConfigDef.Type.LONG;

public final class RemoteLogDeletionConfig {

    public static final String REMOTE_LOG_DELETION_ENABLE_PROP = "remote.log.deletion.enable";
    public static final String REMOTE_LOG_DELETION_ENABLE_DOC = "Whether to enable deletion of remote log segments.";
    public static final boolean DEFAULT_REMOTE_LOG_DELETION_ENABLE = false;

    public static final String REMOTE_LOG_DELETION_THREAD_POOL_SIZE_PROP = "remote.log.deletion.thread.pool.size";
    public static final String REMOTE_LOG_DELETION_THREAD_POOL_SIZE_DOC = "Size of the thread pool used in scheduling tasks " +
            "to delete remote log segments.";
    public static final int DEFAULT_REMOTE_LOG_DELETION_THREAD_POOL_SIZE = 2;

    public static final String REMOTE_LOG_DELETION_BATCH_SIZE_PROP = "remote.log.deletion.batch.size";
    public static final String REMOTE_LOG_DELETION_BATCH_SIZE_DOC = "The number of remote log segments to delete in a single batch.";
    public static final int DEFAULT_REMOTE_LOG_DELETION_BATCH_SIZE = 100;

    public static final String REMOTE_LOG_DELETION_RETRY_BACKOFF_MS_PROP = "remote.log.deletion.retry.backoff.ms";
    public static final String REMOTE_LOG_DELETION_RETRY_BACKOFF_MS_DOC = "The amount of time in milliseconds to wait before retrying a failed remote log segment deletion.";
    public static final long DEFAULT_REMOTE_LOG_DELETION_RETRY_BACKOFF_MS = 500L;

    private final AbstractConfig config;

    public static ConfigDef configDef() {
        return new ConfigDef()
                .define(REMOTE_LOG_DELETION_ENABLE_PROP,
                        BOOLEAN,
                        DEFAULT_REMOTE_LOG_DELETION_ENABLE,
                        MEDIUM,
                        REMOTE_LOG_DELETION_ENABLE_DOC)
                .define(REMOTE_LOG_DELETION_THREAD_POOL_SIZE_PROP,
                        INT,
                        DEFAULT_REMOTE_LOG_DELETION_THREAD_POOL_SIZE,
                        atLeast(1),
                        MEDIUM,
                        REMOTE_LOG_DELETION_THREAD_POOL_SIZE_DOC)
                .define(REMOTE_LOG_DELETION_BATCH_SIZE_PROP,
                        INT,
                        DEFAULT_REMOTE_LOG_DELETION_BATCH_SIZE,
                        atLeast(1),
                        MEDIUM,
                        REMOTE_LOG_DELETION_BATCH_SIZE_DOC)
                .define(REMOTE_LOG_DELETION_RETRY_BACKOFF_MS_PROP,
                        LONG,
                        DEFAULT_REMOTE_LOG_DELETION_RETRY_BACKOFF_MS,
                        atLeast(0),
                        MEDIUM,
                        REMOTE_LOG_DELETION_RETRY_BACKOFF_MS_DOC);
    }

    public RemoteLogDeletionConfig(AbstractConfig config) {
        this.config = config;
    }

    public boolean isRemoteLogDeletionEnabled() {
        return config.getBoolean(REMOTE_LOG_DELETION_ENABLE_PROP);
    }

    public int remoteLogDeletionThreadPoolSize() {
        return config.getInt(REMOTE_LOG_DELETION_THREAD_POOL_SIZE_PROP);
    }

    public int remoteLogDeletionBatchSize() {
        return config.getInt(REMOTE_LOG_DELETION_BATCH_SIZE_PROP);
    }

    public long remoteLogDeletionRetryBackoffMs() {
        return config.getLong(REMOTE_LOG_DELETION_RETRY_BACKOFF_MS_PROP);
    }
}
