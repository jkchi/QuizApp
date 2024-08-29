import { useState, useEffect } from "react";
import { List, Card, Typography, Button, Tabs } from "antd";
import styles from "./Content.module.css";
import QuizCard from "./QuizCard/QuizCard";

const { Text } = Typography;

const quizzes = [
  {
    id: 1,
    title: "Math Fundamentals Quiz",
    text: "This quiz covers the basics of arithmetic, algebra, and geometry.",
    created_at: "2024-08-22T10:00:00Z",
    start_time: "2024-08-29T09:00:00Z",
    duration_min: 60,
    end_time: "2024-08-29T10:00:00Z",
    total_score: 100,
    is_published: true,
  },
  {
    id: 2,
    title: "World History Quiz",
    text: "Test your knowledge of major events and figures in world history.",
    created_at: "2024-08-20T12:00:00Z",
    start_time: "2024-08-29T04:00:00Z",
    duration_min: 90,
    end_time: "2024-08-29T04:30:00Z",
    total_score: 150,
    is_published: true,
  },
  {
    id: 3,
    title: "Basic Python Programming",
    text: "A quiz designed to assess your understanding of basic Python programming concepts.",
    created_at: "2024-08-21T15:30:00Z",
    start_time: "2024-08-27T14:00:00Z",
    duration_min: 45,
    end_time: "2024-08-27T14:45:00Z",
    total_score: 75,
    is_published: true,
  },
  {
    id: 4,
    title: "Advanced Data Structures Quiz",
    text: "This quiz tests your knowledge of advanced data structures, including trees, graphs, and hash tables.",
    created_at: "2024-08-23T16:00:00Z",
    start_time: "2024-08-30T15:00:00Z",
    duration_min: 120,
    end_time: "2024-08-30T17:00:00Z",
    total_score: 200,
    is_published: false,
  },
  {
    id: 5,
    title: "Artificial Intelligence Basics",
    text: "Explore the fundamentals of artificial intelligence, including machine learning and neural networks.",
    created_at: "2024-08-25T09:00:00Z",
    start_time: "2024-09-01T10:00:00Z",
    duration_min: 75,
    end_time: "2024-09-01T11:15:00Z",
    total_score: 125,
    is_published: true,
  },
  {
    id: 6,
    title: "Cybersecurity Essentials",
    text: "Understand the key principles of cybersecurity and how to protect systems from cyber threats.",
    created_at: "2024-08-26T13:00:00Z",
    start_time: "2024-09-05T14:00:00Z",
    duration_min: 60,
    end_time: "2024-09-05T15:00:00Z",
    total_score: 100,
    is_published: true,
  },
];

const Content = () => {
  const now = new Date();

  const publishedQuizzes = quizzes
    .filter((quiz) => quiz.is_published)
    .sort((a, b) => new Date(a.start_time) - new Date(b.start_time));

  const pastQuizzes = publishedQuizzes.filter(
    (quiz) => new Date(quiz.end_time) < now
  );

  const activeOrSoonQuizzes = publishedQuizzes.filter((quiz) => {
    const startTime = new Date(quiz.start_time);
    const endTime = new Date(quiz.end_time);
    return (
      (startTime <= now && endTime >= now) ||
      (startTime > now &&
        startTime <= new Date(now.getTime() + 72 * 60 * 60 * 1000))
    );
  });

  const futureQuizzes = publishedQuizzes.filter((quiz) => {
    const startTime = new Date(quiz.start_time);
    return startTime > new Date(now.getTime() + 72 * 60 * 60 * 1000);
  });

  return (
    <section className={styles.container}>
      <Tabs defaultActiveKey="1">
        <Tabs.TabPane tab="Current or Starting Soon" key="1">
          <List
            grid={{ gutter: 16, xs: 1, sm: 2, md: 2, lg: 3, xl: 3, xxl: 4 }}
            dataSource={activeOrSoonQuizzes}
            renderItem={(quiz) => <QuizCard quiz={quiz} now={now} />}
          />
        </Tabs.TabPane>

        <Tabs.TabPane tab="Future Quizzes" key="2">
          <List
            grid={{ gutter: 16, xs: 1, sm: 2, md: 2, lg: 3, xl: 3, xxl: 4 }}
            dataSource={futureQuizzes}
            renderItem={(quiz) => <QuizCard quiz={quiz} now={now} />}
          />
        </Tabs.TabPane>

        <Tabs.TabPane tab="Past Quizzes" key="3">
          <List
            grid={{ gutter: 16, xs: 1, sm: 2, md: 2, lg: 3, xl: 3, xxl: 4 }}
            dataSource={pastQuizzes}
            renderItem={(quiz) => <QuizCard quiz={quiz} now={now} />}
          />
        </Tabs.TabPane>
      </Tabs>
    </section>
  );
};

export default Content;
