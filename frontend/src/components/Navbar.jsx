import React, { useState, useEffect } from 'react';
import { ShieldCheck, Menu, X, Camera, Sparkles } from 'lucide-react';

const navItems = [
  { id: 'hero', label: 'Home' },
  { id: 'problem', label: 'Problem' },
  { id: 'how-it-works', label: 'How It Works' },
  { id: 'dataset', label: 'Dataset' },
  { id: 'model', label: 'Model' },
  { id: 'results', label: 'Results' },
  { id: 'live-detection', label: 'Live Detection' },
  { id: 'technologies', label: 'Technologies' },
  { id: 'team', label: 'Team' },
];

export const Navbar = ({ activeSection, scrollToSection }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 40);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleNavClick = (id) => {
    scrollToSection(id);
    setMobileMenuOpen(false);
  };

  return (
    <header className={`navbar-header ${scrolled ? 'scrolled' : ''}`}>
      <div className="navbar-container">
        {/* Brand Logo */}
        <a 
          href="#hero" 
          className="navbar-brand"
          onClick={(e) => {
            e.preventDefault();
            handleNavClick('hero');
          }}
        >
          <div className="brand-icon-wrapper">
            <ShieldCheck className="brand-icon" />
          </div>
          <span className="brand-text">
            MaskGuard<span className="brand-highlight">AI</span>
          </span>
          <span className="brand-badge">Hackathon</span>
        </a>

        {/* Desktop Navigation Links */}
        <nav className="desktop-nav">
          {navItems.map((item) => (
            <button
              key={item.id}
              className={`nav-link ${activeSection === item.id ? 'active' : ''}`}
              onClick={() => handleNavClick(item.id)}
            >
              {item.label}
            </button>
          ))}
        </nav>

        {/* Action Button */}
        <div className="navbar-actions">
          <button
            className="btn-nav-primary"
            onClick={() => handleNavClick('live-detection')}
          >
            <Camera className="btn-icon" />
            <span>Try Live Demo</span>
          </button>

          {/* Mobile Menu Toggle Button */}
          <button
            className="mobile-toggle-btn"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle navigation menu"
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer Menu */}
      {mobileMenuOpen && (
        <div className="mobile-menu-drawer">
          <nav className="mobile-nav-list">
            {navItems.map((item) => (
              <button
                key={item.id}
                className={`mobile-nav-link ${activeSection === item.id ? 'active' : ''}`}
                onClick={() => handleNavClick(item.id)}
              >
                <span>{item.label}</span>
                {item.id === 'live-detection' && (
                  <span className="mobile-link-pill">Live</span>
                )}
              </button>
            ))}
          </nav>
        </div>
      )}
    </header>
  );
};

export default Navbar;
