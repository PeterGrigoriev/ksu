# Home Kit Setup

Home Assistant running in Docker for smart home automation.

## Hardware

- **Nuki Smart Lock Go (2025)** — WiFi + Matter support
- **HomePod mini** — Thread border router + Apple Home Hub

## Quick Start

```bash
docker compose up -d
```

Open: http://localhost:8123

## Setup Nuki Smart Lock

1. Install Nuki app and connect lock to WiFi
2. In Nuki app: Settings → Features → Matter → Enable
3. In Home Assistant: Settings → Devices → Add Integration → Matter
4. Scan the Matter QR code from Nuki app

## Directory Structure

```
home-kit/
├── docker-compose.yml
├── config/              # Home Assistant configuration (auto-created)
│   ├── configuration.yaml
│   ├── automations.yaml
│   └── ...
└── README.md
```

## Useful Commands

```bash
# Start
docker compose up -d

# View logs
docker compose logs -f homeassistant

# Restart
docker compose restart

# Stop
docker compose down

# Update to latest version
docker compose pull && docker compose up -d
```

## Adding Zigbee Support (optional)

If you add a Zigbee USB dongle (like SkyConnect), update docker-compose.yml:

```yaml
services:
  homeassistant:
    # ... existing config ...
    devices:
      - /dev/tty.usbserial-XXXX:/dev/ttyUSB0
```

Find your device path:
```bash
ls /dev/tty.usb*
```

## Apple Home Integration

To expose Home Assistant devices to Apple Home:

1. Settings → Devices & Services → Add Integration → HomeKit
2. Scan the QR code with your iPhone
3. Select which devices to expose

## Backups

Backups are stored in `./config/backups/`.

Create manual backup: Settings → System → Backups → Create Backup
