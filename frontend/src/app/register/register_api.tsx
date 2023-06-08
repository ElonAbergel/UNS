import React from 'react';
import { Website_BackEnd_register_response, csrfToken } from '../../../typing';
import Link from 'next/link';
import { application } from 'express';
import axios from 'axios';
import { useGlobalContext } from '../GlobalContexts';

// A check function to check my backend, return message
const fetchRegister = async (
	name,
	email,
	password,
	passport,
	trustNode,
	csrfToken
) => {
	try {
		// // We need to get the csrfToken
		// const response = await fetch('http://127.0.0.1:8000/get_csrf_token/token/');

		// if (!response.ok) {
		// 	throw new Error('Failed to fetch data from the server');
		// }
		// const csrfToken: csrfToken[] = await response.json();
		console.log(csrfToken);
		// we api call the backend to register a user
		const respond = await fetch(
			'http://127.0.0.1:8000/register/register_user/',
			{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': csrfToken,
				},

				body: JSON.stringify({
					name: name,
					email: email,
					password: password,
					passport: passport,
					trustNode: trustNode,
				}),
				cache: 'no-cache',
			}
		);
		if (!respond.ok) {
			throw new Error('Failed to fetch data from the server');
		}
		const respond_in_check: Website_BackEnd_register_response[] =
			await respond.json();
		// check this array thing!
		return respond_in_check;
	} catch (error) {
		console.error('Error fetching data', error);
		return '';
	}
};

export default fetchRegister;
