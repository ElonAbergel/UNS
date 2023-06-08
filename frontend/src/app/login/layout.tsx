import React from 'react';
import LoginPage from './login_page';

export default function RootLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	return (
		<main className="flex">
			<div className="flex-1">
				{/* @ts-ignore */}
				<LoginPage />
			</div>

			<div>{children}</div>
		</main>
	);
}
