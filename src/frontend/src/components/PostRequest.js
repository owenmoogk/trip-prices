import { getCookie } from "./CSRF"

export default function doPost(url, body){
  return fetch(url, {
    method: "POST",
    body: JSON.stringify(body),
    headers:{
      'X-CSRFToken': getCookie('csrftoken'),
      'Authorization': `JWT ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json',
    }
  })
}