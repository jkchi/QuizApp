import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const SignIn = ({ setIsAuthenticated }) => {
  const navigate = useNavigate();

  useEffect(() => {
    const isUserSignedIn = JSON.parse(localStorage.getItem("isAuthenticated"));
    if (isUserSignedIn) {
      navigate("/dashboard");
    }
  }, [navigate]);

  const handleSignIn = () => {
    // Fake sign-in logic
    setIsAuthenticated(true);
    localStorage.setItem("isAuthenticated", true);
    // Navigate to dashboard after sign-in
    navigate("/dashboard");
  };

  return (
    <div>
      <h1>Sign In</h1>
      <button onClick={handleSignIn}>Sign In</button>
    </div>
  );
};

export default SignIn;
