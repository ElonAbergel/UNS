'use client';
import React from 'react';
import Link from 'next/link';
import UNS_logo from '../assets/UNS_logo.jpeg';
import { useGlobalContext } from './GlobalContexts';

function Header() {
	const { isLoggedIn, setIsLoggedIn } = useGlobalContext();
	const handleLogout = () => {
		// Perform logout logic
		setIsLoggedIn(false);
	};

	return (
		<header className="p-3 bg-gradient-to-r from-green-900 to-green-300 text-left">
			<Link href="/">
				<img
					src={UNS_logo.src}
					className="inline-block h-11 w-11 mr-2"
				/>
			</Link>
			{isLoggedIn ? (
				// Show logout and my profile links if user is logged in
				<>
					<Link
						href="/dashboard"
						className="bg-black hover text-white font-bold py-3 px-5 rounded ml-5"
					>
						Dashboard
					</Link>
					<Link
						href="/myprofile"
						className="bg-black hover text-white font-bold py-3 px-5 rounded ml-5"
					>
						My Profile
					</Link>
					<Link
						href="/"
						className="ml-5 rounded px-5 py-3 font-bold text-white hover bg-black"
						onClick={handleLogout}
					>
						Logout
					</Link>
				</>
			) : (
				<>
					<Link
						href="/login"
						className="bg-black hover text-white font-bold py-3 px-5 rounded ml-5"
					>
						Login
					</Link>
					<Link
						href="/register"
						className="bg-black hover text-white font-bold py-3 px-5 rounded ml-5"
					>
						Register
					</Link>
				</>
			)}
		</header>
	);
}

export default Header;

export async function getServerSideProps() {
	// Perform server-side logic to determine the initial isLoggedIn state
	const isLoggedIn = true; // Example: Replace with your server-side logic

	return {
		props: {
			initialIsLoggedIn: isLoggedIn,
		},
	};
}
