import { useEffect, useState, useTransition } from "react"
import React from "react"
import doPost from "../PostRequest"
import { getCookie } from "../CSRF"
import doGet from "../GetRequest"
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Legend} from 'recharts';

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
      for (var key of Object.keys(data)){
        for (var ele of data[key]){
          if (dateData[ele.date]){
            dateData[ele.date][ele.resort.name] = ele.price
          }
          else{
            dateData[ele.date] = {}
            dateData[ele.date][ele.resort.name] = ele.price
          }
        }
      }
      var tmpGraphData = []
      for (var key of Object.keys(dateData)){
        dateData[key]["date"] = key
        tmpGraphData.push(dateData[key])
      }
      tmpGraphData.sort((a,b) => new Date(a.date) - new Date(b.date))
      
      setGraphData(tmpGraphData)

      var tmpResortNames = []
      for (var resortId of Object.keys(data)){
        tmpResortNames.push(data[resortId][0]["resort"]["name"])
      }
      setResortNames(tmpResortNames)
      
    })
  }

  useEffect(() => {
    getFavoriteResortData()
  }, [])  

  function colorWheel(number, bin){
    return 360 / bin * number
  }

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
          <Line type="monotone" dataKey={ele} stroke={'hsl('+colorWheel(index, resortNames.length)+",100%,40%)"} dot={false}/>
        )}
        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
        <XAxis dataKey="date" />
        <YAxis domain={[min-100, max+100]}/>
        <Tooltip />
        <Legend verticalAlign="top" height={40}/>
      </LineChart>
    </div>
    :null
    : null
  )
}