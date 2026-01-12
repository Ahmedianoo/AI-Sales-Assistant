import Link from 'next/link';
import styles from './landing.module.css';

export default function LandingPage() {
  return (
    <div className={`${styles.container} canva-theme`} >
      <header className={styles.header}>
        <h1 className={styles.title}>AI Sales Assistant</h1>
        <p className={styles.subtitle}>
          Stay on top of your competitors. Shhhh, don&apos;t play all your cards!
        </p>
      </header>

      {/* Cards Section */}
      <div className={styles.cardsContainer}>
        <div className={styles.card}>
          <div className={styles.cardInfo}>
            <p className={styles.cardTitle}>Scheduled Battlecards and Reports</p>
          </div>
        </div>
        <div className={styles.card}>
          <div className={styles.cardInfo}>
            <p className={styles.cardTitle}>AI answers on competitor strategies</p>
          </div>
        </div>
        <div className={styles.card}>
          <div className={styles.cardInfo}>
            <p className={styles.cardTitle}>Instant insight with real-time internet scraping </p>
          </div>
        </div>
      </div>

      <div className={styles.cta}>
        <p>Ready to get started?</p>
        <div className={styles.buttonGroup}>
          <Link href="/signup">
            <button className={styles.buttonPrimary}>Sign Up</button>
          </Link>
          <Link href="/login">
            <button className={styles.buttonSecondary}>Log In</button>
          </Link>
        </div>
      </div>
    </div>
  );
}
