
import './App.css';
import "@buildo/bento-design-system/index.css";
import "@buildo/bento-design-system/defaultTheme.css";
import { defaultMessages } from "@buildo/bento-design-system/defaultMessages/en";
import { BentoProvider, Title, Box, Body, Card, Inset, Stack, Inline } from "@buildo/bento-design-system";
import background from './img/background1.png';
import React from "react";


function RenderCard () {
    return <Card elevation="medium" background={"primaryTransparentEnabledBackground"}>
        <Inset spaceX="32" spaceY="24">
            <Stack space="4">
                <Title size="large" color={"primaryInverse"}>Card Title</Title>
                <Body size="large" color="secondary">Card description</Body>
            </Stack>
        </Inset>
    </Card>;
}


function Page() {

    console.log("Text!");
    return (
       <div>Hello World!</div>
    );
}

export default Page;
