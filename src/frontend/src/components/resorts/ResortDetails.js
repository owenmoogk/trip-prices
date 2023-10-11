import { useEffect, useState } from "react"
import React from "react";
import { useParams } from "react-router-dom/cjs/react-router-dom.min";
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';

export default function ResortDetails(){

  const id = useParams().id
  const [resortData, setResortData] = useState()
  const [resortPrices, setResortPrices] = useState()

  function getResortData(){
    fetch("/api/resort/"+id + '/')
    .then(response => response.json())
    .then(data => setResortData(data))
  }

  function getResortPrices(){
    fetch("/api/resortPrices/"+id+"/")
    .then(response => response.json())
    .then(data => setResortPrices(data))
  }

  useEffect(() => {
    getResortData()
    getResortPrices()
  }, [])

  return (
    <>
      {resortData ?
        <h1>{resortData.name}</h1>
      : null}
    
      {resortPrices ?
      <>
        <LineChart width={400} height={400} data={resortPrices}>
          <Line type="monotone" dataKey="price" stroke="#8884d8" />
          <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
        </LineChart>
        <table>
          <tbody>
            <tr>
              <th>Date</th>
              <th>Price</th>
            </tr>
            {resortPrices.map((item) => 
              <tr>
                <td>{item.date}</td>
                <td>{item.price}</td>
              </tr>
            )}
          </tbody>
        </table>
      </>
      : null}

    </>
  );
}