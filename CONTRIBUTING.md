Contributing to SENTINEL SOC Lab

Thank you for your interest in contributing to SENTINEL SOC Lab.

SENTINEL is an independently developed cybersecurity home lab focused on practical Security Operations Center (SOC) workflows, including security monitoring, threat detection, alert investigation, evidence handling, and incident response.

Contributions, suggestions, documentation improvements, and technical feedback are welcome.

Project Scope

Contributions should align with the project's objectives:

- Security monitoring and log analysis.
- Wazuh configuration and detection engineering.
- Incident investigation and evidence documentation.
- Controlled security testing and attack simulation.
- SOC automation and workflow improvements.
- Incident response procedures.
- Technical documentation and reproducible demonstrations.

How to Contribute

1. Open an Issue

Before making significant changes, open an issue describing:

- The problem or proposed improvement.
- Why it is relevant to SENTINEL.
- The expected technical outcome.
- Any supporting evidence or references.

For smaller documentation corrections, a pull request may be sufficient.

2. Fork and Clone

Fork the repository and clone your fork:

git clone https://github.com/<your-username>/sentinel-soc-lab.git
cd sentinel-soc-lab

Create a branch for your contribution:

git checkout -b feature/description

3. Make Your Changes

Please follow these guidelines:

- Keep changes focused and clearly scoped.
- Follow the existing repository structure.
- Document configuration changes and dependencies.
- Include relevant validation steps.
- Preserve existing evidence and investigation history.
- Avoid introducing unnecessary dependencies.
- Do not include credentials, private keys, tokens, or personal information.

4. Test Your Changes

Where applicable:

- Validate configuration syntax.
- Test detection rules using controlled events.
- Document the testing environment.
- Include expected and observed results.
- Record limitations and unresolved issues.
- Avoid claiming a detection works without supporting validation.

5. Submit a Pull Request

Provide a clear description of:

- What changed.
- Why the change was necessary.
- Files or components affected.
- Testing performed.
- Evidence or screenshots, where appropriate.
- Known limitations.

Pull requests will be reviewed for technical accuracy, project relevance, security implications, and documentation quality.

Detection Engineering Guidelines

Detection contributions should include, where applicable:

- Detection objective.
- Relevant log source.
- Detection logic or rule configuration.
- Expected alert behavior.
- Controlled test procedure.
- Observed results.
- False-positive considerations.
- Known limitations.

Do not present an untested detection as validated.

Investigation and Evidence Guidelines

Investigation-related contributions should:

- Distinguish observed facts from assumptions.
- Preserve original evidence where possible.
- Include timestamps and relevant system context.
- Reference evidence files consistently.
- Avoid unsupported conclusions.
- Document gaps and limitations honestly.

Screenshots should support documented findings rather than replace technical evidence where raw data is available.

Security and Safety

All testing must be performed in systems you own or are explicitly authorized to assess.

Do not submit:

- Unauthorized access instructions targeting third-party systems.
- Real credentials or sensitive personal information.
- Malware intended for unauthorized deployment.
- Destructive testing procedures without appropriate safeguards.

Security vulnerabilities should be reported privately in accordance with "SECURITY.md" (SECURITY.md), not disclosed through public issues.

Contribution Expectations

SENTINEL is an independently maintained project. Contributions may be reviewed, deferred, modified, or declined depending on project scope and available maintenance capacity.

Opening a pull request does not guarantee acceptance.

By contributing, you agree to follow the project's "Code of Conduct" (CODE_OF_CONDUCT.md).

Thank you for helping improve SENTINEL SOC Lab.
