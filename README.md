# Agent Skills — Koleksi Terverifikasi

Koleksi **935 skill** keamanan & engineering untuk agent (omp/Claude Code/Cursor/Hermes), terkelompokan 16 kategori. Katalog lengkap dengan deskripsi per skill: **[INDEX.md](INDEX.md)**.

## Struktur

```
skills/              # 935 skill, 1 dir = 1 skill (SKILL.md + assets)
INDEX.md             # katalog terkelompokan (auto-generated)
generate-catalog.py  # regenerator katalog
```

## Sumber koleksi

| Koleksi | Repo |
|---|---|
| frida-skills (15) | [Rudra-ravi/frida-skills](https://github.com/Rudra-ravi/frida-skills) |
| hack-skills (pentest tricks) | [gmh5225/hack-skills](https://github.com/gmh5225/hack-skills) |
| Anthropic-Cybersecurity-Skills (~900) | [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) |

## Kelompok utama

| Kelompok | Jumlah |
|---|---|
| 🛡️ Detection / Blue / SIEM | 110 |
| ☁️ Cloud & Container Security | 106 |
| 🧰 Tooling / Engineering | 190 |
| ⚔️ Offensive / Privesc / C2 / Evasion | 74 |
| 🌐 Web Attack & AppSec | 69 |
| 🔍 RE / Binary / Malware | 66 |
| 🌍 Network & Traffic | 66 |
| 🔬 Forensik & IR | 59 |
| 🔑 Key / Token / Credential | 44 |
| 📋 Governance / Compliance | 46 |
| + 6 kelompok lain | 175 |

## Pemakaian

```bash
# 1 skill on-demand
ln -sfn ~/agent-skills/skills/<name> ~/.agents/skills/<name>

# satu kelompok
for s in ~/agent-skills/skills/frida-*; do
  ln -sfn "$s" ~/.agents/skills/$(basename $s)
done
```

Skill aktif hanya perlu symlink ke tree agent (`~/.agents/skills`) — agent memindai tree itu per-session. Regenerasi katalog setelah menambah/menghapus skill:

```bash
python3 generate-catalog.py
```

## Catatan

- Review skill sebelum pakai; skill berjalan dengan permission penuh agent.
- Jangan commit `~/.agents/skills` legacy lokal — repo ini sumber kebenaran koleksi.
