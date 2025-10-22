import { useHealthStatus, type HealthStatus } from "@/lib/api";

function HealthIndicator() {
  const status = useHealthStatus();

  const getStatusStyles = (status: HealthStatus): string => {
    switch (status) {
      case "online":
        return "bg-[var(--neon-green)] shadow-[0_0_4px_var(--neon-green)]";
      case "offline":
        return "bg-[var(--neon-red)] shadow-[0_0_4px_var(--neon-red)]";
      case "checking":
        return "bg-yellow-400 shadow-[0_0_4px_yellow] animate-pulse-neon";
      default:
        return "bg-[var(--text-muted)] shadow-[0_0_4px_var(--text-muted)]";
    }
  };

  const getStatusText = (status: HealthStatus): string => {
    return `Server: ${status.toUpperCase()}`;
  };

  return (
    <div className="relative group">
      <div
        className={`w-3 h-3 rounded-full cursor-help transition-all duration-200 ${getStatusStyles(status)}`}
        title={getStatusText(status)}
      />
    </div>
  );
}

export default HealthIndicator;
