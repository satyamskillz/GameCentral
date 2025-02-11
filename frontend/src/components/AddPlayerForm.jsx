import PropTypes from "prop-types";
import { useState } from "react";
import { apiUrl } from "../main";

export default function AddPlayerForm({ closeForm, onSubmit, gameId }) {
	const [errorMessage, setErrorMessage] = useState("");

	const handleSubmit = async (e) => {
		e.preventDefault();
		setErrorMessage("");

		const id = e.target.id.value;

		if (!id.trim()) {
			setErrorMessage("Id cannot be empty");
			return null;
		}

		try {
			const response = await fetch(`${apiUrl}/games/${gameId}/contestants/${id}/join`, {
				headers: { "Content-Type": "application/json" },
				method: "POST",
			});

			if (!response.ok) {
				setErrorMessage("Failed to add player");
				return null;
			}
			onSubmit();
			closeForm();
		} catch (error) {
			console.error(error);
			setErrorMessage("Error add player");
		}
	};

	return (
		<form onSubmit={handleSubmit} className="w-full px-6 py-4 border-b gap-2 flex flex-col ">
			<label htmlFor="id" className="text-sm">
				Add player to the game
			</label>
			<input
				id="id"
				type="text"
				name="id"
				placeholder="Enter user id"
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
					onClick={closeForm}
					className="bg-gray-200 py-2 px-4 leading-4 rounded-full text-sm cursor-pointer active:bg-gray-300"
				>
					Cancel
				</button>
				<button
					type="submit"
					className="bg-blue-500 text-white py-2 px-4 leading-4 rounded-full text-sm cursor-pointer active:bg-blue-400"
				>
					Add
				</button>
			</div>
		</form>
	);
}

AddPlayerForm.propTypes = {
	gameId: PropTypes.string.isRequired,
	onSubmit: PropTypes.func.isRequired,
	closeForm: PropTypes.func.isRequired,
};
