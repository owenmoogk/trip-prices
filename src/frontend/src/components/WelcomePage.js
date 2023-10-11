import React from 'react';
import { NavItem } from "./Nav"

export default function WelcomePage(props) {

	return (
		<div id="welcomePage">
      <h1>Welcome to TripPlanner</h1>
      <a href="/login"><button>Log In</button></a>
      <br/>
      <a href="/signup"><button>Sign Up</button></a>
    </div>
	);
}