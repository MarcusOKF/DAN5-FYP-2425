import logo from './logo.svg';
import './App.css';
import axios from 'axios'
import {useEffect, useState} from 'react'

const api = axios.create({baseURL: "http://localhost:8000"})

function App() {
  const [videos, setVideos] = useState([])
  const [loading, setLoading] = useState(true);

  const getData = async () => {
    const response = await api.get('/moments')
    const data = response.data.data
    console.log(data)
    setVideos(data)
    setLoading(false)
  }

  useEffect(() => {
    getData()
  }, [])


  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        {
          loading ? 
          <div>
            Loading
          </div>
          :
          videos.map((vid) => (
              <div key={vid.id}>{vid["video_name"]}</div>
          ))
        }

      </header>
    </div>
  );
}

export default App;
