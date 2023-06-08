import React from 'react';
import Link from 'next/link';
import GridMatrix from '../assets/gridMatrix.gif';

const gridMatrixSrc = GridMatrix.src;
function Home_page() {
	return (
		<div>
			<div>
				<img
					className="matrix-bg fixed top-0 left-0 w-full h-full z-[-1] object-cover"
					src={gridMatrixSrc}
				/>
			</div>
			<main className="container mx-auto py-10 px-4 flex flex-col items-center justify-center">
				<h1 className="text-4xl font-bold mb-8 text-white text-center">
					UNS Demo
				</h1>

				<section className="mt-5 text-white text-center">
					<h2 className="text-2xl font-bold mb-4">About UNS</h2>
					<p className="text-white text-lg font-bold mb-6 font-rubik">
						UNS provides privacy-preserving software and infrastructure for
						identity and access management. Our platform enables solutions
						across various industries and applications, catering to users who
						value security and privacy.
					</p>
					<p className="text-white text-lg font-bold mb-6 font-rubik">
						From device-based account authentications to anonymously linking
						de-identified medical records and detecting bots, UNS creates
						building blocks to prioritize privacy in online communication and
						commerce.
					</p>

					<p className="text-white text-lg font-bold mb-6 font-rubik">
						Join us on this exciting journey as we put privacy at the heart of
						technology and unlock the power of secure and private online
						solutions.
					</p>
				</section>
			</main>
		</div>
	);
}

export default Home_page;
