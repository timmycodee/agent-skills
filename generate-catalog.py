#!/usr/bin/env python3
"""Regenerate INDEX.md dari skills/ — katalog terkelompokan 935 skill.

    python3 generate-catalog.py          # tulis INDEX.md
"""
import os, re, datetime
from collections import defaultdict

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skills")
items = sorted(i for i in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, i)))

GROUPS = [
 ("🔧 Frida / Instrumentasi Dinamis", ["frida-"], "Hooking runtime, bypass proteksi, ekstraksi data dinamis di Android/iOS/native"),
 ("📱 Mobile Pentest & Malware", ["android","ios-","mobile","apk","objection","dex"], "Pentest aplikasi mobile, keychain dump, SSL pinning bypass, malware mobile"),
 ("🔍 RE / Binary / Malware", ["reverse-engineering","vm-and-bytecode","ghidra","disassembl","malware","ransomware","bootkit","rootkit","elf-","mach-o","firmware-","cobalt","mimikatz","crack","packer","upx","ida-","radare","rizin","cutter","binary-ninja"], "Disassembly, decompilation, malware triage, firmware, packed binary"),
 ("🔑 Key / Token / Credential", ["credential","keychain","jwt","oauth","token","dpapi","kerberos","honeytoken","api-key","secret","trufflehog","gitleaks","pass-the-","shadow-credentials","session"], "Ekstraksi key, token attack, credential dump, secret scanning, honeytoken"),
 ("🌐 Web Attack & AppSec Testing", ["sql-injection","xss","csrf","ssrf","xxe","idor","bola","cors","csp-","clickjack","open-redirect","command-injection","deserial","ssti","smuggl","cache","prototype","websocket","graphql","parameter-pollution","host-header","jndi","email-header","crlf","mass-assignment","race-condition","type-juggling","dangling","burp","zap","nikto","waf-bypass","fuzzing"], "Semua kelas serangan web + tooling test (Burp, ZAP, fuzzing)"),
 ("🔐 Crypto Audit & Attack", ["cryptograph","crypto-","-crypto","hash-","rsa-","lattice","aes-","cipher","post-quantum","signing","ed25519","dpapi","pkcs","hsm","key-pair","keygen"], "Audit kripto aplikasi, attack kriptografi, post-quantum migration"),
 ("🌍 Network & Traffic", ["network","packet","pcap","wireshark","zeek","netflow","arp","dns","bgp","http2","wireless","bluetooth","wifi","nmap","scapy","mitm","tcpdump","ip-"], "Analisa trafik, pcap forensik, protokol attack, wireless"),
 ("☁️ Cloud & Container Security", ["aws","azure","gcp","cloud","kubernetes","docker","container","terraform","serverless","lambda","s3","eks","aks","gke","iam","cloudtrail","guardduty","macie","sentinel-","defender-for-cloud","waf-","cloudflare"], "AWS/Azure/GCP IAM abuse, K8s RBAC, container escape, supply chain"),
 ("⚔️ Offensive / Privesc / C2 / Evasion", ["active-directory","adcs","entra","dcsync","zerologon","nopac","ntlm","smb","powershell","bloodhound","lsass","lateral-movement","windows-privilege","linux-privilege","windows-lateral","linux-lateral","uac-","amsi","etw","edr","defender","metasploit","sliver","havoc","covenant","empire","evilginx","gophish","c2-","red-team","purple-team","atomic-red","stratus","caldera","evading","bypass-techniques","ant-debug","anti-frida","sandbox-escape","container-escape","macos-process-injection","macos-security-bypass","heap-exploit","stack-overflow","kernel-exploit","format-string","binary-protection","rop-","pwn"], "Privesc, lateral movement, C2 infra, AV/EDR evasion, eksploitasi memori"),
 ("🔬 Forensik & Incident Response", ["forensic","volatil","memory-dump","autopsy","timeline","plaso","kape","mft","prefetch","shellbag","browser-","artifact","incident","picerl","breach","lessons-learned","containment","triag","malware-response","ransom-response","recovery","disk-image","carving","photorec","dcfldd","usb-","log-analysis","logging"], "Disk/memory forensik, timeline, IR playbook, recovery"),
 ("🛡️ Detection / Blue / SIEM", ["detecting","sigma","splunk","elastic","sentinel","qradar","soc-","siem","yara","hunting-","threat-hunt","beacon","ioc-","misp","stix","taxii","opencti","mitre","attack-framework","navigator","purple-team","soc-metrics","alert","detection-","ueba","siem-"], "Detection engineering, threat hunting, SIEM, YARA, MITRE ATT&CK"),
 ("🎣 Phishing / OSINT / Social", ["phishing","vishing","social-engineering","osint","spiderfoot","sherlock","deepfake","quishing","pretext","spearphish"], "Phishing campaign, OSINT recon, social engineering, deepfake detection"),
 ("📋 Governance / Compliance / Hardening", ["cmmc","gdpr","hipaa","pci","soc2","iso-27001","nerc","nist","csf-","rmf","risk","vendor","privacy","zero-trust","pam-","iga-","sailpoint","cyberark","delinea","beyondcorp","zscaler","prisma","tailscale","sdn","nac-","segmentation","firewall","ids-","ips-","suricata","snort","gateway","harden","cis-","hardening","policy","compliance","governance","govern","awareness","training"], "Framework compliance, zero trust, PAM, hardening benchmark"),
 ("🩺 Vuln Management & Scanning", ["scanning","vulnerability","nessus","openvas","insightvm","qualys","cve-","epss","kev-","ssvc","cvss","patch","remediat","aging","sla-","defectdojo","scout","cloudfox","pacu","stratus","pentest"], "Vulnerability scanning, prioritisasi CVE, patch management"),
 ("🧠 Threat Intel & Atribusi", ["threat-intel","campaign","darkweb","leak-site","infrastructure-track","actor-profile","attribution","kill-chain","diamond","engage","cti-","reporting","intel-"], "Threat intelligence, atribusi kampanye, darkweb monitoring"),
 ("🧰 Tooling / Engineering / Lainnya", [], "Build, deploy, pipeline, CLI, infra tooling, dan skill lain-lain"),
]

def bucket(n):
    for gname, kws, _ in GROUPS:
        if not kws:
            continue
        if any(k in n for k in kws):
            return gname
    return GROUPS[-1][0]

def get_desc(path):
    try:
        head = open(os.path.join(path, "SKILL.md"), encoding="utf-8", errors="replace").read(800)
        m = re.search(r"description:\s*(?:(?!---|\nname:).)*", head, re.S)
        d = m.group(0).replace("description:", "").strip() if m else ""
        d = " ".join(d.split()).strip("-|> ")
        return (d[:140] + "…") if len(d) > 140 else d
    except Exception:
        return ""

g = defaultdict(list)
for n in items:
    g[bucket(n)].append((n, get_desc(os.path.join(ROOT, n))))

order = {gname: i for i, (gname, _, _) in enumerate(GROUPS)}
today = datetime.date.today().isoformat()

lines = []
lines.append("# Agent Skills — Katalog")
lines.append("")
lines.append(f"> Auto-generated {today} oleh `generate-catalog.py`. Koleksi penuh di `skills/`.")
lines.append(f"> Total: **{len(items)} skill** di {len(g)} kelompok.")
lines.append("")
lines.append("## Instalasi")
lines.append("")
lines.append("```bash")
lines.append("# clone & symlink skill yang dibutuhkan ke tree agent (~/.agents/skills)")
lines.append("git clone https://github.com/timmycodee/agent-skills.git")
lines.append("ln -sfn $(pwd)/agent-skills/skills/<skill-name> ~/.agents/skills/<skill-name>")
lines.append("")
lines.append("# atau install semua skill kelompok (contoh: semua skill Frida)")
lines.append("for s in agent-skills/skills/frida-*; do ln -sfn \"$(pwd)/$s\" ~/.agents/skills/$(basename $s); done")
lines.append("```")
lines.append("")
lines.append("## Ringkasan kelompok")
lines.append("")
lines.append("| Kelompok | Jumlah |")
lines.append("|---|---|")
for gname in sorted(g, key=lambda x: order[x]):
    lines.append(f"| {gname} | {len(g[gname])} |")
lines.append("")
for gname in sorted(g, key=lambda x: order[x]):
    _, desc = next(((k, d) for gn, k, d in GROUPS if gn == gname), ([], ""))
    lines.append(f"## {gname}")
    if desc:
        lines.append(f"*{desc}*")
    lines.append("")
    lines.append("| Skill | Deskripsi |")
    lines.append("|---|---|")
    for name, d in sorted(g[gname]):
        safe = d.replace("|", "\\|")
        lines.append(f"| [`{name}`](skills/{name}/) | {safe} |")
    lines.append("")

open("INDEX.md", "w").write("\n".join(lines))
print(f"INDEX.md: {len(items)} skills, {len(g)} groups")
