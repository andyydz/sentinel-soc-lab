---

name: Detection Request
about: Propose a new security detection or an improvement to an existing rule
title: "[DETECTION] "
labels: detection
assignees: ""

Detection Objective

What security behavior, activity, or threat should this detection identify?

Threat Context

Describe the relevant security scenario.

Relevant Log Source

Examples:

- Wazuh Syscheck / FIM
- Authentication logs
- Linux system logs
- Process activity
- Network telemetry

Specify the actual log source where possible.

Proposed Detection Logic

Describe the proposed logic, conditions, or relevant Wazuh rule configuration.

<!-- Optional: proposed detection rule -->

Expected Alert Behavior

What should trigger an alert?

Include relevant rule IDs, severity levels, or expected event details if known.

Testing Approach

Describe how the detection could be validated using controlled and authorized testing.

False-Positive Considerations

What legitimate activity might trigger this detection?

Evidence or References

Include sanitized logs, documentation, screenshots, or relevant technical references.

Known Limitations

Describe any expected coverage gaps, dependencies, or assumptions.

Additional Context

Any other information relevant to this detection proposal.

Important: A proposed detection is not considered validated until its behavior has been tested and supported by evidence.
