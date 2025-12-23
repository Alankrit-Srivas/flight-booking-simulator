import React from 'react';
import './ProgressStepper.css';

function ProgressStepper({ currentStep }) {
  const steps = [
    { number: 1, label: 'Search' },
    { number: 2, label: 'Choose flight' },
    { number: 3, label: 'Choose fare' },
    { number: 4, label: 'Passenger details' },
    { number: 5, label: 'Extra Services' },
    { number: 6, label: 'Payment' }
  ];

  return (
    <div className="progress-stepper">
      {steps.map((step, index) => (
        <React.Fragment key={step.number}>
          <div className={`step ${currentStep >= step.number ? 'active' : ''} ${currentStep > step.number ? 'completed' : ''}`}>
            <div className="step-number">{step.number}</div>
            <div className="step-label">{step.label}</div>
          </div>
          {index < steps.length - 1 && (
            <div className={`step-line ${currentStep > step.number ? 'active' : ''}`}></div>
          )}
        </React.Fragment>
      ))}
    </div>
  );
}

export default ProgressStepper;