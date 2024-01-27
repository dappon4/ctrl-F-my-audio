import React from 'react';
import "./App.css";
import {useState} from "react";
import { Search } from 'lucide-react';
import axios from 'axios';

const Log = () => {
    const [query, setQuery] = useState("");
    const queryEndPoint = 'http://localhost:5000/query'
     //change this later
    const handleClick = async () => {
        let endpoint = queryEndPoint+'/'+query;
        console.log(query);
    }

    const handleDownload = async () => {
        let endpoint = queryEndPoint+'/download';
        console.log(query);
    }

    return (
        <div className="flex items-center justify-center">
            <input
                type="text"
                placeholder="Search..."
                className="pr-0 mr-0 pl-4 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500 w-[50%] text-headerColor"
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
                className="p-2 rounded-full bg-secondary text-Color ml-2 hover:bg-blue-600"
                onClick={handleClick}
            >
                <Search />
            </button>
            <button
                className="px-4 py-2  bg-textColor text-[#041C44] rounded-r-md ml-2 focus:outline-none focus:ring-2 focus:ring-blue-500 hover:bg-[#949494] cursor-pointer"
                onClick={handleDownload}
            >
                Download
            </button>
        </div>
    );
};

export default Log;

