import { useEffect, useState, useTransition } from "react"
import React from "react"
import doPost from "../PostRequest"
import { getCookie } from "../CSRF"
import doGet from "../GetRequest"
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Legend} from 'recharts';
import colorWheel from "../ColorWheel"

export default function FavoritePage(){

  const [resortData, setResortData] = useState()
  const [graphData, setGraphData] = useState()
  const [resortNames, setResortNames] = useState()

  function getFavoriteResortData(){
    doGet("/api/favoriteResortData/")
    .then(response => response.json())
    .then(data => {
      setResortData(data)

      var dateData = {}
      for (var resortName of Object.keys(data)){
        for (var pricePoint of data[resortName]){
          if (dateData[pricePoint.dateCollected]){
            dateData[pricePoint.dateCollected][resortName] = pricePoint.price
          }
          else{
            dateData[pricePoint.dateCollected] = {}
            dateData[pricePoint.dateCollected][resortName] = pricePoint.price
          }
        }
      }

      var tmpGraphData = []
      for (var key of Object.keys(dateData)){
        dateData[key]["dateCollected"] = key
        tmpGraphData.push(dateData[key])
      }

      tmpGraphData.sort((a,b) => new Date(a["dateCollected"]) - new Date(b["dateCollected"]))

      setGraphData(tmpGraphData)

      setResortNames(Object.keys(data))
      
    })
  }

  useEffect(() => {
    getFavoriteResortData()
  }, [])  

  var max = -Infinity
  var min = Infinity
  if (resortData){
    for (var key of Object.keys(resortData)){
      for (var item of resortData[key]){
        if (item.price > max){
          max = item.price
        }
        if (item.price < min){
          min = item.price
        }
      }
    }
  }


  return (
    resortData ?
      resortNames ? 
    <div id='favoritesPage'>
      <h1 style={{textAlign: "center"}}>Welcome to TripPlanner</h1>
      <LineChart width={800} height={400} data={graphData}>
        {resortNames.map((ele, index) => 
          <Line type="monotone" dataKey={ele} stroke={colorWheel(index, resortNames.length)} dot={false}/>
        )}
        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
        <XAxis dataKey="dateCollected" />
        <YAxis domain={[min-100, max+100]}/>
        <Tooltip />
        <Legend verticalAlign="top" height={40}/>
      </LineChart>
    </div>
    :null
    : null
  )
}