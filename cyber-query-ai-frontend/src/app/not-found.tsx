import Image from "next/image";

export default function NotFound() {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center text-center space-y-8">
      {/* Logo */}
      <div className="flex items-center space-x-4 mb-8">
        <Image
          src="/logo.svg"
          alt="CyberQueryAI Logo"
          width={64}
          height={64}
          priority
        />
        <div className="text-2xl font-bold text-text-primary">CyberQueryAI</div>
      </div>

      {/* Error Message */}
      <div className="space-y-4">
        <h1 className="text-6xl font-bold text-neon-red">404</h1>
        <h2 className="text-2xl font-semibold text-text-primary">
          Page Not Found
        </h2>
        <div className="max-w-md mx-auto space-y-2">
          <p className="text-text-secondary">
            The page you&apos;re looking for doesn&apos;t exist.
          </p>
          <p className="text-text-secondary">
            It might have been moved, deleted, or never existed.
          </p>
        </div>
      </div>

      {/* Navigation Tip */}
      <div className="border border-terminal-border bg-terminal-bg rounded-lg p-6">
        <h2 className="text-2xl font-bold text-text-primary mb-4 flex items-center">
          🧠 Tip
        </h2>
        <div className="text-text-secondary space-y-4">
          <p>
            Use the navigation bar above to explore CyberQueryAI&apos;s
            features.
          </p>
        </div>
      </div>
    </div>
  );
}
