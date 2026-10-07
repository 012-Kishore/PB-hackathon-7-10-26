import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Camera, CameraOff, RefreshCw, ShieldCheck, ShieldAlert, AlertTriangle, Activity, Wifi, WifiOff, Settings } from 'lucide-react';
import { checkBackendHealth, predictImage } from '../services/api';

export const LiveDetection = () => {
  // State management
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [stream, setStream] = useState(null);
  const [cameraError, setCameraError] = useState(null);
  
  // Backend health state
  const [backendStatus, setBackendStatus] = useState({
    checked: false,
    connected: false,
    message: 'Checking connection...',
  });

  // Prediction state
  const [isPredicting, setIsPredicting] = useState(false);
  const [predictionResult, setPredictionResult] = useState(null);
  const [predictionError, setPredictionError] = useState(null);
  const [intervalMs, setIntervalMs] = useState(1000); // Default 1 second capture interval

  // Refs
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const timerRef = useRef(null);

  // Health check on mount and interval
  const verifyBackend = useCallback(async () => {
    const health = await checkBackendHealth();
    setBackendStatus({
      checked: true,
      connected: health.connected,
      message: health.connected 
        ? 'Backend Connected' 
        : (health.message || 'Backend unavailable. Please start the backend server.'),
    });
  }, []);

  useEffect(() => {
    verifyBackend();
    const healthInterval = setInterval(verifyBackend, 10000);
    return () => clearInterval(healthInterval);
  }, [verifyBackend]);

  // Capture single frame and request prediction
  const captureAndPredict = useCallback(async () => {
    if (!videoRef.current || !canvasRef.current || !isCameraActive) return;
    const video = videoRef.current;
    
    // Ensure video frame is playing and ready
    if (video.readyState !== video.HAVE_ENOUGH_DATA) return;

    const canvas = canvasRef.current;
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Draw frame to canvas
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    setIsPredicting(true);

    // Convert frame canvas to blob
    canvas.toBlob(
      async (blob) => {
        if (!blob) {
          setIsPredicting(false);
          return;
        }

        const res = await predictImage(blob);
        setIsPredicting(false);

        if (res.success) {
          setPredictionResult({
            prediction: res.normalizedPrediction, // 'MASK' or 'NO MASK'
            isMask: res.isMask,
            confidence: res.confidence, // e.g. 0.964
            rawPrediction: res.rawPrediction,
            timestamp: new Date().toLocaleTimeString(),
          });
          setPredictionError(null);
        } else {
          setPredictionError(res.error || 'Failed to analyze frame');
        }
      },
      'image/jpeg',
      0.85
    );
  }, [isCameraActive]);

  // Start continuous frame capture loop
  useEffect(() => {
    if (isCameraActive) {
      // Run first prediction after camera stabilizes
      const initialDelay = setTimeout(() => {
        captureAndPredict();
      }, 500);

      timerRef.current = setInterval(() => {
        captureAndPredict();
      }, intervalMs);

      return () => {
        clearTimeout(initialDelay);
        if (timerRef.current) clearInterval(timerRef.current);
      };
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }
  }, [isCameraActive, intervalMs, captureAndPredict]);

  // Start WebCam
  const startCamera = async () => {
    setCameraError(null);
    setPredictionError(null);

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      setCameraError('Browser WebCam API (getUserMedia) is not supported in this browser environment.');
      return;
    }

    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 1280 },
          height: { ideal: 720 },
          facingMode: 'user',
        },
        audio: false,
      });

      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      setIsCameraActive(true);
    } catch (err) {
      console.error('Camera Access Error:', err);
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        setCameraError('Camera access denied. Please grant webcam permissions in your browser address bar.');
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        setCameraError('No video camera detected on your device.');
      } else {
        setCameraError(`Failed to open camera: ${err.message || 'Unknown camera error'}`);
      }
      setIsCameraActive(false);
    }
  };

  // Stop WebCam
  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      setStream(null);
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setIsCameraActive(false);
    setIsPredicting(false);
  };

  // Clean up tracks on unmount
  useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, [stream]);

  // Helper formatting confidence percentage
  const formatConfidence = (conf) => {
    if (conf === undefined || conf === null || isNaN(conf)) return '0.0%';
    const pct = conf * 100;
    return `${pct.toFixed(1)}%`;
  };

  return (
    <section id="live-detection" className="section-padding live-detection-section">
      <div className="container">
        <div className="section-header text-center">
          <span className="section-subtitle">Real-Time Interface</span>
          <h2 className="section-title">
            Live <span className="gradient-text">Face Mask Detection</span>
          </h2>
          <p className="section-description">
            Stream browser video frames to Member 3's FastAPI backend for instantaneous MobileNetV2 prediction.
          </p>
        </div>

        {/* Connection & Configuration Bar */}
        <div className="live-controls-bar">
          <div className="connection-status-pill">
            {backendStatus.connected ? (
              <>
                <Wifi className="status-icon green" size={18} />
                <span className="status-text green">Backend Connected</span>
              </>
            ) : (
              <>
                <WifiOff className="status-icon red" size={18} />
                <span className="status-text red">Backend Offline</span>
              </>
            )}
            <button 
              className="btn-icon-refresh" 
              onClick={verifyBackend} 
              title="Refresh backend connection check"
            >
              <RefreshCw size={14} />
            </button>
          </div>

          {/* Interval Selector */}
          <div className="interval-selector">
            <Settings size={16} className="selector-icon" />
            <label htmlFor="interval-select">Capture Rate:</label>
            <select
              id="interval-select"
              value={intervalMs}
              onChange={(e) => setIntervalMs(Number(e.target.value))}
              disabled={isPredicting}
            >
              <option value={500}>Fast (0.5 sec)</option>
              <option value={1000}>Normal (1.0 sec)</option>
              <option value={2000}>Relaxed (2.0 sec)</option>
            </select>
          </div>
        </div>

        {/* Backend Warning Banner if Offline */}
        {!backendStatus.connected && (
          <div className="status-notice-banner danger">
            <AlertTriangle className="banner-icon" size={20} />
            <div>
              <strong>Backend Unavailable:</strong> Please start Member 3's FastAPI backend server at{' '}
              <code>http://localhost:8000</code>.
              <br />
              <small>Run <code>uvicorn main:app --reload</code> in the backend repository.</small>
            </div>
          </div>
        )}

        {/* Main Interface Layout */}
        <div className="detection-workspace-grid">
          {/* Left Column: Camera Preview Box */}
          <div className="camera-preview-container">
            <div className="camera-box-header">
              <div className="camera-status-indicator">
                <span className={`dot ${isCameraActive ? 'live' : 'off'}`}></span>
                <span>{isCameraActive ? 'WebCam Live Stream' : 'Camera Disconnected'}</span>
              </div>
              {isPredicting && (
                <div className="analyzing-pill">
                  <Activity size={14} className="spin" />
                  <span>Analyzing...</span>
                </div>
              )}
            </div>

            <div className="video-viewport">
              {/* Hidden Canvas for Frame Capture */}
              <canvas ref={canvasRef} style={{ display: 'none' }} />

              {/* Video Stream Element */}
              <video
                ref={videoRef}
                autoPlay
                playsInline
                muted
                className={`video-element ${isCameraActive ? 'active' : 'hidden'}`}
              />

              {/* Camera Offline Placeholder View */}
              {!isCameraActive && (
                <div className="viewport-placeholder">
                  <CameraOff size={64} className="placeholder-cam-icon" />
                  <h3>Camera is Turned Off</h3>
                  <p>Click "Start Camera" below to initiate real-time video stream inspection.</p>
                </div>
              )}

              {/* Bounding Box Visual Overlay when prediction exists */}
              {isCameraActive && predictionResult && (
                <div className={`bounding-box-overlay ${predictionResult.isMask ? 'mask' : 'nomask'}`}>
                  <div className="overlay-badge">
                    {predictionResult.isMask ? <ShieldCheck size={14} /> : <ShieldAlert size={14} />}
                    <span>{predictionResult.prediction}</span>
                  </div>
                </div>
              )}
            </div>

            {/* Camera Control Buttons */}
            <div className="camera-action-controls">
              {!isCameraActive ? (
                <button className="btn-camera-start" onClick={startCamera}>
                  <Camera size={20} />
                  <span>Start Camera</span>
                </button>
              ) : (
                <button className="btn-camera-stop" onClick={stopCamera}>
                  <CameraOff size={20} />
                  <span>Stop Camera</span>
                </button>
              )}
            </div>

            {/* Camera Errors display */}
            {cameraError && (
              <div className="camera-error-message">
                <AlertTriangle size={16} />
                <span>{cameraError}</span>
              </div>
            )}
          </div>

          {/* Right Column: Prediction Result Card */}
          <div className="prediction-result-panel">
            <div className="panel-card-header">
              <Activity size={20} />
              <h3>Real-Time Prediction Card</h3>
            </div>

            <div className="panel-card-body">
              {predictionResult ? (
                <div className="prediction-display-box">
                  <div className="prediction-label-group">
                    <span className="field-caption">Prediction Result</span>
                    <div
                      className={`prediction-badge-main ${
                        predictionResult.isMask ? 'badge-mask' : 'badge-nomask'
                      }`}
                    >
                      {predictionResult.isMask ? (
                        <ShieldCheck size={28} />
                      ) : (
                        <ShieldAlert size={28} />
                      )}
                      <span className="prediction-text">{predictionResult.prediction}</span>
                    </div>
                  </div>

                  <div className="confidence-meter-group">
                    <div className="meter-header">
                      <span className="field-caption">Confidence Score</span>
                      <span className="confidence-percentage">
                        {formatConfidence(predictionResult.confidence)}
                      </span>
                    </div>
                    
                    <div className="meter-bar-track">
                      <div
                        className={`meter-bar-fill ${
                          predictionResult.isMask ? 'fill-mask' : 'fill-nomask'
                        }`}
                        style={{
                          width: `${Math.min(
                            100,
                            Math.max(0, (predictionResult.confidence || 0) * 100)
                          )}%`,
                        }}
                      ></div>
                    </div>
                  </div>

                  <div className="prediction-meta-info">
                    <div className="meta-item">
                      <span className="meta-label">Raw Backend Output:</span>
                      <span className="meta-val">{predictionResult.rawPrediction}</span>
                    </div>
                    <div className="meta-item">
                      <span className="meta-label">Last Evaluated:</span>
                      <span className="meta-val">{predictionResult.timestamp}</span>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="prediction-idle-state">
                  <div className="idle-icon-wrapper">
                    <ShieldCheck size={40} />
                  </div>
                  <h4>Awaiting WebCam Frames</h4>
                  <p>
                    {isCameraActive
                      ? 'Analyzing video frames... Output will update dynamically.'
                      : 'Start the camera stream to begin real-time mask inference.'}
                  </p>
                </div>
              )}

              {/* Prediction Error Alert */}
              {predictionError && (
                <div className="prediction-error-alert">
                  <AlertTriangle size={16} />
                  <div>
                    <strong>Prediction Notice:</strong> {predictionError}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default LiveDetection;
