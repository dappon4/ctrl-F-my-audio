import React from 'react';
import "./App.css";
import { useState, useRef } from "react";
import { Search } from 'lucide-react';
import axios from 'axios';
import sample from './sample';
import DisplayLog from './DisplayLog';

const Log = ({video, setVideo}) => {
    const [query, setQuery] = useState("");
    const queryEndPoint = 'http://localhost:5000/query'
    const videoRef = useRef(null);
    const handleSkipToTimestamp = (value) => {
        if (videoRef.current) {
          videoRef.current.currentTime = value;
        }
      };
    //change this later
    const handleClick = async () => {
        let endpoint = queryEndPoint + '/' + query;
        console.log(query);
    }

    const handleDownload = async () => {
        let endpoint = queryEndPoint + '/download';
        console.log(query);
    }

    return (
    <div className='flex flex-col gap-12 items-center'>
        <video ref={videoRef} controls>
          <source key={video.videoFile.name} src={video.videoURL} type="video/mp4" className="max-w-[60vw] max-h-[50vh] object-contain" />
          Your browser does not support the video tag.
        </video>
        <div className = 'flex gap-0 mt-6'>
            <DisplayLog handleSkip={handleSkipToTimestamp}/>
            <div className="flex overflow-scroll justify-center bg-black border-gray-300 border p-2">
                <input
                    type="text"
                    placeholder="Search..."
                    className="h-[50px] text-headerColor indent-2"
                    onChange={(e) => {
                        setQuery(e.target.value);
                        console.log(query)
                    }}
                    onSubmit={(e) => {
                        e.preventDefault();
                        console.log(query)
                    }}
                />
                <button
                    className="rounded-r-md bg-secondary text-Color w-[40px] hover:bg-blue-600 h-[50px] flex justify-center items-center"
                    onClick={handleClick}
                >
                    <Search />
                </button>
            </div>
        </div>
        <button className= "w-[50%] px-4 py-2 bg-textColor text-[#041C44] ml-2 hover:bg-[#949494] cursor-pointer" onClick={handleDownload}>
            Download Log
        </button>
    </div>
    );
};


{/* <button className="mt-2 rounded-xl w-[80px] text-sm h-[50px] md:w-[150px] md:h-[60px] md:text-xl bg-[#1abc9c] text-textColor font-semibold"
    onClick={handleSkipToTimestamp}>
          Skip to 0:10
     </button> */}

export default Log;

