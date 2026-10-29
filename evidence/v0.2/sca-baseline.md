SENTINEL SCA Baseline — CIS Ubuntu Linux 24.04

> Dated observation, 29 October 2026. This report records one Wazuh SCA dashboard view. It is not a completed remediation exercise, a full security audit, or part of the original v0.2 infrastructure capture.



Purpose

Wazuh Security Configuration Assessment (SCA) evaluates an endpoint's configuration against a policy. This report records the baseline results visible on the dashboard so they can be reviewed and prioritized later.

SCA is built-in Wazuh functionality. It is not a custom SENTINEL detection rule.

Assessment context

Item	Value

Observation date	29 October 2026
Endpoint	SENTINEL-LINUX01 (Wazuh agent name sentinel-linux01)
Agent ID	002
Operating system	Ubuntu 24.04.5 LTS
Wazuh version	4.14.8
Policy displayed	CIS Ubuntu Linux 24.04 LTS Benchmark v1.0.0


No scan start time, end time, duration, or scan command was recorded, and none is reported here.

Observed results

The values below were read from the Wazuh dashboard during the documented observation. They come from one assessment view and were not independently reproduced.

Result	Count

Passed	108
Failed	118
Not applicable	53
Displayed score	47%


Wazuh SCA dashboard showing the CIS Ubuntu Linux 24.04 LTS Benchmark results

Interpretation

- The assessment shows a mix of passed, failed, and not-applicable policy checks.
- Failed checks are candidates for investigation and prioritization. The counts alone do not establish exploitability or business risk, and passed checks do not guarantee security.
- The displayed score is not a substitute for reviewing individual checks. It is reported as shown and has not been recalculated or reinterpreted.
- This observation does not show that remediation occurred or that the score improved.
- This report does not claim that the SCA findings generated alerts or incidents. The SCA Events tab showed no events in the view inspected during the review. That does not prove SCA never generates events.

Limitations

- This is a single recorded dashboard observation.
- Individual failed check IDs, descriptions, severity, and remediation status are not included, because no separately saved evidence supports them.
- No before-and-after comparison is documented.
- No remediation or rescan result is claimed.
- No overall security guarantee follows from this score, and it says nothing about SENTINEL's detection performance.

Relationship to the SENTINEL milestones

- The screenshot is stored under evidence/v0.2/ for repository organization only.
- The observation was made on 29 October 2026 and is not part of the original v0.2 capture. The historical claims in infrastructure-and-telemetry-foundation.md are unchanged.
- This is a configuration-posture observation, separate from the custom FIM Rule 100002 investigation.

Follow-up work (planned, none completed)

1. Review individual failed checks and identify which are relevant to the lab.
2. Record selected findings with their check IDs, descriptions, evidence, and remediation rationale.
3. Apply changes only after assessing operational impact.
4. Run a subsequent SCA assessment and capture comparable results.
5. Compare results only when the policy and assessment scope are sufficiently comparable.
