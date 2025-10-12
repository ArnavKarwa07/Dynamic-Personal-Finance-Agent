import React from "react";
import { Link } from "react-router-dom";
import { Button } from "@ui";
import Footer from "@layout/Footer";

export default function HomePage() {
  const features = [
    {
      icon: "🤖",
      title: "AI-Powered Insights",
      description:
        "Get personalized financial advice from our intelligent assistant.",
    },
    {
      icon: "💰",
      title: "Smart Budgeting",
      description:
        "Automatically categorize expenses and optimize your spending.",
    },
    {
      icon: "📊",
      title: "Investment Tracking",
      description:
        "Monitor your portfolio performance with real-time analytics.",
    },
    {
      icon: "🎯",
      title: "Goal Planning",
      description: "Set and achieve your financial goals with guided planning.",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <div className="hero-text">
            <h1>
              Take Control of Your{" "}
              <span className="hero-highlight">Financial Future</span>
            </h1>

            <p>
              Transform your financial life with our AI-powered personal finance
              agent. Get personalized insights, smart budgeting, and investment
              recommendations tailored just for you.
            </p>

            <div className="hero-buttons">
              <Link to="/login" className="btn btn-primary">
                Get Started Free →
              </Link>

              <button className="btn btn-secondary">Watch Demo</button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="section-padding">
        <div className="container mx-auto">
          <div className="text-center mb-12">
            <h2 className="heading-2 text-gray-900 mb-6">
              Powerful Features for Your Financial Success
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Discover how our advanced AI technology and intuitive design can
              help you achieve your financial goals faster than ever before.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <div key={index} className="feature-card animate-fade-in-up">
                <div className="feature-icon">{feature.icon}</div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container mx-auto text-center relative z-10">
          <h2 className="heading-2 text-white mb-6">
            Ready to Transform Your Financial Future?
          </h2>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto mb-10 leading-relaxed">
            Join thousands of users who have already taken control of their
            finances with our AI-powered platform.
          </p>

          <div className="flex justify-center mb-10">
            <Link to="/login" className="btn btn-primary btn-lg">
              Start Your Journey Today →
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-base">
            <div className="flex items-center justify-center gap-3">
              <span className="text-green-400 text-xl">✓</span>
              <span className="text-blue-100">Free to get started</span>
            </div>
            <div className="flex items-center justify-center gap-3">
              <span className="text-green-400 text-xl">✓</span>
              <span className="text-blue-100">No credit card required</span>
            </div>
            <div className="flex items-center justify-center gap-3">
              <span className="text-green-400 text-xl">✓</span>
              <span className="text-blue-100">Cancel anytime</span>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <Footer />
    </div>
  );
}
