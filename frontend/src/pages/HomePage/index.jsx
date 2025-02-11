/* eslint-disable react/prop-types */
import LeaderBoard from "../../components/LeaderBoard";
import GameForm from "../../components/CreateGameForm";
import { useEffect, useState } from "react";
import { NavLink } from "react-router";
import { apiUrl } from "../../main";

export default function HomePage() {
	return (
		<div className="w-full md:max-w-4xl mx-auto min-h-screen flex flex-col border-x">
			<header className="w-full h-14 flex items-center justify-center border-b">
				<p className="text-xl font-semibold">GameCentral</p>
			</header>
			<main className="flex flex-1">
				<GameList />
				<LeaderBoard key="main-page" />
			</main>
		</div>
	);
}

const GameList = () => {
	const [isCreating, setCreating] = useState(false);
	const [games, setGames] = useState([]);

	useEffect(() => {
		const fetchGames = async () => {
			try {
				const response = await fetch(`${apiUrl}/games`);
				const data = await response.json();
				setGames(data);
			} catch (error) {
				console.error("Error fetching games:", error);
			}
		};

		fetchGames();

		return () => {
			setGames([]);
			setCreating(false);
		};
	}, []);

	return (
		<section className="w-full border-r">
			<div className="w-full h-14 px-6 border-b flex items-center">
				<p className="text-md font-medium">Games</p>
				{!isCreating && (
					<button
						onClick={() => setCreating(true)}
						className="bg-gray-200 py-1 px-3 leading-4 rounded-full text-xs ml-auto cursor-pointer active:bg-gray-300"
					>
						Create Game
					</button>
				)}
			</div>
			{isCreating && <GameForm setCreating={setCreating} setGames={setGames} />}

			<ul className="flex flex-col">
				{games.map((item) => (
					<NavLink key={item.id} to={`/game/${item.id}`}>
						<li className="h-12 border-b px-6 flex gap-2 items-center hover:bg-gray-100 active:bg-gray-50 cursor-pointer">
							<span
								className={`text-xl size-2 rounded-full ${
									item.status === "started"
										? "bg-green-500"
										: item.status === "ended"
										? "bg-red-500"
										: "bg-gray-400"
								}`}
							/>

							<p className="">{item.title}</p>
							<span className="ml-auto leading-4 text-xs text-gray-500">
								{item.active_players} Players
							</span>
							<span className="text-lg text-gray-600">{">"}</span>
						</li>
					</NavLink>
				))}
			</ul>
		</section>
	);
};
