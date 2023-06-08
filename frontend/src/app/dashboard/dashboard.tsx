import React from 'react';

function Dashboard() {
	return (
		<div className="flex items-center justify-center h-screen bg-gray-900">
			<div className="w-3/4 p-8 bg-white rounded-lg">
				<h1 className="text-3xl font-bold mb-4 text-center text-gray-900">
					Welcome to Ywitter!
				</h1>

				<div className="flex">
					<div className="w-1/4 p-4 bg-gray-200">
						{/* Sidebar content */}
						<h2 className="text-xl font-bold mb-2">Chat Sidebar</h2>
						{/* Add any additional sidebar content here */}
					</div>
					<div className="w-3/4 p-4 bg-white">
						{/* Chat messages */}
						<div className="space-y-4">
							{/* Display chat messages here */}
							<div className="flex">
								<span className="font-bold mr-2">John Doe:</span>
								<span className="text-gray-600">Hello, how are you?</span>
							</div>
							<div className="flex">
								<span className="font-bold mr-2">Jane Smith:</span>
								<span className="text-gray-600">
									I'm good, thanks! How about you?
								</span>
							</div>
							{/* Add more chat messages here */}
						</div>
					</div>
				</div>
			</div>
		</div>
	);
}

export default Dashboard;
