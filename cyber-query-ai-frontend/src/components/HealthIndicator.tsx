import { useHealthStatus, type HealthStatus } from "@/lib/api";

function HealthIndicator() {
  const status = useHealthStatus();

  const getStatusStyles = (status: HealthStatus): string => {
    switch (status) {
      case "online":
        return "bg-neon-green shadow-[0_0_4px_#00ff41]";
      case "offline":
        return "bg-neon-red shadow-[0_0_4px_#ff0040]";
      case "checking":
        return "bg-yellow-400 shadow-[0_0_4px_yellow] animate-[pulse_2s_cubic-bezier(0.4,0,0.6,1)_infinite]";
      default:
        return "bg-text-muted shadow-[0_0_4px_#888888]";
    }
  };

  const getStatusText = (status: HealthStatus): string => {
    return `Server: ${status.toUpperCase()}`;
  };

  return (
    <div className="relative group">
      <div
        className={`w-3 h-3 rounded-full cursor-help ${getStatusStyles(status)}`}
        title={getStatusText(status)}
      />
    </div>
  );
}

export default HealthIndicator;
