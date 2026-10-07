import React from 'react';
import { Database, Image, CheckCircle, Info, Layers, Layers3 } from 'lucide-react';
import { datasetInfo } from '../data/projectData';

export const Dataset = () => {
  const stats = [
    { label: "Dataset Name", value: datasetInfo.name, icon: Database },
    { label: "Source", value: datasetInfo.source, icon: Info },
    { label: "Number of Classes", value: datasetInfo.classesCount, icon: Layers3 },
    { label: "Image Dimensions", value: datasetInfo.imageDimensions, icon: Image },
    { label: "Total Images", value: datasetInfo.totalImages, icon: Image, placeholder: true },
    { label: "Mask Class Images", value: datasetInfo.maskImages, icon: CheckCircle, placeholder: true },
    { label: "No-Mask Class Images", value: datasetInfo.noMaskImages, icon: CheckCircle, placeholder: true },
    { label: "Training Split", value: datasetInfo.trainingImages, icon: Layers, placeholder: true },
    { label: "Validation Split", value: datasetInfo.validationImages, icon: Layers, placeholder: true },
  ];

  return (
    <section id="dataset" className="section-padding dataset-section">
      <div className="container">
        <div className="section-header text-center">
          <span className="section-subtitle">Data Foundation</span>
          <h2 className="section-title">
            Training & Validation <span className="gradient-text">Dataset</span>
          </h2>
          <p className="section-description">
            Structured image corpus utilized for MobileNetV2 transfer learning model training and evaluation.
          </p>
        </div>

        {/* Pending ML Notice Banner */}
        {!datasetInfo.isUpdatedByML && (
          <div className="status-notice-banner info">
            <Info className="banner-icon" size={20} />
            <div>
              <strong>ML Team Notice (Member 1):</strong> {datasetInfo.statusMessage}.
              <br />
              <small>Actual sample counts will be updated directly in <code>src/data/projectData.js</code> after training completion.</small>
            </div>
          </div>
        )}

        {/* Dataset Stats Cards Grid */}
        <div className="dataset-grid">
          {stats.map((item, index) => {
            const Icon = item.icon;
            const isPlaceholder = item.value === "Pending ML Team" || item.placeholder;

            return (
              <div key={index} className={`dataset-card ${isPlaceholder ? 'placeholder-state' : ''}`}>
                <div className="dataset-card-header">
                  <div className="icon-wrapper">
                    <Icon size={20} />
                  </div>
                  <span className="dataset-label">{item.label}</span>
                </div>
                <div className="dataset-card-body">
                  <span className={`dataset-value ${isPlaceholder ? 'placeholder-text' : ''}`}>
                    {item.value}
                  </span>
                </div>
                {isPlaceholder && (
                  <span className="placeholder-tag">Configurable in projectData.js</span>
                )}
              </div>
            );
          })}
        </div>

        {/* Class Distribution Overview */}
        <div className="dataset-classes-box">
          <h3>Target Classification Categories</h3>
          <div className="classes-grid">
            <div className="class-badge-card mask">
              <span className="status-dot green"></span>
              <div>
                <strong>Class 0: Mask (With Mask)</strong>
                <p>Images featuring individuals correctly wearing protective face masks.</p>
              </div>
            </div>
            
            <div className="class-badge-card nomask">
              <span className="status-dot red"></span>
              <div>
                <strong>Class 1: No Mask (Without Mask)</strong>
                <p>Images featuring individuals without face masks or with incorrect coverage.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Dataset;
