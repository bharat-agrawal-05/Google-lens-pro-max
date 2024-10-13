import React, { useEffect, useRef } from 'react'
import { useState } from 'react'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faArrowUp, faPaperclip, faStopCircle} from '@fortawesome/free-solid-svg-icons'
import { useGSAP } from '@gsap/react'
import gsap from 'gsap'
import axios from 'axios';
import Papa from 'papaparse';

const Form = () => {
  const [promptValue, setPromptValue] = useState('')
  const [fileName, setFileName] = useState('Upload your image here')
  const [csvData, setCsvData] = useState([]);
  const [hidden, setHidden] = useState('hidden')
  const [btn, setBtn] = useState(faArrowUp)
  const fileRef = useRef(null);
  const textAreaRef = useRef(null);

  useEffect(() => {
    if (csvData.length === 0 || fileName === 'Upload your image here') {
      setHidden('hidden');
    }
    else {
      setHidden('');
    }
  }, [csvData, fileName])

  const handleFileNameChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setFileName(file.name)
    }
    else {
      setFileName('Upload your image here')
      setPromptValue('')
    }
  }

  const handleSubmit = async(e) => {
    e.preventDefault();
    setBtn(faStopCircle);
    const file = fileRef.current.files[0];
    const prompt = textAreaRef.current.value;
    const formData = new FormData();
    formData.append('file', file);
    formData.append('prompt', prompt);
    try {
      const res = await axios.post('http://localhost:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      const file = res.data;

      if (file) {
        Papa.parse(file, {
          header: true,
          skipEmptyLines: true,
          complete: (result) => {
            setCsvData(result.data)
          },
          error: (error) => {
            console.error('Error parsing CSV file:', error);
          },
        });
      }
    }
    catch(e) {
      console.log(e)
    }
    setBtn(faArrowUp);
    if (btn == faArrowUp) {
      console.log('hi')
    }
  }

  useGSAP(() => {
    gsap.to('#accept', {
      opacity: 1, 
      stagger: 0.5,
      delay: 2,
    })

    gsap.to('#form', {
      opacity: 1,
      delay: 1.5,
    })
  }, [])

  return (
    <div id = 'form' className = 'opacity-0 flex flex-col justify-center items-center h-full'>
        <div className = 'flex flex-col  items-center h-full w-[80%] bg-gray-300 rounded-3xl'>
            <form onSubmit={handleSubmit} className = 'flex flex-col items-center w-[95%] justify-start'>
              <div id = 'accept' className = 'flex bg-zinc w-full justify-between rounded-xl items-center h-12 m-5 opacity-1'>
                <input 
                  ref = {fileRef}
                  hidden = {true}
                  type = 'file'
                  id = 'file'
                  name = 'file'
                  onChange = {e => handleFileNameChange(e)}
                  required
                />
                <p className = 'sm:text-3xl text-xl sm:ml-10 ml-5 text-gray-500'>{fileName}</p>
                <label htmlFor = 'file' className = 'mr-5'>
                  <FontAwesomeIcon icon = {faPaperclip} className = 'text-2xl cursor-pointer text-gray-500'/>
                </label>
              </div>

              <div id = 'accept' className = {`flex bg-zinc w-full justify-between rounded-xl items-center h-12 m-5 opacity-1 `}>
                <textarea 
                  ref = {textAreaRef}
                  type = 'text'
                  placeholder = 'Enter your prompt here'
                  value = {promptValue}
                  onChange = {e => setPromptValue(e.target.value)}
                  className = {`sm:text-3xl text-xl sm:ml-10 ml-5 w-[90%] bg-transparent text-gray-500 outline-none h-12 resize-none placeholder-gray-500`}
                  required
                />
                <button type = "submit" className = 'mr-5'>
                  <FontAwesomeIcon icon = {btn} className = 'text-2xl cursor-pointer text-gray-500'/>
                </button>
              </div>
            </form>

            <div className = {`bg-zinc w-[95%] h-full mb-5 p-5 rounded-xl text-gray-500 ${hidden}`}>
              <h1 className = 'text-2xl font-medium'>Generated Links</h1>
              <div className = 'flex flex-col w-full h-[90%] overflow-y-auto'>
                {csvData.map((row) => {
                   return  (
                    <div key = {row.index} className = 'flex items-center m-1 '>
                      <a href = {row.href} target = '_blank' rel = 'noreferrer'>{row.href}</a>
                    </div>
                  )
                })}
            </div>
        </div>

        
    </div>
    </div>
  )
}

export default Form;