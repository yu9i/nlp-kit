import React, { useState, useRef, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';



function App() {
  // 텍스트 상태
  const [text, setText] = useState<string>('');

  // 텍스트 에어리어 참조
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  // 텍스트 변경 시 호출되는 함수

   // textarea의 높이를 자동 조절하는 함수
   const autoResizeTextarea = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto'; // 높이를 초기화
      textarea.style.height = `${textarea.scrollHeight}px`; // 입력된 내용에 맞게 높이 조절
    }
  };

  // 텍스트 변경 시 호출되는 함수
  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value);
    autoResizeTextarea();
  };

  // 컴포넌트가 마운트될 때 초기 높이를 조정
  useEffect(() => {
    autoResizeTextarea();
  }, [text]);
  
  return (
    <div className="App">

      <div className='NLPText'>

        <div className="BeforeText">
          <h3>분석 전</h3>
          <textarea
            name="BeforeText"
            placeholder='분석할 내용을 입력해 주세요.'
            value = {text}
            onChange={handleTextChange}
            ref={textareaRef}
            rows={1} // 기본적으로 최소 1줄로 설정
          />
          <button>분석하기</button>
        </div>

        <div className="AfterText">
          <div className="AfterText">
            <h3>분석 후 내용</h3>
            <div>분석 결과 출력 예정 (요약) </div>
            <div>카테고리</div>
            <div>키워드</div>
          </div>
        </div>

      </div>


      {/* <img src={logo} className="App-logo" alt="logo" />
      <p>
        Edit <code>src/App.tsx</code> and save to reload.
      </p>
      <a
        className="App-link"
        href="https://reactjs.org"
        target="_blank"
        rel="noopener noreferrer"
      >
        Learn React
      </a> */}
    </div>
  );
}

export default App;


// import * as D from './data'

// export default function App(){
//   return(
//     <div>
//       <p>
//         {D.randomName()}, {D.randomJobTitle()}, {D.randomDayMonthYear()}
//       </p>

//       <img src={D.randomAvatar()} height="50" />
//       <img src={D.randomImage()} height="300" />
//     </div>
//   )
// }