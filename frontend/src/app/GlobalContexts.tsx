'use client';
import {
	createContext,
	useContext,
	Dispatch,
	SetStateAction,
	useState,
	useEffect,
} from 'react';
import { csrfToken } from '../../typing';

interface ContextProps {
	isLoggedIn: boolean;
	setIsLoggedIn: Dispatch<SetStateAction<boolean>>;
	csrfToken: string | null;
	setCsrfToken: Dispatch<SetStateAction<string | null>>;
}

const GlobalContext = createContext<ContextProps>({
	isLoggedIn: false,
	setIsLoggedIn: () => {},
	csrfToken: null,
	setCsrfToken: () => {},
});

export const GlobalContextProvider = ({ children }) => {
	const [isLoggedIn, setIsLoggedIn] = useState(false);
	const [csrfToken, setCsrfToken] = useState<string | null>(null);

	useEffect(() => {
		// Retrieve login status and csrfToken from cookies if available
		const storedIsLoggedIn = localStorage.getItem('isLoggedIn');
		const storedCsrfToken = localStorage.getItem('csrfToken');

		if (storedIsLoggedIn) {
			setIsLoggedIn(JSON.parse(storedIsLoggedIn));
		}

		if (storedCsrfToken) {
			setCsrfToken(storedCsrfToken);
		}
	}, []);

	useEffect(() => {
		// Save login status and csrfToken to cookies
		localStorage.setItem('isLoggedIn', JSON.stringify(isLoggedIn));
		localStorage.setItem('csrfToken', csrfToken);
	}, [isLoggedIn, csrfToken]);

	useEffect(() => {
		const fetchCsrfToken = async () => {
			try {
				const response = await fetch(
					'http://127.0.0.1:8000/get_csrf_token/token/'
				);

				if (!response.ok) {
					throw new Error('Failed to fetch data from the server');
				}

				const csrfToken_check: csrfToken[] = await response.json();

				// Set the CSRF token as a cookie with an expiration date
				const expirationDate = new Date();
				expirationDate.setDate(expirationDate.getDate() + 1); // Set expiration for 1 day
				document.cookie = `csrftoken=${
					csrfToken_check.token
				}; expires=${expirationDate.toUTCString()}; path=/`;

				setCsrfToken(csrfToken_check.token);
			} catch (error) {
				console.error(error);
			}
		};

		fetchCsrfToken();
	}, []);

	return (
		<GlobalContext.Provider
			value={{ isLoggedIn, setIsLoggedIn, csrfToken, setCsrfToken }}
		>
			{children}
		</GlobalContext.Provider>
	);
};

export const useGlobalContext = () => useContext(GlobalContext);
