# Ksu Network Drive Requirements

## Overview
Shared network storage for music production collaboration between two MacBook Pro users (M1 and M3).

## Use Case
- Multi-track song storage and sharing
- Real-time collaboration on music projects
- Centralized backup for album production

## Available Hardware
- Mac Mini (can be always-on)
- Shared WiFi network

---

## Option Comparison

### Option 1: Mac Mini + External SSD (Simplest)

**Setup:** Plug external SSD into Mac Mini, enable File Sharing

| Pros | Cons |
|------|------|
| Zero setup - macOS native | Not Linux-based |
| SMB/AFP built-in | Less learning opportunity |
| Time Machine compatible | Mac Mini tied to this role |
| Already owned | macOS updates may interrupt |
| Best compatibility with macOS clients | |

**Remote Access:**
- Tailscale for Mac (very easy)
- Built-in Screen Sharing
- iCloud if needed

**Cost:** ~$100-200 for external SSD only

---

### Option 2: Raspberry Pi 5 + SSD (DIY Linux)

**Setup:** Raspberry Pi running OpenMediaVault or Ubuntu Server

| Pros | Cons |
|------|------|
| True Linux experience | Requires setup time |
| Low power (~5-15W) | Slower than Mac Mini |
| Learn server administration | USB 3.0 bottleneck |
| Dedicated purpose | Need to buy Pi + accessories |
| Can run Docker, scripts, etc. | |

**Remote Access:**
- Tailscale / WireGuard
- SSH
- Can run Nextcloud

**Cost:** ~$150-200 (Pi 5 + case + PSU + SSD)

---

### Option 3: Dedicated NAS (Synology/QNAP)

**Setup:** Purpose-built appliance with web UI

| Pros | Cons |
|------|------|
| Polished web interface | Most expensive |
| RAID support built-in | Proprietary OS (Linux-based but limited) |
| Apps ecosystem (Plex, sync, etc.) | Overkill for 2 users |
| Designed for 24/7 operation | |
| Good documentation | |

**Remote Access:**
- Synology QuickConnect / QNAP myQNAPcloud
- VPN apps built-in
- Mobile apps

**Cost:** ~$300-500+ (device + drives)

---

### Option 4: Mini PC with Linux (Powerful DIY)

**Setup:** Intel NUC or similar running Ubuntu/Debian

| Pros | Cons |
|------|------|
| Full Linux server | Higher power consumption |
| Very capable hardware | More expensive than Pi |
| Can run anything | Requires Linux knowledge |
| Good for learning | |

**Remote Access:** Same as Raspberry Pi

**Cost:** ~$200-400 (used NUC + SSD)

---

## Recommendation Matrix

| Priority | Best Option |
|----------|-------------|
| Simplest setup | Mac Mini + SSD |
| Learning Linux | Raspberry Pi |
| Best reliability | NAS (Synology) |
| Best value | Mac Mini + SSD |
| True server experience | Mini PC with Linux |

## Questions to Decide

1. **Primary goal:** Just sharing files, or also learning Linux?
2. **Is the Mac Mini doing other things?** (If dedicated, it's the obvious choice)
3. **Budget priority?**
4. **How important is remote access from outside home?**
5. **Do we need redundancy/backup?** (RAID, cloud sync)

## Storage Sizing

- Typical Ableton/Logic multi-track project: 5-50 GB
- Album of 10-15 songs: 100-500 GB
- **Recommended minimum:** 1 TB SSD
- **Comfortable:** 2 TB SSD

## Next Steps
- [ ] Decide on approach
- [ ] If Mac Mini: buy external SSD, enable sharing
- [ ] If DIY Linux: order hardware, plan setup
- [ ] Configure remote access (Tailscale recommended for simplicity)
- [ ] Test with actual projects
