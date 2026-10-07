import React from 'react';
import { Cpu, Layers, GitFork, ArrowDown, Sparkles, CheckCircle2, ShieldCheck, Zap } from 'lucide-react';
import { modelInfo } from '../data/projectData';

export const Model = () => {
  return (
    <section id="model" className="section-padding model-section">
      <div className="container">
        <div className="section-header text-center">
          <span className="section-subtitle">Deep Learning Architecture</span>
          <h2 className="section-title">
            <span className="gradient-text">{modelInfo.architecture} + Transfer Learning</span>
          </h2>
          <p className="section-description">
            Leveraging pre-trained deep convolutional neural networks for fast, lightweight edge vision inference.
          </p>
        </div>

        {/* Model Overview & Rationale Grid */}
        <div className="model-concepts-grid">
          <div className="concept-card">
            <div className="concept-header">
              <Cpu className="concept-icon" size={22} />
              <h3>What is MobileNetV2?</h3>
            </div>
            <p>
              MobileNetV2 is a lightweight deep convolutional neural network optimized for mobile and embedded vision applications. 
              It introduces <strong>inverted residual blocks</strong> and <strong>depthwise separable convolutions</strong>, 
              dramatically reducing parameters and computational complexity without compromising feature extraction power.
            </p>
          </div>

          <div className="concept-card">
            <div className="concept-header">
              <Layers className="concept-icon" size={22} />
              <h3>What is Transfer Learning?</h3>
            </div>
            <p>
              Transfer learning reuses feature weights learned from a massive dataset (ImageNet) on a new target domain. 
              By freezing early convolutional layers that detect low-level edges and textures, we only need to train custom 
              high-level classification layers for face mask recognition.
            </p>
          </div>

          <div className="concept-card">
            <div className="concept-header">
              <Zap className="concept-icon" size={22} />
              <h3>Why Pretrained Models Help</h3>
            </div>
            <p>
              Training deep vision models from scratch requires millions of labeled images and massive GPU compute hours. 
              Pretrained weights provide strong spatial features out-of-the-box, accelerating training convergence 
              and preventing overfitting on smaller hackathon datasets.
            </p>
          </div>

          <div className="concept-card">
            <div className="concept-header">
              <Sparkles className="concept-icon" size={22} />
              <h3>Why Ideal for Hackathons</h3>
            </div>
            <p>
              MobileNetV2 delivers rapid training cycles, small model size (&lt;15 MB file size), and ultra-low latency inference 
              (&lt;30 ms per frame), making it ideal for seamless live browser video prediction during live judging demonstrations.
            </p>
          </div>
        </div>

        {/* Visual Pipeline Diagram */}
        <div className="model-pipeline-wrapper">
          <h3 className="pipeline-title">Visual Model Architecture Pipeline</h3>
          
          <div className="pipeline-flow">
            <div className="pipeline-node">
              <div className="node-icon"><Cpu size={20} /></div>
              <div className="node-content">
                <span className="node-step">Stage 1</span>
                <span className="node-name">Input Image</span>
                <span className="node-sub">Webcam RGB Frame</span>
              </div>
            </div>

            <div className="pipeline-arrow"><ArrowDown size={18} /></div>

            <div className="pipeline-node">
              <div className="node-icon"><Zap size={20} /></div>
              <div className="node-content">
                <span className="node-step">Stage 2</span>
                <span className="node-name">Preprocessing</span>
                <span className="node-sub">224x224 &bull; Scaled [-1, 1]</span>
              </div>
            </div>

            <div className="pipeline-arrow"><ArrowDown size={18} /></div>

            <div className="pipeline-node highlighted">
              <div className="node-icon"><Layers size={20} /></div>
              <div className="node-content">
                <span className="node-step">Stage 3</span>
                <span className="node-name">MobileNetV2 Backbone</span>
                <span className="node-sub">Inverted Residual Blocks</span>
              </div>
            </div>

            <div className="pipeline-arrow"><ArrowDown size={18} /></div>

            <div className="pipeline-node">
              <div className="node-icon"><Sparkles size={20} /></div>
              <div className="node-content">
                <span className="node-step">Stage 4</span>
                <span className="node-name">Feature Extraction</span>
                <span className="node-sub">Global Average Pooling</span>
              </div>
            </div>

            <div className="pipeline-arrow"><ArrowDown size={18} /></div>

            <div className="pipeline-node">
              <div className="node-icon"><GitFork size={20} /></div>
              <div className="node-content">
                <span className="node-step">Stage 5</span>
                <span className="node-name">Classification Layer</span>
                <span className="node-sub">Dense Layer + Softmax</span>
              </div>
            </div>

            <div className="pipeline-arrow"><ArrowDown size={18} /></div>

            <div className="pipeline-node final">
              <div className="node-icon"><ShieldCheck size={20} /></div>
              <div className="node-content">
                <span className="node-step">Stage 6</span>
                <span className="node-name">Mask / No Mask</span>
                <span className="node-sub">Prediction + Confidence</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Model;
