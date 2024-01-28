import "./App.css";
import { useState, useEffect, useRef } from "react";
import axios from 'axios';
import {Upload } from 'lucide-react';
import Log from "./Log";
import DisplayLog from "./DisplayLog";
import {Link, Routes, Route} from "react-router-dom";

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
        <Link to='/'><p className="inline text-secondary">ctrlF</p>MyVideo</Link>
      </h1>
    </header>
  );
}

function Main() {
  const [video, setVideo] = useState({videoFile: null, videoURL: null})
  const [isUploaded, setIsUploaded] = useState(false)

 
  return (
    <div className="flex flex-col items-center bg-headerColor pb-20">
      <Routes>
        <Route path="/" element={<SendAV video={video} setVideo={setVideo} isUploaded={isUploaded} setIsUploaded = {setIsUploaded}/>} />
        <Route path="/log" element={<Log video={video} setVideo={setVideo}/>} />
      </Routes>
  
    </div>
  );
}


function SendAV({video, setVideo, isUploaded, setIsUploaded}) {
  const url = "https://organic-capybara-qj7v9676r5g347v5-5000.app.github.dev/" //change this to the localhost url
  // const [video, setVideo] = useState({videoFile: null, videoURL: null})
  // const [isUploaded, setIsUploaded] = useState(false)

  function handleUpload(e) {
    setVideo(() => {
      return {
        videoFile: e.target.files[0],
        videoURL: URL.createObjectURL(e.target.files[0])
      }
    })
  }
  const videoRef = useRef(null);

  const handleSkipToTimestamp = () => {
    if (videoRef.current) {
      // Set the desired timestamp (10 seconds in this case)
      videoRef.current.currentTime = startTime;
    }
  };

  const [startTime, setStartTime] = useState(0);

  useEffect(() => {
    // Adjust the start time as necessary
    setStartTime(10); // Start video at 30 seconds
  }, []);

  const handleSubmit = async () => {
    if (video.videoFile !== null) {
      const data = await axios.get(url + '/clear')
      if (data.data.number > 0) {
        const response = await axios.post(url + '/clear')
      }
      const formData = new FormData()
      formData.append(
        'uploaded_file',
        video.videoFile,
        video.videoFile.name
      )

      const response = await axios.post(url + '/convert', formData, {
        onUploadProgress: progressEvent => {
          let progress = Math.round(progressEvent.loaded * 100 / progressEvent.total)
          if (progress === 100) {
            setIsUploaded(true)
          }
          console.log(progress + '%')
        }
      })//get upload progress
      console.log(await response)
    }
  }

  function isSubmitted() {
    return (
      <div>
        <label htmlFor="submit"
          className="rounded-[25px] w-[70px] text-sm h-[20px] md:h-[60px] md:text-xl bg-textColor text-[#041C44] font-semibold hover:bg-[#949494] flex items-center justify-center cursor-pointer"
        ><Upload size={32} strokeWidth={2} /></label>
        <input type="submit" id="submit" name="submit" className='w-0' onClick={handleSubmit} />
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-10">
      <div className="mt-20 bg-[#041C44] flex flex-col items-center max-w-[70vw] rounded-xl pb-10 ">
        <p className="text-center text-2xl mt-10 max-w-[85%]">Wanna find something in your footage? You should ctrlFYourVideo: </p>

        <label htmlFor="video"
          className="mt-16 rounded-sm w-[80px] text-sm h-[50px] md:w-[80%] md:h-[60px] md:text-xl bg-secondary text-textColor font-semibold hover:bg-[#1abc9c] flex items-center justify-center cursor-pointer"
        >Select video file</label>
        <input type="file" id="video" name="video" accept="video/*" className='w-0' onChange={handleUpload} required />

        {isSubmitted()}
        <div className="flex flex-col justify-center items-center">
        {isUploaded && <video ref={videoRef} controls>
          <source key={video.videoFile.name} src={video.videoURL} type="video/mp4" className="w-[80%] h-auto" />
          Your browser does not support the video tag.
        </video>}
        {isUploaded &&  <Link to='/log'>
    <div className="mt-8 rounded-xl w-[80px] text-md h-[60px] md:w-[30vw] md:text-xl bg-secondary text-textColor font-semibold hover:bg-[#1abc9c] flex items-center justify-center cursor-pointer"
  >View Log</div>
  </Link>}

      </div>
      </div>
  
      {/* {isUploaded && <Log/>}
      {isUploaded && <DisplayLog handleSkip = {handleSkipToTimestamp}/>} */}
    </div>
  );
}


export default App;
