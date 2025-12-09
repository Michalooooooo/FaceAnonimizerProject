import { useState } from 'react';
import { Stepper, Button, Group } from '@mantine/core';
import "../css/StepBar.css"

interface StepBarProp {
  activeIdx: number;
}

function StepBar({activeIdx}: StepBarProp) {
  
  return (
    <div className='stepper-wrapper'>
      <Stepper size="lg" active={activeIdx} className='stepper'>
        <Stepper.Step className="step" label="Step 1" description="Load video" />
        <Stepper.Step className="step" label="Step 2" description="Choose processing params" />
        <Stepper.Step className="step" label="Step 3" description="Select faces"/>
        <Stepper.Step className="step" label="Step 4" description="Download processed video"/>
      </Stepper>

    </div>
      
  );
}

export default StepBar