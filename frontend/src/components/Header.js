import styled from 'styled-components';

const HeaderComp = styled.header`
    display: flex;
    align-items: center;
    height: 90px;
    padding: 5px 30px;
    border-bottom: solid 1px #ababab;
    @media (max-width: 540px){
        height: 60px;
        padding: 2px 15px;
        border-bottom: solid 0.5px #ababab;
    }
`;

const HeaderTitle = styled.div`
    font-size: 30px;
    color: #525252;
    font-weight: bold;
    @media (max-width: 540px){
        font-size: 22px;
    }
`;

function Header () {
    return (
        <HeaderComp>
            <HeaderTitle>
                NLP Kit
            </HeaderTitle>
        </HeaderComp>
    )
}

export default Header;