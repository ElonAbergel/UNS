'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import fetchRegister from './register_api';
import { useGlobalContext } from '../GlobalContexts';
function RegisterPage() {
	const { csrfToken } = useGlobalContext();
	const { isLoggedIn, setIsLoggedIn } = useGlobalContext();
	const [name, setName] = useState('');
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [confirmPassword, setConfirmPassword] = useState('');
	const [passportNumber, setPassportNumber] = useState('');
	const [trustNode, setTrustNode] = useState('');

	const router = useRouter();

	const handleSubmit = async (e) => {
		e.preventDefault();

		// Check if all fields are filled
		if (
			!name ||
			!email ||
			!password ||
			!confirmPassword ||
			!passportNumber ||
			!trustNode
		) {
			alert('Please fill in all fields');
			return;
		}

		// Call the registration API
		const response = await fetchRegister(
			name,
			email,
			password,
			passportNumber,
			trustNode,
			csrfToken
		);
		// console.log(response);
		// Assuming the API returns a success status, redirect to the dashboard page
		// check if not need to add [0]
		/* @ts-ignore */
		if (response.status === 'success') {
			setIsLoggedIn(true); // Update the isLoggedIn status in the RegisterPage component
			router.push('/dashboard');
		} else {
			alert('Registration failed. Please try again.');
		}
	};

	return (
		<div className="flex flex-col items-center justify-center min-h-screen bg-gray-900">
			<h1 className="text-white text-3xl font-bold mb-8">Register</h1>
			<form
				className="bg-gray-800 p-6 rounded-lg w-72"
				onSubmit={handleSubmit}
			>
				<div className="mb-4">
					<label
						htmlFor="name"
						className="text-white"
					>
						Name
					</label>
					<input
						type="text"
						id="name"
						className="w-full bg-gray-700 text-white px-3 py-2 rounded"
						placeholder="Enter your full name"
						value={name}
						onChange={(e) => setName(e.target.value)}
					/>
				</div>
				<div className="mb-4">
					<label
						htmlFor="email"
						className="text-white"
					>
						Email
					</label>
					<input
						type="email"
						id="email"
						className="w-full bg-gray-700 text-white px-3 py-2 rounded"
						placeholder="Enter your email"
						value={email}
						onChange={(e) => setEmail(e.target.value)}
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
						value={password}
						onChange={(e) => setPassword(e.target.value)}
					/>
				</div>
				<div className="mb-4">
					<label
						htmlFor="confirm-password"
						className="text-white"
					>
						Confirm Password
					</label>
					<input
						type="password"
						id="confirm-password"
						className="w-full bg-gray-700 text-white px-3 py-2 rounded"
						placeholder="Confirm your password"
						value={confirmPassword}
						onChange={(e) => setConfirmPassword(e.target.value)}
					/>
				</div>
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
						value={passportNumber}
						onChange={(e) => setPassportNumber(e.target.value)}
					/>
				</div>
				<div className="mb-4">
					<label
						htmlFor="trust-node"
						className="text-white"
					>
						Choose Trusted Bank
					</label>
					<select
						id="trust-node"
						className="w-full bg-gray-700 text-white px-3 py-2 rounded"
						value={trustNode}
						onChange={(e) => setTrustNode(e.target.value)}
					>
						<option value="">Select a bank</option>
						<option value="bank1">JPMorgan Chase</option>
						<option value="bank2">Bank of America</option>
						<option value="bank3">Citigroup</option>
					</select>
				</div>
				<button
					type="submit"
					className="bg-blue-500 text-white px-4 py-2 rounded"
				>
					Register
				</button>
			</form>
			<p className="mt-4 text-white">
				Already have an account?{' '}
				<Link
					href="/login"
					className="text-blue-500"
				>
					Login
				</Link>
			</p>
		</div>
	);
}

export default RegisterPage;
