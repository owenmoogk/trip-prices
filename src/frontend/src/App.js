import React, { useEffect, useState } from 'react';
import Nav from './components/Nav';
import Login from './components/accounts/Login';
import Signup from './components/accounts/Signup';
import ResortsList from './components/resorts/ResortsList';
import ResortDetails from './components/resorts/ResortDetails';
import WelcomePage from "./components/WelcomePage"
import {
	BrowserRouter as Router,
	Switch,
	Route
} from 'react-router-dom'
import FavoritePage from './components/resorts/FavoritePage';
import "./styles.css"

export default function App(props) {

	const [username, setUsername] = useState()
	const [loggedIn, setLoggedIn] = useState(localStorage.getItem('access') ? true : false)

	function handleLogout() {
		localStorage.removeItem('access');
		localStorage.removeItem("refresh")
		window.location.href="/"
	};

	function getCurrentUser() {
		fetch('/users/current-user/', {
			headers: {
				Authorization: `Bearer ${localStorage.getItem('access')}`
			}
		})
			.then(response => response.json())
			.then(json => {
				if (json.username) {
					setUsername(json.username)
				}
				else {
					handleLogout()
				}
			});
	}

	useEffect(() => {
		if (loggedIn) {
			getCurrentUser()
		}
	})

	return (

		<Router>
			<Nav
				loggedIn={loggedIn}
				handleLogout={handleLogout}
				username={username}
			/>
			<div id="body">
				<Switch>
					<Route path="/login">
						<Login setLoggedIn={setLoggedIn} setUsername={setUsername} getCurrentUser={getCurrentUser} />
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
						{loggedIn
							? <FavoritePage />
							: <WelcomePage />
						}
					</Route>
				</Switch>
			</div>
		</Router>
	);
}