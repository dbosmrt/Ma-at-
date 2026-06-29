import { useEffect, useState } from "react";

interface SplashScreenProps {
  onComplete: () => void;
}

export default function SplashScreen({ onComplete }: SplashScreenProps) {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false);
      onComplete();
    }, 2800);
    return () => clearTimeout(timer);
  }, [onComplete]);

  if (!visible) return null;

  return (
    <div className="splash-screen" id="splash-screen">
      <span className="splash-logo">Ma'at</span>
      <span className="splash-subtitle">Indian Legal AI</span>
      <div className="splash-bar" />
    </div>
  );
}
