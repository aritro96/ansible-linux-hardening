# Ansible Linux Hardening Framework

## Overview

Ansible Linux Hardening Framework is an infrastructure automation project designed to enforce security best practices and system hardening standards on Red Hat Enterprise Linux (RHEL) systems.

The project uses a modular role-based architecture to automate security configuration, compliance validation, and system auditing while maintaining idempotency and operational safety.

## Features

### SSH Hardening

* Disable insecure SSH configurations
* Control root login access
* Configure password authentication policies
* Set login grace periods
* Configure idle session timeouts
* Restrict maximum authentication attempts
* Disable X11 forwarding
* Validate SSH configuration before service restart

### Password Policy Enforcement

* Configure password complexity requirements
* Enforce password quality standards
* Standardize authentication policies across managed systems

### Auditd Hardening

* Verify auditd package installation
* Configure auditing services
* Enforce audit logging requirements
* Validate audit subsystem configuration

### Compliance Validation

* Automated compliance checks
* Configuration verification
* PASS/FAIL status reporting
* Security posture assessment

### Configuration Management

* Jinja2 template-based configuration deployment
* Backup existing configurations before modification
* Idempotent Ansible execution
* Modular and reusable role design

---

## Project Structure

```text
├── ansible-project
│   ├── group_vars
│   ├── playbooks
│   ├── reports
│   └── roles
├── collections
│   └── ansible_collections
├── group_vars
├── playbooks
├── reports
│   ├── auditcompliance
│   ├── firewalld
│   ├── kernel_hardening
│   ├── pwcomplexity_reports
│   └── ssh_compliance_report
├── roles
│   ├── auditd
│   ├── firewall
│   ├── health_check
│   ├── password_policy
│   ├── ssh_hardening
│   └── sysctl
```
---

## Requirements

* Ansible 2.14+
* RHEL 8 / RHEL 9
* SSH access to managed hosts
* Privilege escalation (sudo)

---

## Usage

### Clone Repository

```bash
git clone https://github.com/aritro96/ansible-project.git
cd ansible-project
```

### Update Inventory

Edit the inventory file:

```ini
[rhel_servers]
server1.example.com
server2.example.com
```

### Run SSH Hardening

```bash
ansible-playbook playbooks/ssh_hardening.yml
```

### Run Password Policy Hardening

```bash
ansible-playbook playbooks/pwcomplexity.yml
```

### Run Auditd Hardening

```bash
ansible-playbook playbooks/audit_hardening.yml
```

### Run Kernel Hardening

```bash
ansible-playbook playbooks/kernel_hardening.yml
```

### Run Firewall Hardening

```bash
ansible-playbook playbooks/firewalld_hardening.yml
```
---

## Design Principles

* Infrastructure as Code (IaC)
* Security First Approach
* Idempotent Automation
* Configuration Validation Before Service Restart
* Modular Role-Based Design
* Reusable Ansible Components

---

## Version History

### v1.0.0

Initial release including:

* SSH Hardening
* Password Complexity Enforcement
* Auditd Hardening
* Firewalld Hardening
* Kernel Hardening
* Compliance Reporting
* Role-Based Architecture

---

## Future Enhancements

* GitHub Actions CI/CD Integration
* Automated Compliance Dashboard
* Multi-Distribution Support

---

## Author

Aritro Sarkar

Linux System Administrator | Automation Enthusiast

Focused on Linux Administration, Security Hardening, Infrastructure Automation, and DevOps practices.
