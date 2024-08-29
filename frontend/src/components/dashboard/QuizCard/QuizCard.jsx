import { useState, useEffect } from "react";
import { List, Card, Typography, Button, Tabs } from "antd";
import styles from "./QuizCard.module.css";

const { Text } = Typography;

// Countdown Timer Component
const CountdownTimer = ({ startTime, endTime }) => {
  const calculateTimeLeft = () => {
    const now = new Date();
    const start = new Date(startTime);
    const end = new Date(endTime);
    const difference = start - now;
    const differenceEnd = end - now;

    if (differenceEnd <= 0) {
      return { status: "ended" };
    }

    if (difference > 72 * 60 * 60 * 1000) {
      // More than 72 hours
      return { status: "over72" };
    }

    if (now >= start && now <= end) {
      return { status: "inProgress" };
    }

    if (difference > 0 && difference <= 72 * 60 * 60 * 1000) {
      return {
        status: "countdown",
        hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
        minutes: Math.floor((difference / (1000 * 60)) % 60),
        seconds: Math.floor((difference / 1000) % 60),
      };
    }

    return { status: "unknown" };
  };

  const [timerData, setTimerData] = useState(calculateTimeLeft());

  useEffect(() => {
    const timer = setInterval(() => {
      setTimerData(calculateTimeLeft());
    }, 1000);

    return () => clearInterval(timer);
  }, [startTime, endTime]);

  if (timerData.status === "inProgress") {
    return (
      <Text className={styles.countdown}>
        This quiz is currently in progress
      </Text>
    );
  }

  if (timerData.status === "ended") {
    return <Text className={styles.countdown}>This quiz has ended</Text>;
  }

  if (timerData.status === "over72") {
    return (
      <Text className={styles.countdown}>Starts in more than 72 hours</Text>
    );
  }

  if (timerData.status === "countdown") {
    const { hours, minutes, seconds } = timerData;
    return (
      <>
        <Text className={styles.label}>Starts in:</Text>
        <Text className={styles.countdown}>
          {`${String(hours).padStart(2, "0")}:${String(minutes).padStart(
            2,
            "0"
          )}:${String(seconds).padStart(2, "0")}`}
        </Text>
      </>
    );
  }

  return null;
};

const QuizCard = ({ quiz, now }) => {
  const startTime = new Date(quiz.start_time);
  const endTime = new Date(quiz.end_time);
  const isDisabled = now < startTime || now > endTime;

  return (
    <List.Item>
      <Card
        title={quiz.title}
        className={styles.card}
        hoverable={!isDisabled}
        actions={[
          <Button
            type="primary"
            className={styles.startButton}
            disabled={isDisabled}
          >
            {isDisabled
              ? now > endTime
                ? "Quiz Ended"
                : "Start Quiz"
              : "Start Quiz"}
          </Button>,
        ]}
      >
        <div className={styles.cardContent}>
          <div className={styles.infoLine}>
            <Text className={styles.label}>Duration:</Text>
            <Text className={styles.number}>{quiz.duration_min}</Text>
            <Text className={styles.unit}>minutes</Text>
          </div>
          <div className={styles.infoLine}>
            <Text className={styles.label}>Total Score:</Text>
            <Text className={styles.number}>{quiz.total_score}</Text>
          </div>
          <div className={styles.infoLine}>
            <Text className={styles.label}>
              {isDisabled && now > endTime ? "Ended at:" : "Starts at:"}
            </Text>
            <Text className={styles.number}>
              {`${new Date(
                isDisabled && now > endTime ? quiz.end_time : quiz.start_time
              ).toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
              })} ${new Date(
                isDisabled && now > endTime ? quiz.end_time : quiz.start_time
              ).toLocaleDateString([], {
                month: "2-digit",
                day: "2-digit",
                year: "2-digit",
              })}`}
            </Text>
          </div>
          {!isDisabled || (isDisabled && now <= endTime) ? (
            <div className={styles.infoLine}>
              <CountdownTimer
                startTime={quiz.start_time}
                endTime={quiz.end_time}
              />
            </div>
          ) : null}
        </div>
      </Card>
    </List.Item>
  );
};

export default QuizCard;
