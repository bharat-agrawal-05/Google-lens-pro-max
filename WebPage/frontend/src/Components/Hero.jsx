import React from 'react'
import { useGSAP } from '@gsap/react'
import Form from './Form'
import gsap from 'gsap'

const Hero = () => {

    useGSAP(() => {
        gsap.to('#heading-div', {
          opacity: 1,
          delay: 1,
          y: 0,
        })
    
        gsap.to('#form' , {
          opacity: 1,
          delay: 1.5,
        })
      }, [])

  return (
    <section>
      <div id = 'heading-div' className = 'flex justify-center items-center h-[100px] w-full opacity-0 translate-y-2'>
        <div className = 'flex justify-center items-center w-full'>
            <img 
              src = '../logo.png' 
              alt = 'logo' 
              width={60} 
              height={60} 
            />
            <h1 className = 'sm:text-3xl text-xl text-white font-semibold'>Google Lens Pro Max</h1>
        </div>
      </div>
    </section>
  )
}

export default Hero