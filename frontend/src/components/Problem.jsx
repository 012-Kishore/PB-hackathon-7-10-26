import React from 'react';
import { AlertTriangle, UserX, Eye, Target, ShieldAlert, CheckCircle2 } from 'lucide-react';

export const Problem = () => {
  const problems = [
    {
      icon: AlertTriangle,
      title: "Public Health Safety",
      description: "Managing mask compliance in crowded public venues, hospitals, transport hubs, and entry gates requires continuous, reliable monitoring.",
    },
    {
      icon: UserX,
      title: "Limitations of Manual Monitoring",
      description: "Manual security inspections are prone to human fatigue, inconsistent enforcement, high operational costs, and unavoidable physical contact risks.",
    },
    {
      icon: Eye,
      title: "Automated Computer Vision Assistance",
      description: "Deep learning models instantly evaluate video frames 24/7 without fatigue, providing contactless, instantaneous detection with objective confidence scores.",
    },
    {
      icon: Target,
      title: "Project Mission & Scope",
      description: "Deliver a lightweight, deployable MobileNetV2 architecture running on web browsers and edge devices for rapid, accurate face mask verification.",
    },
  ];

  return (
    <section id="problem" className="section-padding problem-section">
      <div className="container">
        <div className="section-header text-center">
          <span className="section-subtitle">Challenge & Background</span>
          <h2 className="section-title">
            Why <span className="gradient-text">Automated Mask Detection</span> Matters
          </h2>
          <p className="section-description">
            Addressing safety enforcement bottlenecks through intelligent computer vision and low-latency deep learning.
          </p>
        </div>

        {/* 2x2 Problem Cards Grid */}
        <div className="problem-grid">
          {problems.map((item, index) => {
            const Icon = item.icon;
            return (
              <div key={index} className="problem-card">
                <div className="card-icon-wrapper">
                  <Icon className="card-icon" size={24} />
                </div>
                <h3 className="card-title">{item.title}</h3>
                <p className="card-desc">{item.description}</p>
              </div>
            );
          })}
        </div>

        {/* Comparison Callout Box */}
        <div className="problem-comparison-box">
          <div className="comparison-col manual">
            <div className="comparison-header">
              <ShieldAlert className="col-icon red" size={20} />
              <h4>Manual Monitoring Drawbacks</h4>
            </div>
            <ul>
              <li><span className="bullet red">&times;</span> High labor costs and human error</li>
              <li><span className="bullet red">&times;</span> Slow reaction time & physical exposure risks</li>
              <li><span className="bullet red">&times;</span> Inconsistent compliance logging across shifts</li>
            </ul>
          </div>

          <div className="comparison-divider">
            <span>VS</span>
          </div>

          <div className="comparison-col automated">
            <div className="comparison-header">
              <CheckCircle2 className="col-icon green" size={20} />
              <h4>AI MobileNetV2 Vision Solution</h4>
            </div>
            <ul>
              <li><span className="bullet green">&check;</span> 24/7 continuous real-time video inference</li>
              <li><span className="bullet green">&check;</span> Instant confidence score classification</li>
              <li><span className="bullet green">&check;</span> Lightweight footprint suitable for edge & web</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Problem;
