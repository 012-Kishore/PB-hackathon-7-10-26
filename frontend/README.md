# AI-Powered Face Mask Detection (Frontend)

> **Real-time Face Mask Detection using Transfer Learning with MobileNetV2**  
> *Hackathon Frontend Web Application built by Member 2.*

---

## 📌 Project Overview
This website provides an interactive, hackathon-ready frontend dashboard and live webcam detection interface for real-time face mask compliance checking.

The application communicates with a Python FastAPI backend (Member 3) running a MobileNetV2 transfer learning model (Member 1) to classify browser video frames as **MASK** or **NO MASK** with confidence scores.

---

## 🛠️ Frontend Technology Stack
- **Framework:** React (Vite)
- **Language:** JavaScript (ES6+ / JSX)
- **Styling:** Custom CSS (Glassmorphism Dark Theme, Grid/Flexbox Layouts, Responsive Breakpoints)
- **Icons:** Lucide React (`lucide-react`)
- **API Client:** HTML5 Fetch API & MediaDevices (`getUserMedia`)

---

## 📁 Frontend Directory Structure
```
frontend/
├── public/
├── src/
│   ├── assets/
│   │   └── results/          # Location for ML graphs (confusion matrix, loss curves)
│   ├── components/
│   │   ├── Navbar.jsx        # Sticky navigation bar with mobile menu
│   │   ├── Hero.jsx          # Hero title, call-to-actions, and live preview frame
│   │   ├── Problem.jsx       # Problem statement & automated vision benefits
│   │   ├── HowItWorks.jsx    # Step-by-step pipeline timeline
│   │   ├── Dataset.jsx       # Configurable dataset metrics dashboard
│   │   ├── Model.jsx         # MobileNetV2 transfer learning explanation
│   │   ├── Results.jsx       # Training & validation evaluation graphs placeholder
│   │   ├── LiveDetection.jsx # Live browser webcam interface & prediction card
│   │   ├── Technologies.jsx  # Tech stack overview cards
│   │   ├── Team.jsx          # Team member roles & responsibilities
│   │   └── Footer.jsx        # Footer navigation links & credits
│   ├── data/
│   │   └── projectData.js    # Central data file for ML team updates
│   ├── services/
│   │   └── api.js           # FastAPI backend communication layer
│   ├── App.jsx               # App layout & scroll spy navigation
│   ├── index.css             # Cyber-tech dark design system
│   └── main.jsx              # React app entrypoint
├── .env                      # Local environment configuration
├── .env.example              # Environment template
└── README.md
```

---

## 🚀 How to Run the Frontend

### 1. Install Dependencies
Navigate into the `frontend` folder and run:
```bash
npm install
```

### 2. Configure Backend URL
The default backend URL is set to `http://localhost:8000`.  
If Member 3's FastAPI server runs on a different port or host, update `.env` or set the environment variable:
```env
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Start Development Server
```bash
npm run dev
```
Open your browser at `http://localhost:5173`.

---

## 🔗 Integrating with Team Members

### 👥 Member 1 (Machine Learning)
- Update dataset statistics in `src/data/projectData.js` (`datasetInfo` object).
- Export training graphs from Google Colab and copy them to `src/assets/results/`:
  - `accuracy_loss_curve.png`
  - `confusion_matrix.png`
- Set `resultsInfo.isUpdatedByML = true` in `src/data/projectData.js`.

### ⚡ Member 3 (Backend & Computer Vision)
- Start the FastAPI backend server on `http://localhost:8000` (or update `VITE_API_BASE_URL`).
- Expected endpoints:
  - **`GET /health`** -> Returns `200 OK` (Health status indicator turns green in the UI).
  - **`POST /predict`** -> Accepts `multipart/form-data` with field `file` (JPEG image).  
    Expected JSON response format:
    ```json
    {
      "prediction": "Mask",
      "confidence": 0.964
    }
    ```

---

## 🤝 Team Roles
- **Member 1 (ML):** MobileNetV2 training, transfer learning, dataset curation, accuracy evaluation.
- **Member 2 (Frontend):** React website, UI/UX, browser webcam stream, API integration, status handling.
- **Member 3 (Backend):** Python FastAPI server, OpenCV image processing pipeline, model inference endpoint.
