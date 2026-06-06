# Project TacticalEye

**Zero-Memory Real-Time Utility Telemetry Engine for Counter-Strike 2.**

This project consists of a Python CV worker for minimap inference, a .NET 8 Web API for managing spatial proximity, and a React frontend for the "Three-Picture Paradigm" secondary monitor UI.

## Getting Started

Follow these steps to pull, build, and run the complete application stack.

### 1. Build and Run the .NET Web API Backend
The backend engine handles the proximity logic and broadcasts tactical data over SignalR.

1. Open a terminal and navigate to the backend API directory:
   ```bash
   cd TacticalEye.Api/TacticalEye.Api
   ```
2. Build the project:
   ```bash
   dotnet build
   ```
3. Run the server:
   ```bash
   dotnet run
   ```
   *(The Web API will start listening on `http://localhost:5000` or `https://localhost:5001`. The SignalR hub is available at `/lineuphub`.)*

### 2. Build and Run the React Dashboard Frontend
The dashboard connects to the SignalR hub to display real-time lineups based on your radar position.

1. Open a new terminal window and navigate to the frontend directory:
   ```bash
   cd TacticalEye.Dashboard
   ```
2. Install frontend dependencies:
   ```bash
   npm install
   ```
3. Build or run the frontend:
   *(Note: The React components are scaffolded. If you configure a bundler or CRA/Vite, you can start the dev server here.)*
   ```bash
   npm run build
   ```

### 3. Generate Training Data
To recognize your position on the map, you need to train the YOLO model. We've provided a scraper to gather training resources.

1. Navigate to the root directory of the repository.
2. Install the necessary Python HTTP library:
   ```bash
   pip install requests
   ```
3. Run the scraper script:
   ```bash
   py scrape_nades.py
   ```
   *(This will connect to `csnades.gg` and output a file named `nades_to_train.json` containing URLs you can use to curate training datasets.)*

### 4. Run the Python Inference Worker
Once your YOLO model is trained (`radar_yolov8n.pt`) and placed in a `models/` directory, you can start the screen capture worker.

1. Install the required Python CV and inference libraries:
   ```bash
   pip install mss opencv-python numpy requests ultralytics
   ```
2. Run the worker script:
   ```bash
   py vision_worker.py
   ```
   *(The worker will continuously grab the minimap area of your screen, infer your X/Y coordinates, and send them to the .NET backend for lineup correlation.)*
