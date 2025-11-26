# Copilot Instructions for ThermoHive

## Big Picture Architecture
- **Monorepo Structure:** Contains `Master` and `Worker` folders. `Master/backend` is Python/FastAPI servier, `Worker` a MicroPython application, and `Master/frontend` is a TypeScript/React/Vite/Refine.dev app.
- **Master Backend:**
  - Located in `Master/backend/src/`
  - Handles device management, relay control, telemetry, and scheduling via routers and services.
  - Data layer: `data/` (models, repositories)
  - API layer: `routers/`
  - Business logic: `services/`, `strategies/`
- **Worker Application:**
  - Located in `Worker/src/`
  - Manages hardware integration (sensors, networks, MQTT communication)
  - Data abstraction: `data/`
  - Sensor logic: `sensors/`
  - Network logic: `networks/`
  - MQTT: `services/`
- **Master Frontend:**
  - Located in `Master/frontend/src/`
  - React app for device management and telemetry visualization

## Developer Workflows
- **Build/Run Master Backend:**
  - Use `Makefile` in `Master/backend/` for dependency and build commands
  - Example: `make` runs backend server
- **Build/Run Worker Application:**
  - Use `Makefile` in `Worker/` for dependency and build commands
- **Master Frontend:**
  - Use `pnpm` for install/build/test (see `package.json`)
  - Example: `pnpm start` to start the frontend application
- **Docker:**
  - `Master/Dockerfile` for backend containerisation

## Project-Specific Conventions
- **Configuration:**
  - Python services use `.ini` or `.py` config files in `src/`
  - Frontend uses TypeScript config files (`tsconfig*.json`)
- **Testing:**
  - Frontend: Tests in `src/` with `.test.tsx`/`.test.ts` suffix
- **Linting:**
  - Python: `pylintrc` in each service folder
  - Frontend: ESLint config in `frontend/`
- **Dependency Management:**
  - Python: `requirements.txt` and `requirements.dev.txt`
  - Frontend: `pnpm` workspace

## Integration Points
- **MQTT Communication:**
  - Worker and Master communicate via MQTT (see `services/mqtt.py` and `services/base_mqtt.py`)
- **Database:**
  - Data models and repositories in `data/` folders
- **API:**
  - Routers in `Master/backend/src/routers/` define REST endpoints

## Patterns & Examples
- **Router Example:**
  - `device.py` in `routers/` for device API endpoints
- **Service Example:**
  - `decision_engine.py` in `services/` for business logic
- **Strategy Example:**
  - `avg_strategy.py`, `min_strategy.py` in `strategies/` for device control logic

## Tips for AI Agents
- Always check for a `Makefile` or config file in each major folder for workflow automation.
- Respect the separation between Master (API/business logic), Worker (hardware/MQTT), and Frontend (UI).
- Use existing routers/services/strategies as templates for new features.
- For cross-component features, trace data flow from frontend to backend to worker via MQTT and REST APIs.

---
_Ask for feedback if any section is unclear or missing important project-specific details._
