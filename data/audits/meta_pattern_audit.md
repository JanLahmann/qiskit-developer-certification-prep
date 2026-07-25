# Meta-pattern audit (test-wise guesser simulation)

*Repo-only quality artifact — not linked from the website.*

Scope: **s7** — 24 questions (21 single-answer, 3 multi-select). Random-guess baseline: **24.1%**. Exam pass line: **69%**.

## Blind-guesser scores

| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |
|---|---|---|---|
| position_C | 39.5% | 72% | 35.2% |
| similar_twin_member | 40.7% | 64% | 34.8% |
| position_A | 32.9% | 72% | 30.4% |
| position_B | 32.5% | 73% | 30.2% |
| position_D | 32.5% | 73% | 30.2% |
| stem_keyword_overlap | 29.1% | 96% | 28.9% |
| longest_option | 25.0% | 100% | 25.0% |
| shortest_option | 25.0% | 100% | 25.0% |
| avoid_longest | 24.0% | 93% | 24.0% |
| odd_one_out | 6.3% | 100% | 6.3% |
| most_hedged | 0.0% | 4% | – |
| avoid_hedged | 25.0% | 4% | – |
| least_absolute | 0.0% | 5% | – |
| most_absolute | 30.0% | 5% | – |
| code_formatted_only | – | 0% | – |
| numeric_middle | 44.6% | 18% | – |

## Verdicts

- ✅ no aggregate biases above thresholds

## Flagged questions (5)

- `s7-q015` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 59 chars vs longest distractor 52, ratio 1.13) (in >=1 displayed pool variant)
- `s7-q020` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 55 chars vs longest distractor 50, ratio 1.10) (in >=1 displayed pool variant)
- `s7-q023` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 72 chars vs longest distractor 62, ratio 1.16) (in >=1 displayed pool variant)
- `s7-q024` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 79 chars vs longest distractor 68, ratio 1.16) (in >=1 displayed pool variant)
- `s7-q028` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 107 chars vs longest distractor 97, ratio 1.10) (in >=1 displayed pool variant)
