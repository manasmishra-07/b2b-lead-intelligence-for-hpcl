import { useNavigate } from 'react-router-dom';
import { Zap, Brain, TrendingUp, Shield, Users, Sparkles, ArrowRight, CheckCircle, BarChart3, Bell, Globe } from 'lucide-react';

function Landing() {
  const navigate = useNavigate();

  const features = [
    {
      icon: Brain,
      title: "AI-Powered Intelligence",
      description: "Advanced NLP analyzes web signals and automatically recommends the perfect HPCL products"
    },
    {
      icon: Zap,
      title: "Real-Time Lead Detection",
      description: "Scrapes news, tenders, and company announcements 24/7 to find opportunities instantly"
    },
    {
      icon: TrendingUp,
      title: "Smart Lead Scoring",
      description: "ML algorithms score and prioritize leads based on intent, urgency, and company profile"
    },
    {
      icon: Bell,
      title: "Instant Notifications",
      description: "Email alerts with complete dossiers delivered directly to assigned sales officers"
    },
    {
      icon: BarChart3,
      title: "Analytics Dashboard",
      description: "Track conversion rates, product distribution, and territory performance in real-time"
    },
    {
      icon: Shield,
      title: "Enterprise Security",
      description: "Built with production-grade security and compliance for Fortune 500 operations"
    }
  ];

  const products = [
    "Furnace Oil (FO)",
    "High Speed Diesel (HSD)",
    "Low Sulphur Heavy Stock (LSHS)",
    "Bitumen",
    "Hexane",
    "Marine Bunker Fuel",
    "Light Diesel Oil (LDO)",
    "Solvent 1425",
    "Mineral Turpentine Oil",
    "Jute Batch Oil"
  ];

  const stats = [
    { label: "Lead Detection Accuracy", value: "95%" },
    { label: "Average Lead Score", value: "78/100" },
    { label: "Processing Speed", value: "<2s" },
    { label: "Product Coverage", value: "10+" }
  ];

  return (
    <div className="landing-page">
      {/* Animated Background */}
      <div className="landing-bg-animation"></div>

      {/* Navigation */}
      <nav className="landing-nav">
        <div className="landing-nav-content">
          <div className="landing-logo">
            <div className="logo-icon">HP</div>
            <div>
              <h2>HPCL</h2>
              <p>Lead Intelligence</p>
            </div>
          </div>
          <button onClick={() => navigate('/dashboard')} className="btn-primary">
            Launch Dashboard <ArrowRight className="w-4 h-4 ml-2" />
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-badge">
            <Sparkles className="w-4 h-4" />
            <span>Powered by Advanced AI & ML</span>
          </div>
          <h1 className="hero-title">
            Intelligent <span className="gradient-text">B2B Lead Discovery</span> for HPCL Direct Sales
          </h1>
          <p className="hero-subtitle">
            AI-powered system that automatically discovers high-quality industrial fuel leads, 
            infers product requirements, and delivers actionable insights to your sales team.
          </p>
          <div className="hero-buttons">
            <button onClick={() => navigate('/dashboard')} className="btn-hero-primary">
              <Zap className="w-5 h-5" />
              Get Started
            </button>
            <button className="btn-hero-secondary">
              <Globe className="w-5 h-5" />
              View Demo
            </button>
          </div>

          {/* Stats Grid */}
          <div className="stats-grid">
            {stats.map((stat, idx) => (
              <div key={idx} className="stat-card">
                <div className="stat-value">{stat.value}</div>
                <div className="stat-label">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Hero Visual */}
        <div className="hero-visual">
          <div className="floating-card card-1">
            <div className="mini-chart">
              <div className="chart-bar" style={{height: '60%'}}></div>
              <div className="chart-bar" style={{height: '80%'}}></div>
              <div className="chart-bar" style={{height: '45%'}}></div>
              <div className="chart-bar" style={{height: '90%'}}></div>
              <div className="chart-bar" style={{height: '70%'}}></div>
            </div>
            <p className="mini-text">Lead Analytics</p>
          </div>
          <div className="floating-card card-2">
            <CheckCircle className="w-8 h-8 text-green-400" />
            <p className="mini-text">New Lead Detected</p>
            <p className="mini-subtext">Tata Steel - FO</p>
          </div>
          <div className="floating-card card-3">
            <div className="score-circle">
              <div className="score-value">87</div>
            </div>
            <p className="mini-text">Lead Score</p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="section-header">
          <h2 className="section-title">Powerful Features Built for Enterprise</h2>
          <p className="section-subtitle">
            Everything you need to transform your B2B lead generation and accelerate sales
          </p>
        </div>

        <div className="features-grid">
          {features.map((feature, idx) => (
            <div key={idx} className="feature-card">
              <div className="feature-icon">
                <feature.icon className="w-6 h-6" />
              </div>
              <h3 className="feature-title">{feature.title}</h3>
              <p className="feature-description">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Products Section */}
      <section className="products-section">
        <div className="section-header">
          <h2 className="section-title">Comprehensive Product Coverage</h2>
          <p className="section-subtitle">
            AI trained to identify opportunities across HPCL's complete Direct Sales portfolio
          </p>
        </div>

        <div className="products-grid">
          {products.map((product, idx) => (
            <div key={idx} className="product-badge">
              <CheckCircle className="w-4 h-4 text-green-400" />
              <span>{product}</span>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section className="workflow-section">
        <div className="section-header">
          <h2 className="section-title">How It Works</h2>
          <p className="section-subtitle">Automated intelligence from signal to sale</p>
        </div>

        <div className="workflow-steps">
          <div className="workflow-step">
            <div className="step-number">1</div>
            <div className="step-content">
              <h3>Web Intelligence</h3>
              <p>Continuously scrapes news sites, tender portals, and company announcements</p>
            </div>
          </div>
          <div className="workflow-arrow">→</div>
          <div className="workflow-step">
            <div className="step-number">2</div>
            <div className="step-content">
              <h3>AI Analysis</h3>
              <p>NLP extracts company info, detects keywords, and infers product requirements</p>
            </div>
          </div>
          <div className="workflow-arrow">→</div>
          <div className="workflow-step">
            <div className="step-number">3</div>
            <div className="step-content">
              <h3>Smart Scoring</h3>
              <p>ML algorithms score leads based on intent strength, urgency, and company profile</p>
            </div>
          </div>
          <div className="workflow-arrow">→</div>
          <div className="workflow-step">
            <div className="step-number">4</div>
            <div className="step-content">
              <h3>Instant Delivery</h3>
              <p>Email alerts with complete dossiers sent to territory sales officers</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-content">
          <h2 className="cta-title">Ready to Transform Your Lead Generation?</h2>
          <p className="cta-subtitle">
            Join HPCL's next-generation sales intelligence platform
          </p>
          <button onClick={() => navigate('/dashboard')} className="btn-cta">
            Launch Dashboard Now
            <ArrowRight className="w-5 h-5 ml-2" />
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="footer-content">
          <div className="footer-section">
            <div className="footer-logo">
              <div className="logo-icon-small">HP</div>
              <div>
                <h3>HPCL Lead Intelligence</h3>
                <p>Powered by AI & Machine Learning</p>
              </div>
            </div>
            <p className="footer-description">
              Enterprise B2B lead intelligence platform for HPCL Direct Sales & Bulk Fuels division
            </p>
          </div>
          <div className="footer-section">
            <h4>Platform</h4>
            <ul>
              <li>Dashboard</li>
              <li>Analytics</li>
              <li>Lead Management</li>
              <li>Settings</li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Technology</h4>
            <ul>
              <li>AI/ML Models</li>
              <li>Web Scraping</li>
              <li>NLP Engine</li>
              <li>API Integration</li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Support</h4>
            <ul>
              <li>Documentation</li>
              <li>Contact DSRO</li>
              <li>System Status</li>
              <li>Feedback</li>
            </ul>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© 2026 HPCL Direct Sales. Built for Productathon Round 3.</p>
          <p>Developed with ❤️ using FastAPI, React & Advanced AI</p>
        </div>
      </footer>
    </div>
  );
}

export default Landing;