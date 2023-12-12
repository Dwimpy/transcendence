
import './App.css';
import "@buildo/bento-design-system/index.css";
import "@buildo/bento-design-system/defaultTheme.css";
import { Title, Inset} from "@buildo/bento-design-system";

import React from "react";


function Page() {

    console.log("Text!");
    return (
        <Inset space={16}>
            <Title size="large" color={"primaryInverse"}>Hello World!</Title>
        </Inset>
    );
}

export default Page;
