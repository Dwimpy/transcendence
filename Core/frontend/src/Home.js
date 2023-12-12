
import './App.css';
import "@buildo/bento-design-system/index.css";
import "@buildo/bento-design-system/defaultTheme.css";
import { defaultMessages } from "@buildo/bento-design-system/defaultMessages/en";
import { BentoProvider, Title, Box, Body, Card, Inset, Stack, Inline, Actions, Button } from "@buildo/bento-design-system";
import background from './img/background1.png';
import React from "react";
import Page from "./Page";
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';

function RenderCard () {
    return <Card elevation="medium" background={"primaryTransparentEnabledBackground"}>
        <Inset spaceX="32" spaceY="24">
            <Stack space="4">
                <Title size="large" color={"primaryInverse"}>Card  Title</Title>
                <Body size="large" color="secondary">Card description</Body>
                <Actions primaryAction={{label:"Button" ,onPress: function () {Page()}}} secondaryAction={{label:"cancel"}}>
                </Actions>
            </Stack>
        </Inset>
    </Card>;
}


function Home() {

    return (
        <Box  height={"full"} >
            <BentoProvider defaultMessages={defaultMessages}>
                <Box alignItems={"center"} height={"full"}  justifyContent={"center"} display={"flex"} flexDirection={"column"}>
                    <Box>
                        <Inset spaceY="8">
                            <Inline space={{wide : 12, mobile: 12}} align="center">
                                <RenderCard />
                                <RenderCard />
                            </Inline>
                        </Inset>
                    </Box>
                    <Box>
                        <Inset spaceY="8">
                            <Inline space={{wide : 12, mobile: 12}} align="center">
                                <RenderCard />
                                <RenderCard />
                            </Inline>
                        </Inset>
                    </Box>
                </Box>
            </BentoProvider>
        </Box>
    );
}

export default Home;