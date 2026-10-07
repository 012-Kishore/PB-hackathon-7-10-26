import React from 'react';
import { Code, Cpu, Eye, Server, Wrench } from 'lucide-react';
import { technologiesData } from '../data/projectData';

const categoryIcons = {
  Frontend: Code,
  'AI / Machine Learning': Cpu,
  'Computer Vision & Backend': Server,
  'Development & Workflow': Wrench,
};

export const Technologies = () => {
  return (
    <section id="technologies" className="section-padding technologies-section">
      <div className="container">
        <div className="section-header text-center">
          <span className="section-subtitle">Core Infrastructure</span>
          <h2 className="section-title">
            Project <span className="gradient-text">Technology Stack</span>
          </h2>
          <p className="section-description">
            Modern tools and frameworks powering our end-to-end computer vision and web application.
          </p>
        </div>

        {/* Technology Categories Grid */}
        <div className="tech-categories-grid">
          {technologiesData.map((category, idx) => {
            const Icon = categoryIcons[category.category] || Code;
            return (
              <div key={idx} className="tech-category-card">
                <div className="category-header">
                  <div className="category-icon-box">
                    <Icon size={20} />
                  </div>
                  <h3>{category.category}</h3>
                </div>

                <div className="tech-items-list">
                  {category.items.map((tech, itemIdx) => (
                    <div key={itemIdx} className="tech-item">
                      <div className="tech-item-top">
                        <span
                          className="tech-dot"
                          style={{ backgroundColor: tech.color || '#3b82f6' }}
                        ></span>
                        <h4 className="tech-name">{tech.name}</h4>
                      </div>
                      <p className="tech-desc">{tech.desc}</p>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default Technologies;
