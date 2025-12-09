import { useEffect, useState } from 'react';
import NavBar from '../components/NavBar'
import StepBar from '../components/StepBar';
import { Button } from '@mantine/core';

function Processing() {

    const [activeIndex, setActiveIndex] = useState(0);

    return (
        <div className='page'>
            <NavBar />
            <div className="main-rect">
                {/* <StepBar activeIdx={activeIndex}/> */}
                <Button className='previous-button' onClick={() => setActiveIndex(activeIndex - 1)}>Previous step</Button>
                <Button className='next-button' onClick={() => setActiveIndex(activeIndex + 1)}>Next step</Button>
            </div>
        </div>
    );
}

export default Processing