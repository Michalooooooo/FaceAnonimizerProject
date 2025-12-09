import '../css/Home.css'
import StepBar from '../components/StepBar';
import { useState, useEffect } from 'react';
import Step1 from '../components/Step1'
import Step2 from '../components/Step2'
import Step3 from '../components/Step3';
import Step4 from '../components/Step4';
import ThankYouStep from '../components/ThankYouStep';
import { List } from 'postcss/lib/list';

function Home() {

    const [activeStep, setActiveStep] = useState(0)
    const STEP_MAX = 5
    const [videoId, setVideoId] = useState<string | null>(null);
    const [paramsForm, setParamsForm] = useState<Record<string, any>>();
    const [faces, setFaces] = useState<number[]>([]);

    useEffect(() => {
        console.log('Paramsy po odswiezeniu: ', paramsForm);

    }, [activeStep])
    return (
        <>
            <div className="home-page-wrapper">
                <StepBar activeIdx={activeStep} />
                {activeStep === 0 && <Step1
                    onSubmit={() => { setActiveStep(activeStep => Math.min(activeStep + 1, STEP_MAX)); }}
                    onUpload={(id: string) => { setVideoId(id); console.log(videoId) }} />}
                {activeStep === 1 && <Step2
                    onSubmit={(values) => {
                        setActiveStep(activeStep => Math.min(activeStep + 1, STEP_MAX));
                        setParamsForm(values)

                    }}
                    previous={() => { setActiveStep(activeStep => Math.max(activeStep - 1, 0)) }} />}
                {activeStep === 2 && paramsForm && (
                    <Step3
                        onSubmit={(values) => {
                            console.log("Formularz + wybrane twarze:", values);
                            setFaces(values.selectedFaces); 
                            setActiveStep((step) => Math.min(step + 1, STEP_MAX));
                            console.log("Wywołuje się!!!");
                        }}
                        previous={() => {
                            setActiveStep((step) => Math.max(step - 1, 0));
                        }}
                        videoId={videoId}
                        form={paramsForm}
                    />
                )}
                {activeStep === 3 && videoId && <Step4
                    onSubmit={() => { setActiveStep(activeStep => Math.min(activeStep + 1, STEP_MAX)); console.log('Wywołuje sie!!!') }}
                    previous={() => { setActiveStep(activeStep => Math.max(activeStep - 1, 0)) }} 
                    videoId={videoId}
                    facesList={faces}
                    rotate={paramsForm?.['rotation'] ?? false}/>}

                {activeStep === 4 && <ThankYouStep />}

            </div>
        </>
    );
}

export default Home;