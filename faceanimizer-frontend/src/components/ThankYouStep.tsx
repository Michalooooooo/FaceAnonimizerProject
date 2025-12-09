import { Button, Center } from "@mantine/core";

function ThankYouStep() {
    return (
        <>
        <h1 style={{
            fontWeight: "bold",
            fontSize: "50px",
            color: "rgb(24, 100, 171)",
            marginLeft: "5vw",
            marginRight: "5vw"
        }}>
            Thank you for using my application. If you want to try with another video hit <u>Let's go again</u> button!
        </h1 >
        <Center>
            <Button 
            onClick={() => window.location.reload()}
            style={{
                width: "35vw",
                height: "15vh",
                fontSize: "35px",
                margin: "auto 0"
            }}
            >Let's go again!</Button>
        </Center>
        </>
    );
}

export default ThankYouStep;