import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Home from "../pages/Home";
import Movies from "../pages/Movies";
import Users from "../pages/Users";

function App() {
  return (
    <Router>
      <div className="container mt-5">
        <h1 className="text-center mb-4">Movie Recommendation App</h1>
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path="/movies" component={Movies} />
          <Route path="/users" component={Users} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
