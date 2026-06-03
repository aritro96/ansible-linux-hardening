#!/usr/bin/python3

import os
import re

def get_report_status(filepath):

    with open(filepath, "r") as file:
        content = file.read()

    match = re.search(
        r"OVERALL RESULT[S]?\s*:\s*(PASS|FAIL)",
        content
    )

    if match:
        return match.group(1)

    return "UNKNOWN"

report_sources = {
    "SSH": (
        "./ssh_compliance_report",
        "_ssh_compliance_report.txt"
    ),
    "Kernel": (
        "./kernel_hardening",
        "_kernel_hardening"
    ),
    "Password": (
        "./pwcomplexity_reports",
        "_password_compliance"
    ),
    "Audit": (
        "./auditcompliance",
        "_audit_hardening"
    ),
    "Firewall": (
        "./firewalld/compliance",
        "_firewall_compliance"
    )
}

servers = {}

for report_type, report_info in report_sources.items():

    report_dir = report_info[0]
    suffix = report_info[1]

    for filename in os.listdir(report_dir):

        filepath = os.path.join(report_dir, filename)

        server = filename.replace(suffix,"")

        result = get_report_status(filepath)

        if server not in servers:
            servers[server] = {}

        servers[server][report_type] = result

#print(result)

for server in servers:

    results = servers[server].values()

    if "FAIL" in results:
        servers[server]["Overall"] = "FAIL"
    elif "UNKNOWN" in results:
        servers[server]["Overall"] = "UNKNOWN"
    else:
        servers[server]["Overall"] = "PASS"

#print(servers)

header = (
    f"{'Server':<30}"
    f"{'SSH':<10}"
    f"{'Kernel':<10}"
    f"{'Password':<12}"
    f"{'Audit':<10}"
    f"{'Firewall':<12}"
    f"{'Overall':<10}"
)

print()
print("=" * len(header))
print(header)
print("=" * len(header))

for server, data in sorted(servers.items()):

    print(
        f"{server:<30}"
        f"{data.get('SSH', 'N/A'):<10}"
        f"{data.get('Kernel', 'N/A'):<10}"
        f"{data.get('Password', 'N/A'):<12}"
        f"{data.get('Audit', 'N/A'):<10}"
        f"{data.get('Firewall', 'N/A'):<12}"
        f"{data.get('Overall', 'N/A'):<10}"
    )

print("=" * len(header))

pass_servers = 0
fail_servers = 0

for server, data in servers.items():

    if data["Overall"] == "PASS":
        pass_servers += 1
    else:
        fail_servers += 1

total_servers = len(servers)

compliance_score = (
    pass_servers / total_servers
) * 100

compliance_score = round(compliance_score, 2)

print()
print("SUMMARY")
print("=" * 30)

print(f"Total Servers     : {total_servers}")
print(f"Compliant Servers : {pass_servers}")
print(f"Non-Compliant     : {fail_servers}")
print(f"Compliance Score  : {compliance_score}%")

def generate_txt_report(header,servers,total_servers,pass_servers,fail_servers,compliance_score):
    txt_report = []

    txt_report.append("=" * len(header))
    txt_report.append(header)
    txt_report.append("=" * len(header))

    for server, data in sorted(servers.items()):

        row = (
            f"{server:<30}"
            f"{data.get('SSH', 'N/A'):<10}"
            f"{data.get('Kernel', 'N/A'):<10}"
            f"{data.get('Password', 'N/A'):<12}"
            f"{data.get('Audit', 'N/A'):<10}"
            f"{data.get('Firewall', 'N/A'):<12}"
            f"{data.get('Overall', 'N/A'):<10}"
        )

    txt_report.append(row)

    txt_report.append("=" * len(header))
    txt_report.append("")
    txt_report.append("SUMMARY")
    txt_report.append("=" * 30)
    txt_report.append(f"Total Servers     : {total_servers}")
    txt_report.append(f"Compliant Servers : {pass_servers}")
    txt_report.append(f"Non-Compliant     : {fail_servers}")
    txt_report.append(f"Compliance Score  : {compliance_score}%")

    with open(
    "./master_compliance_report.txt",
    "w"
    ) as report_file:
        report_file.write("\n".join(txt_report))

generate_txt_report(
    header,
    servers,
    total_servers,
    pass_servers,
    fail_servers,
    compliance_score
)

def generate_html_report(
    servers,
    total_servers,
    pass_servers,
    fail_servers,
    compliance_score
):
    html = """
    <html>
    <body>
    <h2>Compliance Report</h2>

    <table border="1" cellpadding="5" cellspacing="0">
    <tr>
        <th>Server</th>
        <th>SSH</th>
        <th>Kernel</th>
        <th>Password</th>
        <th>Audit</th>
        <th>Firewall</th>
        <th>Overall</th>
    </tr>
    """

    for server, data in sorted(servers.items()):
        html += f"""
        <tr>
            <td>{server}</td>
            <td>{data.get('SSH','N/A')}</td>
            <td>{data.get('Kernel','N/A')}</td>
            <td>{data.get('Password','N/A')}</td>
            <td>{data.get('Audit','N/A')}</td>
            <td>{data.get('Firewall','N/A')}</td>
            <td>{data.get('Overall','N/A')}</td>
        </tr>
        """

    html += f"""
    </table>

    <h3>Summary</h3>

    <ul>
        <li>Total Servers: {total_servers}</li>
        <li>Compliant Servers: {pass_servers}</li>
        <li>Non-Compliant Servers: {fail_servers}</li>
        <li>Compliance Score: {compliance_score}%</li>
    </ul>

    </body>
    </html>
    """

    with open("./master_compliance_report.html", "w") as f:
        f.write(html)

import subprocess

def send_html_mail():
    with open(
        "./master_compliance_report.html",
        "r"
    ) as f:
        html_body = f.read()

    mail = f"""From: shutterstoryteller@gmail.com
To: aritro.rmc@gmail.com
Subject: Compliance Report
MIME-Version: 1.0
Content-Type: text/html

{html_body}
"""

    subprocess.run(
        ["/usr/sbin/sendmail", "-t"],
        input=mail,
        universal_newlines=True
    )

generate_html_report(
    servers,
    total_servers,
    pass_servers,
    fail_servers,
    compliance_score
)

send_html_mail()
