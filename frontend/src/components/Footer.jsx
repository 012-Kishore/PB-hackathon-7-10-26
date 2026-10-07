import React from 'react';
import { ShieldCheck } from 'lucide-react';

export const Footer = ({ scrollToSection }) => {
  return (
    <footer className="site-footer">
      <div className="container footer-container">
        <div className="footer-top-grid">
          {/* Brand Info */}
          <div className="footer-brand-col">
            <div className="footer-logo">
              <ShieldCheck className="logo-icon" size={24} />
              <span>MaskGuard<span className="highlight">AI</span></span>
            </div>
            <p className="footer-tagline">
              Real-time face mask detection web application utilizing MobileNetV2 Transfer Learning and FastAPI backend microservices.
            </p>
          </div>

          {/* Quick Navigation Links */}
          <div className="footer-links-col">
            <h4>Quick Navigation</h4>
            <ul>
              <li><button onClick={() => scrollToSection('hero')}>Home</button></li>
              <li><button onClick={() => scrollToSection('problem')}>Problem</button></li>
              <li><button onClick={() => scrollToSection('how-it-works')}>How It Works</button></li>
              <li><button onClick={() => scrollToSection('dataset')}>Dataset</button></li>
              <li><button onClick={() => scrollToSection('model')}>Model Architecture</button></li>
            </ul>
          </div>

          <div className="footer-links-col">
            <h4>Project Sections</h4>
            <ul>
              <li><button onClick={() => scrollToSection('results')}>Results & Metrics</button></li>
              <li><button onClick={() => scrollToSection('live-detection')}>Live Detection Demo</button></li>
              <li><button onClick={() => scrollToSection('technologies')}>Tech Stack</button></li>
              <li><button onClick={() => scrollToSection('team')}>Team Roles</button></li>
            </ul>
          </div>
        </div>

        <div className="footer-bottom-bar">
          <p>&copy; {new Date().getFullYear()} Face Mask Detection Hackathon Project &bull; Member 2 Frontend</p>
          <div className="footer-badges">
            <span className="tech-badge">React</span>
            <span className="tech-badge">MobileNetV2</span>
            <span className="tech-badge">FastAPI</span>
            <span className="tech-badge">OpenCV</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
