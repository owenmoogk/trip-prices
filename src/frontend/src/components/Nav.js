import React from 'react';

export function NavItem(props){
	return(
		<div className="navItem">
			<a href={props.href} onClick={props.onClick}>{props.text}</a>
		</div>
	)
}

export default function Nav(props) {

	return (
		<div id="navigation">
			<div id="navBox">
				<NavItem href="/" text="Home" />
				{props.loggedIn 
					? 
					<>
						<NavItem href="/resorts" text="Resorts" />
						<NavItem onClick={props.handleLogout} text={"Logout" + (props.username ? " ("+props.username+")" : "")} />
					</>
					: <>
						<NavItem href="/login" text="Login" />
						<NavItem href="/signup" text="Sign Up" />
					</>
				}
			</div>
		</div>
	);
}