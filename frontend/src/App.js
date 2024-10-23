import logo from './logo.svg';
import './App.css';
import axios from 'axios'
import {useEffect, useState} from 'react'
import {createClient} from '@supabase/supabase-js'
import { v4 as uuidv4 } from 'uuid'

// Get supabase client
const supabase = createClient("https://zmoyacveypqxzbgsqqky.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inptb3lhY3ZleXBxeHpiZ3NxcWt5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc3OTY4OTUsImV4cCI6MjA0MzM3Mjg5NX0.rEmdsDwkqVtTIp_ty9Yf_eo7tSSOadqBKqjfPViWMG0")
const CDNURL = "https://zmoyacveypqxzbgsqqky.supabase.co/storage/v1/object/public/videos/"

// Connect to FastAPI server
const FASTAPI_SERVER_URL = "http://localhost:8000"
const api = axios.create({baseURL: FASTAPI_SERVER_URL})

// App
function App() {
  const [moments, setMoments] = useState([])
  const [loading, setLoading] = useState(true);

  const getData = async () => {
    const response = await api.get('/moments')
    const data = response.data.data
    console.log(data)
    setMoments(data)
    setLoading(false)
  }

  const uploadVideoToStorage = async (e) => {
    setLoading(true)
    const videoFile = e.target.files[0]
    console.log(videoFile)
    const { error } = await supabase.storage
      .from('videos')
      .upload(uuidv4() + ".mp4", videoFile)
    if (error) {
      alert("Error uploading")
    }
    setLoading(false)
  }

  const vectorizeVideo = async (e) => {
    // Currently hardcode
    const name = `cba080da-405a-4dca-a956-e5189caf89b0.mp4`
    const response = await api.post(`/vectorize/${name}`)
    const data = response.data
    console.log(data)
  }


  useEffect(() => {
    getData()
  }, [])


  return (
    <div className="App">
      <header className="App-header">
        {
          loading ? 
          <div>
            Loading
          </div>
          :
          <div>
          <div>The moments in our database table "moments" for testing GET operation</div>
            {moments.map((m) => (
                <div key={m.id}>{m["video_name"]}</div>
            ))}
          <br></br>
          <label id="upload-btn">First upload video, a new entry is added to 'videos' Buckets. It only supports video upload.</label>
          <input type="file" id="file-input" onChange={(e) => uploadVideoToStorage(e)}/>

          <br></br>
          <label id="upload-btn">Action handler to vectorize a frame (not video) given frame name. The same name as stored in the Bucket</label>
          <button onClick={(e) => vectorizeVideo(e)}>Vectorize Video</button>
            
          </div>

        }
        {/* <br></br>
        <label id="upload-btn">First upload video, a new entry is added to 'videos' Buckets</label>
        <input type="file" id="file-input" onChange={(e) => uploadVideoToStorage(e)}/>

        <br></br>
        <label id="upload-btn">Action handler to vectorize a video given video name, currently hardcoded as test.mp4</label>
        <button onClick={(e) => vectorizeVideo(e)}>Vectorize Video</button> */}

      </header>
    </div>
  );
}

export default App;
