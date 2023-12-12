import React from 'react';
import {BrowserRouter as Router, Route, Link, Routes, useNavigate} from 'react-router-dom';
import "@buildo/bento-design-system/index.css";
import "@buildo/bento-design-system/defaultTheme.css";
import { BentoProvider, Title, Box, Body, Card, Inset, Stack, Inline, Actions, Button } from "@buildo/bento-design-system";
import Page from './Page';
import Home from './Home';

const Nav = () => {

    const navigate = useNavigate();

    return (
        <Box height={"full"}>
            <Inset spaceY={24}>
                <Stack space={12}>
                    <Button onPress={function () {navigate('/')}} label={"Home"}></Button>
                    <Button onPress={function () {navigate('/page')}} label={"Page"}></Button>
                </Stack>
            </Inset>
        </Box>

    );
};

const AppRouter = () => {
    return (
        <Router>
            <div>
                <Nav />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/page" element={<Page />} />
                </Routes>
            </div>
        </Router>
    );
};

export default AppRouter;

