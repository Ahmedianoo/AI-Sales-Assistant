import Link from 'next/link';
import styles from './landing.module.css';

export default function LandingPage() {
  return (
    <div className={`${styles.container} canva-theme`}>
      <header className={styles.header}>
        <h1 className={styles.title}>AI Sales Assistant</h1>
        <p className={styles.subtitle}>
          Your intelligent partner for tracking competitors through scheduled battlecards and reports.
        </p>
      </header>

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