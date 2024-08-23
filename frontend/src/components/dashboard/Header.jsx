import React from "react";
import styles from "./Header.module.css";

const Header = ({ userName, handleLogout }) => {
  return (
    <header className={styles.header}>
      <div className={styles.headerContent}>
        <div className={styles.welcomeMessage}>Welcome, {userName}!</div>
        <button className={styles.logoutButton} onClick={handleLogout}>
          Log Out
        </button>
      </div>
    </header>
  );
};

export default Header;
