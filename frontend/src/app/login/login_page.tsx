import React from 'react';
import { WebsiteBackEnd } from '../../../typing';
import Link from 'next/link';

// A check function to check my backend, return message
const fetchCheck = async () => {
	try {
		const respond = await fetch(`http://127.0.0.1:8000/login/login/`, {
			cache: 'no-cache',
		});
		if (!respond.ok) {
			throw new Error('Failed to fetch data from the server');
		}

		const check: WebsiteBackEnd[] = await respond.json();
		return Array.isArray(check) ? check : [check];
	} catch (error) {
		console.error('Error fetching data', error);
		return [];
	}
};

async function LoginPage() {
	// const checks = await fetchCheck();
	return (
		<div className="flex flex-col items-center justify-center min-h-screen bg-gray-900">
			<h1 className="text-white text-3xl font-bold mb-8">Login</h1>
			<form className="bg-gray-800 p-6 rounded-lg w-72">
				<div className="mb-4">
					<label
						htmlFor="passport-number"
						className="text-white"
					>
						Passport Number
					</label>
					<input
						type="text"
						id="passport-number"
						pattern="[0-9]{8}"
						maxLength={8}
						className="w-full bg-gray-700 text-white px-3 py-2 rounded"
						placeholder="Enter your passport number"
					/>
				</div>
				<div className="mb-4">
					<label
						htmlFor="password"
						className="text-white"
					>
						Password
					</label>
					<input
						type="password"
						id="password"
						className="w-full bg-gray-700 text-white px-3 py-2 rounded"
						placeholder="Enter your password"
					/>
				</div>
				<button
					type="submit"
					className="bg-blue-500 text-white px-4 py-2 rounded"
				>
					Login
				</button>
			</form>
			<p className="mt-4 text-white">
				Don't have an account?{' '}
				<Link
					href="/register"
					className="text-blue-500"
				>
					Register
				</Link>
			</p>
		</div>
		// <div>
		// 	{checks.map((check) => (
		// 		<p key={check.id}>
		// 			Omri shift has a small dick but he is also {check.message}
		// 		</p>
		// 	))}
		// </div>
	);
}

export default LoginPage;
