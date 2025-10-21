import React from 'react';
import './Navbar.css';

const Navbar = () => {
  return (
    <header className="navbar">
      <div className="navbar__logo">MovieManiac</div>
      <nav className="navbar__links" aria-label="Primary navigation">
        <a href="#home">MyHome</a>
        <a href="#movies">Movies</a>
        <a href="#series">Series</a>
      </nav>
    </header>
  );
};

export default Navbar;
