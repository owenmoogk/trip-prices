import { getCookie } from "./CSRF"

export default function doGet(url){
  return fetch(url, {
    method: "GET",
    headers:{
      'X-CSRFToken': getCookie('csrftoken'),
      'Authorization': `Bearer ${localStorage.getItem('access')}`,
    }
  })
}