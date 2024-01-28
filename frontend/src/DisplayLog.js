import React from 'react';
import "./App.css";
import {useState,} from "react";
import { Search } from 'lucide-react';
import axios from 'axios';
import sample from './sample';


const DisplayLog = ({handleSkip}) => {
    return(
        <div className='flex overflow-scroll will-change-scroll justify-center text-textColor border-gray-300 border bg-black p-2'>
            <div className='flex flex-col gap-2'>
                <p className='text-xl w-[50vw] h-[40px] text-center border-b'>Audio Log</p>
                <div className='flex flex-col flex-wrap items-start h-[50px]'>
                {Object.entries(sample).map(([key, value]) => (
                    <div className='flex gap-[10px] '>
                        <p className='cursor-pointer' onClick={()=>handleSkip(value)}>{value} : </p>
                        <p>{key}</p>
                    </div>
                ))}
                </div>
          </div>
        </div>
    )
}

export default DisplayLog;