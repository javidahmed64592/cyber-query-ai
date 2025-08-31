import { useHealthStatus, type HealthStatus } from "@/lib/useHealthStatus";

function HealthIndicator() {
  const status = useHealthStatus();

  const getStatusColor = (status: HealthStatus): string => {
    switch (status) {
      case "online":
        return "text-green-400";
      case "offline":
        return "text-red-400";
      case "checking":
        return "text-yellow-400";
      default:
        return "text-gray-400";
    }
  };

  const getStatusIcon = (status: HealthStatus): string => {
    switch (status) {
      case "online":
        return "🟢";
      case "offline":
        return "🔴";
      case "checking":
        return "🟡";
      default:
        return "⚪";
    }
  };

  const getStatusText = (status: HealthStatus): string => {
    return `Server: ${status.toUpperCase()}`;
  };

  return (
    <div className="relative group">
      <div
        className={`text-sm cursor-help ${getStatusColor(status)}`}
        title={getStatusText(status)}
      >
        {getStatusIcon(status)}
      </div>
    </div>
  );
}

export default HealthIndicator;
