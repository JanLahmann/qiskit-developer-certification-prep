# Meta-pattern audit (test-wise guesser simulation)

*Repo-only quality artifact — not linked from the website.*

Scope: **s1** — 37 questions (32 single-answer, 5 multi-select). Random-guess baseline: **25.0%**. Exam pass line: **69%**.

## Blind-guesser scores

| Heuristic | EV accuracy (answered) | Coverage | Est. exam score |
|---|---|---|---|
| similar_twin_member | 46.8% | 39% | 33.6% |
| position_B | 35.1% | 80% | 33.1% |
| position_A | 31.5% | 79% | 30.2% |
| position_D | 31.5% | 79% | 30.2% |
| position_C | 27.7% | 79% | 27.1% |
| avoid_longest | 26.5% | 100% | 26.5% |
| most_absolute | 26.5% | 28% | 25.4% |
| least_absolute | 20.5% | 28% | 23.8% |
| shortest_option | 22.9% | 100% | 22.9% |
| longest_option | 22.8% | 100% | 22.8% |
| code_formatted_only | 15.3% | 35% | 21.6% |
| stem_keyword_overlap | 18.9% | 73% | 20.5% |
| odd_one_out | 13.4% | 100% | 13.4% |
| most_hedged | 0.0% | 20% | – |
| avoid_hedged | 41.0% | 20% | – |
| numeric_middle | 0.0% | 4% | – |

## Verdicts

- ✅ no aggregate biases above thresholds

## Flagged questions (8)

- `s1-q012` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 82 chars vs longest distractor 70, ratio 1.17) (in >=1 displayed pool variant)
- `s1-q015` (mcq) — **length_tell** [low]: correct option(s) strictly longest (min correct 70 chars vs longest distractor 69, ratio 1.01) (in >=1 displayed pool variant)
- `s1-q016` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 80 chars vs longest distractor 65, ratio 1.23) (in >=1 displayed pool variant)
- `s1-q020` (spot-bug) — **length_tell** [low]: correct option(s) strictly longest (min correct 93 chars vs longest distractor 81, ratio 1.15) (in >=1 displayed pool variant)
- `s1-q026` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 69 chars vs longest distractor 60, ratio 1.15) (in >=1 displayed pool variant)
- `s1-q035` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 85 chars vs longest distractor 79, ratio 1.08) (in >=1 displayed pool variant)
- `s1-q037` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 71 chars vs longest distractor 70, ratio 1.01) (in >=1 displayed pool variant)
- `s1-q040` (predict-output) — **length_tell** [low]: correct option(s) strictly longest (min correct 41 chars vs longest distractor 34, ratio 1.21) (in >=1 displayed pool variant)
