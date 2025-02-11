import PropTypes from "prop-types";
import { useState } from "react";
import { apiUrl } from "../main";

export default function GameForm({ setCreating, setGames }) {
	const [errorMessage, setErrorMessage] = useState("");

	const handleSubmit = async (e) => {
		e.preventDefault();
		setErrorMessage("");

		const title = e.target.title.value;

		if (!title.trim()) {
			setErrorMessage("Title cannot be empty");
			return null;
		}

		try {
			const response = await fetch(`${apiUrl}/games`, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ title }),
			});

			if (response.ok) {
				const newGame = await response.json();
				setGames((prevGames) => [...prevGames, newGame]);
				setCreating(false);
			} else {
				setErrorMessage("Failed to create game");
			}
		} catch (error) {
			console.error(error);
			setErrorMessage("Error creating game");
		}
	};

	return (
		<form onSubmit={handleSubmit} className="w-full px-6 py-4 border-b gap-2 flex flex-col ">
			<label htmlFor="title" className="text-sm">
				Create New Game
			</label>
			<input
				id="title"
				type="text"
				name="title"
				placeholder="Enter Title"
				className="border px-3 py-2 outline-none"
			/>
			{errorMessage && (
				<div
					role="alert"
					className="bg-red-100 border border-red-400 text-red-700 px-3 py-2 relative text-sm flex items-center gap-1"
				>
					<strong className="font-bold">Error: </strong>
					<span className="block sm:inline">{errorMessage}</span>
					<button
						type="button"
						className="absolute right-0 px-4 py-3"
						onClick={() => setErrorMessage("")}
					>
						<span className="text-red-500">&times;</span>
					</button>
				</div>
			)}
			<div className="flex justify-between">
				<button
					type="button"
					onClick={() => setCreating(false)}
					className="bg-gray-200 py-2 px-4 leading-4 rounded-full text-sm cursor-pointer active:bg-gray-300"
				>
					Cancel
				</button>
				<button
					type="submit"
					className="bg-blue-500 text-white py-2 px-4 leading-4 rounded-full text-sm cursor-pointer active:bg-blue-400"
				>
					Create
				</button>
			</div>
		</form>
	);
}

GameForm.propTypes = {
	setCreating: PropTypes.func.isRequired,
	setGames: PropTypes.func.isRequired,
};
