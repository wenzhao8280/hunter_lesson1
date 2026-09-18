export default function StepProgress({ steps, currentStepId }) {
  const currentIndex = steps.findIndex((step) => step.id === currentStepId);

  return (
    <ol className="step-progress">
      {steps.map((step, index) => {
        let state = "upcoming";
        if (currentIndex === -1) state = "upcoming";
        else if (index < currentIndex) state = "done";
        else if (index === currentIndex) state = "current";

        return (
          <li key={step.id} className={`step step-${state}`}>
            <div className="step-marker">{index + 1}</div>
            <div className="step-body">
              <div className="step-name">{step.name}</div>
              {step.actor && <div className="step-actor">{step.actor}</div>}
            </div>
          </li>
        );
      })}
    </ol>
  );
}
