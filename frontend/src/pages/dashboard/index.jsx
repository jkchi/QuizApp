import Header from "../../components/dashboard/Header";
import styles from "./index.module.css";

const Dashboard = () => {
  const handleLogout = () => {
    // Implement your log-out logic here
    console.log("User logged out");
  };

  return (
    <div className={styles.container}>
      <Header userName="John Doe" handleLogout={handleLogout} />
      <div className={styles.content}>
        <h1>Dashboard</h1>
        <p>Welcome to the dashboard!</p>
      </div>
    </div>
  );
};

export default Dashboard;
