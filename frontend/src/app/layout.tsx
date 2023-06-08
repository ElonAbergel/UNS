import '../app/globals.css';
import { Inter } from 'next/font/google';
import Header from './Header';
import { GlobalContextProvider } from './GlobalContexts';
export default function RootLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	return (
		<html>
			<head></head>

			<body suppressHydrationWarning={true}>
				{/* @ts-ignore */}
				<GlobalContextProvider>
					<Header />
					{children}
				</GlobalContextProvider>
			</body>
		</html>
	);
}
