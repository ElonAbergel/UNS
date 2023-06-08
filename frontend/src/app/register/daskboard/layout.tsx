import React from 'react';
import Dashboard from './dashboard';

export default function RootLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	return (
		<main className="flex">
			<div className="flex-1">
				{/* @ts-ignore */}
				<Dashboard />
			</div>
			<div>{children}</div>
		</main>
	);
}
