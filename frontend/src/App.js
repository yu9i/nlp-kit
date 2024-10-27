import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import './App.css';

const AllContents = styled.div`
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: space-between;
  align-items: stretch;
  padding: 15px 30px;
  @media (max-width: 540px){
    display: flex;
    flex-direction: column;
    justify-content: stretch;
    align-items: stretch;
    padding: 20px 15px;
  }
`;

const BeforeTextBox = styled.div`
  width: 45%;
  display: flex;
  flex-direction: column;
  column-gap: 10px;
  flex-wrap: nowrap;
  border: 2px solid #98c8ff;
  border-radius: 10px;
  padding: 15px;
  @media (max-width: 540px){
    width: 94%;
    margin-bottom: 18px;
  }
`;

const Title = styled.div`
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
`;

const Textarea = styled.div`
  height: 100%;
  width: 100%;
  margin: 10px 0;
  border-top: solid 1.4px gray;
  border-bottom: solid 1.4px gray;
  padding: 10px 0;
`;

const StyledTextarea = styled.textarea`
  width: 100%;
  height: 100%;
  border: none;
  outline: none;
  resize: none;
  font-size: 16px;
  box-sizing: border-box;
  padding: 10px;
  overflow: hidden;
  border-radius: 10px;
  border: 1.2px solid gray;
`;

const AfterTextBox = styled.div`
  width: 45%;
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  border: 2px solid #98c8ff;
  border-radius: 10px;
  padding: 15px;
  @media (max-width: 540px){
    width: 94%;
  }
`;

const StartButton = styled.button`
  margin-top: 10px 0;
`;
const AfterTextBoxFin = styled.div`

`;



function App() {
  // 텍스트 상태
  const [text, setText] = useState('');
  const textareaRef = useRef(null);
  const [result, setResult] = useState({summary: "", keywords: [], category: ""});
  const [loading, setLoading] = useState(false);

  // textarea의 높이를 자동 조절하는 함수
  const autoResizeTextarea = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = '94%'; //textarea 초기 높이 사이즈
      textarea.style.height = `${textarea.scrollHeight}px`; // 입력된 내용에 맞게 높이 조절
    }
  };

  // 텍스트 변경 시 호출
  const handleTextChange = (e) => {
    setText(e.target.value);
    autoResizeTextarea();
  };

  // 분석하기 버튼 클릭 시 서버와 통신
  const handleAnalyze = async () => {
    if (text === "") return;
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:5000/analyze", {
        text: text,
      });
      setResult(response.data);
    } catch (err) {
      // console.log("분석 중 오류가 발생했습니다.");
      console.error(err);
    }
    setLoading(false);
  };

  // 컴포넌트가 마운트될 때 초기 높이를 조정
  useEffect(() => {
    autoResizeTextarea();
  }, [text]);

  return (
    <AllContents>
      <BeforeTextBox>
        <Title>분석 전</Title>
        <Textarea>
          <StyledTextarea
            name="BeforeText"
            placeholder='분석할 내용을 입력해 주세요.'
            value={text}
            onChange={handleTextChange}
            ref={textareaRef}
          />
        </Textarea>
        <StartButton onClick={handleAnalyze}>분석하기</StartButton>
      </BeforeTextBox>
      <AfterTextBox>
        <Title>분석 후</Title>
        <Textarea>
          <AfterTextBoxFin>
          {loading ? (
              <p>분석 중...</p>
            ) : result ? (
              <>
                <strong>요약:</strong>
                <p>{result.summary}</p>
                <p></p>
                <strong>키워드:</strong>
                <p>{result.keywords.join(", ")}</p>
                <p></p>
                <strong>카테고리:</strong>
                <p>{result.category}</p>
              </>
            ) : (
              <p>결과가 없습니다.</p>
            )}
          </AfterTextBoxFin>
        </Textarea>
      </AfterTextBox>
    </AllContents>
  );
}

export default App;
