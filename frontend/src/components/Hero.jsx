import React from 'react';
import { Camera, ChevronRight, Cpu, ShieldCheck, Sparkles, Zap } from 'lucide-react';

export const Hero = ({ scrollToSection }) => {
  return (
    <section id="hero" className="hero-section">
      <div className="hero-background-glow"></div>
      <div className="hero-grid-pattern"></div>
      
      <div className="container hero-container">
        <div className="hero-content">
          {/* Top Pill Tag */}
          <div className="hero-pill-badge">
            <Sparkles className="pill-icon" size={16} />
            <span>Hackathon Project &bull; Transfer Learning Architecture</span>
          </div>

          {/* Main Titles */}
          <h1 className="hero-title">
            AI-Powered <span className="gradient-text">Face Mask Detection</span>
          </h1>
          
          <h2 className="hero-subtitle">
            Real-time face mask detection using MobileNetV2 Transfer Learning
          </h2>

          <p className="hero-description">
            An end-to-end computer vision application designed for real-time face mask compliance tracking. 
            Powered by a lightweight MobileNetV2 deep convolutional neural network, integrated with a high-performance 
            FastAPI backend and responsive React web interface.
          </p>

          {/* CTA Buttons */}
          <div className="hero-cta-group">
            <button
              className="btn-hero-primary"
              onClick={() => scrollToSection('live-detection')}
            >
              <Camera className="btn-icon" size={20} />
              <span>Try Live Detection</span>
              <ChevronRight className="btn-arrow" size={18} />
            </button>

            <button
              className="btn-hero-secondary"
              onClick={() => scrollToSection('how-it-works')}
            >
              <Zap className="btn-icon" size={20} />
              <span>How It Works</span>
            </button>
          </div>

          {/* Feature Highlights (No fake stats, strictly feature specs) */}
          <div className="hero-feature-pills">
            <div className="feature-pill">
              <Cpu className="pill-stat-icon" size={18} />
              <div>
                <span className="pill-title">MobileNetV2</span>
                <span className="pill-sub">Lightweight Backbone</span>
              </div>
            </div>
            
            <div className="feature-pill">
              <Zap className="pill-stat-icon" size={18} />
              <div>
                <span className="pill-title">Real-Time</span>
                <span className="pill-sub">Low Latency WebCam Streaming</span>
              </div>
            </div>

            <div className="feature-pill">
              <ShieldCheck className="pill-stat-icon" size={18} />
              <div>
                <span className="pill-title">FastAPI Backend</span>
                <span className="pill-sub">RESTful OpenCV Inference</span>
              </div>
            </div>
          </div>
        </div>

        {/* Visual Mockup Container */}
        <div className="hero-visual">
          <div className="hero-card-frame">
            <div className="card-header-bar">
              <div className="window-dots">
                <span className="dot red"></span>
                <span className="dot yellow"></span>
                <span className="dot green"></span>
              </div>
              <span className="window-title">Vision Pipeline Preview</span>
              <span className="live-status-badge">Ready</span>
            </div>

            <div className="card-visual-body">
              <div className="mockup-camera-box">
                <div className="grid-overlay"></div>
                <div className="scanning-line"></div>

                <div className="mockup-face-box mask-detected">
                  <div className="bounding-box">
                    <span className="box-corner top-left"></span>
                    <span className="box-corner top-right"></span>
                    <span className="box-corner bottom-left"></span>
                    <span className="box-corner bottom-right"></span>
                  </div>
                  <div className="prediction-tag mask">
                    <ShieldCheck size={14} />
                    <span>MASK DETECTED</span>
                  </div>
                </div>

                <div className="camera-tech-overlay">
                  <span>Frame Rate: 30 FPS</span>
                  <span>Input: 224x224 RGB</span>
                  <span>Engine: MobileNetV2</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
