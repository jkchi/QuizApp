import Content from "../../components/dashboard/Content";
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
      <Content />
    </div>
  );
};

export default Dashboard;
