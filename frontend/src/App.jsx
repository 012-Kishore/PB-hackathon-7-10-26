import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Problem from './components/Problem';
import HowItWorks from './components/HowItWorks';
import Dataset from './components/Dataset';
import Model from './components/Model';
import Results from './components/Results';
import LiveDetection from './components/LiveDetection';
import Technologies from './components/Technologies';
import Team from './components/Team';
import Footer from './components/Footer';

export function App() {
  const [activeSection, setActiveSection] = useState('hero');

  const scrollToSection = (id) => {
    setActiveSection(id);
    const element = document.getElementById(id);
    if (element) {
      const offset = 80; // Navbar offset height
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - offset;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth',
      });
    }
  };

  useEffect(() => {
    const handleScroll = () => {
      const sections = [
        'hero',
        'problem',
        'how-it-works',
        'dataset',
        'model',
        'results',
        'live-detection',
        'technologies',
        'team',
      ];

      const scrollPosition = window.scrollY + 200;

      for (const sectionId of sections) {
        const element = document.getElementById(sectionId);
        if (element) {
          const top = element.offsetTop;
          const height = element.offsetHeight;
          if (scrollPosition >= top && scrollPosition < top + height) {
            setActiveSection(sectionId);
            break;
          }
        }
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="app-root">
      <Navbar activeSection={activeSection} scrollToSection={scrollToSection} />
      
      <main>
        <Hero scrollToSection={scrollToSection} />
        <Problem />
        <HowItWorks />
        <Dataset />
        <Model />
        <Results />
        <LiveDetection />
        <Technologies />
        <Team />
      </main>

      <Footer scrollToSection={scrollToSection} />
    </div>
  );
}

export default App;
