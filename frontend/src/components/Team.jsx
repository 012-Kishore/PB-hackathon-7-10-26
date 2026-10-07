import React from 'react';
import { User, CheckCircle2, Award } from 'lucide-react';
import { teamData } from '../data/projectData';

export const Team = () => {
  return (
    <section id="team" className="section-padding team-section">
      <div className="container">
        <div className="section-header text-center">
          <span className="section-subtitle">Hackathon Collaboration</span>
          <h2 className="section-title">
            Meet The <span className="gradient-text">Project Team</span>
          </h2>
          <p className="section-description">
            A 3-member cross-functional team collaborating across machine learning, web frontend, and backend computer vision.
          </p>
        </div>

        {/* 3 Team Cards Grid */}
        <div className="team-grid">
          {teamData.map((member, index) => (
            <div key={index} className="team-card">
              <div className="team-avatar-box">
                <User size={36} className="avatar-icon" />
              </div>

              <div className="team-role-tag">{member.tag}</div>
              
              <h3 className="team-member-role">{member.role}</h3>
              <h4 className="team-member-name">{member.name}</h4>

              <div className="responsibilities-list">
                <span className="resp-header">Key Responsibilities:</span>
                <ul>
                  {member.responsibilities.map((resp, respIdx) => (
                    <li key={respIdx}>
                      <CheckCircle2 size={14} className="check-icon" />
                      <span>{resp}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Team;
