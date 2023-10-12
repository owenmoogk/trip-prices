import React, { useState } from 'react';
import { getCookie } from "../CSRF"

export default function LoginForm(props) {

	const [username, setUsername] = useState()
	const [password, setPassword] = useState()
	const [message, setMessage] = useState()

	function handleLogin(e) {
		e.preventDefault();
		fetch('/users/jwt/create/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken'),
			},
			body: JSON.stringify({ username: username, password: password })
		})
			.then(response => response.json())
			.then(json => {
				if (json.access) {
					localStorage.setItem('access', json.access);
					localStorage.setItem('refresh', json.refresh)
					props.setLoggedIn(true)
					window.location.href="/"
				}
				else{
					setMessage(json[Object.keys(json)[0]])
				}
			});
	};

	return (
		<>
			<form onSubmit={e => handleLogin(e)}>
				<h4>Log In</h4>
				<label htmlFor="username">Username</label>
				<input
					type="text"
					name="username"
					value={username}
					onChange={e => setUsername(e.target.value)}
				/>
				<label htmlFor="password">Password</label>
				<input
					type="password"
					name="password"
					value={password}
					onChange={e => setPassword(e.target.value)}
				/>
				<p className='error'>{message}</p>
				<input type="submit" />
			</form>
		</>
	);
}