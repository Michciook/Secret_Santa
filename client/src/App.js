import React, { useState, useEffect } from 'react'

function App() {

  const [data, setData] = useState([{}])
  
  useEffect(() => {
    fetch("/test").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
      }
    )
  }, [])

  return (
    <div>
      {data ? <p>{data.test}</p> : <p>Loading...</p>}
    </div>
  )
}

export default App