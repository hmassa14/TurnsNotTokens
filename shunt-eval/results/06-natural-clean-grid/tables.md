## Summary across all tasks

### Mean per run, all tasks and variants

Runs per arm: A · stock = 63, B · shunt = 63, B' · shunt strict = 63

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 0.98 | 0.98 | 0.96 |
| Pass rate | 100% | 98% | 97% |
| Pass^k (all reps passed) | yes (k=63) | no (k=63) | no (k=63) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 6,016 | 3,721 | 2,919 |
| Lines read into main context (Read only) | 487 | 260 | 70 |
| Lines read by subagent or worker | 0 | 13 | 4 |
| Tool calls | 5.6 | 7.2 | 8.8 |
| Reads, whole file | 1.1 | 1.0 | 1.0 |
| Reads, targeted | 0.7 | 1.5 | 1.2 |
| Reads blocked by hook | 0.0 | 0.4 | 1.5 |
| Hook bypassed via offset/limit | 0.0 | 0.3 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.1 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 38.8 | 45.1 | 50.8 |
| API requests | 6.1 | 7.7 | 9.2 |
| Longest API call (s) | 12.6 | 12.8 | 12.3 |
| Time in tools (s) | 3.9 | 5.0 | 6.6 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 2.0 |
| **Cost** | | | |
| Total, list price ($) | 0.121 | 0.131 | 0.144 |
| Main model ($) | 0.121 | 0.131 | 0.141 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.003 |
| Finding phase ($) | 0.023 | 0.024 | 0.023 |
| Answering phase ($) | 0.098 | 0.107 | 0.118 |
| Input tokens, uncached | 12 | 15 | 17 |
| Cache write tokens | 19,334 | 16,673 | 15,571 |
| Cache read tokens | 210,351 | 252,402 | 292,565 |
| Output tokens | 3,061 | 3,445 | 3,659 |
| Spotify-style tokens avoided | 0 | 0 | 786 |

## Per example

### CT1 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 2,605 | 2,605 | 2,605 |
| Lines read into main context (Read only) | 268 | 254 | 254 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 8.0 | 7.7 | 7.3 |
| Reads, whole file | 2.0 | 1.7 | 1.7 |
| Reads, targeted | 0.0 | 0.0 | 0.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 46.4 | 52.6 | 50.2 |
| API requests | 8.0 | 8.3 | 8.3 |
| Longest API call (s) | 16.0 | 17.4 | 18.0 |
| Time in tools (s) | 4.6 | 4.4 | 9.2 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.133 | 0.138 | 0.141 |
| Main model ($) | 0.133 | 0.138 | 0.141 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.020 | 0.020 | 0.020 |
| Answering phase ($) | 0.113 | 0.118 | 0.121 |
| Input tokens, uncached | 16 | 17 | 17 |
| Cache write tokens | 15,891 | 16,037 | 17,513 |
| Cache read tokens | 261,200 | 280,593 | 278,035 |
| Output tokens | 4,114 | 4,211 | 4,192 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### CT2 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 0.98 |
| Pass rate | 100% | 100% | 67% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | no (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 3,091 | 3,537 | 3,369 |
| Lines read into main context (Read only) | 369 | 505 | 307 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 11.3 | 12.7 | 15.0 |
| Reads, whole file | 1.7 | 2.0 | 2.3 |
| Reads, targeted | 1.0 | 1.3 | 2.3 |
| Reads blocked by hook | 0.0 | 0.0 | 2.3 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 88.9 | 94.6 | 98.3 |
| API requests | 12.3 | 13.3 | 14.3 |
| Longest API call (s) | 27.0 | 23.2 | 21.6 |
| Time in tools (s) | 6.3 | 18.2 | 18.7 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.234 | 0.259 | 0.273 |
| Main model ($) | 0.234 | 0.259 | 0.273 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.020 | 0.020 | 0.021 |
| Answering phase ($) | 0.214 | 0.239 | 0.253 |
| Input tokens, uncached | 25 | 27 | 29 |
| Cache write tokens | 24,863 | 29,451 | 29,752 |
| Cache read tokens | 453,387 | 520,728 | 573,386 |
| Output tokens | 8,133 | 8,122 | 8,438 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### CT3 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 763 | 763 | 763 |
| Lines read into main context (Read only) | 108 | 108 | 108 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 2.0 | 2.0 | 2.0 |
| Reads, whole file | 1.0 | 1.0 | 1.0 |
| Reads, targeted | 0.0 | 0.0 | 0.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 9.5 | 9.0 | 8.1 |
| API requests | 3.0 | 3.0 | 3.0 |
| Longest API call (s) | 2.7 | 2.7 | 2.3 |
| Time in tools (s) | 0.1 | 0.1 | 0.1 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.042 | 0.041 | 0.040 |
| Main model ($) | 0.042 | 0.041 | 0.040 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.020 | 0.021 | 0.020 |
| Answering phase ($) | 0.022 | 0.020 | 0.020 |
| Input tokens, uncached | 6 | 6 | 6 |
| Cache write tokens | 8,456 | 7,986 | 7,903 |
| Cache read tokens | 84,532 | 84,181 | 84,098 |
| Output tokens | 376 | 383 | 337 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### HM1 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 3,231 | 3,719 | 2,607 |
| Lines read into main context (Read only) | 203 | 237 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 3.3 | 3.0 | 4.7 |
| Reads, whole file | 0.0 | 0.0 | 0.0 |
| Reads, targeted | 1.3 | 1.0 | 2.0 |
| Reads blocked by hook | 0.0 | 0.0 | 2.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 13.1 | 12.3 | 19.7 |
| API requests | 4.3 | 4.0 | 5.7 |
| Longest API call (s) | 3.8 | 3.2 | 5.0 |
| Time in tools (s) | 0.2 | 0.2 | 0.3 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.062 | 0.061 | 0.072 |
| Main model ($) | 0.062 | 0.061 | 0.072 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.020 | 0.020 | 0.020 |
| Answering phase ($) | 0.042 | 0.040 | 0.052 |
| Input tokens, uncached | 9 | 8 | 11 |
| Cache write tokens | 11,173 | 11,925 | 11,082 |
| Cache read tokens | 128,917 | 119,229 | 170,443 |
| Output tokens | 797 | 703 | 1,029 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### HM2 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 2,006 | 1,279 | 1,958 |
| Lines read into main context (Read only) | 17 | 17 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 3.7 | 3.3 | 5.0 |
| Reads, whole file | 0.0 | 0.0 | 0.0 |
| Reads, targeted | 1.0 | 0.7 | 1.0 |
| Reads blocked by hook | 0.0 | 0.0 | 1.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 14.4 | 14.0 | 24.5 |
| API requests | 4.7 | 4.3 | 6.0 |
| Longest API call (s) | 4.2 | 4.3 | 6.7 |
| Time in tools (s) | 0.2 | 0.2 | 0.2 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.064 | 0.059 | 0.080 |
| Main model ($) | 0.064 | 0.059 | 0.080 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.021 | 0.021 | 0.021 |
| Answering phase ($) | 0.043 | 0.038 | 0.059 |
| Input tokens, uncached | 9 | 9 | 12 |
| Cache write tokens | 9,993 | 9,313 | 11,020 |
| Cache read tokens | 139,814 | 127,776 | 182,909 |
| Output tokens | 1,077 | 1,055 | 1,605 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### HM3 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 1,710 | 1,663 | 1,348 |
| Lines read into main context (Read only) | 97 | 63 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 3.0 | 3.0 | 4.0 |
| Reads, whole file | 0.0 | 0.0 | 0.0 |
| Reads, targeted | 1.0 | 0.7 | 0.7 |
| Reads blocked by hook | 0.0 | 0.0 | 0.7 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 10.0 | 14.0 | 16.3 |
| API requests | 4.0 | 4.0 | 5.0 |
| Longest API call (s) | 3.1 | 4.6 | 4.2 |
| Time in tools (s) | 0.2 | 0.2 | 0.2 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.053 | 0.053 | 0.061 |
| Main model ($) | 0.053 | 0.053 | 0.061 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.020 | 0.021 | 0.021 |
| Answering phase ($) | 0.033 | 0.033 | 0.041 |
| Input tokens, uncached | 8 | 8 | 10 |
| Cache write tokens | 8,872 | 8,917 | 8,812 |
| Cache read tokens | 115,868 | 116,127 | 146,365 |
| Output tokens | 736 | 749 | 1,014 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### HM4 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 13,423 | 2,885 | 2,347 |
| Lines read into main context (Read only) | 1,123 | 192 | 53 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 9.0 | 10.3 | 13.0 |
| Reads, whole file | 1.0 | 1.0 | 1.0 |
| Reads, targeted | 1.3 | 3.0 | 2.0 |
| Reads blocked by hook | 0.0 | 1.0 | 2.3 |
| Hook bypassed via offset/limit | 0.0 | 1.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 71.1 | 86.1 | 85.1 |
| API requests | 9.7 | 10.3 | 13.7 |
| Longest API call (s) | 20.0 | 32.6 | 18.7 |
| Time in tools (s) | 0.8 | 0.6 | 0.7 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.227 | 0.186 | 0.208 |
| Main model ($) | 0.227 | 0.186 | 0.208 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.038 | 0.027 | 0.032 |
| Answering phase ($) | 0.190 | 0.159 | 0.176 |
| Input tokens, uncached | 19 | 21 | 27 |
| Cache write tokens | 34,076 | 16,525 | 17,248 |
| Cache read tokens | 393,842 | 335,148 | 455,188 |
| Output tokens | 6,305 | 7,781 | 7,356 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### HM5 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 14,223 | 9,400 | 5,030 |
| Lines read into main context (Read only) | 1,011 | 632 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 7.7 | 14.7 | 11.3 |
| Reads, whole file | 0.7 | 1.7 | 0.3 |
| Reads, targeted | 2.0 | 5.0 | 2.7 |
| Reads blocked by hook | 0.0 | 1.3 | 3.0 |
| Hook bypassed via offset/limit | 0.0 | 1.3 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 100.8 | 117.8 | 92.3 |
| API requests | 8.7 | 15.7 | 12.3 |
| Longest API call (s) | 38.4 | 31.7 | 36.6 |
| Time in tools (s) | 0.8 | 0.8 | 0.9 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.233 | 0.294 | 0.207 |
| Main model ($) | 0.233 | 0.294 | 0.207 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.020 | 0.020 | 0.023 |
| Answering phase ($) | 0.213 | 0.274 | 0.184 |
| Input tokens, uncached | 17 | 31 | 25 |
| Cache write tokens | 33,007 | 29,101 | 18,577 |
| Cache read tokens | 329,711 | 648,496 | 413,702 |
| Output tokens | 8,431 | 9,169 | 7,728 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### ND1 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 586 | 719 | 655 |
| Lines read into main context (Read only) | 42 | 22 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 2.7 | 3.3 | 5.0 |
| Reads, whole file | 0.0 | 0.0 | 0.0 |
| Reads, targeted | 1.0 | 1.0 | 1.3 |
| Reads blocked by hook | 0.0 | 0.0 | 1.3 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 10.6 | 13.9 | 20.9 |
| API requests | 3.7 | 4.3 | 6.0 |
| Longest API call (s) | 2.8 | 3.1 | 4.3 |
| Time in tools (s) | 0.1 | 0.2 | 0.2 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.051 | 0.052 | 0.068 |
| Main model ($) | 0.051 | 0.052 | 0.068 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.034 | 0.021 | 0.020 |
| Answering phase ($) | 0.017 | 0.032 | 0.047 |
| Input tokens, uncached | 7 | 9 | 12 |
| Cache write tokens | 8,876 | 7,672 | 8,173 |
| Cache read tokens | 105,283 | 124,778 | 176,808 |
| Output tokens | 746 | 821 | 1,189 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### ND2 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 3,652 | 2,958 | 1,184 |
| Lines read into main context (Read only) | 30 | 0 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 4.0 | 2.7 | 2.0 |
| Reads, whole file | 0.0 | 0.0 | 0.0 |
| Reads, targeted | 0.3 | 0.0 | 0.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 15.7 | 11.3 | 10.0 |
| API requests | 5.0 | 3.3 | 3.0 |
| Longest API call (s) | 3.4 | 3.5 | 3.1 |
| Time in tools (s) | 0.2 | 0.2 | 0.1 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.070 | 0.055 | 0.044 |
| Main model ($) | 0.070 | 0.055 | 0.044 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.020 | 0.021 | 0.021 |
| Answering phase ($) | 0.050 | 0.034 | 0.023 |
| Input tokens, uncached | 10 | 7 | 6 |
| Cache write tokens | 12,478 | 11,637 | 8,548 |
| Cache read tokens | 146,961 | 94,765 | 84,073 |
| Output tokens | 920 | 705 | 560 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### ND3 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 1,437 | 1,339 | 1,460 |
| Lines read into main context (Read only) | 57 | 52 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 4.3 | 5.0 | 7.3 |
| Reads, whole file | 0.0 | 0.0 | 0.0 |
| Reads, targeted | 1.0 | 1.0 | 1.0 |
| Reads blocked by hook | 0.0 | 0.0 | 1.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 14.1 | 18.6 | 18.7 |
| API requests | 5.0 | 5.0 | 6.7 |
| Longest API call (s) | 2.8 | 4.2 | 3.3 |
| Time in tools (s) | 0.3 | 0.3 | 0.4 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.062 | 0.073 | 0.078 |
| Main model ($) | 0.062 | 0.073 | 0.078 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.040 | 0.032 | 0.039 |
| Answering phase ($) | 0.022 | 0.041 | 0.039 |
| Input tokens, uncached | 10 | 10 | 13 |
| Cache write tokens | 9,487 | 13,043 | 10,121 |
| Cache read tokens | 146,709 | 153,191 | 202,431 |
| Output tokens | 887 | 925 | 1,225 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### ND4 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 1,411 | 3,168 | 1,952 |
| Lines read into main context (Read only) | 72 | 235 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 3.7 | 3.7 | 6.7 |
| Reads, whole file | 0.0 | 0.0 | 0.0 |
| Reads, targeted | 1.3 | 1.3 | 2.0 |
| Reads blocked by hook | 0.0 | 0.0 | 2.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 16.8 | 13.9 | 23.9 |
| API requests | 4.3 | 4.3 | 7.3 |
| Longest API call (s) | 4.0 | 3.3 | 3.8 |
| Time in tools (s) | 0.2 | 0.2 | 0.4 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.057 | 0.064 | 0.087 |
| Main model ($) | 0.057 | 0.064 | 0.087 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.025 | 0.028 | 0.025 |
| Answering phase ($) | 0.032 | 0.036 | 0.063 |
| Input tokens, uncached | 9 | 9 | 15 |
| Cache write tokens | 9,004 | 11,891 | 10,601 |
| Cache read tokens | 127,764 | 127,336 | 224,349 |
| Output tokens | 931 | 874 | 1,604 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### SB1 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 0.70 |
| Pass rate | 100% | 100% | 67% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | no (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 10,106 | 10,620 | 7,699 |
| Lines read into main context (Read only) | 617 | 616 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 3.7 | 6.0 | 11.7 |
| Reads, whole file | 1.0 | 1.0 | 1.0 |
| Reads, targeted | 0.0 | 2.0 | 2.7 |
| Reads blocked by hook | 0.0 | 1.0 | 3.7 |
| Hook bypassed via offset/limit | 0.0 | 1.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.3 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 36.5 | 65.6 | 96.8 |
| API requests | 4.7 | 7.0 | 12.7 |
| Longest API call (s) | 15.2 | 26.4 | 17.9 |
| Time in tools (s) | 0.7 | 0.6 | 12.7 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 11.3 |
| **Cost** | | | |
| Total, list price ($) | 0.141 | 0.190 | 0.262 |
| Main model ($) | 0.141 | 0.190 | 0.248 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.013 |
| Finding phase ($) | 0.020 | 0.021 | 0.021 |
| Answering phase ($) | 0.121 | 0.169 | 0.228 |
| Input tokens, uncached | 9 | 14 | 25 |
| Cache write tokens | 27,548 | 29,396 | 29,864 |
| Cache read tokens | 166,412 | 247,272 | 468,388 |
| Output tokens | 3,869 | 6,653 | 8,001 |
| Spotify-style tokens avoided | 0 | 0 | 2,192 |

### SB2 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 0.90 | 0.93 | 0.87 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 8,571 | 1,936 | 3,005 |
| Lines read into main context (Read only) | 754 | 160 | 240 |
| Lines read by subagent or worker | 0 | 271 | 80 |
| Tool calls | 4.7 | 12.3 | 16.3 |
| Reads, whole file | 2.7 | 3.7 | 3.7 |
| Reads, targeted | 0.0 | 1.3 | 1.3 |
| Reads blocked by hook | 0.0 | 1.0 | 2.3 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.3 | 0.3 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 24.3 | 51.3 | 46.9 |
| API requests | 3.7 | 10.7 | 14.7 |
| Longest API call (s) | 12.6 | 15.1 | 17.9 |
| Time in tools (s) | 0.5 | 0.6 | 0.7 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.089 | 0.166 | 0.205 |
| Main model ($) | 0.089 | 0.166 | 0.205 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.021 | 0.048 | 0.032 |
| Answering phase ($) | 0.069 | 0.118 | 0.173 |
| Input tokens, uncached | 7 | 9 | 7 |
| Cache write tokens | 19,252 | 9,059 | 9,263 |
| Cache read tokens | 110,837 | 135,807 | 105,766 |
| Output tokens | 1,915 | 2,238 | 1,668 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### SB3 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 0.82 | 0.82 | 0.82 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 2,007 | 2,007 | 1,992 |
| Lines read into main context (Read only) | 266 | 214 | 189 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 6.3 | 5.3 | 5.0 |
| Reads, whole file | 3.3 | 2.3 | 2.0 |
| Reads, targeted | 0.0 | 0.0 | 0.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 32.9 | 24.5 | 24.0 |
| API requests | 5.3 | 4.7 | 4.3 |
| Longest API call (s) | 12.2 | 9.7 | 9.9 |
| Time in tools (s) | 0.5 | 0.4 | 0.5 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.088 | 0.074 | 0.073 |
| Main model ($) | 0.088 | 0.074 | 0.073 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.021 | 0.024 | 0.021 |
| Answering phase ($) | 0.067 | 0.050 | 0.052 |
| Input tokens, uncached | 11 | 9 | 9 |
| Cache write tokens | 12,260 | 10,876 | 11,000 |
| Cache read tokens | 163,043 | 139,378 | 128,209 |
| Output tokens | 2,501 | 1,906 | 1,968 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### SB4 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 1,961 | 1,970 | 1,991 |
| Lines read into main context (Read only) | 189 | 189 | 189 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 8.0 | 6.7 | 8.7 |
| Reads, whole file | 2.0 | 2.0 | 2.0 |
| Reads, targeted | 0.0 | 0.0 | 0.0 |
| Reads blocked by hook | 0.0 | 0.0 | 0.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 68.2 | 54.4 | 63.5 |
| API requests | 7.7 | 6.0 | 8.3 |
| Longest API call (s) | 10.4 | 14.7 | 13.0 |
| Time in tools (s) | 41.5 | 26.5 | 26.5 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.109 | 0.103 | 0.123 |
| Main model ($) | 0.109 | 0.103 | 0.123 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.020 | 0.021 | 0.021 |
| Answering phase ($) | 0.088 | 0.082 | 0.102 |
| Input tokens, uncached | 15 | 12 | 17 |
| Cache write tokens | 14,165 | 14,718 | 15,405 |
| Cache read tokens | 241,477 | 188,871 | 273,326 |
| Output tokens | 2,481 | 2,848 | 2,942 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### SC1 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 9,099 | 8,643 | 2,745 |
| Lines read into main context (Read only) | 786 | 717 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 2.7 | 7.7 | 8.7 |
| Reads, whole file | 1.0 | 1.0 | 1.0 |
| Reads, targeted | 0.3 | 3.3 | 1.3 |
| Reads blocked by hook | 0.0 | 1.0 | 2.3 |
| Hook bypassed via offset/limit | 0.0 | 1.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 1.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 39.6 | 53.7 | 73.9 |
| API requests | 3.7 | 8.7 | 9.7 |
| Longest API call (s) | 24.4 | 16.4 | 15.5 |
| Time in tools (s) | 0.3 | 0.3 | 22.0 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 19.7 |
| **Cost** | | | |
| Total, list price ($) | 0.113 | 0.163 | 0.163 |
| Main model ($) | 0.113 | 0.163 | 0.138 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.025 |
| Finding phase ($) | 0.020 | 0.021 | 0.020 |
| Answering phase ($) | 0.092 | 0.143 | 0.118 |
| Input tokens, uncached | 7 | 17 | 19 |
| Cache write tokens | 20,139 | 22,295 | 13,957 |
| Cache read tokens | 112,858 | 293,479 | 301,054 |
| Output tokens | 3,973 | 4,902 | 4,298 |
| Spotify-style tokens avoided | 0 | 0 | 6,647 |

### SC2 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 0.87 | 0.88 | 0.87 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 12,651 | 6,746 | 4,193 |
| Lines read into main context (Read only) | 1,274 | 590 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 11.7 | 12.7 | 14.7 |
| Reads, whole file | 1.0 | 0.3 | 0.0 |
| Reads, targeted | 3.0 | 3.3 | 2.0 |
| Reads blocked by hook | 0.0 | 0.0 | 2.0 |
| Hook bypassed via offset/limit | 0.0 | 0.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 73.8 | 68.1 | 77.7 |
| API requests | 12.0 | 13.3 | 15.7 |
| Longest API call (s) | 16.2 | 15.8 | 16.7 |
| Time in tools (s) | 0.6 | 0.6 | 0.9 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.262 | 0.237 | 0.244 |
| Main model ($) | 0.262 | 0.237 | 0.244 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.022 | 0.028 | 0.023 |
| Answering phase ($) | 0.241 | 0.209 | 0.221 |
| Input tokens, uncached | 24 | 27 | 31 |
| Cache write tokens | 37,824 | 26,470 | 23,670 |
| Cache read tokens | 490,464 | 508,071 | 571,660 |
| Output tokens | 6,944 | 6,957 | 7,052 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### SC3 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 0.84 | 1.00 |
| Pass rate | 100% | 67% | 100% |
| Pass^k (all reps passed) | yes (k=3) | no (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 13,798 | 2,324 | 2,220 |
| Lines read into main context (Read only) | 1,412 | 37 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 4.0 | 8.0 | 7.7 |
| Reads, whole file | 2.0 | 1.3 | 1.7 |
| Reads, targeted | 0.0 | 0.3 | 0.3 |
| Reads blocked by hook | 0.0 | 1.3 | 2.0 |
| Hook bypassed via offset/limit | 0.0 | 0.3 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 28.0 | 27.9 | 36.8 |
| API requests | 4.0 | 8.0 | 7.7 |
| Longest API call (s) | 11.0 | 5.1 | 8.6 |
| Time in tools (s) | 0.3 | 0.3 | 0.4 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.122 | 0.100 | 0.100 |
| Main model ($) | 0.122 | 0.100 | 0.100 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.020 | 0.020 | 0.020 |
| Answering phase ($) | 0.102 | 0.080 | 0.079 |
| Input tokens, uncached | 8 | 16 | 15 |
| Cache write tokens | 28,635 | 11,935 | 11,776 |
| Cache read tokens | 135,199 | 242,848 | 234,441 |
| Output tokens | 2,340 | 2,178 | 2,333 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### SC4 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 9,868 | 6,077 | 8,108 |
| Lines read into main context (Read only) | 617 | 337 | 0 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 3.0 | 7.7 | 9.3 |
| Reads, whole file | 1.0 | 1.0 | 1.3 |
| Reads, targeted | 0.0 | 3.7 | 1.0 |
| Reads blocked by hook | 0.0 | 1.0 | 2.0 |
| Hook bypassed via offset/limit | 0.0 | 1.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 0.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 22.3 | 35.5 | 58.6 |
| API requests | 4.0 | 8.7 | 10.3 |
| Longest API call (s) | 14.4 | 14.2 | 15.3 |
| Time in tools (s) | 0.2 | 0.3 | 6.0 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 0.0 |
| **Cost** | | | |
| Total, list price ($) | 0.118 | 0.149 | 0.190 |
| Main model ($) | 0.118 | 0.149 | 0.190 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.000 |
| Finding phase ($) | 0.020 | 0.021 | 0.021 |
| Answering phase ($) | 0.098 | 0.128 | 0.169 |
| Input tokens, uncached | 8 | 17 | 21 |
| Cache write tokens | 26,546 | 21,375 | 26,713 |
| Cache read tokens | 131,863 | 298,488 | 372,336 |
| Output tokens | 2,546 | 3,578 | 4,825 |
| Spotify-style tokens avoided | 0 | 0 | 0 |

### SC5 · natural prompt

| | A · stock | B · shunt | B' · shunt strict |
|---|---|---|---|
| **Performance** | | | |
| Score | 1.00 | 1.00 | 1.00 |
| Pass rate | 100% | 100% | 100% |
| Pass^k (all reps passed) | yes (k=3) | yes (k=3) | yes (k=3) |
| Found target file | 100% | 100% | 100% |
| Lucky passes (right answer, target never found) | 0% | 0% | 0% |
| Target content into main context, any tool (tokens, chars/4) | 10,133 | 3,778 | 4,068 |
| Lines read into main context (Read only) | 911 | 289 | 140 |
| Lines read by subagent or worker | 0 | 0 | 0 |
| Tool calls | 11.0 | 14.3 | 18.7 |
| Reads, whole file | 3.0 | 2.0 | 2.7 |
| Reads, targeted | 0.0 | 2.3 | 1.0 |
| Reads blocked by hook | 0.0 | 1.0 | 2.0 |
| Hook bypassed via offset/limit | 0.0 | 1.0 | 0.0 |
| Subagent or worker calls | 0.0 | 0.0 | 1.0 |
| Re-read after delegation | 0.0 | 0.0 | 0.0 |
| **Latency** | | | |
| Wall clock (s) | 77.0 | 107.1 | 119.7 |
| API requests | 10.0 | 14.3 | 18.3 |
| Longest API call (s) | 19.4 | 17.1 | 14.8 |
| Time in tools (s) | 24.4 | 50.7 | 37.6 |
| Time in worker or subagent (s) | 0.0 | 0.0 | 10.0 |
| **Cost** | | | |
| Total, list price ($) | 0.213 | 0.235 | 0.301 |
| Main model ($) | 0.213 | 0.235 | 0.279 |
| Worker or subagent ($) | 0.000 | 0.000 | 0.022 |
| Finding phase ($) | 0.020 | 0.039 | 0.020 |
| Answering phase ($) | 0.192 | 0.196 | 0.259 |
| Input tokens, uncached | 20 | 29 | 37 |
| Cache write tokens | 33,472 | 30,520 | 25,991 |
| Cache read tokens | 431,224 | 513,892 | 696,895 |
| Output tokens | 4,256 | 5,593 | 7,486 |
| Spotify-style tokens avoided | 0 | 0 | 7,668 |

