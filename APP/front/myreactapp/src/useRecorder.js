import { useEffect, useState } from "react";

const useRecorder = (register) => {
  const [audioURL, setAudioURL] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [recorder, setRecorder] = useState(null);
  const [returnValue, setReturnValue] = useState({emotion : -1, text : "not recorded yet"});

  var address = register ? `http://localhost:5000/register-record` : `http://localhost:5000/diary-record`

  useEffect(() => {
    // Lazily obtain recorder first time we're recording.
    if (recorder === null) {
      if (isRecording) {
        requestRecorder().then(setRecorder, console.error);
      }
      return;
    }

    // Manage recorder state.
    if (isRecording) {
      recorder.start();
    } else {
      recorder.stop();
    }

    // Obtain the audio when ready.
    const handleData = async e => {

        const myFile = new File([e.data], "audio.webm", {
            type: e.data.type,
        });

        const data = new FormData();
        data.append("audio_file", myFile);

        try {

          var return_val = await fetch(address, {method:"POST", body:data})
          .then(response => {
              if (response.ok) return response;
              else throw Error(`Server returned ${response.status}: ${response.statusText}`)
          })
          .then(response => response.json()) 
          
          console.log(return_val);
          setReturnValue(return_val);
          
        } catch (error) {
          alert(error);
        }

        setAudioURL(URL.createObjectURL(e.data));
    };

    recorder.addEventListener("dataavailable", handleData);
    return () => recorder.removeEventListener("dataavailable", handleData);
  }, [recorder, isRecording, address]);

  const startRecording = () => {
    setIsRecording(true);
  };

  const stopRecording = () => {
    setIsRecording(false);
  };

  return [audioURL, isRecording, returnValue, startRecording, stopRecording];
};

async function requestRecorder() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  return new MediaRecorder(stream);
}



export default useRecorder;
