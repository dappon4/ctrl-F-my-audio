import "./App.css";
import { useState, useEffect } from "react";



function App() {
  return (
    <div className="App">
      <Header />
      <Main />
    </div>
  );
}

function Header() {
  return (
    <header className="p-7 bg-headerColor border-b-gray-500 border-b-[1px] sticky top-0">
      <h1 className='text-center text-4xl tracking-wider font-["Nunito Sans"] text-textColor'>
        <p className="inline text-secondary">ctrlF</p>MyVideo
      </h1>
    </header>
  );
}

function Main() {
  const [selectedTemplate, setSelectedTemplate] = useState(null);

  return (
    <div className="flex justify-center bg-headerColor h-[100vh]">
      <SendAV selectedTemplate={selectedTemplate}/>
    </div>
  );
}



function SendAV({selectedTemplate}) {
  const [input, setinput] = useState("");
  const [latex, setLatex] = useState("");

  return (
    <div className="flex flex-col gap-10 justify-center items-center ">
      <p className="text-center text-2xl">Upload the File Below:</p>
      <button
        className="mt-5 rounded-xl w-[80px] text-sm h-[50px] md:w-[150px] md:h-[60px] md:text-xl bg-secondary text-textColor font-semibold hover:bg-[#1abc9c]"
      >
        Send
      </button>
    </div>
  );
}

export default App;
