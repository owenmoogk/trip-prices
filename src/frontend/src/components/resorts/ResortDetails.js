import { elementType } from "prop-types";
import { useEffect, useState } from "react"
import React from "react";
import { useParams } from "react-router-dom/cjs/react-router-dom.min";
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Legend } from 'recharts';
import colorWheel from "../ColorWheel"

export default function ResortDetails() {

  const id = useParams().id
  const [resortData, setResortData] = useState()
  const [resortPrices, setResortPrices] = useState()
  const [graphData, setGraphData] = useState()
  const [dateIdMatch, setDateIdMatch] = useState()

  function getResortData() {
    fetch("/api/resort/" + id + '/')
      .then(response => response.json())
      .then(data => setResortData(data))
  }

  function getResortPrices() {
    fetch("/api/resortPrices/" + id + "/")
      .then(response => response.json())
      .then(data => {

        setResortPrices(data)

        var dateData = {}
        var tmpDateIdMatch = {}

        for (var weekPrices of data) {

          tmpDateIdMatch[weekPrices.startDate + " - " + weekPrices.endDate] = { "start": weekPrices.startDate, "end": weekPrices.endDate }

          for (var price of weekPrices.prices) {
            if (dateData[price.dateCollected]) {
              dateData[price.dateCollected][weekPrices.startDate + " - " + weekPrices.endDate] = price.price
            }
            else {
              dateData[price.dateCollected] = {}
              dateData[price.dateCollected][weekPrices.startDate + " - " + weekPrices.endDate] = price.price
            }
          }
        }

        setDateIdMatch(tmpDateIdMatch)
        var tmpGraphData = []
        for (var key of Object.keys(dateData)) {
          dateData[key]["dateCollected"] = key
          tmpGraphData.push(dateData[key])
        }
        tmpGraphData.sort((a, b) => new Date(a["dateCollected"]) - new Date(b["dateCollected"]))

        setGraphData(tmpGraphData)
      })
  }

  useEffect(() => {
    getResortData()
    getResortPrices()
  }, [])

  var max = -Infinity
  var min = Infinity
  if (resortPrices){
    for (var item of resortPrices){
      for (var pricePoint of item.prices){
        if (pricePoint.price > max){
          max = pricePoint.price
        }
        if (pricePoint.price < min){
          min = pricePoint.price
        }
      }
    }
  }

  return (
    <div id="resortDetails">
      {resortData ?
        <h1>{resortData.name.trim()}</h1>
        : null}

      {resortPrices ?
        dateIdMatch ?
          <>
            <LineChart width={400} height={400} data={graphData}>
              {Object.keys(dateIdMatch).map((element, index) => 
                <Line type="monotone" dataKey={element} stroke={colorWheel(index, Object.keys(dateIdMatch).length)} />
              )}
              <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
              <XAxis dataKey="dateCollected" />
              <YAxis domain={[min-100, max+100]}/>
              <Tooltip />
              <Legend />
            </LineChart>
            <table>
              <tbody>
                <tr>
                  <th>Date</th>
                  {resortPrices.map((element) =>
                    <th>
                      Price ({element.startDate} - {element.endDate})
                    </th>
                  )}
                </tr>
                {/* {resortPrices.map((item) => 
              <tr>
              item.map(() =>
                  <td>{item.price}</td>
                  <td>{item.price}</td>
              </tr>
              )
            )} */}
              </tbody>
            </table>
          </>
          : null
        : null
      }

    </div>
  );
}