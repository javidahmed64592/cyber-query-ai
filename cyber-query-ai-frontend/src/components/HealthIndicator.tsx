import { useHealthStatus, type HealthStatus } from "@/lib/api";

function HealthIndicator() {
  const status = useHealthStatus();

  const getStatusStyles = (status: HealthStatus): string => {
    switch (status) {
      case "online":
        return "bg-neon-green shadow-[0_0_4px_currentColor] animate-pulse";
      case "offline":
        return "bg-neon-red shadow-[0_0_4px_currentColor] animate-pulse";
      case "checking":
        return "animate-pulse bg-yellow-400 shadow-[0_0_4px_currentColor]";
      default:
        return "bg-text-muted shadow-[0_0_4px_currentColor]";
    }
  };

  const getStatusText = (status: HealthStatus): string => {
    return `Server: ${status.toUpperCase()}`;
  };

  return (
    <div className="group relative">
      <div
        className={`h-3 w-3 cursor-help rounded-full transition-all duration-200 ${getStatusStyles(status)}`}
        title={getStatusText(status)}
      />
    </div>
  );
}

export default HealthIndicator;
