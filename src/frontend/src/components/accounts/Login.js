import React, { useState } from 'react';
import { Redirect } from 'react-router';
import { getCookie } from "../CSRF"

export default function LoginForm(props) {

	const [username, setUsername] = useState()
	const [password, setPassword] = useState()
	const [message, setMessage] = useState()
	const [redirect, setRedirect] = useState()

	function handleLogin(e) {
		e.preventDefault();
		fetch('/token-auth/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken'),
			},
			body: JSON.stringify({ username: username, password: password })
		})
			.then(response => response.json())
			.then(json => {
				if (json.token) {
					localStorage.setItem('token', json.token);
					props.setLoggedIn(true)
					props.setUsername(json.user.username)
					setRedirect(true)
				}
				else{
					setMessage(json[Object.keys(json)[0]])
				}
			});
	};

	return (
		<>
			{redirect ?
				<Redirect to='/' />
				: null
			}
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