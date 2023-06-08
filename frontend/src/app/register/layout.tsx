import React from 'react';
import RegisterPage from './register_page';

export default function RootLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	return (
		<main className="flex">
			<div className="flex-1">
				{/* @ts-ignore */}
				<RegisterPage />
			</div>
			<div>{children}</div>
		</main>
	);
}
