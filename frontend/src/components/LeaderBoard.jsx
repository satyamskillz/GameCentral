import PropTypes from "prop-types";
import { useEffect, useState } from "react";
import CreatePlayerForm from "./CreatePlayerForm";
import { apiUrl } from "../main";
import AddPlayerForm from "./AddPlayerForm";

export default function LeaderBoard({ gameMode = false, gameId }) {
	const [isCreatingOrAdding, setCreatingOrAdding] = useState(false);
	const [players, setPlayers] = useState([]);
	const [flag, setFlag] = useState(false);

	useEffect(() => {
		const fetchPlayers = async () => {
			try {
				const url = gameMode
					? `${apiUrl}/leaderboard/games/${gameId}`
					: `${apiUrl}/leaderboard`;

				const response = await fetch(url);
				const data = await response.json();
				setPlayers(data);
			} catch (error) {
				console.error("Error fetching games:", error);
			}
		};

		fetchPlayers();

		return () => {
			setCreatingOrAdding(false);
			setPlayers([]);
		};
	}, [gameId, gameMode, flag]);

	const onPlayerCreate = (player) => {
		alert("Player Created: " + player.id);
	};
	const onPlayerAdd = () => {
		setFlag((prev) => !prev);
	};

	const exitPlayer = async (id) => {
		try {
			const response = await fetch(`${apiUrl}/games/${gameId}/contestants/${id}/exit`, {
				headers: { "Content-Type": "application/json" },
				method: "PUT",
			});

			if (!response.ok) throw new Error();

			setFlag((prev) => !prev);
		} catch (error) {
			console.error(error);
			alert("Failed to exit");
		}
	};

	const deletePlayer = async (id) => {
		try {
			const response = await fetch(`${apiUrl}/contestants/${id}`, {
				headers: { "Content-Type": "application/json" },
				method: "DELETE",
			});

			if (!response.ok) throw new Error();

			setFlag((prev) => !prev);
		} catch (error) {
			console.error(error);
			alert("Failed to Delete player");
		}
	};

	return (
		<section className="w-full">
			<div className="w-full h-14 px-6 border-b flex items-center">
				<p className="text-md font-medium">{gameMode ? "Game" : "Global"} Leaderboard</p>
				{!isCreatingOrAdding && (
					<button
						onClick={() => setCreatingOrAdding(true)}
						className="bg-gray-200 py-1 px-3 leading-4 rounded-full text-xs ml-auto cursor-pointer active:bg-gray-300"
					>
						{gameMode ? "Add player" : "Create Player"}
					</button>
				)}
			</div>
			{isCreatingOrAdding && !gameMode && (
				<CreatePlayerForm
					closeForm={() => setCreatingOrAdding(false)}
					onSubmit={onPlayerCreate}
				/>
			)}
			{isCreatingOrAdding && gameMode && (
				<AddPlayerForm
					gameId={gameId}
					onSubmit={onPlayerAdd}
					closeForm={() => setCreatingOrAdding(false)}
				/>
			)}
			<ul className="flex flex-col">
				{players.map((player) => (
					<li key={player.id} className="h-12 border-b px-6 flex gap-2 items-center">
						<p className="mr-auto">
							{player.name} ({player.id})
						</p>
						<span className="text-xs text-gray-600">{player.score} Points</span>
						<span className="text-sm text-gray-600">·</span>
						{gameMode ? (
							<span
								onClick={() => exitPlayer(player.id)}
								className="text-xs text-gray-600 cursor-pointer hover:underline hover:text-red-500"
							>
								EXIT
							</span>
						) : (
							<span
								onClick={() => deletePlayer(player.id)}
								className="text-xs text-gray-600 cursor-pointer hover:underline hover:text-red-500"
							>
								DELETE
							</span>
						)}
					</li>
				))}
			</ul>
		</section>
	);
}

LeaderBoard.propTypes = {
	gameMode: PropTypes.bool,
	gameId: PropTypes.string,
};
