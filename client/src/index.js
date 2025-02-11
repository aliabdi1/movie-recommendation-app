import React from "react";
import ReactDOM from "react-dom";
import App from "./App";          // ✅ Only import App
import "./index.css";

ReactDOM.render(
  <React.StrictMode>
    <App />                       {/* ✅ No BrowserRouter here */}
  </React.StrictMode>,
  document.getElementById("root")
);
