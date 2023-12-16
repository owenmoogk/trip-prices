import moment from "moment"

function getDates(startDate, stopDate) {

  function addDays(date, days) {
    var date = new Date(date);
    date.setDate(date.getDate() + days);
    return date;
  }

  var dateArray = new Array();
  var currentDate = addDays(startDate,2);
  while (currentDate <= stopDate) {
    dateArray.push(new Date (currentDate));
    currentDate = addDays(currentDate,1)
  }
  return dateArray;
}

export default function smoothGraphingData(data){
  var newData = []  
  var prevDate = Date.parse(data[0].dateCollected)
  for (var dataPoint of data){
    var currDate = Date.parse(dataPoint.dateCollected)
    var datesBetween = getDates(prevDate, currDate)
    for(var newDate of datesBetween){
      var dataCopy = {...dataPoint}
      dataCopy.dateCollected = moment(newDate).format("YYYY-MM-DD")
      newData.push(dataCopy)
    }
    newData.push(dataPoint)
    prevDate = currDate
  }
  console.log(newData)
  return newData
}