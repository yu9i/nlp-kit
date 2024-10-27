import styled from 'styled-components';

const FooterComp = styled.footer`
    height: 70px;
    padding: 5px 30px;
    border-top: solid 1px #ababab;
    color: gray;
    @media (max-width: 540px){
        height: 30px;
        padding: 2px 15px;
        border-top: solid 0.5px #ababab;
    }
`;

function Footer () {
    return (
        <FooterComp>
            <p>졸업작품</p>
            <p>성균관대학교 소프트웨어학과 이유기</p>
            
        </FooterComp>
    )
}

export default Footer;