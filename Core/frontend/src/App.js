
import './App.css';
import "@buildo/bento-design-system/index.css";
import "@buildo/bento-design-system/defaultTheme.css";
import React from "react";
import AppRouter from "./AppRouter";
import {Body, Box, Display, Headline, Inset, Stack, Title} from "@buildo/bento-design-system";

function App() {

  return (
      <Box height={"full"}>
          <Inset space={16} spaceY={24}>
              <Stack space={12} align={"center"}>
                  <Title align={"center"} color={"primaryInverse"} size="large">Your App</Title>
                  <AppRouter />
              </Stack>
          </Inset>
      </Box>
  );
}

export default App;
