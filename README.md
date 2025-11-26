# ThermoHive

ThermoHive is smart thermostat, which contains a distributed temperature control and telemetry platform designed for smart device management, automation, and real-time monitoring. It consists of a Python-based backend (Master), a MicroPython-based hardware controller (Worker), and a modern TypeScript/React frontend.

---

## Project Goals

- **Device Management:** Register, monitor, and control distributed devices (e.g., relays, sensors).
- **Telemetry Collection:** Gather and visualize real-time sensor data.
- **Automation & Scheduling:** Enable programmable control strategies and scheduling.
- **Scalable Architecture:** Support multiple devices and extensible business logic.
- **Seamless Communication:** Use MQTT for robust Master-Worker messaging.

---

## Hardware Requirements
- **Microcontroller:** ESP32 or similar with MicroPython support. ESP32-C3 SuperMini is used in development.
- **Sensors:** Temperature sensors compatible with MicroPython (e.g., DHT22, DS18B20). SHT20 is used in development.
- **Actuators:** Relays or similar devices for controlling heating elements. A flip-flop self-locking latching relay is used in development.
- **(Optional) Voltage Detector:** A voltage detector module to monitor battery capacity.
- **(Optional) Voltage Regulator:** A voltage regulator module to ensure stable power supply to the relay.
- **Power Supply:** Batteries or power adapters suitable for the microcontroller and peripherals.

---

## Project Structure

```
ThermoHive/
├── Master/
│   ├── backend/      # FastAPI backend (Python)
│   │   ├── src/
│   │   │   ├── data/         # Models, repositories
│   │   │   ├── routers/      # API endpoints
│   │   │   ├── services/     # Business logic, MQTT, scheduling
│   │   │   ├── strategies/   # Device control strategies
│   │   │   └── ...           # Config, utils
│   │   ├── Makefile
│   │   └── requirements*.txt
│   ├── frontend/    # React frontend (TypeScript, Vite, Refine.dev)
│   │   ├── src/
│   │   ├── package.json
│   │   └── tsconfig*.json
│   └── Dockerfile   # Backend containerization
├── Worker/
│   ├── src/         # MicroPython application
│   │   ├── data/         # Data abstraction
│   │   ├── sensors/      # Sensor logic
│   │   ├── networks/     # Network logic
│   │   ├── services/     # MQTT, device services
│   │   └── ...           # Config, utils
│   └── Makefile
└── .github/
    └── copilot-instructions.md
```

---

## Development Workflows

### Master Backend (Python/FastAPI)

- **Install dependencies:**  
  ```sh
  cd Master/backend
  make venv
  source venv/bin/activate
  make upgrade
  ```
- **Run server:**  
  ```sh
  make
  ```
- **Configuration:**  
  Edit `.env` config files in `Master/backend` as needed.
- **Testing & Linting:**  
  Use `pylintrc` for linting. Tests should be placed under `Master/backend/tests`.

---

### Master Frontend (React/TypeScript)

- **Install dependencies:**  
  ```sh
  cd Master/frontend
  pnpm i
  ```
- **Start development server:**  
  ```sh
  pnpm start
  ```
- **Testing:**  
  Place tests in `src/` with `.test.tsx`/`.test.ts` suffix.
  ```sh
  pnpm test
  ```
- **Linting:**  
  ESLint config is provided in `frontend/`.
  ```sh
  pnpm lint
  ```

---

### Worker Application (MicroPython)

- **Install dependencies (only for development):**  
  ```sh
  cd Worker
  make venv
  source venv/bin/activate
  make upgrade
  ```
- **Configuration:**  
  Adjust config files in `src/configs.py` as needed.
- **Flashing firmware:**
  ```sh
  make flash
  ```
- **Deployment:**
  ```sh
  make deploy
  ```

---

### Docker (Backend)

- **Build Docker image:**  
  ```sh
  cd Master
  make deploy
  ```

---

## Integration Points

- **MQTT:**  
  Master and Worker communicate via MQTT (`services/mqtt.py`, `services/base_mqtt.py`).
- **Database:**  
  Data models and repositories are in `data/` folders.
- **API:**  
  REST endpoints are defined in `Master/backend/src/routers/`.

---

## Conventions & Tips

- Use the provided `Makefile` or config files for automation in each major folder.
- Respect the separation between Master (API/business logic), Worker (hardware/MQTT), and Frontend (UI).
- Use existing routers, services, and strategies as templates for new features.
- For cross-component features, trace data flow from frontend to backend to worker via MQTT and REST APIs.
