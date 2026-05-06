# Lunar Solar Ring Simulator

[![CI/CD Pipeline](https://github.com/your-username/lunar-solar-simulator/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/your-username/lunar-solar-simulator/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)

A full-stack interactive simulation platform that models a futuristic concept of generating solar energy from the Moon and transmitting it wirelessly to Earth.

> Inspired by next-generation space-based solar power systems like the Shimizu Corporation's Luna Ring concept.

![Demo](./screenshots/demo.gif)

---

## Features

### Core Simulation
- **3D Earth-Moon Visualization** - Interactive Three.js scene with orbital mechanics
- **Real-time Energy Streaming** - WebSocket-powered live data visualization
- **Physics-Based Calculations** - Accurate energy generation and transmission models
- **AI-Powered Insights** - Intelligent analysis and recommendations

### Advanced Physics (v2.0)
- **Lunar Day/Night Cycle** - 29.5-day rotation effects on solar exposure
- **Atmospheric Absorption** - Weather and zenith angle impact modeling
- **Beam Spreading Loss** - Distance-based transmission calculations
- **Panel Degradation** - Time-based efficiency reduction

### Optimization & Analysis
- **Parameter Optimization** - Optuna-powered AI optimization
- **Ground Station Placement** - Optimal location algorithms
- **Scenario Comparison** - Compare multiple configurations
- **Data Export** - JSON, CSV, and HTML report generation

### Production Ready
- **Docker Support** - Containerized deployment
- **CI/CD Pipeline** - GitHub Actions automation
- **Comprehensive Tests** - pytest with coverage
- **Type Safety** - Full TypeScript and Python type hints

---

## Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| Python 3.12+ | Core language |
| FastAPI | REST API & WebSocket |
| Pydantic | Data validation |
| Optuna | Parameter optimization |
| NumPy | Scientific computing |
| pytest | Testing framework |

### Frontend
| Technology | Purpose |
|------------|---------|
| React 19 | UI framework |
| TypeScript | Type safety |
| Vite | Build tool |
| Three.js | 3D visualization |
| React Three Fiber | React renderer for Three.js |
| Tailwind CSS | Styling |
| Framer Motion | Animations |
| Plotly.js | Interactive charts |

### DevOps
| Technology | Purpose |
|------------|---------|
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| GitHub Actions | CI/CD pipeline |
| Nginx | Frontend serving |

---

## Project Structure

```
lunar_solar_ring_simulator/
├── lunar-backend/                 # Python FastAPI backend
│   ├── api.py                     # Main API endpoints
│   ├── config.py                  # Environment configuration
│   ├── models/
│   │   ├── request.py             # Input validation models
│   │   └── response.py            # Output data models
│   ├── services/
│   │   ├── simulation_service.py  # Main orchestrator
│   │   ├── energy_model.py        # Energy calculations
│   │   ├── transmission_model.py  # Transmission physics
│   │   ├── physics_model.py       # Advanced physics
│   │   ├── station_optimizer.py   # Ground station optimization
│   │   ├── parameter_optimizer.py # Optuna optimization
│   │   └── export_service.py      # Data export
│   ├── utils/
│   │   ├── constants.py           # Physical constants
│   │   └── logger.py              # Logging config
│   ├── tests/                     # pytest test suite
│   ├── requirements.txt
│   └── Dockerfile
│
├── lunar-frontend/                # React TypeScript frontend
│   ├── src/
│   │   ├── App.tsx                # Main application
│   │   ├── components/
│   │   │   ├── EarthMoonSystem.tsx    # 3D visualization
│   │   │   ├── SimulationForm.tsx     # Input controls
│   │   │   ├── Results.tsx            # Results display
│   │   │   ├── EnergyGraph.tsx        # Live chart
│   │   │   ├── Insights.tsx           # AI insights
│   │   │   ├── ErrorBoundary.tsx      # Error handling
│   │   │   └── LoadingSpinner.tsx     # Loading states
│   │   ├── hooks/
│   │   │   ├── useSimulation.ts       # Simulation state
│   │   │   └── useWebSocketSimulation.ts
│   │   ├── types/
│   │   │   └── simulation.ts          # TypeScript types
│   │   ├── config/
│   │   │   └── api.ts                 # API configuration
│   │   └── services/
│   │       └── api.ts                 # API client
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml             # Container orchestration
├── .github/workflows/ci.yml       # CI/CD pipeline
└── README.md
```

---

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 20+
- Docker (optional)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-username/lunar-solar-simulator.git
cd lunar-solar-simulator

# Start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

#### Backend
```bash
cd lunar-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd lunar-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/simulate` | Run simulation |
| POST | `/optimize` | AI parameter optimization |
| POST | `/optimize/quick` | Quick suggestions |
| POST | `/export/json` | Export as JSON |
| POST | `/export/csv` | Export as CSV |
| POST | `/export/report` | Generate HTML report |
| WS | `/ws/simulate` | Real-time streaming |

### Simulation Request

```json
{
  "ring_width_km": 50,
  "panel_efficiency": 0.22,
  "transmission_type": "microwave",
  "num_ground_stations": 5,
  "simulation_hours": 24,
  "include_lunar_cycle": false,
  "include_atmospheric_effects": false
}
```

### Simulation Response

```json
{
  "total_energy_generated_gw": 1234.56,
  "energy_received_gw": 987.65,
  "transmission_loss_percent": 20.0,
  "system_efficiency": 0.80,
  "stations": [...],
  "time_series": [...],
  "insights": [...]
}
```

---

## Physical Constants

| Constant | Value | Unit |
|----------|-------|------|
| Moon Radius | 1,737.4 | km |
| Solar Constant | 1,361 | W/m² |
| Earth-Moon Distance | 384,400 | km |
| Lunar Day | 708 | hours |
| Microwave Base Loss | 15 | % |
| Laser Base Loss | 30 | % |

---

## Testing

### Backend Tests
```bash
cd lunar-backend
pytest tests/ -v --cov=services --cov-report=term-missing
```

### Frontend Build
```bash
cd lunar-frontend
npm run build
npm run lint
```

---

## Deployment

### Vercel + Railway (Recommended)
1. Deploy frontend to Vercel
2. Deploy backend to Railway
3. Update environment variables

### AWS / GCP / Azure
Use the provided Dockerfiles for container deployment.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Roadmap

- [ ] User authentication
- [ ] Saved scenarios database
- [ ] Real-time collaboration
- [ ] Mobile app (React Native)
- [ ] VR visualization mode
- [ ] Integration with real satellite data

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Acknowledgments

- [Shimizu Corporation's Luna Ring Concept](https://www.shimz.co.jp/en/topics/dream/content03/)
- [NASA Space-Based Solar Power Research](https://www.nasa.gov/topics/technology/features/solar_power.html)
- Three.js and React Three Fiber communities
- FastAPI and Pydantic maintainers

---

## Author

Built with passion for space technology and clean energy.

**Star this repo if you find it useful!**
