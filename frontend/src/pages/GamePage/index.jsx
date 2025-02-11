/* eslint-disable react/prop-types */
import LeaderBoard from "../../components/LeaderBoard";

import { useNavigate, useParams } from "react-router";
import { useEffect, useState } from "react";
import { apiUrl } from "../../main";

export default function HomePage() {
	let navigate = useNavigate();

	const params = useParams();
	const { id: gameId } = params;

	return (
		<div className="w-full md:max-w-4xl mx-auto min-h-screen flex flex-col border-x">
			<header className="relative w-full h-14 flex items-center justify-center border-b">
				<button
					className="absolute left-6 size-8 rounded-full grid place-items-center bg-gray-100 cursor-pointer"
					onClick={() => navigate(-1)}
				>
					<p className="text-md leading-4 text-gray-600">&#10094;</p>
				</button>
				<p className="text-xl font-semibold">GameCentral</p>
			</header>
			<main className="flex flex-1">
				<GameDetails gameId={gameId} />
				<LeaderBoard key="game-page" gameMode={true} gameId={gameId} />
			</main>
		</div>
	);
}

const GameDetails = ({ gameId }) => {
	const [gameDetails, setGameDetails] = useState(null);

	useEffect(() => {
		const fetchGameDetails = async () => {
			try {
				const response = await fetch(`${apiUrl}/games/${gameId}/details`);
				const data = await response.json();
				setGameDetails(data);
			} catch (error) {
				console.error("Failed to fetch game details:", error);
			}
		};

		fetchGameDetails();
	}, [gameId]);

	const startGame = async () => {
		try {
			await fetch(`${apiUrl}/games/${gameId}/start`, {
				method: "PUT",
			});
			setGameDetails((prev) => ({
				...prev,
				status: "started",
			}));
		} catch (error) {
			console.error("Unable to start game", error);
		}
	};
	const stopGame = async () => {
		try {
			await fetch(`${apiUrl}/games/${gameId}/end`, {
				method: "PUT",
			});
			setGameDetails((prev) => ({
				...prev,
				status: "ended",
			}));
		} catch (error) {
			console.error("Unable to end game", error);
		}
	};

	return (
		<section className="w-full border-r">
			<div className="w-full h-14 px-6 border-b flex items-center">
				<p className="text-md font-medium">{gameDetails?.title}</p>

				<div className="ml-auto flex space-x-2">
					{gameDetails?.status === "pending" ? (
						<button
							onClick={startGame}
							className="size-6 rounded-full grid place-items-center bg-green-100 cursor-pointer"
						>
							<p className="text-xs leading-4 text-green-600">&#9654;</p>
						</button>
					) : gameDetails?.status === "started" ? (
						<button
							onClick={stopGame}
							className="size-6 rounded-full grid place-items-center bg-red-100 cursor-pointer"
						>
							<p className="text-xs leading-4 text-red-600">&#9632;</p>
						</button>
					) : null}
				</div>
			</div>
			<div className="w-full h-14 px-6 border-b flex items-center">
				<p className="text-md">Popularity Index</p>
				<span className="ml-auto text-xs text-gray-600">
					{gameDetails?.popularity_index}
				</span>
			</div>
			<div className="w-full h-14 px-6 border-b flex items-center">
				<p className="text-md">Active Players</p>
				<span className="ml-auto text-xs text-gray-600">{gameDetails?.w2}</span>
			</div>
			<div className="w-full h-14 px-6 border-b flex items-center">
				<p className="text-md">Upvotes</p>
				<span className="ml-auto text-xs text-gray-600">{gameDetails?.w3}</span>
			</div>
		</section>
	);
};
