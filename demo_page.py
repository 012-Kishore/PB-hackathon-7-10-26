"""HTML/CSS/JS template for the interactive Face Mask Detection web demo."""

DEMO_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Face Mask Detection | MobileNetV2 Live Demo</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-primary: #0b0f19;
      --bg-card: rgba(17, 24, 39, 0.75);
      --bg-card-border: rgba(255, 255, 255, 0.08);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --accent-cyan: #06b6d4;
      --accent-blue: #3b82f6;
      --mask-green: #10b981;
      --mask-green-glow: rgba(16, 185, 129, 0.35);
      --nomask-red: #ef4444;
      --nomask-red-glow: rgba(239, 68, 68, 0.35);
      --radius: 16px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    body {
      background-color: var(--bg-primary);
      background-image: 
        radial-gradient(at 0% 0%, rgba(6, 182, 212, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(59, 130, 246, 0.12) 0px, transparent 50%);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      padding: 24px;
    }

    header {
      max-width: 1280px;
      margin: 0 auto 28px auto;
      width: 100%;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--bg-card-border);
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .brand-icon {
      width: 44px;
      height: 44px;
      background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      box-shadow: 0 4px 20px rgba(6, 182, 212, 0.3);
    }

    .brand-text h1 {
      font-size: 1.4rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      background: linear-gradient(to right, #ffffff, #cbd5e1);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .brand-text p {
      font-size: 0.85rem;
      color: var(--text-muted);
    }

    .header-pills {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    .pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 0.8rem;
      font-weight: 500;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--bg-card-border);
      backdrop-filter: blur(8px);
      text-decoration: none;
      color: var(--text-main);
      transition: all 0.2s;
    }

    .pill:hover {
      background: rgba(255, 255, 255, 0.1);
    }

    .pill-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--mask-green);
      box-shadow: 0 0 8px var(--mask-green);
    }

    main {
      max-width: 1280px;
      margin: 0 auto;
      width: 100%;
      flex: 1;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
    }

    @media (max-width: 900px) {
      main {
        grid-template-columns: 1fr;
      }
    }

    .card {
      background: var(--bg-card);
      border: 1px solid var(--bg-card-border);
      backdrop-filter: blur(16px);
      border-radius: var(--radius);
      padding: 24px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
      position: relative;
    }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }

    .card-title {
      font-size: 1.15rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .view-container {
      position: relative;
      width: 100%;
      height: 380px;
      background: #030712;
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.05);
      display: flex;
      align-items: center;
      justify-content: center;
    }

    video {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transform: scaleX(-1);
    }

    #previewImg {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      display: none;
    }

    .hud-badge {
      position: absolute;
      top: 16px;
      left: 16px;
      padding: 10px 18px;
      border-radius: 10px;
      font-size: 0.95rem;
      font-weight: 700;
      letter-spacing: 0.03em;
      text-transform: uppercase;
      display: none;
      backdrop-filter: blur(10px);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
      z-index: 10;
      transition: all 0.25s ease;
    }

    .hud-badge.mask {
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(16, 185, 129, 0.85);
      color: #ffffff;
      box-shadow: 0 0 25px var(--mask-green-glow);
      border: 1px solid #34d399;
    }

    .hud-badge.nomask {
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(239, 68, 68, 0.85);
      color: #ffffff;
      box-shadow: 0 0 25px var(--nomask-red-glow);
      border: 1px solid #f87171;
    }

    .fps-counter {
      position: absolute;
      bottom: 12px;
      right: 12px;
      font-size: 0.75rem;
      color: rgba(255, 255, 255, 0.7);
      background: rgba(0, 0, 0, 0.6);
      padding: 4px 8px;
      border-radius: 6px;
      font-family: monospace;
      z-index: 10;
    }

    .controls {
      display: flex;
      gap: 12px;
      margin-top: 18px;
      flex-wrap: wrap;
    }

    .btn {
      padding: 10px 20px;
      border-radius: 10px;
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      border: none;
      transition: all 0.2s;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }

    .btn-primary {
      background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
      color: #ffffff;
      box-shadow: 0 4px 15px rgba(6, 182, 212, 0.25);
    }

    .btn-primary:hover {
      opacity: 0.92;
      transform: translateY(-1px);
    }

    .btn-secondary {
      background: rgba(255, 255, 255, 0.08);
      color: var(--text-main);
      border: 1px solid var(--bg-card-border);
    }

    .btn-secondary:hover {
      background: rgba(255, 255, 255, 0.14);
    }

    .btn-sample {
      font-size: 0.8rem;
      padding: 8px 14px;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.05);
      color: #cbd5e1;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .btn-sample:hover {
      background: rgba(255, 255, 255, 0.12);
      color: #ffffff;
    }

    .dropzone {
      border: 2px dashed rgba(255, 255, 255, 0.15);
      border-radius: 12px;
      padding: 30px 20px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s;
      background: rgba(255, 255, 255, 0.02);
      margin-bottom: 16px;
    }

    .dropzone:hover, .dropzone.dragover {
      border-color: var(--accent-cyan);
      background: rgba(6, 182, 212, 0.06);
    }

    .dropzone-icon {
      font-size: 32px;
      margin-bottom: 8px;
      color: var(--text-muted);
    }

    .dropzone p {
      font-size: 0.85rem;
      color: var(--text-muted);
    }

    .result-box {
      margin-top: 18px;
      background: rgba(0, 0, 0, 0.35);
      border-radius: 12px;
      padding: 16px;
      border: 1px solid var(--bg-card-border);
    }

    .result-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      font-size: 0.9rem;
    }

    .result-label {
      color: var(--text-muted);
    }

    .result-value {
      font-weight: 700;
    }

    .progress-track {
      width: 100%;
      height: 10px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 9999px;
      overflow: hidden;
      margin-top: 4px;
    }

    .progress-fill {
      height: 100%;
      width: 0%;
      border-radius: 9999px;
      transition: width 0.35s ease, background 0.35s ease;
    }

    .sample-chips {
      display: flex;
      gap: 10px;
      margin-top: 12px;
      flex-wrap: wrap;
      align-items: center;
    }

    .sample-label {
      font-size: 0.8rem;
      color: var(--text-muted);
    }

    footer {
      max-width: 1280px;
      margin: 28px auto 0 auto;
      width: 100%;
      text-align: center;
      font-size: 0.8rem;
      color: var(--text-muted);
      padding-top: 20px;
      border-top: 1px solid var(--bg-card-border);
    }
  </style>
</head>
<body>

  <header>
    <div class="brand">
      <div class="brand-icon">😷</div>
      <div class="brand-text">
        <h1>Face Mask Detection Demo</h1>
        <p>Transfer Learning with MobileNetV2 &bull; OpenCV Pipeline &bull; FastAPI</p>
      </div>
    </div>
    <div class="header-pills">
      <div class="pill" id="healthPill">
        <span class="pill-dot"></span>
        <span id="healthText">Connecting to API...</span>
      </div>
      <a class="pill" href="/docs" target="_blank" title="Open Interactive Swagger Documentation">
        <span>📖 Swagger API Docs</span>
      </a>
      <a class="pill" href="/health" target="_blank" title="Health Endpoint">
        <span>🩺 /health</span>
      </a>
    </div>
  </header>

  <main>
    <!-- Card 1: Live Webcam Detection -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">
          <span>📹</span> Real-time Webcam Stream
        </div>
        <span class="pill" id="camStatusPill" style="font-size:0.75rem;">Camera Offline</span>
      </div>

      <div class="view-container" id="webcamContainer">
        <video id="webcamVideo" autoplay playsinline muted></video>
        <div class="hud-badge" id="webcamHudBadge">MASK DETECTED</div>
        <div class="fps-counter" id="webcamLatency">Latency: --</div>
      </div>

      <div class="controls">
        <button class="btn btn-primary" id="btnStartCam" onclick="toggleWebcam()">
          <span>▶</span> Start Webcam
        </button>
        <button class="btn btn-secondary" id="btnStopCam" onclick="stopWebcam()" style="display:none;">
          <span>⏹</span> Stop Webcam
        </button>
      </div>

      <div class="result-box">
        <div class="result-row">
          <span class="result-label">Live Classification:</span>
          <span class="result-value" id="livePredLabel">Standby</span>
        </div>
        <div class="result-row">
          <span class="result-label">Confidence:</span>
          <span class="result-value" id="liveConfLabel">0.0%</span>
        </div>
        <div class="result-row">
          <span class="result-label">Face Localization:</span>
          <span class="result-value" id="liveFaceLabel" style="font-size:0.85rem; font-weight:500; color:var(--text-muted);">Standby</span>
        </div>
        <div class="progress-track">
          <div class="progress-fill" id="liveProgressFill"></div>
        </div>
      </div>
    </div>

    <!-- Card 2: Image Upload & Sample Testing -->
    <div class="card">
      <div class="card-header">
        <div class="card-title">
          <span>🖼️</span> Image Upload & Test Samples
        </div>
      </div>

      <div class="dropzone" id="dropzone" onclick="document.getElementById('fileInput').click()">
        <input type="file" id="fileInput" accept="image/*" style="display:none;" onchange="handleFileSelect(event)">
        <div class="dropzone-icon">📁</div>
        <strong>Click or Drag & Drop an image here</strong>
        <p>Supports JPEG, PNG, WebP (Automatically preprocessed with OpenCV to 224&times;224)</p>
      </div>

      <div class="sample-chips">
        <span class="sample-label">Quick Test Samples:</span>
        <button class="btn btn-sample" onclick="loadSample('with_mask_sample.png')">
          😷 Sample 1: With Mask
        </button>
        <button class="btn btn-sample" onclick="loadSample('without_mask_sample.jpg')">
          👤 Sample 2: Without Mask
        </button>
      </div>

      <div class="view-container" style="margin-top: 16px; height: 260px;">
        <img id="previewImg" alt="Upload Preview">
        <div class="hud-badge" id="uploadHudBadge">MASK DETECTED</div>
        <div class="fps-counter" id="uploadLatency">Latency: --</div>
      </div>

      <div class="result-box">
        <div class="result-row">
          <span class="result-label">Prediction:</span>
          <span class="result-value" id="uploadPredLabel">No image analyzed yet</span>
        </div>
        <div class="result-row">
          <span class="result-label">Confidence Score:</span>
          <span class="result-value" id="uploadConfLabel">--</span>
        </div>
        <div class="result-row">
          <span class="result-label">Face Localization:</span>
          <span class="result-value" id="uploadFaceLabel" style="font-size:0.85rem; font-weight:500; color:var(--text-muted);">--</span>
        </div>
        <div class="progress-track">
          <div class="progress-fill" id="uploadProgressFill"></div>
        </div>
      </div>
    </div>
  </main>

  <footer>
    <p>Face Mask Detection &bull; MobileNetV2 Transfer Learning Backend &bull; Ready for React Frontend Integration (Member 2)</p>
  </footer>

  <script>
    // ---------------------------------------------------------
    // Health Check Initialization
    // ---------------------------------------------------------
    async function checkHealth() {
      try {
        const res = await fetch('/health');
        if (res.ok) {
          const data = await res.json();
          const dot = document.querySelector('.pill-dot');
          const text = document.getElementById('healthText');
          if (data.model_loaded) {
            dot.style.background = '#10b981';
            dot.style.boxShadow = '0 0 8px #10b981';
            text.textContent = 'API Ready • Model Loaded';
          } else {
            dot.style.background = '#f59e0b';
            dot.style.boxShadow = '0 0 8px #f59e0b';
            text.textContent = 'API Ready • Model Not Loaded';
          }
        }
      } catch (e) {
        const dot = document.querySelector('.pill-dot');
        const text = document.getElementById('healthText');
        dot.style.background = '#ef4444';
        dot.style.boxShadow = '0 0 8px #ef4444';
        text.textContent = 'Backend Offline';
      }
    }
    checkHealth();

    // ---------------------------------------------------------
    // Webcam Live Stream
    // ---------------------------------------------------------
    const video = document.getElementById('webcamVideo');
    let stream = null;
    let streamInterval = null;
    let isPredicting = false;

    async function toggleWebcam() {
      if (stream) {
        stopWebcam();
        return;
      }
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: { width: { ideal: 640 }, height: { ideal: 480 }, facingMode: 'user' }
        });
        video.srcObject = stream;
        document.getElementById('btnStartCam').style.display = 'none';
        document.getElementById('btnStopCam').style.display = 'inline-flex';
        document.getElementById('camStatusPill').textContent = 'Camera Active (2 FPS)';
        document.getElementById('camStatusPill').style.color = '#10b981';

        // Capture frame every 500ms (2 FPS)
        streamInterval = setInterval(captureAndPredictWebcamFrame, 500);
      } catch (err) {
        alert('Could not access webcam: ' + err.message + '\\nYou can still test with image upload or sample chips on the right!');
        console.error('Camera access error:', err);
      }
    }

    function stopWebcam() {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
      }
      if (streamInterval) {
        clearInterval(streamInterval);
        streamInterval = null;
      }
      video.srcObject = null;
      document.getElementById('btnStartCam').style.display = 'inline-flex';
      document.getElementById('btnStopCam').style.display = 'none';
      document.getElementById('camStatusPill').textContent = 'Camera Offline';
      document.getElementById('camStatusPill').style.color = 'var(--text-muted)';
      document.getElementById('webcamHudBadge').style.display = 'none';
      document.getElementById('livePredLabel').textContent = 'Standby';
      document.getElementById('liveConfLabel').textContent = '0.0%';
      document.getElementById('liveProgressFill').style.width = '0%';
    }

    async function captureAndPredictWebcamFrame() {
      if (!stream || isPredicting || video.readyState < 2) return;
      isPredicting = true;

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 480;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      const t0 = performance.now();
      canvas.toBlob(async (blob) => {
        if (!blob) {
          isPredicting = false;
          return;
        }

        const formData = new FormData();
        formData.append('file', blob, 'webcam.jpg');

        try {
          const res = await fetch('/predict', { method: 'POST', body: formData });
          const latency = Math.round(performance.now() - t0);
          document.getElementById('webcamLatency').textContent = `Latency: ${latency}ms`;

          if (res.ok) {
            const data = await res.json();
            updateLiveHud(data);
          }
        } catch (e) {
          console.error('Webcam prediction error:', e);
        } finally {
          isPredicting = false;
        }
      }, 'image/jpeg', 0.85);
    }

    function updateLiveHud(data) {
      const badge = document.getElementById('webcamHudBadge');
      const predLabel = document.getElementById('livePredLabel');
      const confLabel = document.getElementById('liveConfLabel');
      const progress = document.getElementById('liveProgressFill');

      const isMask = data.prediction.toLowerCase().includes('mask') && !data.prediction.toLowerCase().includes('without');
      const pct = (data.confidence * 100).toFixed(1);

      predLabel.textContent = data.prediction;
      confLabel.textContent = pct + '%';
      progress.style.width = pct + '%';

      const liveFace = document.getElementById('liveFaceLabel');
      if (liveFace) {
        if (data.face_detected && data.box) {
          liveFace.textContent = `Face Localized [${data.box.join(', ')}]`;
          liveFace.style.color = '#38bdf8';
        } else {
          liveFace.textContent = 'Full Frame Fallback';
          liveFace.style.color = 'var(--text-muted)';
        }
      }

      if (isMask) {
        badge.className = 'hud-badge mask';
        badge.innerHTML = `<span>✓</span> MASK DETECTED (${pct}%)`;
        predLabel.style.color = '#10b981';
        progress.style.background = '#10b981';
      } else {
        badge.className = 'hud-badge nomask';
        badge.innerHTML = `<span>✕</span> NO MASK (${pct}%)`;
        predLabel.style.color = '#ef4444';
        progress.style.background = '#ef4444';
      }
      badge.style.display = 'flex';
    }

    // ---------------------------------------------------------
    // Image Upload & Sample Testing
    // ---------------------------------------------------------
    const dropzone = document.getElementById('dropzone');
    dropzone.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.classList.add('dragover'); });
    dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
    dropzone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropzone.classList.remove('dragover');
      if (e.dataTransfer.files.length) {
        predictFile(e.dataTransfer.files[0]);
      }
    });

    function handleFileSelect(event) {
      if (event.target.files.length) {
        predictFile(event.target.files[0]);
      }
    }

    async function loadSample(filename) {
      try {
        const res = await fetch('/samples/' + filename);
        if (!res.ok) throw new Error('Could not fetch sample');
        const blob = await res.blob();
        predictFile(blob, filename);
      } catch (err) {
        alert('Failed to load sample: ' + err.message);
      }
    }

    async function predictFile(fileOrBlob, filename = 'image.jpg') {
      const previewImg = document.getElementById('previewImg');
      previewImg.src = URL.createObjectURL(fileOrBlob);
      previewImg.style.display = 'block';

      const formData = new FormData();
      formData.append('file', fileOrBlob, filename);

      const t0 = performance.now();
      try {
        const res = await fetch('/predict', { method: 'POST', body: formData });
        const latency = Math.round(performance.now() - t0);
        document.getElementById('uploadLatency').textContent = `Latency: ${latency}ms`;

        if (!res.ok) {
          const err = await res.json();
          alert('Prediction failed: ' + (err.detail || res.statusText));
          return;
        }

        const data = await res.json();
        updateUploadResult(data);
      } catch (err) {
        console.error('Upload prediction error:', err);
        alert('Network error connecting to API');
      }
    }

    function updateUploadResult(data) {
      const badge = document.getElementById('uploadHudBadge');
      const predLabel = document.getElementById('uploadPredLabel');
      const confLabel = document.getElementById('uploadConfLabel');
      const progress = document.getElementById('uploadProgressFill');

      const isMask = data.prediction.toLowerCase().includes('mask') && !data.prediction.toLowerCase().includes('without');
      const pct = (data.confidence * 100).toFixed(1);

      predLabel.textContent = data.prediction;
      confLabel.textContent = pct + '%';
      progress.style.width = pct + '%';

      const uploadFace = document.getElementById('uploadFaceLabel');
      if (uploadFace) {
        if (data.face_detected && data.box) {
          uploadFace.textContent = `Face Localized [${data.box.join(', ')}]`;
          uploadFace.style.color = '#38bdf8';
        } else {
          uploadFace.textContent = 'Full Frame Fallback';
          uploadFace.style.color = 'var(--text-muted)';
        }
      }

      if (isMask) {
        badge.className = 'hud-badge mask';
        badge.innerHTML = `<span>✓</span> MASK DETECTED (${pct}%)`;
        predLabel.style.color = '#10b981';
        progress.style.background = '#10b981';
      } else {
        badge.className = 'hud-badge nomask';
        badge.innerHTML = `<span>✕</span> NO MASK (${pct}%)`;
        predLabel.style.color = '#ef4444';
        progress.style.background = '#ef4444';
      }
      badge.style.display = 'flex';
    }
  </script>
</body>
</html>
"""
