# SENTINEL — SOC Lab

> **Does your detection still work when the attacker changes tactics?**

SENTINEL is a virtual cybersecurity SOC lab designed to simulate attacks, collect security telemetry, engineer detections, investigate incidents, respond to threats, and continuously test whether defensive controls actually work.

## Project Concept

SENTINEL models a small enterprise environment inside isolated virtual machines.

The project follows a continuous security lifecycle:

**SIMULATE → DETECT → INVESTIGATE → RESPOND → MEASURE → IMPROVE → RETEST**

Instead of simply installing security tools, SENTINEL focuses on validating the complete defensive process.

## Current Architecture

```text
                    INTERNET
                       |
                    NAT
                       |
              +----------------+
              | SENTINEL-WAZUH |
              | 10.10.10.10    |
              | Wazuh SOC       |
              +----------------+
                       |
                SENTINEL-LAB
                10.10.10.0/24
                       |
              +--------+--------+
              |                 |
       +-------------+   +-------------+
       | SENTINEL-   |   | SENTINEL-   |
       | KALI        |   | WIN01       |
       | 10.10.10.20 |   | 10.10.10.30 |
       | Attacker    |   | Endpoint    |
       +-------------+   +-------------+
