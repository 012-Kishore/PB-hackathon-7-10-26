import React from 'react';
import { Camera, Sliders, Cpu, GitFork, ArrowRight, ShieldCheck, PieChart, Layers } from 'lucide-react';

const workflowSteps = [
  {
    step: "01",
    title: "Camera / Image Input",
    icon: Camera,
    description: "Captures live video frames directly from browser webcam using HTML5 MediaDevices API.",
  },
  {
    step: "02",
    title: "Image Preprocessing",
    icon: Sliders,
    description: "Resizes frame to 224x224 RGB format, converts color space, and normalizes pixel values for model intake.",
  },
  {
    step: "03",
    title: "MobileNetV2 Architecture",
    icon: Cpu,
    description: "Leverages lightweight inverted residual blocks and depthwise separable convolutions for high-speed feature extraction.",
  },
  {
    step: "04",
    title: "Transfer Learning",
    icon: Layers,
    description: "Uses pre-trained ImageNet weights as feature backbone with a custom trained classification head.",
  },
  {
    step: "05",
    title: "Classification Layer",
    icon: GitFork,
    description: "Evaluates dense layer logits through Softmax/Sigmoid activation function for binary mapping.",
  },
  {
    step: "06",
    title: "Mask / No Mask Result",
    icon: ShieldCheck,
    description: "Outputs primary classification decision: MASK (Compliant) or NO MASK (Non-Compliant).",
  },
  {
    step: "07",
    title: "Confidence Score",
    icon: PieChart,
    description: "Calculates probability percentage (e.g., 96.4%) representing prediction certainty.",
  },
];

export const HowItWorks = () => {
  return (
    <section id="how-it-works" className="section-padding how-it-works-section">
      <div className="container">
        <div className="section-header text-center">
          <span className="section-subtitle">System Architecture</span>
          <h2 className="section-title">
            How The <span className="gradient-text">Detection Pipeline</span> Works
          </h2>
          <p className="section-description">
            From raw webcam frames to deep learning feature extraction and instant web UI prediction display.
          </p>
        </div>

        {/* Workflow Timeline / Cards Container */}
        <div className="workflow-timeline">
          {workflowSteps.map((item, index) => {
            const Icon = item.icon;
            return (
              <React.Fragment key={index}>
                <div className="timeline-card">
                  <div className="timeline-badge">
                    <span>{item.step}</span>
                  </div>
                  <div className="timeline-icon-box">
                    <Icon size={24} />
                  </div>
                  <h3 className="timeline-title">{item.title}</h3>
                  <p className="timeline-desc">{item.description}</p>
                </div>
                
                {index < workflowSteps.length - 1 && (
                  <div className="timeline-arrow">
                    <ArrowRight className="arrow-icon" size={20} />
                  </div>
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
