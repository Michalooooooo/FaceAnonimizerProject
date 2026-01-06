import { useForm } from '@mantine/form';
import { TextInput, NumberInput, Switch, Button, Group, Box, Select, Center, SimpleGrid } from '@mantine/core';
import { useState } from 'react';
import "../css/Step2.css";

function Step2({ onSubmit, previous }: { onSubmit: (values: any) => void, previous: (values: any) => void }) {
    const [disableREID, setDisableREID] = useState(false);

    const form = useForm({
        validateInputOnChange: true,

        initialValues: {
            norfair_params: {
                distance_function: 'mean_euclidean',
                distance_threshold: 30,
                hit_counter_max: 10,
                initialization_delay: 2,
                reid_distance_function: 'cosine',
                pointwise_hit_counter_max: 0,
                detection_threshold: 0.4,
                past_detections_length: 5,
                reid_distance_threshold: 0.2,
                reid_hit_counter_max: 300,
            },
            yolo_model: 'yolo11s_reduced_dataset',
            yolo_batch_size: 32,
            yolo_params: {
                conf: 0.4,
                iou: 0.4,
                half: true,
                device: 'cuda',
                verbose: false,
            },
            rotation: false,
        },

        validate: {
            yolo_model: (v) => v ? null : "Required",
            yolo_batch_size: (v) => v > 0 ? null : "Must be > 0",

            yolo_params: {
                conf: (v) => v > 0 ? null : "Required",
                iou: (v) => v > 0 ? null : "Required",
            },

            norfair_params: {
                distance_threshold: (v) => v > 0 ? null : "Required",
                hit_counter_max: (v) => v > 0 ? null : "Required",
                initialization_delay: (v) => v >= 0 ? null : "Required",
                pointwise_hit_counter_max: (v) => v >= 0 ? null : "Required",
                detection_threshold: (v) => v > 0 ? null : "Required",
                past_detections_length: (v) => v >= 0 ? null : "Required",

                // REID pola walidujemy tylko gdy włączone
                reid_distance_threshold: (v) =>
                    disableREID ? (v > 0 ? null : "Required") : null,

                reid_hit_counter_max: (v) =>
                    disableREID ? (v > 0 ? null : "Required") : null,
            }
        }
    });

    const removeInactiveFields = () => {
        const values = form.values;

        if (!disableREID) {
            const { reid_distance_threshold, reid_hit_counter_max, reid_distance_function, ...norfairRest } =
                values.norfair_params;
            return { ...values, norfair_params: norfairRest };
        }

        return values;
    };

    const inputStyles = {
        input: { backgroundColor: "rgba(197, 220, 232, 1)", border: "1px solid rgb(24, 100, 171)", color: "rgb(36, 36, 36)" },
        label: { color: "rgb(24, 100, 171)", fontSize: 18 },
    };

    const isValid = Object.keys(form.errors).length === 0;

    return (
        <>
            <center><h1 style={{ fontWeight: "bold", fontSize: "50px", color: "rgb(24, 100, 171)" }}>Select processing parameters</h1></center>

            <form onSubmit={form.onSubmit(() => onSubmit(removeInactiveFields()))}>
                <Center>
                    <SimpleGrid cols={2} spacing="20rem">

                        {/* LEFT PANEL --------------------------------------------------*/}
                        <Box mb="md">
                            <h3 style={{ fontWeight: "bold", fontSize: "30px", color: "rgb(24, 100, 171)" }}>Video position</h3>
                            <Switch
                                label="Rotation"
                                {...form.getInputProps('rotation', { type: 'checkbox' })}
                                styles={inputStyles}
                            />

                            <h3 style={{ fontWeight: "bold", fontSize: "30px", color: "rgb(24, 100, 171)" }}>YOLO Params</h3>

                            <NumberInput label="Confidence" step={0.01} {...form.getInputProps('yolo_params.conf')} styles={inputStyles} />
                            <NumberInput label="IOU" step={0.01} {...form.getInputProps('yolo_params.iou')} styles={inputStyles} />

                            <Select
                                label="Device"
                                data={[
                                    { value: 'cpu', label: 'CPU' },
                                    { value: 'cuda', label: 'CUDA' },
                                ]}
                                {...form.getInputProps('yolo_params.device')}
                                styles={inputStyles}
                            />
                            <Select
                                label="YOLO Model"
                                data={[
                                    { value: 'yolo11s_reduced_dataset', label: 'yolo11s_reduced_dataset' },
                                    { value: 'yolo11n_FDDB', label: 'yolo11n_FDDB' },
                                ]}
                                {...form.getInputProps('yolo_model')}
                                onChange={(v: string | null) => {
                                    if (v !== null) form.setFieldValue('yolo_model', v);
                                }}
                                value={form.values.yolo_model}
                                styles={inputStyles}
                            />
                            <NumberInput label="YOLO Batch Size" {...form.getInputProps('yolo_batch_size')} styles={inputStyles} />

                            <Switch label="Half precision" {...form.getInputProps('yolo_params.half', { type: 'checkbox' })} styles={inputStyles} />
                            <Switch label="Verbose" {...form.getInputProps('yolo_params.verbose', { type: 'checkbox' })} styles={inputStyles} />
                        </Box>

                        <Box mb="md">
                            <h3 style={{ fontWeight: "bold", fontSize: "30px", color: "rgb(24, 100, 171)" }}>Norfair Params</h3>

                            <Select
                                label="Distance Function"
                                data={[
                                    { value: 'mean_euclidean', label: 'Mean Euclidean' },
                                    { value: 'frobenius', label: 'Frobenius' },
                                    { value: 'mean_manhattan', label: 'Mean Manhattan' },
                                ]}
                                {...form.getInputProps('norfair_params.distance_function')}
                                styles={inputStyles}
                            />

                            <NumberInput label="Distance Threshold" {...form.getInputProps('norfair_params.distance_threshold')} styles={inputStyles} />
                            <NumberInput label="Hit Counter Max" {...form.getInputProps('norfair_params.hit_counter_max')} styles={inputStyles} />
                            <NumberInput label="Initialization Delay" {...form.getInputProps('norfair_params.initialization_delay')} styles={inputStyles} />
                            <NumberInput label="Detection Threshold" step={0.1} {...form.getInputProps('norfair_params.detection_threshold')} styles={inputStyles} />
                            <NumberInput label="Past Detections Length" {...form.getInputProps('norfair_params.past_detections_length')} styles={inputStyles} />

                            <Switch
                                label="Activate REID"
                                checked={disableREID}
                                onChange={(e) => setDisableREID(e.currentTarget.checked)}
                                styles={inputStyles}
                            />

                            <Select
                                label="REID Distance Function"
                                data={[
                                    { value: 'euclidean_squared', label: 'Euclidean squared' },
                                    { value: 'euclidean', label: 'Euclidean' },
                                    { value: 'cosine', label: 'Cosine' },
                                ]}
                                {...form.getInputProps('norfair_params.reid_distance_function')}
                                styles={inputStyles}
                                disabled={!disableREID}
                            />

                            <NumberInput
                                label="ReID Distance Threshold"
                                step={0.1}
                                {...form.getInputProps('norfair_params.reid_distance_threshold')}
                                styles={inputStyles}
                                disabled={!disableREID}
                            />

                            <NumberInput
                                label="ReID Hit Counter Max"
                                {...form.getInputProps('norfair_params.reid_hit_counter_max')}
                                styles={inputStyles}
                                disabled={!disableREID}
                            />
                        </Box>
                    </SimpleGrid>
                </Center>

                <Group style={{ justifyContent: "space-between", marginLeft: "2vw", marginRight: "2vw", marginTop: "2vh", marginBottom: "1vh" }}>
                    <Button
                        type="button"
                        variant="light"
                        onClick={previous}
                        style={{ width: "20vw", height: "7vh", fontSize: "20px", margin: "20px" }}
                        color="rgb(24, 100, 171)"
                    >
                        Previous
                    </Button>

                    <Button
                        className='next-button'
                        type="submit"
                        disabled={!isValid}
                        style={{ width: "20vw", height: "7vh", fontSize: "20px", margin: "20px" }}
                        color="rgb(24, 100, 171)"
                    >
                        Next
                    </Button>
                </Group>
            </form>
        </>
    );
}

export default Step2;
