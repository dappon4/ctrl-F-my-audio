import React from 'react';
import "./App.css";
import {useState} from "react";
import { Search } from 'lucide-react';
import axios from 'axios';
import sample from './sample';


const DisplayLog = ({handleskip}) => {
    return(
        <div className='flex overflow-scroll will-change-scroll justify-center w-[100%] bg-black p-10'>
            {Object.entries(sample).map(([key, value]) => (
            <div className='flex gap-[10px]'>
                <p className=''>{value}</p>
                <p>{key}</p>
            </div>
          ))}
        </div>
    )
}

export default DisplayLog;