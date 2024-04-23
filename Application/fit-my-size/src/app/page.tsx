'use client'
import getApiResponse from '@/utils/getApiResponse';
import React, { useRef, useState } from 'react';
import Webcam from 'react-webcam';

const CameraPage = () => {
  const [suggestion, setSuggestion] = useState<string | undefined>(undefined);
  const webcamRef = useRef<Webcam>(null);

  const capture = async () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      try {
        const suggestionResponse = await getApiResponse(imageSrc);
        setSuggestion(suggestionResponse);
      }catch(error) {
        console.log(error);
      }
    }
  };

  return (
    <div>
      <div>
        <Webcam
          audio={false}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
        />
      </div>
      <div>
        <button className='primary-btn' onClick={capture}>Take photo</button>
      </div>
      {suggestion &&
        <p>Suggestion: {suggestion}</p>
      }
    </div>
  );
};

export default CameraPage;
