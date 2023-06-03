import { ConnectButton } from "@rainbow-me/rainbowkit";
import type { NextPage } from "next";
import Head from "next/head";
import { ThemeProvider } from "styled-components";

import { GlobalStyles } from "../styles/GlobalStyles";
import { light } from "../styles/Themes";
import Navigation from "../components/Navigation";
import Home from "../components/sections/Home";
import About from "../components/sections/About";
import Roadmap from "../components/sections/Roadmap";
import Showcase from "../components/sections/Showcase";
import Team from "../components/sections/Team";
import Faq from "../components/sections/Faq";
import Footer from "../components/Footer";

const Main: NextPage = () => {
  return (
    <>
      <GlobalStyles />
      <ThemeProvider theme={light}>
        <Navigation />
        <About />
        <Showcase />
        <Footer />
      </ThemeProvider>
    </>
  );
};

export default Main;
