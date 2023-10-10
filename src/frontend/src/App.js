import React, { useEffect, useState } from 'react';
import Nav from './components/Nav';
import Login from './components/accounts/Login';
import Signup from './components/accounts/Signup';
import ResortsList from './components/resorts/ResortsList';
import ResortDetails from './components/resorts/ResortDetails';
import {
	BrowserRouter as Router,
	Switch,
	Route
} from 'react-router-dom'

export default function App(props) {

	const [username, setUsername] = useState()
	const [loggedIn, setLoggedIn] = useState(localStorage.getItem('token') ? true : false)

	function handleLogout() {
		localStorage.removeItem('token');
		setLoggedIn(false)
		setUsername('')
	};

	useEffect(() => {
		if (loggedIn) {
			fetch('/users/current_user/', {
				headers: {
					Authorization: `JWT ${localStorage.getItem('token')}`
				}
			})
				.then(response => response.json())
				.then(json => {
					if (json.username){
						setUsername(json.username)
					}
					else{
						handleLogout()
					}
				});
		}
	})

	return (

		<Router>
			<Nav
				loggedIn={loggedIn}
				handleLogout={handleLogout}
			/>
			<Switch>
				<Route path="/login">
					<Login setLoggedIn={setLoggedIn} setUsername={setUsername} />
				</Route>
				<Route path="/signup">
					<Signup setLoggedIn={setLoggedIn} setUsername={setUsername} />
				</Route>
				<Route path="/resorts">
					<Switch>
						<Route exact path="/resorts">
							<ResortsList />
						</Route>
						<Route path="/resorts/:id">
							<ResortDetails />
						</Route>
					</Switch>
				</Route>
				<Route exact path=''>
					<ResortsList />
				</Route>
			</Switch>
		</Router>
	);
}