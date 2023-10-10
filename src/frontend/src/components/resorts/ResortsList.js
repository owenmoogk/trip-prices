import { useEffect, useState } from "react"
import React from "react"

export default function ResortsList(){

  const [resortData, setResortData] = useState()

  function getResortsList(){
    fetch("/api/resorts/")
    .then(response => response.json())
    .then(data => setResortData(data))
  }

  useEffect(() => {
    getResortsList()
  }, [])

  return(
    resortData ?
      <table style={{width: "500px"}}>
        <tbody>
          {resortData.map((item, index) => 
              <tr>
                {console.log(item.id)}
                <td style={{border: "1px solid black"}}>{item.id}</td>
                <td style={{border: "1px solid black"}}><a href={'/resorts/'+item.id}>{item.name}</a></td>
              </tr>
          )}
        </tbody>
      </table>
    : null
  );
}