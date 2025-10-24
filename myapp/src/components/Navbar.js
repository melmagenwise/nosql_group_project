import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <header className="navbar">
      <div className="navbar__logo">MovieManiac</div>
      <nav className="navbar__links" aria-label="Primary navigation">
        <Link to="/">MyHome</Link>
        <Link to="/#movies">Movies</Link>
        <Link to="/#series">Series</Link>
        <Link to="/#actors">Actors</Link>
        <Link to="/#myprofile">MyProfile</Link>
      </nav>
    </header>
  );
};

export default Navbar;
