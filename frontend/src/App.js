import "./App.css";
import { useState, useEffect } from "react";
import axios from 'axios';



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
  return (
    <div className="flex justify-center bg-headerColor h-[100vh]">
      <SendAV />
    </div>
  );
}



function SendAV({ props }) {
  const url = "http://127.0.0.1:5000/convert" //change this to the localhost url
  const [video, setVideo] = useState(null)

  function handleUpload(e) {
    setVideo(()=>e.target.files[0])
  }
  

  const handleSubmit = async () =>{
  
  const formData = new FormData()
  formData.append(
    'uploaded_file',
    video,
    video.name
  )

  const response = await axios.post(url, formData,{
    onUploadProgress: progressEvent => {
      let progress = Math.round(progressEvent.loaded*100 / progressEvent.total)
      if(progress == 100){
        setVideo(null)
      }
      console.log(progress+'%')
    }
  })//get upload progress
  console.log(await response)
}
  function isUploaded(){
    if(video!==null){
      return (
        <div>
          <label for="submit"
        className="mt-5 rounded-xl w-[150px] text-sm h-[50px] md:h-[60px] md:text-xl bg-secondary text-textColor font-semibold hover:bg-[#1abc9c] flex items-center justify-center cursor-pointer"
      >Submit</label>
      <input type="submit" id="submit" name="submit" className='w-0' onClick={handleSubmit} />
        </div>
      )
    }

  }
  return (
    <div className="bg-[#041C44] h-[60%] mt-32 flex flex-col items-center max-w-[70vw] rounded-sm">
      <p className="text-center text-2xl mt-10 max-w-[85%]">Lorem ipsum dolor sit amet consectetur adipisicing elit. Esse, soluta iure voluptatem quibusdam sapiente eligendi voluptatem quibusdam sapiente eligendi:</p>

      <label for="video"
        className="mt-16 rounded-sm w-[80px] text-sm h-[50px] md:w-[80%] md:h-[60px] md:text-xl bg-secondary text-textColor font-semibold hover:bg-[#1abc9c] flex items-center justify-center cursor-pointer"
      >Select video file</label>
      <input type="file" id="video" name="video" accept="video/*" className='w-0' onChange={handleUpload} required/>

      {isUploaded()}

    </div>
  );
}

export default App;
