import { BrowserRouter, Route, Routes } from "react-router";
import { createRoot } from "react-dom/client";
import { StrictMode } from "react";
import "./index.css";

// Pages
import HomePage from "./pages/HomePage";
import GamePage from "./pages/GamePage";

export const apiUrl = "http://localhost:8000";

createRoot(document.getElementById("root")).render(
	<StrictMode>
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<HomePage />} />
				<Route path="/game/:id" element={<GamePage />} />
			</Routes>
		</BrowserRouter>
	</StrictMode>
);
